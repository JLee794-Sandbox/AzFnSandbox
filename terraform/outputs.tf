output "function_app_url" {
  value = azurerm_function_app.example.default_hostname
}

output "key_vault_id" {
  value = azurerm_key_vault.example.id
}
