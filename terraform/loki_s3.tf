resource "aws_s3_bucket" "loki" {
  bucket        = "${var.project_name}-loki"
  force_destroy = true
}