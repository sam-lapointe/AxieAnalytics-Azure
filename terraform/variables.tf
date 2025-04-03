variable "environment" {
    type = string
    validation {
      condition = contains(["prod", "staging", "dev"], var.environment)
      error_message = "Invalid environment. Allowed values are: prod, staging, dev."
    }
}

variable "rg_name" {
    type = string
    description = "Resource group name."
}

variable "alchemy_signing_key" {
    type = string
    ephemeral = true
    sensitive = true
}

variable "authorized_ips" {
    description = "List of allowed IP addresses to interact with the Azure Function App webhook listener."
    type = list(string)
    default = []
}