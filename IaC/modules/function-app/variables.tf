variable "service_plan_name" {
  type = string
}

variable "function_app_name" {
  type = string
}

variable "app_insights_name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "tags" {
}

variable "log_workspace_id" {
  type = string
}

variable "storage_account_name" {
  description = "The storage account name which will be used by this Function App."
  type        = string
}

variable "storage_account_access_key" {
  description = "The access key of the storage account which will be used by this Function App."
  type        = string
  sensitive   = true
}

variable "umi_key_vault" {
  description = "The User Managed Identity to use to access Key Vault."
  type        = string
  default     = ""
}

variable "user_managed_identities" {
  description = "List of IDs for User Managed Identities to assign to the Function App."
  type        = list(string)
  default     = []
}

variable "authorized_ips" {
  description = "List of allowed IP addresses to interact with the Azure Function App webhook listener."
  type        = list(string)
  default     = []
}

variable "python_version" {
  description = "The version of Python to use."
  type = string
}

variable "app_settings" {
  description = "A map of key-value pairs for App Settings and custom values."
  type        = map(string)
  default     = {}
}