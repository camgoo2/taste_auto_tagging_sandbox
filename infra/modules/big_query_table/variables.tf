variable "project_id" {
  type    = string
  description = "The name of the project where the dataset and Big Query table will be located"
}

variable "bq_dataset_id" {
  type    = string
  description = "The name of the dataset/schema where the Big Query table is located"
}

variable "bq_table_id" {
  type    = string
  description = "The name of the Big Query table results will be inserted into"
}
