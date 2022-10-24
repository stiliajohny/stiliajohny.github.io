---
Title: SSH made easy
date: 2021-08-30
author: "John Stilia"
description: "Streamline your SSH workflow by PIMPing your SSH config"
categories: [Software, Config, SSH, Linux]
tags: [Software, Config, SSH, Linux]

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

Streamline your SSH workflow by PIMPing your SSH config

<!--more-->

# What is SSH Agent and SSH config

The [ssh-agent](https://linux.die.net/man/1/ssh-agent) tool, in conjunction with SSH key authentication, makes it possible for you to start a session and, as long as you are within that session, you can log in and out of a remote server without having to type an SSH password or authentication passphrase. Once you’ve finished with your remote work, end the session and all is well.

The [ssh config](https://github.com/stiliajohny/dotfiles/blob/master/.ssh/config) is a file usually located under `~/.ssh/config` for every user and instructs the ssh-agent on how to establish a connection on a given host ( username, keypair, etc )

# Create an SSH key

On the system, you want to SSH from open a terminal and execute the following commands.

1. Create a keypair.

   - `-t`: Choosing the algorithm (I've chosen ed25519)
   - `-f`: Choose the path to save the keypair. Consider using a name pattern that suggests the algorithm and where you use the key as you might end up having many.
   - `-C`: Add a comment in the keypair

   {{< admonition tip>}} Consider using a password on your keypair {{</ admonition >}}

   ```shell
   ssh-keygen -t ed25519 -f ~/.ssh/ssh_keypair_aws_ed25519_passwd -C "this is a comment"
   ```

1. Once you’ve created your SSH key-pair, you’ll then need to copy the private key to the server you are planning to log in password free

   ```shell
   ssh-copy-id ubuntu@52.45.123.65
   ```

# PIMP your config

Let's assume you are in a situation that you have AWS, GCP, Digital Ocean. Ideally, you want to have different keys for the different providers/environments and potentially different users across.
Let see how we can PIMP the config to accommodate those settings without complexity.

1. Create the folder structure.

   ```shell
   $ tree ~/.ssh
   ~/.ssh
   ├── authorized_keys
   ├── config
   ├── config.d
   │   ├── aws_infra
   │   ├── gcp_infra
   │   ├── github
   │   ├── oci_infra
   │   ├── proxmox_infra
   │   └── rpi_infra
   ├── github_ed25519_P
   ├── github_ed25519_P.pub
   ├── aws_ed25519_P
   ├── aws_ed25519_P.pub
   ├── gcp_ed25519_P
   ├── gcp_ed25519_P.pub
   ├── rpi_ed25519_P
   ├── rpi_ed25519_P.pub
   ├── digiocean_ed25519_P
   └── digiocean_ed25519_P.pub
   ```

   <em> Create the key-pairs in advance based on your needs.</em>

1. Now let's edit the main ssh config located at `~/.ssh/config`

   ```shell
   Include config.d/*

   Host * !github.com  #github doesn't like complex settings ( in particular TTY requests)
     Compression yes
     ControlMaster auto
     ControlPersist 4800
     ForwardAgent no
     ForwardX11 yes
     HashKnownHosts yes
     IdentitiesOnly yes
     LogLevel VERBOSE
     MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com
     KexAlgorithms curve25519-sha256@libssh.org,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256
     Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
     PasswordAuthentication no
     PubkeyAuthentication yes
     PreferredAuthentications publickey
     Protocol 2
     RequestTTY yes
     TCPKeepAlive yes
     VisualHostKey yes
   ```

   <em> Those settings are a suggestion. Do your research before using them on your system</em>

   We can now see on the first line it includes the context of the folder `config.d`

1. We are now going to create the `config.d/` configs.

   1. Github: Located under `~/.ssh/config.d/github`

      ```shell
      Host github.com
        HostName github.com
        IdentityFile ~/.ssh/github_ed25519_P
        User git
      ```

   1. RaspberryPi: Located under `~/.ssh/config.d/rpi_infra`

      ```shell
      Host 192.168.1.2
          HostName 192.168.1.2
          IdentityFile ~/.ssh/rpi_ed25519_P
          User ubuntu

      Host 192.168.1.3
          HostName 192.168.1.3
          IdentityFile ~/.ssh/rpi_ed25519_P
          User raspberrypi
      ```

   1. AWS: Located under `~/.ssh/config.d/aws_infra`

      ```shell
      Host JUMPBOX
          HostName 10.0.2.1
          IdentityFile ~/.ssh/aws_ed25519_P
          User ubuntu

      Host DB
        ProxyJump 10.0.2.1
          IdentityFile ~/.ssh/aws_ed25519_P
          User ubuntu
      Host WEB
        ProxyJump 10.0.2.2
          IdentityFile ~/.ssh/aws_ed25519_P
          User automation
      ```

   On the latest config ( AWS ) we can see the use of `ProxyJump`, more on this in a future article

   You might have noticed, on the definition of `Host` some have an IP some have a Name. This is due to the flexibility of SSH to give entries a "nickname".

   That way you can do:

   ```shell
   ssh WEB
   ```

# The cherry on the cake: ssh-add

As you might have already done, your ssh private keys have a password configured.

If you find yourself connecting to remote servers multiple times, ssh-agent will ask you to provide the password.
To minimize the headache, add the keys you want to use most of the time in the ssh authentications agent for implementing single sign-on

```shell
$ ssh-add ~/.ssh/github_ed25519_P
Enter passphrase for ~/.ssh/github_ed25519_P:
Identity added: ~/.ssh/github_ed25519_P (git@my_laptop)
```

Then you can view all the added keys by using:

```shell
$ ssh-add -L
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIP3oC2Z/xSCUldQ8tTCP+EyaOspgZI4mXvWwvDyg1PLd git@my_laptop
```
