
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
    engine_version               = "16.3"
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

# ECR's
data "aws_ecr_image" "gog-scraper-image" {
  repository_name = "c13-lakshmibai-gog-scraper"
  image_tag       = "latest"
}

data "aws_ecr_image" "steam-scraper-image" {
  repository_name = "c13-lakshmibai-steam-scraper"
  image_tag       = "latest"
}

data "aws_ecr_image" "epic-scraper-image" {
  repository_name = "c13-lakshmibai-epic-extract"
  image_tag       = "latest"
}

data "aws_ecr_image" "report-image" {
  repository_name = "c13-lakshmibai-report-summary"
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

resource "aws_lambda_function" "epic-scraper-lambda" {
  function_name = "c13-lakshmibai-epic-scraper-lambda"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  timeout = 900
  memory_size = 512

  image_uri = data.aws_ecr_image.epic-scraper-image.image_uri
   environment {
    variables = {
      AWS_ACCOUNT_ID = var.AWS_ACCOUNT_ID
      ECR_REPO_NAME = var.ECR_REPO_NAME
    }
   }
}

resource "aws_lambda_function" "report-lambda" {
  function_name = "c13-lakshmibai-report-lambda"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  timeout = 900
  memory_size = 512

  image_uri = data.aws_ecr_image.report-image.image_uri
  environment {
    variables = {
      DB_HOST=var.DB_HOST
      DB_NAME= var.DB_NAME
      DB_USER=var.DB_USER
      DB_PASSWORD=var.DB_PASSWORD
      DB_PORT=var.DB_PORT
      AWS_REGION_NAME= var.AWS_REGION
      MY_AWS_ACCESS_KEY = var.AWS_ACCESS_KEY
      MY_AWS_SECRET_KEY = var.AWS_SECRET_KEY
      AWS_ACCOUNT_ID = var.AWS_ACCOUNT_ID
      ECR_REPO_NAME = var.ECR_REPO_NAME
      FROM_EMAIL = var.FROM_EMAIL
    }
  }
}

### WEEKLY SCHEDULER

data  "aws_iam_policy_document" "assume-weekly-schedule-role" {
    statement {
        effect = "Allow"
        principals {
            type        = "Service"
            identifiers = ["scheduler.amazonaws.com"]
        }
        actions = ["sts:AssumeRole"]
    }
}

# Permissions for the role: invoking a lambda, passing the IAM role
data  "aws_iam_policy_document" "weekly-schedule-permissions-policy" {
    statement {
        effect = "Allow"
        resources = [
                aws_lambda_function.report-lambda.arn
            ]
        actions = [
            "lambda:InvokeFunction"
        ]
    }

    statement {
        effect = "Allow"
        resources = [
            "*"
        ]
        actions = [
            "iam:PassRole"
        ]
    }
}

# IAM role for scheduler
resource "aws_iam_role" "iam_for_weekly_schedule" {
    name               = "c13-lakshmibai-weekly-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.assume-weekly-schedule-role.json
}

# Adding policies to role
resource "aws_iam_role_policy" "weekly_schedule_role_policy" {
  name   = "c13-lakshmibai-weekly-schedule-role-policy"
  role   = aws_iam_role.iam_for_weekly_schedule.id
  policy = data.aws_iam_policy_document.weekly-schedule-permissions-policy.json
}

# weekly schedule
resource "aws_scheduler_schedule" "weekly-schedule" {
    name = "c13-lakshmibai-weekly-schedule"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(0 12 ? * 1 *)"
    schedule_expression_timezone = "UTC+1"

    target {
        arn = aws_lambda_function.report-lambda.arn 
        role_arn = aws_iam_role.iam_for_weekly_schedule.arn
    }
}


