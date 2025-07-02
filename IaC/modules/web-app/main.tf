resource "azurerm_linux_web_app" "web_app" {
  name                = var.web_app_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags

  service_plan_id                 = var.service_plan_id
  key_vault_reference_identity_id = var.umi_key_vault

  site_config {
    application_stack {
      python_version = var.python_version
    }

    app_command_line = var.startup_command != "" ? var.startup_command : null
  }

  app_settings = var.app_settings

  identity {
    type = "UserAssigned"
    identity_ids = var.user_managed_identities
  }
}