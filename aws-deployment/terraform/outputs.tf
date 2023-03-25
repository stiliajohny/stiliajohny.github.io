
output "indraft-nameservers" {
  value = aws_route53_zone.indraft-blog.name_servers
}
