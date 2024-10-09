

provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
    
}

data "aws_db_subnet_group" "public-subnet-group" {
    name = var.SUBNET_NAME
}

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