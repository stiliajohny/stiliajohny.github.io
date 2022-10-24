---
title: "View AWS CLI logs in Real-Time"
date: 2021-12-28
author: "John Stilia"
description: "Almost traditional log viewing in the AWS Console, but in real-time on your terminal!"
categories: ["AWS", "CloudWatch"]
tags: ["AWS", "CloudWatch", "Logs"]

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

<style>
img {
    box-shadow: inset 10px 10px 60px #fff;
    -moz-border-radius:25px;
    border-radius:10px;
}
</style>

Almost traditional log viewing in the AWS Console, but in real-time on your terminal!

<!--more-->

# How to tail AWS CLI logs

After installing the [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) on your machine, you can start tailing your logs in real-time among other AWS services.
The primary use of the command requires you to specify the log group and log stream.

An example of the command is:
{{< highlight bash >}}aws logs tail "/aws/lambda/slack_event_handler"{{< /highlight >}}

## --follow (tail -f)

In order to tail the CloudWatch logs in real-time, add the `--follow` parameter to the AWS logs tail command. The command tails the logs for a specific CloudWatch log group.
By setting the `--follow` parameter, the command continuously polls for new logs.

An example of the command is:
{{< highlight bash >}}aws logs tail "/aws/lambda/slack_event_handler" --follow{{< /highlight >}}
Results:
{{< figure src="follow-log-output.png" class="img" height="100%" width="100%" link="follow-log-output.png">}}

## --format

By default, the logs tail command prints the following:

- timestamp and timezone
- log stream name
- log messages

For a more readable version, set the `--format` parameter to short. ( The current options are `detailed` and `short`, It defaults to `detailed`)

An example of the command is:
{{< highlight bash >}}aws logs tail "/aws/lambda/slack_event_handler" --follow --format short{{< /highlight >}}
Results:
{{< figure src="format-log-output.png" class="img" height="100%" width="100%" link="format-log-output.png">}}

## --since

The aws logs tail command also enables us to view the generated logs of a CloudWatch log group for a specific time period.
By default the command returns the logs from the past **10 minutes**.

To return the logs from a specific time period, use the `--since` parameter:
An example of the commands are:

{{< highlight bash >}}
aws logs tail "/aws/lambda/slack_event_handler" --follow --since 10s
aws logs tail "/aws/lambda/slack_event_handler" --follow --since 30m
aws logs tail "/aws/lambda/slack_event_handler" --follow --since 3h
aws logs tail "/aws/lambda/slack_event_handler" --follow --since 2d
aws logs tail "/aws/lambda/slack_event_handler" --follow --since 3w
{{< /highlight >}}

## --filter-pattern (grep)

You can filter which log messages the aws logs tail commands displays to your terminal, by using the `--filter-pattern` parameter.
The following example only returns log messages that include the string Hello.

An example of the command is:
{{< highlight bash >}}aws logs tail "/aws/lambda/slack_event_handler" --follow --format short --filter-pattern "NoneType"{{< /highlight >}}
Results:
{{< figure src="filter-log-output.png" class="img" height="100%" width="100%" link="filter-log-output.png">}}

{{< admonition tip "This is a tip" true >}}
To filter for multiple strings, simply prefix them with a ? character.
{{< /admonition >}}

# References

- <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>
- <https://awscli.amazonaws.com/v2/documentation/api/latest/reference/logs/tail.html>

{{< script >}}
console.log('Hello LoveIt!');
{{< /script >}}
