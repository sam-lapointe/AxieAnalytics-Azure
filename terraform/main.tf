terraform {
    backend "azurerm" {}


    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "4.25.0"
        }
    }
}

provider "azurerm" {
    resource_provider_registrations = "none"
    features {}
}

data "azurerm_client_config" "current" {
}

# The resource group already exists
data "azurerm_resource_group" "rg" {
    name = var.rg_name
}

resource "azurerm_key_vault" "key_vault" {
    name = "${var.environment}-axie-kv"
    resource_group_name = data.azurerm_resource_group.rg.name
    location = data.azurerm_resource_group.rg.location
    tenant_id = data.azurerm_client_config.current.tenant_id
    purge_protection_enabled = false

    sku_name = "standard"

    enable_rbac_authorization = true
}

resource "azurerm_key_vault_secret" "alchemy_signing_key" {
    name = "alchemy-signing-key"
    value = var.alchemy_signing_key
    key_vault_id = azurerm_key_vault.key_vault.id
}

resource "azurerm_storage_account" "func_storage_account" {
    name = "${var.environment}axie${substr(data.azurerm_client_config.subscription_id, 0, 4)}"
    resource_group_name = data.azurerm_resource_group.rg.name
    location = data.azurerm_resource_group.rg.location
    account_tier = "Standard"
    account_replication_type = "LRS"
}

resource "azurerm_service_plan" "webhook_listener" {
    name = "${var.environment}-axie-webhook-ASP"
    resource_group_name = data.azurerm_resource_group.rg.name
    location = data.azurerm_resource_group.rg.location
    os_type = "Linux"
    sku_name = "Y1"
}

resource "azurerm_linux_function_app" "webhook_listener" {
    name = "${var.environment}-axie-webhook-FuncApp"
    resource_group_name = data.azurerm_resource_group.rg.name
    location = data.azurerm_resource_group.rg.location

    storage_account_name = azurerm_storage_account.func_storage_account.name
    storage_account_access_key = azurerm_storage_account.func_storage_account.primary_access_key
    service_plan_id = azurerm_service_plan.webhook_listener.id
    functions_extension_version = "~4"

    site_config {
        application_stack {
          python_version = "3.11"
        }

        dynamic "ip_restriction" {
          for_each = var.authorized_ips
          content{
            ip_address = ip_restriction.value
            action = "Allow"
          }
        }
    }

    app_settings = {
        "KEY_VAULT_NAME" = azurerm_key_vault.key_vault.name
        "SIGNING_KEY" = azurerm_key_vault_secret.alchemy_signing_key.name
        "AUTHORIZED_IPS" = var.authorized_ips
    }
}