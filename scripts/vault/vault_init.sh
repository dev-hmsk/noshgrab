#!/bin/bash

VAULT_KEY=$INSTALL_DIR/vault/vault_data

# Create Unseal Keys and Tokens 
# Sleep commands are required to delay vault operator init execution
# 
# until systemctl is-active --quiet vault.service; do 
#      sleep 1
# done
#
sleep 10 
export VAULT_ADDR=http://127.0.0.1:8200
echo "Setting VAULT_ADDR to http://127.0.0.1:8200"
echo "VAULT_ADDR = "$VAULT_ADDR
sleep 10
vault operator init > $VAULT_KEY/vault_keys.txt

# Assign Key and Unseal
for i in $(seq 1 3); do
    key=$(grep "Unseal Key $i" $VAULT_KEY/vault_keys.txt | awk -F": " '{print $2}')
    vault operator unseal $key
done

# Assign Root Token
root_token=$(grep "Initial Root Token" $VAULT_KEY/vault_keys.txt | awk -F": " '{print $2}') 

# Login to Vault
vault login $root_token

# Enable K/V v2 engine at path noshgrab/
vault secrets enable -description="noshgrab secrets" -path="noshgrab" -version=2 kv

# Enter Vault Secrets
bash $INSTALL_DIR/scripts/vault/vault_enter_secrets.sh

