variable "storage_account_name" {
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

variable "file_share_contributor_ids" {
  type = list(string)
}