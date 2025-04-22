variable "servicebus_namespace_name" {
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

variable "servicebus_sku" {
    type = string
    default = "Standard"
}

variable "topics" {
    description = "List of topics with allowed principal IDs to send data and their subscription configurations."
    type = list(object({
        topic_name = string
        sender_ids = list(string)
        subscriptions = list(object({
            subscription_name = string
            max_delivery_count = number
        }))
    }))
}