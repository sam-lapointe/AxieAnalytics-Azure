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

variable "POSTGRESQL_WEBHOOK_USERNAME" {
  type      = string
  sensitive = true
}

variable "POSTGRESQL_WEBHOOK_PASSWORD" {
  type      = string
  sensitive = true
}