#!/bin/bash

# Set DIR locations
BASE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export INSTALL_DIR=/home/ubuntu/noshgrab
SCRIPT_DIR=$INSTALL_DIR/scripts/setup
export VAULT_ADDR=http://127.0.0.1:8200

# Uncomment below if a new aws ec2 security group is required
# See documentation within aws_server_config.sh for more info
# bash $SCRIPT_DIR/aws_server_config.sh

# Create ~/Noshgrab dir 
mkdir -p $INSTALL_DIR
cp -r $BASE_DIR/../.. $INSTALL_DIR

# Check and Upgrade Linux
sudo apt update -y 
sudo apt-get update -y

# Install Python3
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install python3.10-venv -y 

# Vault Setup
bash $SCRIPT_DIR/vault_setup.sh

# Start vault.service
sudo mv $INSTALL_DIR/systemd_service/vault.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable vault.service
sudo systemctl start vault.service
# sudo systemctl status vault.service

# Vault Init
bash $SCRIPT_DIR/../vault/vault_init.sh
 
# AWS Cred Creation
bash $SCRIPT_DIR/aws_cred_setup.sh

# VENV Setup
bash $SCRIPT_DIR/venv_setup.sh

# Docker Setup
bash $SCRIPT_DIR/docker_setup.sh

# Start noshgrab.service
sudo mv $INSTALL_DIR/systemd_service/noshgrab.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable noshgrab.service
sudo systemctl start noshgrab.service
# sudo systemctl status noshgrab.service
