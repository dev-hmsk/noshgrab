#!/bin/bash

# Input Square Token
echo "input TOKEN" && read TOKEN
vault kv put -mount=noshgrab TOKEN TOKEN=$TOKEN

# Input DB_PASS
echo "input DB_PASS" && read DB_PASS
vault kv put -mount=noshgrab DB_PASS DB_PASS=$DB_PASS

# Input aws_access_key_id
echo "input aws_access_key_id" && read aws_access_key_id
vault kv put -mount=noshgrab aws_access_key_id aws_access_key_id=$aws_access_key_id

# Input aws_secret_access_key
echo "input aws_secret_access_key" && read aws_secret_access_key
vault kv put -mount=noshgrab aws_secret_access_key aws_secret_access_key=$aws_secret_access_key







