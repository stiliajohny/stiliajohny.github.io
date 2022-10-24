---
title: "Devcontainers: Clean environment everytime"
date: 2022-04-18
author: "John Stilia"
categories: ["Docker", "VSCode"]
tags: ["VSCode", "Docker", "Devcontainers", "Developement"]

resources:
  - name: featured-image
    src: devcontainer-architecture.png
  - name: featured-image-preview
    src: devcontainer-architecture.png

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

Imagine each repo has its own dev environment with the specific tools and configuration you need.

<!--more-->

# What are devcontainers?

We have all faced the challenge of syncing dependencies and tools with the rest of our team. Regardless if you are in a Dev team or a DevOps team, the challenge remains the same. We have to keep our environment clean and up to date; Have the correct linters, tools versions, and dependencies.

Docker can be a great tool to do just this, and VSCode has a great extension to do this for you.
Using the [Remote Development extension pack.](https://aka.ms/vscode-remote/download/extension) you can detect a devcontainer configuration in a repo and open your repo in a docker environment.

# What are the benefits?

Using devcontainers, you can:

- Lower overhead: Containers use fewer resources than traditional virtual machine environments.
- Portability: Applications running in containers are abstracted away from the physical platform they are hosted on.
- Consistency: Teams can be confident that their containerized code will run the same, regardless of where they are deployed.
- Improved DevOps: Applications running in containers can easily be scaled up and down, restarted and patched due to their virtual nature.

# Getting started

## Prerequisites

- [VS Code](https://code.visualstudio.com/download)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows/Mac or [Docker CC/CE](https://docs.docker.com/get-docker/) for Linux
- VS Code [Remote Development Extension Pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

## Base config

You have now installed all the prerequisites and are ready to use devcontainers.
VSCode provides you with a simple and easy way to do so.

Follow these steps:

- Open VSCode
- Add the repository or folder of your choise
- Open the Command Pallet ( <kbd>Ctrl/Cmd</kbd> + <kbd>Shift</kbd> + <kbd>p</kbd> )
- Select `Remote-Containers - Add Development Container Configuration ...`
  - Select one of the predefined Docker Image variants
  - Select one of the availables Docker Image versions

After finalizing the process of adding a devcontainer configuration, you will be presented with a new folder containing the following files:

- devcontainer.json - The configuration file
- Dockerfile - The Dockerfile to build the container

The `devcontainer.json` file contains information on how VSCode should act upon loading your folder and how the container should be built.
You can set up which Docker image you want to use, which VSCode extensions you want to install and which VSCode settings you want to use.
A more comprehensive list of options can be found [here](https://code.visualstudio.com/docs/remote/devcontainerjson-reference)<br>
The `Dockerfile` is a template file used to build the container. The Dockerfile will be built every time you open the folder in VSCode or request a rebuild through the extension. Here you can install any specific tools and apps needed for the particular case.

## Advance config

As we saw in the previous section, you can use the `devcontainer.json` file to set up the environment. You can add your extensions and settings there.
For example, you can add specific extensions.

```json
"extensions": [
  "ms-vscode.vscode-typescript-tslint-plugin",
  "ms-vscode.vscode-typescript-tslint-autofix",
]
```

Or we can add specific VSCode Settings.

```json
"settings": {
  "default": {
    "shell": "/bin/sh",
    "auto-start": true,
    "editor.saveFiles": "afterDelay",
    "editor.tabSize": 2,
  }
}
```

Or configure the start commands and remote user.

```json
"postCreateCommand": "uname -a",
"runArgs": [ "--init", "--cap-add=SYS_PTRACE", "--security-opt", "seccomp=unconfined" ],
"remoteUser": "vscode"
```

For more options for those configuration files, please check the [Remote Development extension pack](https://code.visualstudio.com/docs/remote/devcontainerjson-reference) documentation.

## Smart way

So far, we have seen how we can use Devcontainers to set up the environment. But, we can all agree it takes time and effort to onboard this to a new team or scale it up.
What about templating it? Glad you asked :)

You can visit my repository [here](https://github.com/stiliajohny/cookiecutter-collection) and check under [devconteiners](https://github.com/stiliajohny/cookiecutter-collection/tree/main/devcontainer).
<br>
Using cookiecutter, you can create a new template that will be used to create a new devcontainer configuration. I have created a template with some of my favourite basic devcontainer configurations. that can be used as a base. <br>
Simply change the directory in the folder you want to apply the template and run the command `cookiecutter gh:stiliajohny/cookiecutter-collection --directory= "devcontainer"`.<br>
After answering a few questions, your template will be ready to use.

# Pros / Cons of Devcontainers

## Pros

- "Works on my machine": The old analogy is never more valid. Devcontainers finally level the playing field; regardless of what host OS we are using, we get a consistent environment with everything we need to be included.
- Consistency: Everyone working on the codebase is now using the same toolset. Gone are the days of developer A using a code linter and developer B not using a code linter because they can't be bothered to download the tooling.
- Reusability: We can easily reuse this dev container for other C# projects we build. This keeps our codebases even more consistent.
- Ease of use: Imagine someone new joins your dev team now; rather than having to spend half the day setting up their machine, they can be up and running in 15–30 mins and productive.
- Git works in there: The guys who developed this VSCode extension have done some incredible wizardry to get your git credentials to work inside the dev container. This means all your credentials and ssh keys get passed through and work automagically!

## Cons

- They take time to set up: They have some initial upfront time/effort cost. The templates provided are fantastic starting points, but you will eventually need to extend them to include extra tooling etc.
  They do add a layer of complexity: Inherently, they require some knowledge of Docker and containers and therefore aren't quite as simple as just opening an IDE like Visual Studio, PyCharm or Rider.
- Everyone in your team needs to buy into them: Dev containers only really work when everyone uses them. There is minimal value-add if only some of your team use them and others decide they will ignore them and do their own thing.
- They can become stale: Because the dev container is not part of the main codebase, it is effortless to forget to keep the dependencies updated.

# References

- <https://truestorydavestorey.medium.com/getting-started-with-dev-containers-ad22a293037f>
- <https://www.aaron-powell.com/posts/2021-03-08-your-open-source-project-needs-a-dev-container-heres-why/>
- <https://code.visualstudio.com/docs/remote/containers>
