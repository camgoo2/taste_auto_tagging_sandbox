project_name = "even-lyceum-400005"

location = "australia-southeast1"

location_id = "australia-southeast1-c"

use_case = "taste-auto-tagging-sandbox"

use_case_conversation = "taiste-recipe-conversation"

cloud_run_job_name = "data-preprocessing"

cloud_run_service_name = "tagging-feedback-apis"

enable_apis = true

apis = [
    "artifactregistry.googleapis.com",
    "aiplatform.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "run.googleapis.com"
]

topic_schema_path = "../../../search/config/pub_sub_schema.avsc"

topic_conversation_schema_path = "../../../search/config/pub_sub_schema_conversation.avsc"

dataset_id = "taste_auto_tagging"

bq_table_entity_tag_prediction_result = "entity_tag_prediction_result"

bq_table_entity_tag_prediction_feedback = "entity_tag_prediction_feedback"

bq_table_entity_tag_prediction_evaluation = "entity_tag_prediction_evaluation"

bq_table_overall_evaluation_metrics = "overall_evaluation_metrics"

bq_table_recipe_tag_taxonomy = "recipe_tag_taxonomy"

mlops_sa_email = "new-mlops-service-account@even-lyceum-400005.iam.gserviceaccount.com"

mlops_sa_roles_list = [
    "roles/aiplatform.admin",
    "roles/artifactregistry.admin",
    "roles/bigquery.dataEditor",
    "roles/run.developer",
    "roles/storage.admin",
    "roles/iam.serviceAccountUser",
    "roles/bigquery.user",
    "roles/run.invoker"
]

environment = "nonprod"
