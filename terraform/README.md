# Terraform

## Overview

This terraform folder creates all the required AWS services for this project. This includes the AWS postgres RDS ...

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
SUBNET_NAME="XXXX"
VPC_ID="XXXX"
```

Set up folder with `terraform init`.

To run first check with `terraform plan`.

Then run with `terraform apply`.

After use, destroy with `terraform destroy`.

## Architecture Diagram

This image shows the architecture diagram for this project.

<img src="../architecture_diagram.png" alt="Data Visualisation" width="600"/>