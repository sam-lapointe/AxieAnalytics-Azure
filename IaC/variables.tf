variable "environment" {
  type = string
  validation {
    condition     = contains(["prod", "staging", "dev"], var.environment)
    error_message = "Invalid environment. Allowed values are: prod, staging, dev."
  }
}

variable "subscription_id" {
  type = string
}

variable "rg_name" {
  type        = string
  description = "Resource group name."
}

variable "ALCHEMY_SIGNING_KEY" {
  type      = string
  sensitive = true
}

variable "ALCHEMY_NODE_PROVIDER" {
  type      = string
  sensitive = true
}

variable "webhook_authorized_ips" {
  description = "List of allowed IP addresses to interact with the Azure Function App webhook listener."
  type        = list(string)
  default     = []
}

variable "POSTGRESQL_AUTHORIZED_IPS" {
  description = "List of allowed IP addresses to connect to the PostgreSQL database."
  type        = list(string)
  default     = []
  sensitive   = true
}

variable "POSTGRESQL_ADMIN_USERNAME" {
  type      = string
  sensitive = true
}

variable "POSTGRESQL_ADMIN_PASSWORD" {
  type      = string
  sensitive = true
}

variable "POSTGRESQL_SALES_USERNAME" {
  type      = string
  sensitive = true
}

variable "POSTGRESQL_SALES_PASSWORD" {
  type      = string
  sensitive = true
}

variable "POSTGRESQL_AXIES_USERNAME" {
  type      = string
  sensitive = true
}

variable "POSTGRESQL_AXIES_PASSWORD" {
  type      = string
  sensitive = true
}

variable "AXIE_API_KEY" {
  type      = string
  sensitive = true
}