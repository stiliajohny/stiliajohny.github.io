const express = require('express');
const mysql = require('mysql2/promise');
const bodyParser = require('body-parser');
const morgan = require('morgan');

const app = express();
app.use(bodyParser.json());
app.use(morgan('combined'));

const dbConfig = {
  host: process.env.MYSQL_HOST || 'localhost',
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || 'your_root_password',
  database: process.env.MYSQL_DATABASE || 'your_database_name',
};

async function createTableIfNeeded(connection) {
  const createTableSql = `
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message VARCHAR(255) NOT NULL
        )
    `;
  await connection.query(createTableSql);
}

async function connectToDatabase() {
  try {
    const connection = await mysql.createConnection(dbConfig);
    console.log('Connected to the MySQL database.');
    await createTableIfNeeded(connection);
    console.log('Ensured that the messages table exists.');
    return connection;
  } catch (error) {
    console.error('Error connecting to the MySQL database:', error);
    return null;
  }
}

app.get('/api/messages', async (req, res) => {
  const connection = await connectToDatabase();
  if (!connection) {
    res.status(500).json({ error: 'Error connecting to the database' });
    return;
  }

  try {
    const [rows] = await connection.query('SELECT * FROM messages');
    res.json(rows);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching messages' });
  } finally {
    connection.end();
  }
});

app.post('/api/messages', async (req, res) => {
  const connection = await connectToDatabase();
  if (!connection) {
    res.status(500).json({ error: 'Error connecting to the database' });
    return;
  }

  try {
    const message = req.body.message;
    if (!message) {
      res.status(400).json({ error: 'Message is required' });
      return;
    }

    const [result] = await connection.execute('INSERT INTO messages (message) VALUES (?)', [message]);
    res.status(201).json({ message: 'Message added successfully' });
  } catch (error) {
    res.status(500).json({ error: 'Error adding message' });
  } finally {
    connection.end();
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
