
### Define provider

provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
    
}


### SET UP POSTGRES RDS

# gets subnet group
data "aws_db_subnet_group" "public-subnet-group" {
    name = var.SUBNET_NAME
}

# creates relevent security group
resource "aws_security_group" "games-tracker-db-sg" {
    name = "c13-games-tracker-db-sg"
    vpc_id = var.VPC_ID
    ingress {
    from_port        = var.DB_PORT
    to_port          = var.DB_PORT
    protocol         = "TCP"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

# creates RDS
resource "aws_db_instance" "games-db" {
    allocated_storage            = 10
    db_name                      = var.DB_NAME
    identifier                   = "c13-games-tracker-rds"
    engine                       = "postgres"
    engine_version               = "16.1"
    instance_class               = "db.t3.micro"
    publicly_accessible          = true
    performance_insights_enabled = false
    skip_final_snapshot          = true
    db_subnet_group_name         = data.aws_db_subnet_group.public-subnet-group.name
    vpc_security_group_ids       = [aws_security_group.games-tracker-db-sg.id]
    username                     = var.DB_USER
    password                     = var.DB_PASSWORD
}


### SET UP LAMBDAS 

# Assuming the role for the lambda
data "aws_iam_policy_document" "assume_lambda_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

#Permissions for role
data "aws_iam_policy_document" "lambda_permissions_policy" {
  statement {
    effect = "Allow"
    actions = [
      "rds:DescribeDBInstances",
      "rds:Connect"
    ]
    resources = ["*"] 
  }
  statement {
    effect = "Allow"
    actions = [
      "ses:SendEmail",
      "ses:SendRawEmail"
    ]
    resources = ["*"] 
  }
  statement {
    effect = "Allow"
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission",
    ]
    resources = ["*"] 
  }
}

# IAM role for lambda
resource "aws_iam_role" "iam_for_lambda" {
  name               = "c13-lakshmibai-lambda-exec-role"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda_role.json
}

# Adding policies to role
resource "aws_iam_role_policy" "lambda_role_policy" {
  name   = "c13-lakshmibai-lambda-role-policy"
  role   = aws_iam_role.iam_for_lambda.id
  policy = data.aws_iam_policy_document.lambda_permissions_policy.json
}


# Exract ECR's
data "aws_ecr_image" "gog-scraper-image" {
  repository_name = "c13-lakshmibai-gog-scraper"
  image_tag       = "latest"
}

data "aws_ecr_image" "steam-scraper-image" {
  repository_name = "c13-lakshmibai-steam-scraper"
  image_tag       = "latest"
}

# The lambda functions
resource "aws_lambda_function" "gog-scraper-lambda" {
  function_name = "c13-lakshmibai-gog-scraper-lambda"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  timeout = 900
  memory_size = 512

  image_uri = data.aws_ecr_image.gog-scraper-image.image_uri
}

resource "aws_lambda_function" "steam-scraper-lambda" {
  function_name = "c13-lakshmibai-steam-scraper-lambda"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  timeout = 900
  memory_size = 512

  image_uri = data.aws_ecr_image.steam-scraper-image.image_uri
}