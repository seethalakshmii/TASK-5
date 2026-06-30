#Allow EKS worker nodes to upload files into S3

resource "aws_iam_policy" "eks_s3_upload_policy" {
  name        = "eks-s3-upload-policy"
  description = "Allow EKS nodes to upload files to S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::task5-uploads"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = [
          "arn:aws:s3:::task5-uploads/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_node_s3" {
  role       = module.eks.eks_managed_node_groups["default"].iam_role_name
  policy_arn = aws_iam_policy.eks_s3_upload_policy.arn
}