terraform {
  backend "azurerm" {}


  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.25.0"
    }
  }
}

provider "azurerm" {
  resource_provider_registrations = "none"
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }

  subscription_id = var.subscription_id
}

locals {
  tags = {
    Environment = title(var.environment)
    App         = "AxieMarket"
  }

  # Enter each secret name that will be created in Azure Key Vault here to centrally manage them for Key Vault and Functions Apps
  ALCHEMY_SIGNING_KEY_NAME         = "alchemy-signing-key"
  POSTGRESQL_ADMIN_USERNAME_NAME   = "postgres-admin-username"
  POSTGRESQL_ADMIN_PASSWORD_NAME   = "postgres-admin-password"
  POSTGRESQL_WEBHOOK_USERNAME_NAME = "postgres-webhook-username"
  POSTGRESQL_WEBHOOK_PASSWORD_NAME = "postgres-webhook-password"
}

data "azurerm_client_config" "current" {
}

# The resource group already exists
data "azurerm_resource_group" "rg" {
  name = var.rg_name
}

resource "azurerm_user_assigned_identity" "umi_functionapp_external" {
  name                = "${var.environment}-axie-umi-external"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
}

resource "azurerm_user_assigned_identity" "umi_functionapp_internal" {
  name                = "${var.environment}-axie-umi-internal"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
}

resource "azurerm_user_assigned_identity" "umi_functionapp_database" {
  name                = "${var.environment}-axie-umi-database"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
}

module "key_vault_external" {
  source = "./modules/key-vault"

  key_vault_name      = "${var.environment}-axie-kv-ext"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
  tenant_id           = data.azurerm_client_config.current.tenant_id

  secrets_user_ids    = [azurerm_user_assigned_identity.umi_functionapp_external.principal_id]
  secrets_officer_ids = [data.azurerm_client_config.current.object_id]
  secrets = {
    (local.ALCHEMY_SIGNING_KEY_NAME) = var.ALCHEMY_SIGNING_KEY
  }

  depends_on = [azurerm_user_assigned_identity.umi_functionapp_external]
}

module "key_vault_internal" {
  source = "./modules/key-vault"

  key_vault_name      = "${var.environment}-axie-kv-int"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
  tenant_id           = data.azurerm_client_config.current.tenant_id

  secrets_user_ids    = [azurerm_user_assigned_identity.umi_functionapp_internal.principal_id]
  secrets_officer_ids = [data.azurerm_client_config.current.object_id]
  secrets = {
    (local.POSTGRESQL_WEBHOOK_USERNAME_NAME) = var.POSTGRESQL_WEBHOOK_USERNAME
    (local.POSTGRESQL_WEBHOOK_PASSWORD_NAME) = var.POSTGRESQL_WEBHOOK_PASSWORD
  }

  depends_on = [azurerm_user_assigned_identity.umi_functionapp_internal]
}

module "key_vault_database_admins" {
  source = "./modules/key-vault"

  key_vault_name      = "${var.environment}-axie-kv-admins"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
  tenant_id           = data.azurerm_client_config.current.tenant_id

  secrets_user_ids    = [azurerm_user_assigned_identity.umi_functionapp_database.principal_id]
  secrets_officer_ids = [data.azurerm_client_config.current.object_id]
  secrets = {
    (local.POSTGRESQL_ADMIN_USERNAME_NAME) = var.POSTGRESQL_ADMIN_USERNAME
    (local.POSTGRESQL_ADMIN_PASSWORD_NAME) = var.POSTGRESQL_ADMIN_PASSWORD
  }

  depends_on = [azurerm_user_assigned_identity.umi_functionapp_database]
}

module "function_app_storage_account" {
  source = "./modules/storage-account"

  storage_account_name = "${var.environment}axie${substr(var.subscription_id, 0, 4)}"
  resource_group_name  = data.azurerm_resource_group.rg.name
  location             = data.azurerm_resource_group.rg.location
  tags                 = local.tags
}

resource "azurerm_log_analytics_workspace" "logs_workspace" {
  name                = "${var.environment}-axie-logs"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags

  sku               = "PerGB2018"
  retention_in_days = 30
}

module "webhook_function_app" {
  source = "./modules/function-app"

  service_plan_name   = "${var.environment}-axie-webhook-sp"
  function_app_name   = "${var.environment}-axie-webhook-func"
  app_insights_name   = "${var.environment}-axie-webhook-ai"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags

  log_workspace_id           = azurerm_log_analytics_workspace.logs_workspace.id
  storage_account_name       = module.function_app_storage_account.storage_account_name
  storage_account_access_key = module.function_app_storage_account.primary_access_key
  umi_key_vault              = azurerm_user_assigned_identity.umi_functionapp_external.id
  user_managed_identities    = [azurerm_user_assigned_identity.umi_functionapp_external.id]
  python_version             = "3.11"
  authorized_ips             = var.authorized_ips
  app_settings = {
    "KEY_VAULT_NAME"                       = module.key_vault_external.key_vault_name
    "SIGNING_KEY"                          = local.ALCHEMY_SIGNING_KEY_NAME
    "AUTHORIZED_IPS"                       = jsonencode(var.authorized_ips)
    "SERVICEBUS_FULLY_QUALIFIED_NAMESPACE" = module.service_bus.endpoint
    "SERVICEBUS_TOPIC_NAME"                = "sales"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"       = "true"
    "AZURE_CLIENT_ID"                      = azurerm_user_assigned_identity.umi_functionapp_external.client_id
    "TEST"                                 = "Test2"
  }

  depends_on = [
    module.function_app_storage_account,
    azurerm_user_assigned_identity.umi_functionapp_external,
    module.service_bus
  ]
}

module "store_sales_function_app" {
  source = "./modules/function-app"

  service_plan_name   = "${var.environment}-axie-store-sales-sp"
  function_app_name   = "${var.environment}-axie-store-sales-func"
  app_insights_name   = "${var.environment}-axie-store-sales-ai"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags

  log_workspace_id           = azurerm_log_analytics_workspace.logs_workspace.id
  storage_account_name       = module.function_app_storage_account.storage_account_name
  storage_account_access_key = module.function_app_storage_account.primary_access_key
  umi_key_vault              = azurerm_user_assigned_identity.umi_functionapp_internal.id
  user_managed_identities    = [azurerm_user_assigned_identity.umi_functionapp_internal.id]
  python_version             = "3.11"

  depends_on = [
    module.function_app_storage_account,
    azurerm_user_assigned_identity.umi_functionapp_internal
  ]
}

module "service_bus" {
  source = "./modules/service-bus"

  servicebus_namespace_name = "${var.environment}-axie-servicebus"
  resource_group_name       = data.azurerm_resource_group.rg.name
  location                  = data.azurerm_resource_group.rg.location
  tags                      = local.tags

  topics = [
    {
      topic_name = "sales",
      sender_ids = [azurerm_user_assigned_identity.umi_functionapp_external.principal_id],
      subscriptions = [
        {
          subscription_name  = "add_to_database",
          max_delivery_count = 1
        }
      ]
    }
  ]

  depends_on = [azurerm_user_assigned_identity.umi_functionapp_external]
}

module "postgresql_server" {
  source = "./modules/postgresql"

  postgres_server_name = "${var.environment}-axie-db"
  resource_group_name  = data.azurerm_resource_group.rg.name
  location             = data.azurerm_resource_group.rg.location
  tags                 = local.tags

  administrator_username  = var.POSTGRESQL_ADMIN_USERNAME
  administrator_password  = var.POSTGRESQL_ADMIN_PASSWORD
  sku_name                = "B_Standard_B1ms"
  storage_mb              = 32768
  storage_tier            = "P4"
  postgresql_version      = 16
  fw_allow_azure_services = true
}