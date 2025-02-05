import os
from enum import Enum

import dotenv

# Load env variables from file
dotenv.load_dotenv()

# Load env variables (coming from terraform output)
# GCP project ID
PROJECT_ID = os.environ.get("PROJECT_ID", "even-lyceum-400005")

NEWS_QUERY_PRD_PROJECT_ID = os.environ.get(
    "NEWS_QUERY_PRD_PROJECT_ID", "ncau-data-newsquery-prd"
)
RESULT_DATASET_ID = os.environ.get("RESULT_DATASET_ID", "taste_auto_tagging")
RESULT_TABLE_ID = os.environ.get("RESULT_TABLE_ID", "entity_tag_prediction_result")

EVAL_DATASET_ID = os.environ.get("EVAL_DATASET_ID", "taste_auto_tagging")
EVAL_TABLE_ID = os.environ.get("EVAL_TABLE_ID", "entity_tag_prediction_evaluation")

OVERALL_METRIC_DATASET_ID = os.environ.get(
    "OVERALL_METRIC_DATASET_ID", "taste_auto_tagging"
)
OVERALL_METRIC_TABLE_ID = os.environ.get(
    "OVERALL_METRIC_TABLE_ID", "overall_evaluation_metrics"
)

MAX_CREATE_DATE_RECIPE_EVAL = "2024-12-06"

USE_SEMANTIC_SIMILARITY_FOR_EVAL = False

FEEDBACK_DATASET_ID = os.environ.get("FEEDBACK_DATASET_ID", "taste_auto_tagging")

FEEDBACK_TABLE_ID = os.environ.get(
    "FEEDBACK_TABLE_ID", "entity_tag_prediction_feedback"
)


class EntityType(Enum):
    RECIPES = "recipes"
    ARTICLES = "articles"
    GALLLERY = "gallery"
