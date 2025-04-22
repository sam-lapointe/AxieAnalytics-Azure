locals {
  tags_to_add = {
    "hidden-link: /app-insights-conn-string"         = ""
    "hidden-link: /app-insights-instrumentation-key" = ""
    "hidden-link: /app-insights-resource-id"         = ""
  }

  tags_func = merge(var.tags, local.tags_to_add)
}

resource "azurerm_service_plan" "service_plan" {
  name                = var.service_plan_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags

  os_type  = "Linux"
  sku_name = "Y1"
}

resource "azurerm_application_insights" "app_insights" {
  name                = var.app_insights_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags

  workspace_id = var.log_workspace_id
  application_type = "web"
}

resource "azurerm_linux_function_app" "function_app" {
  name                = var.function_app_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = local.tags_func

  storage_account_name            = var.storage_account_name
  storage_account_access_key      = var.storage_account_access_key
  service_plan_id                 = azurerm_service_plan.service_plan.id
  functions_extension_version     = "~4"
  key_vault_reference_identity_id = var.umi_key_vault

  site_config {
    application_stack {
      python_version = var.python_version
    }

    application_insights_connection_string = azurerm_application_insights.app_insights.connection_string
    application_insights_key               = azurerm_application_insights.app_insights.instrumentation_key

    dynamic "ip_restriction" {
      for_each = var.authorized_ips
      content {
        ip_address = "${ip_restriction.value}/32"
        action     = "Allow"
      }
    }
  }

  app_settings = var.app_settings

  identity {
    type = "UserAssigned"
    identity_ids = var.user_managed_identities
  }

  lifecycle {
    ignore_changes = [
      tags["hidden-link: /app-insights-conn-string"],
      tags["hidden-link: /app-insights-instrumentation-key"],
      tags["hidden-link: /app-insights-resource-id"]
    ]
  }
}

resource "azurerm_linux_function_app_slot" "function_app_staging_slot" {
  name                       = "staging"
  tags                       = local.tags_func
  function_app_id            = azurerm_linux_function_app.function_app.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key

  site_config {
    application_stack {
      python_version = var.python_version
    }

    application_insights_connection_string = azurerm_application_insights.app_insights.connection_string
    application_insights_key               = azurerm_application_insights.app_insights.instrumentation_key

    dynamic "ip_restriction" {
      for_each = var.authorized_ips
      content {
        ip_address = "${ip_restriction.value}/32"
        action     = "Allow"
      }
    }
  }

  app_settings = var.app_settings

  identity {
    type = "UserAssigned"
    identity_ids = var.user_managed_identities
  }

  lifecycle {
    ignore_changes = [
      tags["hidden-link: /app-insights-conn-string"],
      tags["hidden-link: /app-insights-instrumentation-key"],
      tags["hidden-link: /app-insights-resource-id"]
    ]
    create_before_destroy = false
    replace_triggered_by = [
      azurerm_linux_function_app.function_app
    ]
  }
}