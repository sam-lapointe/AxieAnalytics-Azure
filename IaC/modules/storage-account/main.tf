resource "azurerm_storage_account" "func_storage_account" {
  name                = var.storage_account_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags

  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  allow_nested_items_to_be_public = false
}

resource "azurerm_role_assignment" "storage_file_data_SMB_share_contributor" {
  count                = length(var.file_share_contributor_ids)
  scope                = azurerm_storage_account.func_storage_account.id
  role_definition_name = "Storage File Data SMB Share Contributor"
  principal_id         = var.file_share_contributor_ids[count.index]

  depends_on = [azurerm_storage_account.func_storage_account]
}