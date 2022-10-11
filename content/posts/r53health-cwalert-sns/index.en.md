---
title: "[note to my self] AWS Route53 Health Check Monitoring"
date: 2022-10-11
author: "John Stilia"
categories: ["AWS", "Terraform"]
tags: ["AWS", "Terraform", "Route53", "Health Check", "CloudWatch", "SNS"]

resources:
  - name: featured-image
    src: r53-sns-alert.png
  - name: featured-image-preview
    src: r53-sns-alert.png

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

Configuring AWS Route53 Health Check Monitoring with CloudWatch and SNS.

<!--more-->

# What AWS resources are we using?
- [Route53 Health Check](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks.html)
- [CloudWatch Alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [SNS Topic](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [SNS Subscription](https://docs.aws.amazon.com/sns/latest/dg/sns-subscription-filter-policies.html)

# What is the problem we are trying to solve?
We want to be notified when a Route53 Health Check fails. If an endpoint is not available or is not responding, we want to know about it. We can use CloudWatch to monitor the health check and send an SNS notification when the health check fails.

# How do we solve the problem?
We will use Terraform to create the resources we need. We will create a Route53 Health Check, a CloudWatch Alarm, an SNS Topic, and an SNS Subscription. We will use the Route53 Health Check to monitor the health of the endpoint. We will use the CloudWatch Alarm to monitor the Route53 Health Check. We will use the SNS Topic to send the notification. We will use the SNS Subscription to subscribe to the SNS Topic.

# Things to note
- The CloudWatch Alarm will send a notification to the SNS Topic when the Route53 Health Check fails.
- The SNS Subscription will subscribe to the SNS Topic and send the notification to the email address specified in the SNS Subscription.
- The SNS Subscription will only send the notification if the SNS Topic sends a notification with the subject "ALARM: ".
- The SNS subscription will only send notifications if the email recepient is subscribed to the SNS Topic.

# What is the Terraform code?

**Cloudwatch alarm for the health check**
```hcl
resource "aws_cloudwatch_metric_alarm" "iusearchbtw_blog" {
  alarm_name          = "iusearchbtw.blog"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "HealthCheckStatus"
  namespace           = "AWS/Route53"
  period              = "60"
  statistic           = "Minimum"
  threshold           = "1"

  dimensions = {
    HealthCheckId = aws_route53_health_check.iusearchbtw_blog.id
  }

  alarm_description = "This metric monitors status of the health check iusearchbtw.blog"
  alarm_actions     = [aws_sns_topic.iusearchbtw_blog.arn]

  tags = {
    creation-type = "terraform-cloud"
  }
}
```

**Route53 health check**
```hcl
resource "aws_route53_health_check" "iusearchbtw_blog" {
  fqdn              = "iusearchbtw.blog"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/"
  failure_threshold = "5"
  request_interval  = "30"

  tags = {
    creation-type = "terraform-cloud"
  }
}
```

**SNS topic**
```hcl
resource "aws_sns_topic" "iusearchbtw_blog" {
  name = "iusearchbtw_blog"

  tags = {
    creation-type = "terraform-cloud"
  }
}
```

**SNS subscription**
```hcl
resource "aws_sns_topic_subscription" "iusearchbtw_blog" {
  topic_arn = aws_sns_topic.iusearchbtw_blog.arn
  protocol  = "email"
  endpoint  = "stilia.johny@gmail.com"
}

```
