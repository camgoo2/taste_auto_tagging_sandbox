variable "cloud_run_service_name" {
  type    = string
  description = "Cloud Run Service name"
}

variable "location" {
  type    = string
  description = "Location of artifact repository"
}

variable "project_id" {
  type    = string
  description = "GCP project name"
}

variable "service_account_email" {
    type = string
    description = "Service account email to assign IAM policies to"
}

variable "environment" {
    type = string
    description = "environment to deploy"
}
