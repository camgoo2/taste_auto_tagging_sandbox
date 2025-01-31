module "project-services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 14.4"

  project_id                  = var.project_name
  enable_apis                 = var.enable_apis
  disable_services_on_destroy = false

  // Add new required API's in the array below
  activate_apis = var.apis
}

module "iam_policies_mlops_sa" {
  source = "../../modules/iam"
  project_id = var.project_name
  service_account_email = var.mlops_sa_email
  roles_list = var.mlops_sa_roles_list
}

module "big_query_ds" {
  source        = "../../modules/big_query_ds"
  bq_dataset_id = var.dataset_id
  project_id = var.project_name
}

module "big_query_table_entity_tag_prediction_result" {
  source        = "../../modules/big_query_table"
  project_id = var.project_name
  bq_dataset_id = var.dataset_id
  bq_table_id = var.bq_table_entity_tag_prediction_result
  depends_on = [module.big_query_ds]
}

module "big_query_table_entity_tag_prediction_feedback" {
  source        = "../../modules/big_query_table"
  project_id = var.project_name
  bq_dataset_id = var.dataset_id
  bq_table_id = var.bq_table_entity_tag_prediction_feedback
  depends_on = [module.big_query_ds]
}

module "big_query_table_entity_tag_prediction_evaluation" {
  source        = "../../modules/big_query_table"
  project_id = var.project_name
  bq_dataset_id = var.dataset_id
  bq_table_id = var.bq_table_entity_tag_prediction_evaluation
  depends_on = [module.big_query_ds]
}

module "big_query_table_overall_evaluation_metrics" {
  source        = "../../modules/big_query_table"
  project_id = var.project_name
  bq_dataset_id = var.dataset_id
  bq_table_id = var.bq_table_overall_evaluation_metrics
  depends_on = [module.big_query_ds]
}

module "big_query_table_recipe_tag_taxonomy" {
  source        = "../../modules/big_query_table"
  project_id = var.project_name
  bq_dataset_id = var.dataset_id
  bq_table_id = var.bq_table_recipe_tag_taxonomy
  depends_on = [module.big_query_ds]
}

module "google_storage_bucket" {
  source        = "../../modules/cloud_storage"
  project_name  = var.project_name
  location      = var.location
  bucket_name   = "${var.use_case}-${var.environment}"
}

module "google_storage_bucket_test" {
  source        = "../../modules/cloud_storage"
  project_name  = var.project_name
  location      = var.location
  bucket_name   = "${var.use_case}-${var.environment}-test"
}

module "artifact_registry" {
  source        = "../../modules/artifact_registry"
  project_name  = var.project_name
  location      = var.location
  repository_id = var.use_case
}

module "cloud_run" {
  source        = "../../modules/cloud_run"
  environment = var.environment
  project_id = var.project_name
  location = var.location
  cloud_run_service_name = var.cloud_run_service_name
  service_account_email = var.mlops_sa_email
}
