output "webhook_function_hostname" {
  value = module.webhook_function_app.function_app_hostname
}

output "database_hostname" {
  value = module.postgresql_server.hostname
}