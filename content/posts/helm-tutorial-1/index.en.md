---
title: 'Ahoy Matey! Charting Your Course to Kubernetes Deployment with Helm'
date: 2023-04-23
author: 'John Stilia'
categories: [DevOps]
tags:
  [
    helm charts,
    kubernetes,
    container orchestration,
    deployment,
    devops,
    cloud-native,
    containerization,
    chart repositories,
    yaml,
    kubernetes resources,
  ]

resources:
  - name: featured-image
    src: featured-image.PNG
  - name: featured-image-preview
    src: featured-image-preview.PNG

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

A comprehensive guide to Helm charts for Kubernetes deployment, covering installation, customization, dependency management, and security.

<!--more-->

## Helm charts 101: An Introduction

So, you're just getting started with Kubernetes, eh? Well, you've probably heard of Helm charts, but maybe you're unsure what they are or how they can help you. No worries, mate! Think of Helm charts as pre-made packages of Kubernetes resources that are all set up and ready to go. They've got everything you need to deploy and manage a specific application or service on your Kubernetes cluster, including deployment manifests, service manifests, and configuration files. And the best part? You can easily install and manage them using the Helm package manager. In this section, we'll review the basics of Helm charts and show how they can simplify your Kubernetes deployments. Sound good? Alright then, let's dive in!

## Installing Helm: A Step-by-Step Guide

Before you can start using Helm, install it on your machine. Fortunately, the installation process is straightforward and only takes a few minutes. Here's how to do it:

Head over to the [Helm website](https://helm.sh/docs/intro/install/) and download the appropriate version for your operating system.

Once the download is complete, open up your terminal and run the following command to unpack the Helm binary:

For MacOS simply install it with brew

```bash
brew install helm
```

Verify that Helm is installed correctly by running the following command:

```bash
helm version
version.BuildInfo{Version:"v3.11.3", GitCommit:"66a969e7cc08af2377d055f4e6283c33ee84be33", GitTreeState:"clean", GoVersion:"go1.20.3"}

```

This command should return the version number of the Helm client.

Congratulations, you've now installed Helm on your machine! In the next section, we'll explore how to create your first Helm chart.

## Creating a Helm Chart: A Tutorial

it's time to create your first Helm chart! Don't worry, it's not as complicated as you might think. A Helm chart is a bunch of files defining your application and its dependencies. These files are usually written in YAML and contain deployment manifests, service manifests, and configuration files. This section will show you how to create a simple Helm chart for a sample application. We'll cover all the files you need and some best practices to follow. By the end of this section, you'll be able to package your own applications as Helm charts like a pro. Sound good? Alright then, let's get started!

1. Create a new directory for your Helm chart:

```bash
mkdir mychart
```

2. Navigate to the new directory:

```bash
cd mychart
```

3. Use the Helm CLI to create a new chart:

```bash
helm create mychart
```

This will create a new chart in the current directory called `mychart`.

Open up the mychart directory and take a look at what's inside. You'll see a bunch of files and directories, including:

- `Chart.yaml` - This file contains metadata about the chart, such as its name, version, and description.
- `values.yaml` - This file contains default values that will be used to configure the resources in the chart.
- `templates/` - This directory contains templates for the Kubernetes resources that will be created by the chart.
  Modify the `Chart.yaml` file to include your application's metadata, such as its name, version, and description.

Modify the `values.yaml` file to include any configuration options or default values that your application requires.

Modify the templates in the `templates/` directory to include the Kubernetes resources required by your application, such as deployments, services, and config maps. You can use the default templates as a starting point and modify them as needed.

Once you've created your chart, you can package it up using the following command:

```bash
helm package mychart/
```

This will create a `.tgz` file containing your chart.

Congratulations, you've now created your first Helm chart! The next section will explore how to customize your charts using values files and templates.

## Customizing Helm Charts: Tips and Tricks

So you've created your first Helm chart - good on ya? But what if you want to customize it a bit more?

You may need to configure different settings for different environments, or you may want to include additional Kubernetes resources in your chart. That's where customizing Helm charts comes in. In this section, we'll cover some tips and tricks for customizing your Helm charts to suit your specific needs. We'll show you how to use values files to configure your charts and modify the templates to include additional Kubernetes resources. By the end of this section, you'll understand how to customize your Helm charts like a pro.

Alright then, let's dive in!

1. Use values files to configure your charts for different environments. Values files allow you to override the default values in your chart with environment-specific values. For example, you might have one values file for your development environment and another for your production environment. You can use the `--values` flag with the `helm install` command to specify which values file to use. For example:

```bash
helm install mychart --values values-dev.yaml
```

1. Create reusable templates for common Kubernetes resources. You can create reusable templates for Kubernetes resources like deployments, services, and config maps, and then include them in your Helm charts using the `{{ template }}` function. This can save you time and reduce duplication in your charts.

2. Use conditionals to include or exclude resources based on configuration options. You can use the `{{ if }}` and `{{ else }}` functions in your templates to include or exclude resources based on the values in your `values.yaml` file. For example, you might include a specific Kubernetes resource only if a certain configuration option is set to true.

3. Use subcharts to manage dependencies between charts. Suppose your application has dependencies on other applications or services. In that case, you can include those dependencies as subcharts in your Helm chart. This allows you to manage the dependencies and their versions separately from your application code.

4. Use environment variables to pass configuration options to your containers. You can use the env field in your deployment templates to pass environment variables to your containers at runtime. You can also use the `--set` flag with the helm install command to set environment variables dynamically. For example:

```bash
helm install mychart --set mycontainer.envvar=value
```

## Sharing Your Helm Charts: Best Practices

By sharing your chart, you can help other Kubernetes users, and even contribute to the wider community. But if you're new to sharing your charts, it can feel a bit daunting. Not to worry - in this section, we'll show you some best practices for sharing your Helm charts with the world. We'll cover everything from packaging and distribution to ensuring your chart is secure and up-to-date. By the end of this section, you'll be able to share your Helm charts like a pro, and join the ranks of the top chart-makers out there.

1. Use a version control system like Git to keep track of changes to your chart over time. This will make it easier for others to contribute to your chart and stay up-to-date with the latest changes.
2. Package your chart as a .tgz file using the helm package command. This will create a self-contained package that others can install on their own Kubernetes clusters.
3. Use a Helm repository to make your chart easily accessible to others. Helm repositories allow you to store and distribute your charts to others, and they can be public or private depending on your needs.
4. Include documentation with your chart to help others understand how to use it. This can include things like a README file, usage examples, and configuration options.
5. Follow security best practices when sharing your chart. This includes things like using secure sources for dependencies, scanning your chart for vulnerabilities, and avoiding hard-coded secrets.

Following these best practices ensures that your Helm chart is easy to use, secure, and accessible to others in the Kubernetes community. In the next section, we'll explore some advanced features of Helm charts that can help you take your charts to the next level.

## Advanced Helm Chart Features: Deep Dive

So you've created your Helm chart, customized it to your heart's content, and shared it with others in the Kubernetes community - good on ya! But if you're looking to take your Helm charting skills to the next level, you'll want to explore some of the more advanced features that Helm has to offer. In this section, we'll take a deep dive into some of these advanced features, including:

- Using subcharts to manage complex dependencies
- Using hooks to perform pre- and post-installation actions
- Creating conditionals to make your charts more dynamic
- Using chart templates to create reusable components
- Using global values to share configuration across multiple charts

### Using subcharts to manage complex dependencies

Suppose your application has complex dependencies on other applications or services. In that case, you can use subcharts to manage those dependencies separately from your application code. A subchart is essentially a Helm chart that's packaged within another chart. You can use the dependencies field in your parent chart's Chart.yaml file to specify which subcharts it depends on. For example:

```yaml
dependencies:
  - name: mydependency
    version: '1.2.3'
    repository: https://example.com/charts
```

This tells Helm to include the mydependency chart in your parent chart's dependencies. When you install your parent chart, Helm will automatically install any required subcharts.

### Using hooks to perform pre- and post-installation actions

Hooks are a powerful feature of Helm that allow you to perform pre- and post-installation actions. Hooks can be used to perform tasks like initializing databases, running migrations, or configuring external services. Hooks are defined in a `hooks/` directory in your chart, and can be written in any language that can be executed as a script. For example, you might define a pre-installation hook like this:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
  annotations:
    'helm.sh/hook': pre-install
spec:
  template:
    spec:
      containers:
        - name: my-container
          image: my-image
          command: ['/bin/sh']
          args: ['-c', 'echo Pre-install hook']
```

This tells Helm to run the my-job Kubernetes job before installing the chart.

## Securing Your Helm Charts: Best Practices

Security is a critical concern when it comes to deploying applications on Kubernetes, and Helm charts are no exception. If your Helm chart contains sensitive information like credentials or secrets, it's important to ensure that your chart is secure and protected from unauthorized access. In this section, we'll explore some best practices for securing your Helm charts. We'll cover topics such as using secure sources for dependencies, scanning your chart for vulnerabilities, avoiding hard-coded secrets, and ensuring that your chart is up-to-date with the latest security patches. By following these best practices, you can rest assured that your Helm chart is secure and ready for deployment on any Kubernetes cluster.

### Use secure sources for dependencies

When creating a Helm chart, it's important to use secure sources for your dependencies. This ensures that your chart is not vulnerable to known security exploits or malicious code injection. You should only use trusted sources for your dependencies, such as official Helm charts or reputable third-party charts. Additionally, you should verify the integrity of your dependencies using digital signatures or checksums.

### Scan your chart for vulnerabilities

Before deploying your Helm chart, it's a good idea to scan it for vulnerabilities using a vulnerability scanner. There are several tools available that can scan your chart for known vulnerabilities and alert you to any issues. For example, the Helm Security Scanner is a tool that can scan your chart and provide a report of any security issues that are detected.

### Avoid hard-coded secrets

When creating a Helm chart, it's important to avoid hard-coding secrets like passwords or API keys. Instead, you should use Kubernetes secrets to store sensitive information, and reference those secrets in your chart using environment variables or volume mounts. This ensures that your sensitive information is stored securely and is not visible in your chart's configuration files.

### Ensure your chart is up-to-date with the latest security patches

As with any software, it's important to ensure that your Helm chart is up-to-date with the latest security patches. This includes regularly updating your chart's dependencies and monitoring for any security advisories related to the software or libraries used in your chart. You should also keep an eye on the Helm repository you're using for your chart, and ensure that any updates or security patches are applied in a timely manner.

By following these best practices, you can ensure that your Helm chart is secure and ready for deployment on any Kubernetes cluster. In the next section, we'll wrap up our journey through Helm charts and offer some final thoughts on next steps.

## References

- <https://jfrog.com/blog/10-helm-tutorials-to-start-your-kubernetes-journey>
- <https://jfrog.com/blog/10-helm-tutorials-to-start-your-kubernetes-journey>
- <https://jfrog.com/blog/helm-charts-best-practices>
- <https://www.youtube.com/watch?v=WugC_mbbiWU&t=3s>
- <https://www.youtube.com/watch?v=TJ9hPLn0oAs>
- <https://www.youtube.com/watch?v=vQX5nokoqrQ>
- <https://www.youtube.com/watch?v=iZajBVBdCNQ&t=2143s>
- <https://www.youtube.com/watch?v=cZ1S2Gp47ng>
- <https://jfrog.com/knowledge-base/helm-repository-best-practices>
- <https://jfrog.com/knowledge-base/what-is-helm-in-kubernetes>
- <https://jfrog.com/cheat-sheet/kubernetes-made-easy>
