
storage "file" {
  path = "/home/ubuntu/noshgrab/vault/vault_data/"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}

ui = true
