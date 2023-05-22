#!/bin/bash

# This script is only required to set up aws ec2 security groups 'vault-sg' if required
# This script would be utilized outside of an ec2 instance prior to standing up an ec2 server
# This script only needs to be used once to create a security group and then can be safely ignored 

# Install Required Modules
sudo apt install unzip -y
sudo apt install jq -y 

# Install awscli 
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Run AWS Configure <- Alternative to using aws_cred_setup.sh
# aws configure 

# Create Security Group 
aws ec2 create-security-group --group-name vault-sg --description Vault | jq -r '.GroupId'

# Open Port 8200 for Vault Server & Port 22 to connect to ec2 via SSH
aws ec2 authorize-security-group-ingress --group-name vault-sg --protocol tcp --port 22 --cidr '0.0.0.0/0'
aws ec2 authorize-security-group-ingress --group-name vault-sg --protocol tcp --port 8200 --cidr '0.0.0.0/0'
