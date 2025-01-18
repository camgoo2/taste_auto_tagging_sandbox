resource "google_bigquery_dataset" "dataset" {
  project = var.project_id
  dataset_id = var.bq_dataset_id
  delete_contents_on_destroy = true
}
