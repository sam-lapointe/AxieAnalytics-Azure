resource "azurerm_key_vault" "key_vault" {
  name                = var.key_vault_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags
  tenant_id           = var.tenant_id

  purge_protection_enabled  = false
  sku_name                  = "standard"
  enable_rbac_authorization = true
}

resource "azurerm_role_assignment" "secrets_user" {
  count                = length(var.secrets_user_ids)
  scope                = azurerm_key_vault.key_vault.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = var.secrets_user_ids[count.index]
}

resource "azurerm_role_assignment" "secrets_officer" {
  count                = length(var.secrets_officer_ids)
  scope                = azurerm_key_vault.key_vault.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = var.secrets_officer_ids[count.index]
}

resource "azurerm_key_vault_secret" "secret" {
  count = length(keys(var.secrets))

  name         = nonsensitive(element(keys(var.secrets), count.index))
  value        = var.secrets[element(keys(var.secrets), count.index)]
  key_vault_id = azurerm_key_vault.key_vault.id

  depends_on = [azurerm_role_assignment.secrets_officer]
}