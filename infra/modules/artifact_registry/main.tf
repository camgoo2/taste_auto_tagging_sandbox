resource "google_artifact_registry_repository" "docker" {
  project       = var.project_name
  location      = var.location
  repository_id = var.repository_id
  description   = "Docker repo for taste ai recipe search"
  format        = "DOCKER"
}
