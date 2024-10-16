# Terraform

## Overview

This terraform folder creates all the required AWS services for this project bar the ECR's containing the images. 
This includes 
    - AWS postgres RDS
    - Extract lambdas
    - Report lambda 
    - Transform & load lambda
    - AWS Step functions State Machine 
    - Report Scheduler
    - Pipeline Scheduler
    - Dashboard Task Definition
    - Dashboard Service

## Set-up and Running

You need to create a `terraform.tfvars` file which includes the following:
```
AWS_REGION = "XXXX"
AWS_ACCESS_KEY = "XXXX"
AWS_SECRET_KEY = "XXXX"
DB_PASSWORD = "XXXX"
DB_USER = "XXXX"
DB_NAME="XXXX"
DB_PORT="XXXX"
DB_PORT_S="XXXX"
DB_HOST="XXXX"

SUBNET_NAME="XXXX"
VPC_ID="XXXX"

FROM_EMAIL="XXXX"
ECR_REPO_NAME="XXXX"
AWS_ACCOUNT_ID="XXXX"

GOG_ECR="XXXX"
STEAM_ECR="XXXX"
EPIC_ECR="XXXX"
REPORT_ECR="XXXX"
tf_ECR="XXXX"
DASHBOARD_ECR="XXXX"
```

Before running this terraform script, you need to go into the [web_scraping](../web_scraping), [report](../report),[load_to_rds](../load_to_rds) and [dashboard](../dashboard) folders and follow the instructions for `Deploying to the Cloud`, which involves making the ECRs containing the Docker images. Once the ECR's have been created then the terraform can be run.

Set up folder with `terraform init`.

To run first check with `terraform plan`.

Then run with `terraform apply`.

After use, destroy with `terraform destroy`.

## Architecture Diagram

This image shows the architecture diagram for this project.

<img src="../architecture_diagram.png" alt="Architecture Diagram" width="600"/>