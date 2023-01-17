---
title: 'How to always run local-exec with Terraform'
date: 2023-01-17
author: 'John Stilia'
categories: [DevOps]
tags: [Terraform, DevOps]

resources:
  - name: featured-image
    src: 'featured-image..webp'
  - name: featured-image-preview
    src: 'featured-image-preview.png'

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
    -moz-border-radius: 25px;
    border-radius: 10px;
  }
</style>

<!--more-->

To ensure that a certain terraform local-exec script runs consistently, you can use a null_resource in conjunction with a timestamp. This way, each time you execute terraform apply - either to the entire project or to a specific resource - the state of the null resource will be invalidated, triggering the local-exec script.

Here's an example of how this can be done, in the context of building a local docker image:

```bash
resource "null_resource" "docker_build" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = "docker build -t ${var.image_name}:${var.image_tag} ./path-to-docker-file-Folder"
    }
}
```

So now, whenever you run:

```bash
terraform apply
```

To invalidate previous state, you can utilize the trigger block definition in conjunction with a variable referencing the terraform timestamp method. This ensures that the state is always invalidated with each apply or targeted execution.

And that's all there is to it! We hope this information was useful.

Thank you for reading!
