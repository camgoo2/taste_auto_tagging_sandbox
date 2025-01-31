variable "project_name" {
  type    = string
  description = "GCP project name"
}

variable "environment" {
  type    = string
  description = "environment to deploy (e.g., dev, prod)"
}

variable "location" {
  default = "australia-southeast1"
  type    = string
}

variable "location_id" {
  default = "australia-southeast1-c"
  type    = string
}

variable "use_case" {
  type    = string
  description = "Use case name"
}

variable "enable_apis" {
  default = true
  type    = bool
}

variable "apis" {
  type    = list(string)
  description = "List of GCP API to enable"
}

variable "dataset_id" {
  type    = string
  description = "The name of the BQ dataset results will be inserted into"
}

variable "bq_table_entity_tag_prediction_result" {
  type    = string
  description = "The name of the Big Query table prediction results are saved to"
}

variable "bq_table_entity_tag_prediction_feedback" {
  type    = string
  description = "The name of the Big Query table user feedback is saved to"
}

variable "bq_table_entity_tag_prediction_evaluation" {
  type    = string
  description = "The name of the Big Query table evaluation results are saved to"
}

variable "bq_table_overall_evaluation_metrics" {
  type    = string
  description = "The name of the Big Query table overall evaluation metrics are saved to"
}

  variable "bq_table_recipe_tag_taxonomy" {
  type        = string
  description = "The recipe taxonomy"
  }

variable "mlops_sa_email" {
    type = string
    description = "Service account email to assign IAM policies to"
}

variable "mlops_sa_roles_list" {
    type = list(string)
    description = "List of IAM roles to assign to service account"
}

variable "cloud_run_service_name" {
  type    = string
  description = "Cloud Run Service name"
}
