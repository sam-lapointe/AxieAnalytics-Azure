variable "web_app_name" {
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

variable service_plan_id {
  description = "The ID of the service plan to use for the Web App."
  type        = string
}

variable "umi_key_vault" {
  description = "The User Managed Identity to use to access Key Vault."
  type        = string
  default     = ""
}

variable "user_managed_identities" {
  description = "List of IDs for User Managed Identities to assign to the Web App."
  type        = list(string)
  default     = []
}

variable "language" {
    description = "The application language (e.g., python, node)."
    type        = string
    validation {
        condition     = contains(["python", "node"], var.language)
        error_message = "Invalid language. Allowed values are: python, node."
    }
}

variable "language_version" {
  description = "The version of the language to use."
  type = string
}

variable "app_settings" {
  description = "A map of key-value pairs for App Settings and custom values."
  type        = map(string)
  default     = {}
}

variable "startup_command" {
  description = "The startup command for the Web App."
  type        = string
  default     = ""
}