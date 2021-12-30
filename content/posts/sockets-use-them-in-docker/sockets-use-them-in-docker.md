---
Title: SSH Sockets. Use them in Docker
date: 2021-09-01
author: "John Stilia"
description: "There have been few occasions recently where I needed to have a Docker container to be able to ssh into other machines in the network"
tags: [Linux, SSH, Docker]
tags: [Linux, SSH, Docker]

# resources:
# - name: featured-image
#   src: java-vurn.png
# - name: featured-image-preview
#   src: log4j-1.png

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

There have been few occasions recently where I needed to have a Docker container to be able to ssh into other machines in the network

<!--more-->

# Summary

Recently I have been working on a Docker-webtop environment that needs to have to have ssh access without knowing of my ssh private keys.
Why? you may ask. Why not :)
Docker is extremely agile and advances to run few tools and an X11 ( more of this on a future post ).

While I was trying to find the best and arguably the most secure solution, I thought, **Linux Socket.**

SSH agent creates a socket on init. Any ssh-agent can use the same or separate socket. On each socket, the agent can have ssh keys open for the life of the socket. Let's got to work!

**EDIT**
{{< admonition tip>}}MacOS seems to be problematic with docker engine and linux sockets. watch this place for more updates {{</ admonition>}}

# Sharing the SSH-Agent

Lets refresh our memory a bit:

- Start an ssh-agent

  ```shell
  $ ssh-agent
  SSH_AUTH_SOCK=/tmp/ssh-XXXXXXiW0eJh/agent.3639620; export SSH_AUTH_SOCK;
  SSH_AGENT_PID=3639624; export SSH_AGENT_PID;
  echo Agent pid 3639624;
  ```

  Here we see a Linux socket created for the ssh agent. Wonder what can we do with this...

- Let's copy the output and paste it in the same terminal session and paste `Enter`/
  Now your session has an active ssh-agent that talks to/via a socket.

- We now need to give the agent a private key.

  ```shell
  $ ssh-add ~/.ssh/github_ed25519_P
  Identity added: /home/jstilia/.ssh/github_ed25519_P (user@vm_sandbox.internal)
  ```

- We list the keys known to the agent.

  ```shell
  $ ssh-add -L
  ssh-ed25519 AAAAAADGFFAJIWUAAJHGAU232/AALVDHJKC/AAAAA user@vm_sandbox.internal
  ```

- Let's run a Docker container and mount this socket.

  ```shell
  $ docker run -it -e SSH_AUTH_SOCK=/ssh-agent -v ${SSH_AUTH_SOCK}:/ssh-agent ubuntu:latest /bin/bash
  root@4a0ffef682f1:/#
  ```

  Here we have:

  - **-e** : Sets the environment variables in the Docker container
  - **-v** : mounts the existing ( on the host) socket in the container on the predefined ( by the variable above ) location

- In the container ( you might need to install ssh )

  ```shell
  $ ssh git@github.com
  The authenticity of host 'github.com (140.82.121.3)' can't be established.
  RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
  Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
  Warning: Permanently added 'github.com,140.82.121.3' (RSA) to the list of known hosts.
  PTY allocation request failed on channel 0
  Hi stiliajohny! You've successfully authenticated, but GitHub does not provide shell access.
  Connection to github.com closed.
  ```

  :party: The ssh in Docker using the agent on host that was aware of our private key to connect to GitHub and do the key exchange.
  Most importantly, the ssh keypair never moved in the container.

# What's next?

The terminal is your oyster. You can run any ssh related command from inside the Docker container as soon as you have let the agent know of your private key, **in advance**.
