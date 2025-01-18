output "project_name" {
  description = "GCP project name"
  value = var.project_name
}

output "location" {
  description = "GCP location"
  value = var.location
}

output "use_case" {
  description = "Use case name to use for naming conventions"
  value = var.use_case
}

output "dataset_id" {
  description = "Use case name using underscore for dataset"
  value = var.dataset_id
}

output "mlops_sa_email" {
  description = "Use case name using underscore for dataset"
  value = var.mlops_sa_email
}
