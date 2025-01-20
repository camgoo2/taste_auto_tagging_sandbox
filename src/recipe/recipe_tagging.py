from datetime import datetime
from typing import Dict
from typing import List

import pytz  # type: ignore

from src.config import FEEDBACK_DATASET_ID
from src.config import FEEDBACK_TABLE_ID
from src.config import PROJECT_ID
from src.config import RESULT_DATASET_ID
from src.config import RESULT_TABLE_ID
from src.config import EntityType
from src.llms.llm_base import LLM
from src.prompts import RECIPE_TAGGING_PROMPT
from src.recipe.recipe_models import RECIPE_TAGGING_LLM_RESPONSE_SCHEMA
from src.recipe.recipe_models import RecipeFeedback
from src.recipe.recipe_models import RecipeTaggingRequest
from src.recipe.recipe_models import RecipeTaggingResponse

from ..bigquery_utils import fetch_candidate_tags
from ..bigquery_utils import write_data_bq
from ..sql_queries import QUERY_TAXONOMY


class RecipeTagging:
    def __init__(self) -> None:
        self.candidate_tags = fetch_candidate_tags(QUERY_TAXONOMY, PROJECT_ID)

    def generate_tags(
        self, recipe_tagging_request: RecipeTaggingRequest, llm_model: LLM
    ) -> str:

        prompt_data = {
            "title": recipe_tagging_request.title,
            "description": recipe_tagging_request.description,
            "method_steps": ", ".join(recipe_tagging_request.method_steps),
            "ingredients": ". ".join(recipe_tagging_request.ingredients),
        }
        # Generate model prompt based on the recipe
        prompt = RECIPE_TAGGING_PROMPT.format(
            categories=self.candidate_tags, data=prompt_data
        )
        print(prompt)

        llm_response = llm_model.generate(prompt, RECIPE_TAGGING_LLM_RESPONSE_SCHEMA)

        return llm_response

    def select_tags(self, all_tags: List, max_tags: int) -> List:
        """
        Reduce tags to the requested max number of tags. Each category gets at least one tag,
        and remaining slots are allocated based on confidence score.
        """
        # Group tags by category
        tags_by_category: Dict = {}
        for tag in all_tags:
            if tag.tag_category not in tags_by_category:
                tags_by_category[tag.tag_category] = []
            tags_by_category[tag.tag_category].append(tag)

        # Ensure each category has at least one tag
        selected_tags = []
        remaining_tags = []
        for category, tags in tags_by_category.items():
            # Sort tags within each category by confidence score
            tags.sort(key=lambda t: t.confidence_score, reverse=True)
            if tags:
                # Select the top tag from each category
                selected_tags.append(tags.pop(0))
            # Add remaining tags to the pool
            remaining_tags.extend(tags)

        # Allocate remaining slots based on confidence score
        remaining_tags.sort(key=lambda t: t.confidence_score, reverse=True)
        additional_tags_needed = max_tags - len(selected_tags)
        if additional_tags_needed < 1:
            selected_tags.sort(key=lambda t: t.confidence_score, reverse=True)
            return selected_tags[:max_tags]
        else:
            selected_tags.extend(remaining_tags[:additional_tags_needed])

        return selected_tags

    def save_prediction_result(
        self,
        recipe_tagging_request: RecipeTaggingRequest,
        prediction_response: RecipeTaggingResponse,
    ) -> List:
        prediction_id = prediction_response.prediction_id

        tz = pytz.timezone("Australia/Sydney")
        insert_timestamp = str(datetime.now(tz))
        entity_type = EntityType.RECIPES.value

        tag_list = [tag.to_dict() for tag in prediction_response.tags]

        bq_result = [
            {
                "prediction_id": prediction_id,
                "insert_timestamp": insert_timestamp,
                "entity_type": entity_type,
                "tags": tag_list,
                "request": recipe_tagging_request.to_dict(),
            }
        ]

        error_list = write_data_bq(
            project_id=PROJECT_ID,
            dataset_id=RESULT_DATASET_ID,
            table_id=RESULT_TABLE_ID,
            rows=bq_result,
        )

        print(error_list)
        return error_list

    def save_prediction_feedback_bq(self, recipe_feedback: RecipeFeedback) -> List:
        prediction_id = recipe_feedback.prediction_id
        tz = pytz.timezone("Australia/Sydney")
        insert_timestamp = str(datetime.now(tz))

        overall_feedback = recipe_feedback.overall_feedback
        saved_tags = [tag.to_dict() for tag in recipe_feedback.saved_tags]
        bq_result = [
            {
                "prediction_id": prediction_id,
                "insert_timestamp": insert_timestamp,
                "overall_feedback": overall_feedback,
                "saved_tags": saved_tags,
            }
        ]

        error_list = write_data_bq(
            project_id=PROJECT_ID,
            dataset_id=FEEDBACK_DATASET_ID,
            table_id=FEEDBACK_TABLE_ID,
            rows=bq_result,
        )

        print(error_list)
        return error_list
