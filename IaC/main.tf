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
  POSTGRESQL_SALES_USERNAME_NAME   = "postgres-sales-username"
  POSTGRESQL_SALES_PASSWORD_NAME   = "postgres-sales-password"
  POSTGRESQL_AXIES_USERNAME_NAME   = "postgres-axies-username"
  POSTGRESQL_AXIES_PASSWORD_NAME   = "postgres-axies-password"
  POSTGRESQL_BACKEND_USERNAME_NAME = "postgres-backend-username"
  POSTGRESQL_BACKEND_PASSWORD_NAME = "postgres-backend-password"
  AXIE_API_KEY_NAME                = "axie-api-key"

  # Servicebus
  SERVICEBUS_TOPIC_SALES_NAME   = "sales"
  SERVICEBUS_TOPIC_AXIES_NAME   = "axies"
  STORE_SALES_SUBSCRIPTION_NAME = "store_sales"
  STORE_AXIES_SUBSCRIPTION_NAME = "store_axies"

  # Databases
  AXIEMARKET_DATABASE = "axie_market"
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
    (local.POSTGRESQL_SALES_USERNAME_NAME)   = var.POSTGRESQL_SALES_USERNAME
    (local.POSTGRESQL_SALES_PASSWORD_NAME)   = var.POSTGRESQL_SALES_PASSWORD
    (local.POSTGRESQL_AXIES_USERNAME_NAME)   = var.POSTGRESQL_AXIES_USERNAME
    (local.POSTGRESQL_AXIES_PASSWORD_NAME)   = var.POSTGRESQL_AXIES_PASSWORD
    (local.POSTGRESQL_BACKEND_USERNAME_NAME) = var.POSTGRESQL_BACKEND_USERNAME
    (local.POSTGRESQL_BACKEND_PASSWORD_NAME) = var.POSTGRESQL_BACKEND_PASSWORD
    (local.AXIE_API_KEY_NAME)                = var.AXIE_API_KEY
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
  authorized_ips             = var.webhook_authorized_ips
  app_settings = {
    "KEY_VAULT_NAME"                       = module.key_vault_external.key_vault_name
    "SIGNING_KEY"                          = local.ALCHEMY_SIGNING_KEY_NAME
    "AUTHORIZED_IPS"                       = jsonencode(var.webhook_authorized_ips)
    "SERVICEBUS_FULLY_QUALIFIED_NAMESPACE" = module.service_bus.endpoint
    "SERVICEBUS_TOPIC_NAME"                = "sales"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"       = "true"
    "AZURE_CLIENT_ID"                      = azurerm_user_assigned_identity.umi_functionapp_external.client_id
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
  app_settings = {
    "AZURE_CLIENT_ID"                               = azurerm_user_assigned_identity.umi_functionapp_internal.client_id
    "KEY_VAULT_NAME"                                = module.key_vault_internal.key_vault_name
    "ServiceBusConnection__fullyQualifiedNamespace" = module.service_bus.endpoint
    "SERVICEBUS_TOPIC_SALES_NAME"                   = local.SERVICEBUS_TOPIC_SALES_NAME
    "SERVICEBUS_TOPIC_AXIES_NAME"                   = local.SERVICEBUS_TOPIC_AXIES_NAME
    "SERVICEBUS_SALES_SUBSCRIPTION_NAME"            = local.STORE_SALES_SUBSCRIPTION_NAME
    "KV_PG_USERNAME"                                = local.POSTGRESQL_SALES_USERNAME_NAME
    "KV_PG_PASSWORD"                                = local.POSTGRESQL_SALES_PASSWORD_NAME
    "PG_HOST"                                       = "${module.postgresql_server.hostname}.postgres.database.azure.com"
    "PG_PORT"                                       = 5432
    "PG_DATABASE"                                   = local.AXIEMARKET_DATABASE
    "NODE_PROVIDER"                                 = var.ALCHEMY_NODE_PROVIDER
  }

  depends_on = [
    module.function_app_storage_account,
    azurerm_user_assigned_identity.umi_functionapp_internal,
    module.service_bus
  ]
}

module "store_axies_function_app" {
  source = "./modules/function-app"

  service_plan_name   = "${var.environment}-axie-store-axies-sp"
  function_app_name   = "${var.environment}-axie-store-axies-func"
  app_insights_name   = "${var.environment}-axie-store-axies-ai"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags

  log_workspace_id           = azurerm_log_analytics_workspace.logs_workspace.id
  storage_account_name       = module.function_app_storage_account.storage_account_name
  storage_account_access_key = module.function_app_storage_account.primary_access_key
  umi_key_vault              = azurerm_user_assigned_identity.umi_functionapp_internal.id
  user_managed_identities    = [azurerm_user_assigned_identity.umi_functionapp_internal.id]
  python_version             = "3.11"
  app_settings = {
    "AZURE_CLIENT_ID"                               = azurerm_user_assigned_identity.umi_functionapp_internal.client_id
    "KEY_VAULT_NAME"                                = module.key_vault_internal.key_vault_name
    "ServiceBusConnection__fullyQualifiedNamespace" = module.service_bus.endpoint
    "SERVICEBUS_TOPIC_AXIES_NAME"                   = local.SERVICEBUS_TOPIC_AXIES_NAME
    "SERVICEBUS_AXIES_SUBSCRIPTION_NAME"            = local.STORE_AXIES_SUBSCRIPTION_NAME
    "KV_PG_USERNAME"                                = local.POSTGRESQL_AXIES_USERNAME_NAME
    "KV_PG_PASSWORD"                                = local.POSTGRESQL_AXIES_PASSWORD_NAME
    "PG_HOST"                                       = "${module.postgresql_server.hostname}.postgres.database.azure.com"
    "PG_PORT"                                       = 5432
    "PG_DATABASE"                                   = local.AXIEMARKET_DATABASE
    "AXIE_API_KEY_NAME"                             = local.AXIE_API_KEY_NAME
  }
}

module "service_bus" {
  source = "./modules/service-bus"

  servicebus_namespace_name = "${var.environment}-axie-servicebus"
  resource_group_name       = data.azurerm_resource_group.rg.name
  location                  = data.azurerm_resource_group.rg.location
  tags                      = local.tags

  topics = [
    {
      topic_name   = local.SERVICEBUS_TOPIC_SALES_NAME,
      sender_ids   = [azurerm_user_assigned_identity.umi_functionapp_external.principal_id],
      receiver_ids = [azurerm_user_assigned_identity.umi_functionapp_internal.principal_id],
      subscriptions = [
        {
          subscription_name  = local.STORE_SALES_SUBSCRIPTION_NAME,
          max_delivery_count = 3
        }
      ]
    },
    {
      topic_name   = local.SERVICEBUS_TOPIC_AXIES_NAME,
      sender_ids   = [azurerm_user_assigned_identity.umi_functionapp_internal.principal_id],
      receiver_ids = [azurerm_user_assigned_identity.umi_functionapp_internal.principal_id],
      subscriptions = [
        {
          subscription_name  = local.STORE_AXIES_SUBSCRIPTION_NAME,
          max_delivery_count = 3
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
  authorized_ips          = var.POSTGRESQL_AUTHORIZED_IPS
  databases               = [local.AXIEMARKET_DATABASE]
}

resource "azurerm_service_plan" "web_app_service_plan" {
  name                = "${var.environment}-axie-web-app-sp"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags

  os_type  = "Linux"
  sku_name = "B1"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.environment}-axie-vnet"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_private_dns_zone" "private_dns_zone" {
  name                = "privatelink.azurewebsites.net"
  resource_group_name = data.azurerm_resource_group.rg.name
  tags                = local.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "webapp_dns_link" {
  name                  = "${var.environment}-axie-webapp-dns-link"
  resource_group_name   = data.azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.private_dns_zone.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}

resource "azurerm_subnet" "webapp_subnet" {
  name                 = "web-app-subnet"
  resource_group_name  = data.azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.5.0/24"]

  delegation {
    name = "WebAppDelegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "redis_subnet" {
  name                 = "redis-subnet"
  resource_group_name  = data.azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.6.0/24"]
}

module "backend" {
  source = "./modules/web-app"

  web_app_name              = "${var.environment}-axie-web-backend"
  resource_group_name       = data.azurerm_resource_group.rg.name
  location                  = data.azurerm_resource_group.rg.location
  tags                      = local.tags
  service_plan_id           = azurerm_service_plan.web_app_service_plan.id
  umi_key_vault             = azurerm_user_assigned_identity.umi_functionapp_internal.id
  user_managed_identities   = [azurerm_user_assigned_identity.umi_functionapp_internal.id]
  language                  = "python"
  language_version          = "3.11"
  startup_command           = "gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.app:app"
  virtual_network_subnet_id = azurerm_subnet.webapp_subnet.id

  app_settings = {
    "KEY_VAULT_NAME"                 = module.key_vault_internal.key_vault_name
    "PG_HOST"                        = "${module.postgresql_server.hostname}.postgres.database.azure.com"
    "PG_PORT"                        = 5432
    "PG_DATABASE"                    = local.AXIEMARKET_DATABASE
    "KV_PG_USERNAME"                 = local.POSTGRESQL_BACKEND_USERNAME_NAME
    "KV_PG_PASSWORD"                 = local.POSTGRESQL_BACKEND_PASSWORD_NAME
    "AZURE_CLIENT_ID"                = azurerm_user_assigned_identity.umi_functionapp_internal.client_id
    "AXIE_API_KEY_NAME"              = local.AXIE_API_KEY_NAME
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }
}

module "frontend" {
  source = "./modules/web-app"

  web_app_name        = "${var.environment}-axie-web-frontend"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  tags                = local.tags
  service_plan_id     = azurerm_service_plan.web_app_service_plan.id
  language            = "node"
  language_version    = "22-lts"
  startup_command     = "pm2 serve /home/site/wwwroot --no-daemon --spa"
}

resource "azurerm_redis_cache" "redis_cache" {
  name                = "${var.environment}-axie-redis"
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  tags                = local.tags

  capacity                           = 0
  family                             = "C"
  sku_name                           = "Basic"
  minimum_tls_version                = "1.2"
  access_keys_authentication_enabled = false

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.umi_functionapp_internal.id
    ]
  }

  redis_configuration {
    active_directory_authentication_enabled = true
  }
}

resource "azurerm_private_endpoint" "redis_private_endpoint" {
  name                = "${var.environment}-axie-redis-pe"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location
  subnet_id           = azurerm_subnet.redis_subnet.id

  private_service_connection {
    name                           = "backend-privateserviceconnection"
    is_manual_connection           = false
    private_connection_resource_id = module.backend.web_app_id
    subresource_names              = ["sites"]
  }
}