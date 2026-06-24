# IAM Policy

resource "aws_iam_policy" "external_secrets" {

  name = "task5-external-secrets-policy"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret",
          "secretsmanager:ListSecrets"
        ]

        Resource = "*"
      }
    ]
  })
}


# Trust Policy

data "aws_iam_policy_document" "external_secrets_assume_role" {

  statement {

    actions = [
      "sts:AssumeRoleWithWebIdentity"
    ]

    principals {
      type = "Federated"

      identifiers = [
        module.eks.oidc_provider_arn
      ]
    }

    condition {
      test = "StringEquals"

      variable = "${replace(module.eks.cluster_oidc_issuer_url, "https://", "")}:sub"

      values = [
        "system:serviceaccount:external-secrets:external-secrets"
      ]
    }
  }
}


# IAM Role

resource "aws_iam_role" "external_secrets" {

  name = "task5-external-secrets-role"

  assume_role_policy = data.aws_iam_policy_document.external_secrets_assume_role.json
}


# Attach Policy

resource "aws_iam_role_policy_attachment" "external_secrets" {

  role = aws_iam_role.external_secrets.name

  policy_arn = aws_iam_policy.external_secrets.arn
}



