---
title: "Github Container Registry"
date: 2021-08-17
author: "John Stilia"
description: "Containerize all the things and store them in GitHub Container Registry"
categories: [Software, Container, Docker]
tags: [GitHub, Dontainer, Docker, GHCR]

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

Containerize all the things and store them in GitHub Container Registry

<!--more-->

# Account Preparation

1. Create a Repo [here](https://github.com/new)
1. Create a new personal access token (PAT) with the appropriate scopes for the tasks you want to accomplish. If your organization requires SSO, you must enable SSO for your new token. [create here](https://github.com/settings/tokens/new?scopes=write:packages,delete:packages)

1. Save your PAT. I recommend saving your PAT as an environment variable usong the command `read`. This command will expect a user input, paste your token and press enter ( nothing will be saved to the terminal history ).

   ```shell
   read CR_PAT
   ```

1. Using the CLI for your container type, sign in to the Container registry service at ghcr.io.

   ```shell
   echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
   ```

# Push to Container registry

## Attached Packages to Account

1. Write your Docekrfile
2. Building container images<br>

   ```shell
   docker build -t hello_docker .
   ```

3. Tagging container images

   1. Find the ID for the Docker image you want to tag.

      ```shell
      $ docker images
      > REPOSITORY                                            TAG                 IMAGE ID            CREATED             SIZE
      > ghcr.io/my-org/hello_docker         latest              38f737a91f39        47 hours ago        91.7MB
      > ghcr.io/my-username/hello_docker    latest              38f737a91f39        47 hours ago        91.7MB
      > hello-world                                           latest              fce289e99eb9        16 months ago       1.84kB
      ```

   2. Tag your Docker image using the image ID and your desired image name and hosting destination.

      ```shell
      docker tag 38f737a91f39 ghcr.io/OWNER/NEW_IMAGE_NAME:latest
      ```

   3. Pushing container images

      ```shell
      docker push ghcr.io/OWNER/IMAGE_NAME:latest
      ```

## Attached Packages to a Repo

1. Write your Docekrfile

{{< admonition type=warning title="This is a tip" open=true >}}
In order to attach a package to a specific repository add the following lable in your Dockerfile

`LABEL org.opencontainers.image.source="https://github.com/OWNER/REPO_NAME"`

{{< /admonition >}}

1. Building container images

   ```shell
   docker build -t ghcr.io/OWNER/REPO_NAME/IMAGE_NAME:latest .
   ```

1. Tagging container images

   1. Find the ID for the Docker image you want to tag.

      ```shell
      $ docker images
      > REPOSITORY                                            TAG                 IMAGE ID            CREATED             SIZE
      > ghcr.io/my-org/hello_docker         latest              38f737a91f39        47 hours ago        91.7MB
      > ghcr.io/my-username/hello_docker    latest              38f737a91f39        47 hours ago        91.7MB
      > hello-world                                           latest              fce289e99eb9        16 months ago       1.84kB
      ```

   2. Tag your Docker image using the image ID and your desired image name and hosting destination.

      ```shell
      docker tag 38f737a91f39 ghcr.io/OWNER/NEW_IMAGE_NAME:latest
      ```

   3. Pushing container images

      ```shell
      docker push ghcr.io/OWNER/IMAGE_NAME:latest
      ```

# Security

1. Access to this package can be managed via the packages' settings
   1. It can be inherited from the repo's ACL or it can be specified separately
1. Private repos need to invite users in order to view containers.
