provider "google" {
  user_project_override = true
  billing_project       = var.project_name
  region                = var.location
}

provider "google-beta" {
  user_project_override = true
  billing_project       = var.project_name
}
