source .env

aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com
aws ecr create-repository --repository-name $ECR_REPO_NAME --region eu-west-2
docker build --platform "linux/amd64" -t $ECR_REPO_NAME . 
docker tag $ECR_REPO_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_REPO_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/$ECR_REPO_NAME:latest