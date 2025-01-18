variable "project_name" {
  type    = string
  description = "GCP project name"
}

variable "location" {
  type    = string
  description = "Location of artifact repository"
}

variable "bucket_name" {
  type    = string
  description = "Name for Cloud storage bucket"
}
