FROM node:14-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
# RUN npm run build

# Use a runtime stage to run the app
FROM node:14-alpine AS runtime

WORKDIR /app

COPY package*.json ./
RUN npm install --only=production

COPY --from=builder /app /app

EXPOSE 3000

CMD ["npm", "start"]