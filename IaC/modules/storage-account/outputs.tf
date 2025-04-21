output "storage_account_name" {
    value = azurerm_storage_account.func_storage_account.name
}

output "primary_access_key" {
  value     = azurerm_storage_account.func_storage_account.primary_access_key
  sensitive = true
}