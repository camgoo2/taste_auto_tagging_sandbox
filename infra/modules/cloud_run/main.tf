resource "google_cloud_run_v2_job" "default" {
  name     = var.cloud_run_job_name
  location = var.location

  template {
    template {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello"
      }
    }
  }

  lifecycle {
    ignore_changes = all
  }
}

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

resource "google_cloud_run_v2_service" "dev" {
  # count    = var.environment == "dev" ? 1 : 0
  name     = format("%s-dev", var.cloud_run_service_name)
  location = var.location
  ingress = "INGRESS_TRAFFIC_ALL"
  project = var.project_id

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"
    }
  }

  lifecycle {
    ignore_changes = all
    prevent_destroy = true
  }
}

resource "google_cloud_run_service" "mock-llm-server" {
  name     = "mock-llm-server"
  location = var.location
  # ingress = "INGRESS_TRAFFIC_ALL"
  project = var.project_id

  template {
    spec {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello"
      }
    }
  }

  lifecycle {
    ignore_changes = all
    prevent_destroy = true
  }
}

resource "google_cloud_scheduler_job" "default" {
  project = var.project_id
  name             = var.cloud_run_job_name
  schedule         = "0 12 * * *"

  http_target {
    http_method = "POST"
    uri         = "https://${var.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/${var.cloud_run_job_name}:run"

    oauth_token {
      service_account_email = var.service_account_email
    }
  }
  depends_on = [google_cloud_run_v2_job.default]
}
