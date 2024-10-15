
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

data "aws_ecr_image" "transform-image" {
  repository_name = "c13-lakshmibai-transform-load"
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

resource "aws_lambda_function" "transform-load-lambda" {
  function_name = "c13-lakshmibai-transform-load-lambda"
  role          = aws_iam_role.iam_for_lambda.arn

  package_type = "Image"
  timeout = 900
  memory_size = 512

  image_uri = data.aws_ecr_image.transform-image.image_uri
  environment {
    variables = {
      DB_HOST=var.DB_HOST
      DB_NAME= var.DB_NAME
      DB_USER=var.DB_USER
      DB_PASSWORD=var.DB_PASSWORD
      DB_PORT=var.DB_PORT
    }
  }
}

### STEP FUNCTION


# iam role
resource "aws_iam_role" "step_function_role" {
  name = "c13-lakshmibai-step-function-role"
  assume_role_policy = jsonencode( {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "states.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
} )
}


# iam policy 
resource "aws_iam_policy" "step_function_policy" {
  name = "c13-lakshmibai-step-function-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "lambda:InvokeFunction"
        Resource = "*"
      }
    ]
  })
}

# attaching the role and the policy 
resource "aws_iam_role_policy_attachment" "attach_step_function_policy" {
  role       = aws_iam_role.step_function_role.name
  policy_arn = aws_iam_policy.step_function_policy.arn
}

# Step function state machine
resource "aws_sfn_state_machine" "scrape-pipeline-state-function" {
  name     = "c13-lakshmibai-scrape-pipeline-step-function"
  role_arn = aws_iam_role.step_function_role.arn
  definition = jsonencode({
    "Comment": "Step function to invoke the 3 scrape lambdas and the transform and load Lambda",
    "StartAt": "Scrape",
    "States": {
      "Scrape": {
        "Type": "Parallel",
         "Branches": [ {
          "StartAt": "steam scraper",
          "States": {
            "steam scraper": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$",
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c13-lakshmibai-steam-scraper-lambda:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        },{
          "StartAt": "gog scraper",
          "States": {
            "gog scraper": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$",
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c13-lakshmibai-gog-scraper-lambda:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        },{
          "StartAt": "epic scraper",
          "States": {
            "epic scraper": {
              "Type": "Task",
              "Resource": "arn:aws:states:::lambda:invoke",
              "OutputPath": "$.Payload",
              "Parameters": {
                "Payload.$": "$", 
                "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c13-lakshmibai-epic-scraper-lambda:$LATEST"
              },
              "Retry": [
                {
                  "ErrorEquals": [
                    "Lambda.ServiceException",
                    "Lambda.AWSLambdaException",
                    "Lambda.SdkClientException",
                    "Lambda.TooManyRequestsException"
                  ],
                  "IntervalSeconds": 1,
                  "MaxAttempts": 3,
                  "BackoffRate": 2
                }
              ],
              "End": true
            }
          }
        }
        ],
        "Next": "Transform_and_Load"
      },
      "Transform_and_Load": {
        "Type": "Task",
        "Resource": "arn:aws:states:::lambda:invoke",
        "OutputPath": "$.Payload",
        "Parameters": {
          "Payload.$": "$",
          "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c13-lakshmibai-transform-load-lambda:$LATEST"
        },
        "Retry": [
          {
            "ErrorEquals": [
              "Lambda.ServiceException",
              "Lambda.AWSLambdaException",
              "Lambda.SdkClientException",
              "Lambda.TooManyRequestsException"
            ],
            "IntervalSeconds": 1,
            "MaxAttempts": 3,
            "BackoffRate": 2
          }
        ],
        "End": true
      }
    }
  })
}

### WEEKLY SCHEDULER

data  "aws_iam_policy_document" "assume-schedule-role" {
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
data  "aws_iam_policy_document" "schedule-permissions-policy" {
    statement {
        effect = "Allow"
        resources = [
                aws_lambda_function.report-lambda.arn,
                aws_sfn_state_machine.scrape-pipeline-state-function.arn
            ]
        actions = [
            "states:StartExecution",
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
resource "aws_iam_role" "iam_for_schedule" {
    name               = "c13-lakshmibai-scheduler-role"
    assume_role_policy = data.aws_iam_policy_document.assume-schedule-role.json
}

# Adding policies to role
resource "aws_iam_role_policy" "schedule_role_policy" {
  name   = "c13-lakshmibai-schedule-role-policy"
  role   = aws_iam_role.iam_for_schedule.id
  policy = data.aws_iam_policy_document.schedule-permissions-policy.json
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
        role_arn = aws_iam_role.iam_for_schedule.arn
    }
}


### STEP FUNCTION SCHEDULER

resource "aws_scheduler_schedule" "pipeline-schedule" {
    name = "c13-lakshmibai-pipeline-schedule"
    flexible_time_window {
      mode = "OFF"
    }
    schedule_expression = "cron(0 */3 ? * * *)"
    schedule_expression_timezone = "UTC+1"

    target {
        arn = aws_sfn_state_machine.scrape-pipeline-state-function.arn
        role_arn = aws_iam_role.iam_for_schedule.arn
    }
}


### DASHBOARD 

# A public subnet
data "aws_subnet" "c13-public-subnet" {
  id = "subnet-0f5e0c5f66f561ab0"
}

# The cluster we will run tasks on
data "aws_ecs_cluster" "c13-cluster" {
    cluster_name = "c13-ecs-cluster"
}

# IAM role for running ECS task 
data "aws_iam_role" "iam_for_task_def" {
  name = "ecsTaskExecutionRole"
}

# ECR with dashboard image
data "aws_ecr_image" "dashboard_image" {
  repository_name = "c13-lakshmibai-dashboard"
  image_tag       = "latest"
}

# Task definition
resource "aws_ecs_task_definition" "dashboard_task_definition" {
  family = "c13-lakshmibai-task-def"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  execution_role_arn = data.aws_iam_role.iam_for_task_def.arn
  cpu       = 512
  memory    = 1024
  container_definitions = jsonencode([
    {
      name      = "c13-lakshmibai-dashboard"
      image     = data.aws_ecr_image.dashboard_image.image_uri
      essential = true
      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
        }
      ]
      environment = [
        {
            name="DB_NAME"
            value=var.DB_NAME
        },
        {
            name="DB_HOST"
            value=var.DB_HOST
        },
        {
            name="DB_USER"
            value=var.DB_USER
        },
        {
            name="DB_PASSWORD"
            value=var.DB_PASSWORD
        },
        {
            name="DB_PORT"
            value="5432"
        },
        {
            name="REGION"
            value=var.AWS_REGION
        },
        {
            name="AWS_ACCESS_KEY"
            value=var.AWS_ACCESS_KEY
        },
        {
            name="AWS_SECRET_KEY"
            value=var.AWS_SECRET_KEY
        },

      ]
     logConfiguration = {
        logDriver = "awslogs"
        options = {
        awslogs-group         = "/ecs/c13-lakshmibai-dashboard"
        mode                  = "non-blocking"
        awslogs-create-group  = "true"
        max-buffer-size       = "25m"
        awslogs-region        = "eu-west-2"
        awslogs-stream-prefix = "ecs"
      }
    }
    }])
}


resource "aws_security_group" "dashboard_security_group" {
  name        = "c13-lakshmibai-dashboard-sg"
  description = "Allow TCP traffic on port 8501"
  vpc_id      = var.VPC_ID

  ingress {
    description      = "Allow TCP traffic on port 8501"
    from_port        = 8501
    to_port          = 8501
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECS Service for dashboard
resource "aws_ecs_service" "dashboard_service" {
  name            = "c13-lakshmibai-dashboard-service"
  cluster         = data.aws_ecs_cluster.c13-cluster.id
  task_definition = aws_ecs_task_definition.dashboard_task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [data.aws_subnet.c13-public-subnet.id]
    security_groups  = [aws_security_group.dashboard_security_group.id]
    assign_public_ip = true
  }
}



