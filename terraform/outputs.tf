
# Describe Information Terraform will share with you

output "db_address" {
    value = aws_db_instance.games-db.address
  
}