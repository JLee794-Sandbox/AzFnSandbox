output "function_app_url" {
  value = azurerm_linux_function_app.this.default_hostname
}

output "key_vault_id" {
  value = azurerm_key_vault.this.id
}
