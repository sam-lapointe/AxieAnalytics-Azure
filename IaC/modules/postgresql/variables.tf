variable "postgres_server_name" {
    type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "administrator_username" {
    description = "PostgresSQL Administrator Username"
    type = string
    sensitive = true
}

variable "administrator_password" {
    description = "PostgreSQL Administrator Password"
    type = string
    sensitive = true
}

variable "sku_name" {
  type = string
  default = "B_Standard_B1ms"
}

variable "storage_mb" {
  type = number
  default = 32768
}

variable "storage_tier" {
  type = string
  default = "P4"
}

variable "postgresql_version" {
  type = number
  default = 16
}

# This is needed for Azure Functions Apps with consumption plan that need to acces the database.
variable "fw_allow_azure_services" {
  description = "Allow public access from Azure Services"
  type = bool
  default = true
}

variable "authorized_ips" {
  description = "List of allowed IP addresses to connect to the database."
  type        = list(string)
  default     = []
}