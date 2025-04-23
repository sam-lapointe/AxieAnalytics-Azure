output "endpoint" {
  value = replace(azurerm_servicebus_namespace.servicebus_namespace.endpoint, ":443/", "")
}