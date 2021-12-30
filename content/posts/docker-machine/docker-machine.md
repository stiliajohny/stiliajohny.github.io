---
Title: 100mph on a docker-machine
date: 2021-09-13
author: "John Stilia"
description: "Use multiple envidonments on your Local or Remote development with docker-machine"
categories: [Docker, Linux]
tags: [Development, Docker]

resources:
  - name: "featured-image"
    src: "featured-image.jpg"

lightgallery: true
fontawesome: true
linkToMarkdown: true
rssFullText: false

toc:
  auto: false
comment:
  enable: true
---

Use multiple envidonments on your Local or Remote development with docker-machine

<!--more-->

# Prerequiments

- Oracle VirtualBox
- docker cli
- Available Disk Storage > 20GB
- Internet Connectivity :D

# What is docker-machine

It allows you to control the docker engine of a VM created using `docker-machine` remotely.

When you have a containerized application, it's essential to quickly deploy them in the cloud, not only running them locally using Docker for Mac/Windows or from a Linux box locally. The tool to easily create a remote virtual machine (VM) and manage those containers is docker-machine.

# What's the difference between Docker Engine and Docker Machine?

When people say "Docker" they typically mean Docker Engine, the client-server application made up of the Docker daemon, a REST API that specifies interfaces for interacting with the daemon and a command-line interface (CLI) client that talks to the daemon (through the REST API wrapper). Docker Engine accepts docker commands from the CLI, such as `docker run <image>`, `docker ps` to list running containers, docker image ls to list images, and so on.

Docker Machine is a tool for provisioning and managing your Dockerized hosts (hosts with Docker Engine on them). Typically, you install Docker Machine on your local system. Docker Machine has its own command-line client, `docker-machine`, and the Docker Engine client, `docker`. You can use Machine to install Docker Engine on one or more virtual systems. These virtual systems can be local (as when you use Machine to install and run Docker Engine in VirtualBox on Mac or Windows) or remote (as when you use Machine to provision Dockerized hosts on cloud providers). The Dockerized hosts themselves can be thought of and are sometimes referred to as managed "machines".

# How to create a docker-machine?

For more information, read the documentation on [github.com/docker/machine](https://github.com/docker/machine)

## Create it using VirtualBox

```bash
docker-machine create \
    --driver "virtualbox" \
    --engine-install-url "https://get.docker.com" \
    --virtualbox-cpu-count "4" \
    --virtualbox-disk-size "20000" \
    --virtualbox-hostonly-cidr "192.168.100.1/24" \
    --virtualbox-memory "4096" \
    --virtualbox-ui-type "headless" \
    --engine-opt dns=8.8.8.8 \
    --engine-opt log-driver=syslog \
    --virtualbox-share-folder $HOME:/host-home \
    development
```

# You have a docker-machine VM; now what?

## Most used commands

- `docker-machine ls`
  Show a list of docker-machines
- `docker-machine ssh development` SSH access to the Machine
- `eval $(docker-machine env development)` Enable current session with the Machine
- `docker-machine active` Shows the current Docker Machine
- `docker-machine ip development` Shows the current Machine's IP
- `docker-machine scp ~/localfile.txt demo-machine:~/` SCP files into the Machine
- `docker-machine env -u` Go back to the local docker
- `docker-machine rm development` Delete the Machine

## Deploy a docker container in the Docker Machine

Docker CLI is looking for some default [environment variables](https://docs.docker.com/engine/reference/commandline/cli/#environment-variables) when it's executed. When we create the docker-machine, we can export the variables for the docker-machine VM we wish.

## Export ENV of a docker-machine

```bash
$ docker-machine env development
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.100.100:2376"
export DOCKER_CERT_PATH="/home/user/.docker/machine/machines/development"
export DOCKER_MACHINE_NAME="development"
# Run this command to configure your shell:
# eval $(docker-machine env development)
```

fter exporting the
After running this command or for a shorter time, you could have run `eval $(docker-machine env development)`, which would have automatically exported the environment variables.

# The End

After this we can run any docker commands towards the `development` docker-machin siting on our local VM

When ready, to restore back to your "normal" local docker environment

```bash
unset DOCKER_TLS_VERIFY
unset DOCKER_HOST
unset DOCKER_CERT_PATH
unset DOCKER_MACHINE_NAME
```
