#!/bin/bash

export VAULT_ADDR=http://127.0.0.1:8200

# Create .aws credentials file & populate with Vault secrets
mkdir -p /home/ubuntu/.aws
mv $INSTALL_DIR/templates/credentials /home/ubuntu/.aws/

aws_access_key_id=$(vault kv get -field=aws_access_key_id -mount=noshgrab aws_access_key_id)
sed -i "s|AWS_ACCESS_KEY_ID|$aws_access_key_id|g" /home/ubuntu/.aws/credentials

aws_secret_access_key=$(vault kv get -field=aws_secret_access_key -mount=noshgrab aws_secret_access_key)
sed -i "s|AWS_SECRET_ACCESS_KEY|$aws_secret_access_key|g" /home/ubuntu/.aws/credentials
