locals {
  sender_role_assignments = flatten([
    for topic in var.topics : [
      for sender_id in topic.sender_ids : {
        topic_name = topic.topic_name
        sender_id  = sender_id
      }
    ]
  ])
}

resource "azurerm_servicebus_namespace" "servicebus_namespace" {
  name                = var.servicebus_namespace_name
  resource_group_name = var.resource_group_name
  location            = var.location
  tags                = var.tags

  sku = "Standard"
}

resource "azurerm_servicebus_topic" "topic" {
  for_each = {
    for topic in var.topics : topic.topic_name => topic
  }

  name         = each.key
  namespace_id = azurerm_servicebus_namespace.servicebus_namespace.id
}

resource "azurerm_servicebus_subscription" "subscription" {
  for_each = {
    for pair in flatten([
      for topic in var.topics : [
        for sub in topic.subscriptions : {
          key = "${topic.topic_name}-${sub.subscription_name}"
          value = {
            topic_name = topic.topic_name
            subscription_name = sub.subscription_name
            max_delivery_count = sub.max_delivery_count
          }
        }
      ]
    ]) : pair.key => pair.value
  }

  name               = each.value.subscription_name
  topic_id           = azurerm_servicebus_topic.topic[each.value.topic_name].id
  max_delivery_count = each.value.max_delivery_count
}

resource "azurerm_role_assignment" "servicebus_data_sender" {
  for_each = {
    for idx, pair in local.sender_role_assignments : idx => pair
  }

  scope                = azurerm_servicebus_topic.topic[each.value.topic_name].id
  role_definition_name = "Azure Service Bus Data Sender"
  principal_id         = each.value.sender_id
}