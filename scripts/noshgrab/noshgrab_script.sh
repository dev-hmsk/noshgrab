#!/bin/bash

MAIN_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Source Noshgrab_venv
pushd $MAIN_DIR/../../
source noshgrab_venv/bin/activate

# Export non-secret enviromental variables
export VAULT_ADDR=http://127.0.0.1:8200
export ENVIRONMENT="DEVELOPMENT"

# Read and Export each secret as an enviromental variable. 
export TOKEN=$(vault kv get -field=TOKEN -mount=noshgrab TOKEN)
export DB_PASS=$(vault kv get -field=DB_PASS -mount=noshgrab DB_PASS)

# Start Docker Container
sudo docker start noshgrab-db 

# Run app.py
python3 app.py