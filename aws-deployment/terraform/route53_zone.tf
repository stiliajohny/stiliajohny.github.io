resource "aws_route53_zone" "indraft-blog" {
  comment       = "Zone for the indraft blog which is my main domain"
  force_destroy = "false"
  name          = "indraft.blog"

  tags = {
    creation-type = "terraform-cloud"
  }

  tags_all = {
    creation-type = "terraform-cloud"
  }
}
