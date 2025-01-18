resource "google_storage_bucket" "source" {
  name                        = var.bucket_name
  project                     = var.project_name
  location                    = var.location
  force_destroy               = true
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  storage_class               = "STANDARD"
}
