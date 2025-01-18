variable "project_id" {
  type    = string
  description = "GCP project name"
}

variable "service_account_email" {
    type = string
    description = "Service account email to assign IAM policies to"
}

variable "roles_list" {
    type = list(string)
    description = "List of IAM roles to assign to service account"
}
