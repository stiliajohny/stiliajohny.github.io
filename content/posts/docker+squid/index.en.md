---
title: "Speed up Docker builds with a local cache proxy"
date: 2022-05-05
author: "John Stilia"
categories: ["Docker", "Proxy"]
tags: ["Squid", "Docker", "Proxy", "Developement"]

resources:
  - name: featured-image
    src: docker+squid.png
  - name: featured-image-preview
    src: docker+squid.png

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

<style>
img {
    box-shadow: inset 10px 10px 60px #fff;
    -moz-border-radius:25px;
    border-radius:10px;
}
</style>

Speed up your docker build by caching packages locally.

<!--more-->

# Introduction

Imagine a world where your docker build would take tenfold less. Most times, your docker build is delayed due to package download for your Docker OS Updates or packages elsewhere ( npm, Python, etc.).

If this is on a Cloud server, it is usually not a problem as network speeds are perfect. Still, if this is on your local laptop while developing your code to meet your timeline, this can be particularly stressful.

{{< admonition type=tip title="Tip" open=true >}}
Worth mentioning, the build speed increases the more you use the proxy as it is caching the packages locally.
{{< /admonition >}}

# Benchmark results

| Benchmark   | Without cache (s) | With cache (s) | Speedup      |
| ----------- | ----------------- | -------------- | ------------ |
| apt-update  | 250               | 7              | ~35x faster  |
| apt-install | 1000              | 120            | ~8.3x faster |
| yum-update  | 15                | 10             | ~1.5x faster |
| yum-install | 36                | 30             | ~1.2x faster |
| npm-install | 54                | 49             | ~1.1x faster |

# Prerequisites

- Docker :D
- Docker :)
- Internet :0

# Run a Local Proxy

Running a local proxy can be particularly challenging as you will need to go through the proxy configuration.
This article can discover how easy it can be with a little googling.

In our case, we will run Squid Proxy with a local cache.

## Configure Your Local Proxy

First, let's look into the configuration and preparation of the squid proxy. <br>
We will need a couple of folders and a config.

```bash
mkdir squid && cd squid
mkdir cfg cache
```

Now we can go ahead and get the docker image as well as run it once to create some of the files and directories in the folders we just created.<br>
when the docker output stops ( ignore any errors ), you can go ahead and exit by pressing <kbd>ctrl + c</kbd>

```bash
docker pull woahbase/alpine-squid:x86_64
docker run -it --rm -v $(pwd)/cfg:/etc/squid -v $(pwd):/var/cache/squid woahbase/alpine-squid:x86_64
```

Now that we have all the folder structures, let's create a config.<br>
The config will have the following settings:

- No authentication
- Using 20GB of cache
- Accessible to all clients on the 192.168.1.xxx network.

Create a file ( as root as this is the user in the container) under `cfg/squid.conf` with the following content:

```config
#
# Recommended minimum configuration:
#
visible_hostname squid

# Example rule allowing access from your local networks.
# Adapt to list your (internal) IP networks from where browsing
# should be allowed
# acl localnet src 10.0.0.0/8   # RFC1918 possible internal network
# acl localnet src 172.16.0.0/12    # RFC1918 possible internal network
# acl localnet src 192.168.0.0/16   # RFC1918 possible internal network
# acl localnet src fc00::/7       # RFC 4193 local private network range
# acl localnet src fe80::/10      # RFC 4291 link-local (directly plugged) machines

acl localnet src 172.17.0.0/24  # docker
acl localnet src 192.168.1.0/24 # internal (CHANGE IT TO MATCH YOUR LAN)

acl SSL_ports port 443
acl Safe_ports port 80      # http
acl Safe_ports port 21      # ftp
acl Safe_ports port 443     # https
acl Safe_ports port 70      # gopher
acl Safe_ports port 210     # wais
acl Safe_ports port 1025-65535  # unregistered ports
acl Safe_ports port 280     # http-mgmt
acl Safe_ports port 488     # gss-http
acl Safe_ports port 591     # filemaker
acl Safe_ports port 777     # multiling http

acl purge method PURGE
acl CONNECT method CONNECT

# authenticated proxy
# auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/.htpasswd
# auth_param basic realm proxy
# acl authenticated proxy_auth REQUIRED

#
# Recommended minimum Access Permission configuration:
#
# Deny requests to certain unsafe ports
http_access deny !Safe_ports

# Deny CONNECT to other than secure SSL ports
http_access deny CONNECT !SSL_ports

# Only allow cachemgr access from localhost
http_access allow localhost manager
http_access deny manager
http_access deny purge

# We strongly recommend the following be uncommented to protect innocent
# web applications running on the proxy server which think the only
# one who can access services on "localhost" is a local user
http_access deny to_localhost

#
# INSERT YOUR OWN RULE(S) HERE TO ALLOW ACCESS FROM YOUR CLIENTS
#

# Example rule allowing access from your local networks.
# Adapt localnet in the ACL section to list your (internal) IP networks
# from where browsing should be allowed
http_access allow localhost

# enable this bit if using without authentication
http_access allow localnet
http_reply_access allow localnet
icp_access allow localnet
always_direct allow localnet

# otherwise use htpasswd authentication for hosts
#http_access allow authenticated localnet
#http_reply_access allow authenticated localnet
#icp_access allow authenticated localnet
#always_direct allow authenticated localnet

# And finally deny all other access to this proxy
http_access deny all

# Squid normally listens to port 3128
http_port 3128
http_port 3129 intercept

# Uncomment and adjust the following to add a disk cache directory.
cache_dir aufs /var/cache/squid 20000 16 256 # HERE WE COǸFIGURE 20GB OF CACHE
cache_replacement_policy heap LFUDAcache_mem 128 MB

maximum_object_size 1024 MB
maximum_object_size_in_memory 10240 KB

# Leave coredumps in the first cache dir
coredump_dir /var/cache/squid

allow_underscore on

dns_defnames on
dns_v4_first on

access_log /dev/stdout
cache_log /dev/stdout
cache_store_log /dev/stdout

httpd_suppress_version_string on
shutdown_lifetime 5 seconds

# forwarded_for transparent
forwarded_for delete
via off

# from https://www.linode.com/docs/networking/squid/squid-http-proxy-ubuntu-12-04
request_header_access Allow allow all
request_header_access Authorisation allow all
request_header_access WWW-Authenticate allow all
request_header_access Proxy-Authorization allow all
request_header_access Proxy-Authenticate allow all
request_header_access Cache-Control allow all
request_header_access Content-Encoding allow all
request_header_access Content-Length allow all
request_header_access Content-Type allow all
request_header_access Date allow all
request_header_access Expires allow all
request_header_access Host allow all
request_header_access If-Modified-Since allow all
request_header_access Last-Modified allow all
request_header_access Location allow all
request_header_access Pragma allow all
request_header_access Accept allow all
request_header_access Accept-Charset allow all
request_header_access Accept-Encoding allow all
request_header_access Accept-Language allow all
request_header_access Content-Language allow all
request_header_access Mime-Version allow all
request_header_access Retry-After allow all
request_header_access Title allow all
request_header_access Connection allow all
request_header_access Proxy-Connection allow all
request_header_access User-Agent allow all
request_header_access Cookie allow all
request_header_access All deny all

#  Response Headers Spoofing
reply_header_access Via deny all
reply_header_access X-Cache deny all
reply_header_access X-Cache-Lookup deny all
#
# Add any of your own refresh_pattern entries above these.
#
refresh_pattern -i .rpm$ 129600 100% 129600 refresh-ims override-expire
refresh_pattern -i .iso$ 129600 100% 129600 refresh-ims override-expire
refresh_pattern -i .deb$ 129600 100% 129600 refresh-ims override-expire
refresh_pattern ^ftp:       1440    20% 10080
refresh_pattern ^gopher:    1440    0%  1440
refresh_pattern -i (/cgi-bin/|\?) 0 0%  0
refresh_pattern .       0   20% 4320

```

Let's also create a Docker network that we can use later for the `docker build command.`

```bash
docker network create build-net-proxy
```

## Start Your Local Proxy

So far, we have configured all the necessary settings to run a local proxy.<br>
There is only one thing left to do: Start the proxy.

```bash
docker run -d \
  --restart always \
  --name squid --hostname squid \
  --network build-net-proxy \
  -c 256 -m 256m \
  -e PGID=1000 -e PUID=1000 \
  -p 3128:3128 -p 3129:3129 \
  -v $(pwd)/cfg:/etc/squid \
  -v $(pwd)/cache:/var/cache/squid \
  -v /etc/hosts:/etc/hosts:ro \
  -v /etc/localtime:/etc/localtime:ro \
  woahbase/alpine-squid:x86_64
```

And doing a `docker ps` should show the proxy running.

```bash
╭─jstilia at dell-xps-7590 in ~/Documents/GitHub 22-05-05 - 18:49:01
╰─○ docker ps
CONTAINER ID   IMAGE                          COMMAND   CREATED         STATUS         PORTS                                                           NAMES
1ea21f6b40b8   woahbase/alpine-squid:x86_64   "/init"   3 seconds ago   Up 2 seconds   0.0.0.0:3128-3129->3128-3129/tcp, :::3128-3129->3128-3129/tcp   squid
```

# Configure Docker to Use Your New Proxy

Great news, we have Squid proxy running in docker. Now what?

There are a few ways to utilise this new proxy.

## Configure Docker Deamon to use the proxy

Create a local file on your PC under $HOME/.docker/config.json:

```bash
touch $HOME/.docker/config.json
```

Add your proxy IP address to the file. Don't use your machine name because it may not be resolved correctly inside a container:

```JSON
"proxies":
{
    "proxies": {
        "default": {
            "httpProxy": "http://192.168.1.5:3128",
            "httpsProxy": "http://192.168.1.5:3128",
            "noProxy": "localhost,127.0.0.1,*.local,192.168.*"
        }
    }
}
```

You should notice that packages are downloaded only once, and your builds will be much faster from now on.

## Use the Proxy network to pass traffic through the proxy

Docker can take `args` to pass to the container as part of the `docker build` command.
These args **will not** be stored in the container.<br>
We also want to use the proxy network; we can pass the `--network` argument to the `docker build` command.

We can use that dynamically only on the builds we would like with a command like this:

`docker build --network build-net --build-arg http_proxy=http://squid:3128 .`

## Use the proxy globally on your system

Either on your terminal or your browser. You can use the proxy by setting the proxy environment variables.
There are a few ways to do this.

Docker has exposed a port to the host machine, so you can use the `<LOCAL_IP>:3128` to access the proxy.

for example, if your laptop/Desktop is under the IP 192.168.1.100, you can use the following proxy URL:
`192.168.1.100:3128`

From environment variables on your terminal, you can set it like this:

```bash
export http_proxy=http://192.168.1.100:3128
export https_proxy=http://192.168.1.100:3128
```

# References

- <https://developer.toradex.com/knowledge-base/how-to-speed-up-docker-image-builds-on-linux>
- <https://mrmagooey.github.io/articles/speeding-up-container-builds>
- <https://gist.github.com/reegnz/990d0b01b5f5e8670f78257875d8daa8>
