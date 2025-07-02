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
  value = module.store_axies_function_app.function_app_hostname
}

output "axies_function_name" {
  value = module.store_axies_function_app.function_app_name
}

output "backend_web_app_name" {
  value = module.backend.web_app_name
}

output "frontend_web_app_name" {
  value = module.frontend.web_app_name
}

output "database_hostname" {
  value = module.postgresql_server.hostname
}