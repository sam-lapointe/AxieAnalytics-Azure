output "webhook_function_hostname" {
  value = module.webhook_function_app.function_app_hostname
}

output "webhook_function_name" {
  value = module.webhook_function_app.function_app_name
}

output "sales_function_hostname" {
  value = module.store_sales_function_app.function_app_hostname
}

output "sales_function_name" {
  value = module.store_sales_function_app.function_app_name
}

output "axies_function_hostname" {
  value = modules.store_axies_function_app.function_app_hostname
}

output "axies_function_name" {
  value = modules.store_axies_function_app.function_app_name
}

output "database_hostname" {
  value = module.postgresql_server.hostname
}