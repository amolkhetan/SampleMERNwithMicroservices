#!/bin/bash
exec > /var/log/user-data.log 2>&1
set -x

# Update and install required packages
apt update -y
apt install -y docker.io unzip curl

# Start and enable Docker
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu
sleep 10

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
rm -rf aws/
unzip -o awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip
/usr/local/bin/aws --version || echo "AWS CLI installation failed"

# Configure AWS credentials
mkdir -p /home/ubuntu/.aws
cat <<EOF > /home/ubuntu/.aws/credentials
[default]
aws_access_key_id=AWS_ID
aws_secret_access_key=AWS_KEY
EOF
cat <<EOF > /home/ubuntu/.aws/config
[default]
region=us-west-2
output=json
EOF
chown -R ubuntu:ubuntu /home/ubuntu/.aws

# Authenticate with AWS ECR
/usr/local/bin/aws ecr get-login-password --region us-west-2 | \
docker login --username AWS --password-stdin 975050024946.dkr.ecr.us-west-2.amazonaws.com

# Remove existing containers
docker rm -f helloservice profileservice frontend || true

# Pull and run containers
docker run -d --restart unless-stopped --name helloservice -p 3001:3001 \
  975050024946.dkr.ecr.us-west-2.amazonaws.com/helloservice:2.0

docker run -d --restart unless-stopped --name profileservice -p 3002:3002 \
  975050024946.dkr.ecr.us-west-2.amazonaws.com/profileservice:2.0

docker run -d --restart unless-stopped --name frontend -p 80:3000 \
  975050024946.dkr.ecr.us-west-2.amazonaws.com/frontend:2.0

# Log running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
