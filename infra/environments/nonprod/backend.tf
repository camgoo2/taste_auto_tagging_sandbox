// Cannot use variables in backend specification
terraform {
  backend "gcs" {
    bucket = "even-lyceum-400005-tfstate"
    prefix  = "terraform/state"
  }
}
