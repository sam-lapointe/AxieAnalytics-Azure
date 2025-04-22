variable "key_vault_name" {
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

variable "tenant_id" {
  type = string
}

variable "secrets_user_ids" {
  type = list(string)
}

variable "secrets_officer_ids" {
  type = list(string)
}

variable "secrets" {
  type = map(string)
  sensitive = true
  default = {}
}