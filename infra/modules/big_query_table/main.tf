resource "google_bigquery_table" "table" {
  deletion_protection = false
  project = var.project_id
  table_id   = var.bq_table_id
  dataset_id = var.bq_dataset_id

  schema = file("../../../config/bq_table_${var.bq_table_id}_schema.json")
}
