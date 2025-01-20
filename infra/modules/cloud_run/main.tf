resource "google_cloud_run_v2_service" "default" {
  # count    = var.environment != "dev" ? 1 : 0
  name     = var.cloud_run_service_name
  location = var.location
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }

  lifecycle {
    # prevent_destroy = var.environment == "dev" ? true
    prevent_destroy = true
    # ignore_changes  = var.environment != "dev" ? all
    ignore_changes  = all
  }

}
