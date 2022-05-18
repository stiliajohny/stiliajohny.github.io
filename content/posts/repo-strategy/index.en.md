---
title: "Mono-repo VS Multi-repo VS Poly-as-Mono"
date: 2022-05-18
author: "John Stilia"
categories: ["Version Control", "Ways of Working"]
tags: ["Version Control", "Ways of Working", "Git", "DevOps", "Debate"]

resources:
  - name: featured-image
    src: repo-strategy.png
  - name: featured-image-preview
    src: repo-strategy.png

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

LIke tabs VS spaces, but better :D

<!--more-->

# The challenge

So you and your team have a front end, back end and terraform code, and currently, you are working on three different repos. Some front-end code directly relates to the back-end code for local testing purposes, and you would like to have them in the "same repo". So, GitHub sounds excellent, but you have to track commits and branches.

# What Is a Monorepo?

- "In version control systems, a monorepo is a software development strategy where code for many projects is stored in the same repository. This software engineering practice dates back to at least the early 2000s when it was known as a 'shared codebase'." -- [Wikipedia](https://en.wikipedia.org/wiki/Monorepo)

- "A monorepo is a software development strategy where code for many projects is stored in the same repository. This software engineering practice dates back to at least the early 2000s, known as a 'shared codebase'." -- Internet talks

`TLDR: All files, tech, and code in one folder.`

# Monorepo misconception

## Monorepo !== Monolith

"We will have to release all the sack in one day; I don't like monoliths."

It is a common misconception that monorepo is not the same as monolith based on the association of a repository with a deployment artefact.<br>
See companies like Google and Facebook have used monorepo, yet they release their applications in different versions. Because monorepos simplify code sharing and cross-project refactorings, they significantly lower the cost of creating libs, microservices and micro-frontends. So adopting a monorepo often enables more deployment flexibility.

## It lets other teams change my code

"Another team can break my app, without my knowing, right before the release!"

This originates from the wrong fact that you can only set permissions on a repo but not per folder or file.<br>
Not many know that many tools let you configure ownership on a folder basis.

For instance, GitHub has a feature called [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners). You can provision a file that looks like this:

```plain
apps/app-a/* @susan
apps/app-b/* @bob
```

If you have a PR updating App A, Susan will have to approve it with this configuration. Bob will have to approve if the PR touches only App B. And if the PR touches A and B, both Susan and Bob will have to approve it.

## It does not scale

"Would I need to wait for half-day for a CI to pass before I can deploy?"

Rebuilding and retesting everything on every commit is slow. It does not scale beyond a handful of projects. But, **when using monorepo tools,** you only rebuild and retest what is affected.

# Real Challenges

## Trunk-based development

Monorepos and long-lived feature branches do not play together nicely. Chances are, you will have to adopt some form of trunk-based development.

## Not all services work with it

Since monorepos are not mainstream yet, some services do not work well with them.

## CI

Moving to a monorepo requires you to rethink how you do continuous integration.

# Benefits of Monorepo

## Low entry barrier

Starting in a company or a new team often comes with getting a lot of code from multiple repos and understanding the association. With monorepo being the new way of doing things, you can start with a single repo and work on it.

## Centrally Located Code Management

Having all the code in one repo allows for better visibility and collaboration. It gives you a single point of entry to all the code, but it also allows for easier version control. Also, you don't need to figure out which repository you need to create a new issue and use cross repo tags.

## Sharing same development culture

We have all been in a situation where different teams have different ways of working on code, from documentation to code factoring or even code standards security implementation. Since all the code is in a single place, sharing the same development methodologies and tools makes it easier to enable cross-team collaboration.

# What Is Multi-Repo?

"The multi-repo approach uses several repositories to host the multiple libraries or services of a project developed by a company. At its most extreme, it'll host every minimum set of reusable code or standalone functionality (such as a microservice) under its repository." -- [https://kinsta.com](https://kinsta.com/blog/monorepo-vs-multi-repo/#centrally-located-code-management)

`TLDR: You can have multiple repos, but they must be related to each other.`

# Benefits of Multi-Repo

## Autonomy of the code

Working on multi-repos allows the team to work autonomy. A significant contributing factor to choosing monorepo vs multi-repo is the team's size and impact through a project on the broader product.

## Independently version different components/libraries.

Using the GitOps way of working, if your VSC manages versions via git tags, multi-repo offers the only way to version different components/libraries.
Having multiple repos makes it easier to create dependencies graphs and manage them.

## Helps Define Access Control Across the Organization

Dont confuse it with [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

With a multi-repo, you can have ACL through your team, department, or organisation on who can access a repository. Anything from the viewing, administering, maintaining or triage on this repository.

## The Hashi-Terraform Suggestion

As mentioned in the Terraform article [here](https://www.terraform.io/cloud-docs/workspaces/configurations#code-organization-and-repository-structure)

In short, terraform suggests:

- As a best practice for repository structure, each repository containing Terraform code should be a manageable chunk of infrastructure, such as an application, service, or specific type of infrastructure (like common networking infrastructure).
- Small configurations connected by the remote state are more efficient for collaboration than monolithic repos
- Using a single repo attached to multiple workspaces is the most straightforward best-practice approach

# Issues With the Multi-Repo Approach

## Sync Sync Sync

Libraries and components need to be synced constantly via a CI/CD pipeline or a periodic PR to the primary branch.

## Could fragment the team.

A smaller team with multiple repos could split the group into front-end and back-end sub-teams, r to Dev and DevOps.
Even though this could be a good idea if it is necessary, it will be a terrible idea if the opposite is required.

# Hybrid Poly-As-Mono Approach

If you cannot decide which approach to use, here are two suggestions to consider. Each with its perks and drawbacks.

## Submodules

Git Submodules is an ancient way of managing multiple repositories linked under one repo. It is not a monorepo; it is like a git symbolic link.

Submodules are using a file in the main repo called [.gitmodules](https://github.com/stiliajohny/monorepo-ansible-provisioning/blob/restructuring/.gitmodules) in which you reference a submodule repo and where it should be clone in reference to the main repo.

The main repo doesn't contain the submodule repo, but it only contains instructions on where to clone the submodule repo.

It can get very complicated; however, when submodules are getting nested, you have to manage them. It is not a good idea to have a submodule that is a submodule.

{{< image src="submodules-github.png" caption="Submodules on Github front-end"  >}}

## Meta Tool

[Meta](https://github.com/mateodelnorte/meta) is a tool for managing multi-project systems and libraries. It answers the conundrum of choosing between a mono repo or many repos by saying "both" with a meta repo!

Meta is powered by plugins that wrap common commands, letting you execute them against some or all of the repos in your solution at once. Meta is built on a loop and, as such, inherits loops' ability to easily target a particular set of directories for executing a standard command (e.g. meta git status --include-only dir1,dir2. See loop for more available options).

{{< image src="meta.png" caption="Submodules on Github front-end"  >}}

# References

- My own codebase
  - https://github.com/stiliajohny/monorepo-ansible-provisioning
- https://www.freecodecamp.org/news/git-under-the-hood/
- https://kinsta.com/blog/monorepo-vs-multi-repo/#what-is-a-monorepo
- https://blog.nrwl.io/misconceptions-about-monorepos-monorepo-monolith-df1250d4b03c
- https://adinermie.com/mono-vs-multi-which-repo-structure-is-right-for-you/
- https://github.com/mateodelnorte/meta/issues/296
- https://medium.com/outbrain-engineering/mono-repo-vs-multi-repo-vs-hybrid-whats-the-right-approach-5436c575c6e0
- https://semaphoreci.com/blog/what-is-monorepo
