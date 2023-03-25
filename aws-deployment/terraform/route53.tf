resource "aws_route53_record" "_github-pages-challenge-stiliajohny-002E-infraft-002E-blog-002E-_TXT_" {
  name    = "_github-pages-challenge-stiliajohny"
  records = ["7166572bb78aa167b148bab7cabb7f"]
  ttl     = "60"
  type    = "TXT"
  zone_id = aws_route53_zone.indraft-blog.zone_id
}

resource "aws_route53_record" "indraft-blog-002E-_A_" {
  name    = ""
  records = ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"]
  ttl     = "60"
  type    = "A"
  zone_id = aws_route53_zone.indraft-blog.zone_id
}

resource "aws_route53_record" "indraft-blog-002E-_MX_" {
  name    = ""
  records = ["1 ASPMX.L.GOOGLE.COM", "10 ALT3.ASPMX.L.GOOGLE.COM", "10 ALT4.ASPMX.L.GOOGLE.COM", "15 3hkwyh2cxu5uv5cq5ggixho2nuenvsx35l6jpr2f7nb6yehwxukq.mx-verification.google.com.", "5 ALT1.ASPMX.L.GOOGLE.COM", "5 ALT2.ASPMX.L.GOOGLE.COM"]
  ttl     = "60"
  type    = "MX"
  zone_id = aws_route53_zone.indraft-blog.zone_id
}


resource "aws_route53_record" "www-002E-infraft-002E-blog-002E-_CNAME_" {
  name    = "www"
  records = ["www.stiliajohny.github.io"]
  ttl     = "60"
  type    = "CNAME"
  zone_id = aws_route53_zone.indraft-blog.zone_id
}
