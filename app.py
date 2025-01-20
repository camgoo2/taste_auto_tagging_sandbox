import logging
import uuid

from fastapi import FastAPI
from fastapi import HTTPException

from src.config import PROJECT_ID
from src.llms.gemini import Gemini
from src.prompts import RECIPE_TAGGING_PROMPT_INSTRUCTIONS
from src.recipe.recipe_models import PredictedTag
from src.recipe.recipe_models import RecipeFeedback
from src.recipe.recipe_models import RecipeTaggingRequest
from src.recipe.recipe_models import RecipeTaggingResponse
from src.recipe.recipe_tagging import RecipeTagging
from src.utils import parse_json_from_gemini

# Get a logger instance
logger = logging.getLogger(__name__)

app = FastAPI()
recipe_tagging = RecipeTagging()
llm_model = Gemini(
    project_id=PROJECT_ID,
    model_name="gemini-1.5-pro-001",
    prompt_instruction=RECIPE_TAGGING_PROMPT_INSTRUCTIONS,
    temperature=0,
    max_output_tokens=1000,
)


@app.get("/health")
def health_check() -> dict:
    logger.info("Recieved health request")
    return {"status": "ok"}


@app.post("/predict-recipe-tags")
def predict_recipe_tags(
    recipe_tagging_request: RecipeTaggingRequest,
) -> RecipeTaggingResponse:
    # Validate request input
    if recipe_tagging_request is None:
        raise HTTPException(status_code=400, detail="Missing request body")
    elif not recipe_tagging_request.description:
        raise HTTPException(status_code=400, detail="Missing recipe description")
    elif not recipe_tagging_request.title:
        raise HTTPException(status_code=400, detail="Missing recipe title")
    elif len(recipe_tagging_request.ingredients) == 0:
        raise HTTPException(status_code=400, detail="Empty Ingredient List")
    elif len(recipe_tagging_request.method_steps) == 0:
        raise HTTPException(status_code=400, detail="Empty Method Step List")
    elif (
        recipe_tagging_request.max_num_of_tags
        and recipe_tagging_request.max_num_of_tags < 1
    ):
        raise HTTPException(
            status_code=400, detail="Maxiumum number of tags should be greater than 0"
        )

    prediction_id = str(uuid.uuid4())

    llm_response = recipe_tagging.generate_tags(
        recipe_tagging_request=recipe_tagging_request, llm_model=llm_model
    )
    print(f"llm response{llm_response}")
    json_llm_response = parse_json_from_gemini(json_str=llm_response)

    # Parse the response into PredictedTag objects
    response_tags = []
    for category_result in json_llm_response["classification"]:
        tag_category = category_result["category"]
        for tag_recommendation in category_result["tags"]:
            tag = tag_recommendation["tag"]
            confidence = tag_recommendation["confidence"]
            explanation = tag_recommendation["explanation"]
            response_tags.append(
                PredictedTag(
                    tag=tag,
                    confidence_score=confidence,
                    explanation=explanation,
                    tag_category=tag_category,
                )
            )

    # After retrieving all tags, reduce to max_num_of_tags
    max_tags = recipe_tagging_request.max_num_of_tags or 10
    reduced_tags = recipe_tagging.select_tags(response_tags, max_tags)

    # Construct the final response
    response = RecipeTaggingResponse(prediction_id=prediction_id, tags=reduced_tags)

    # Save prediction result to BQ
    errors_bq = recipe_tagging.save_prediction_result(recipe_tagging_request, response)

    if len(errors_bq) > 0:
        error_message = f"""Could not save result for recipe title: {recipe_tagging_request.title},
            recipe description: {recipe_tagging_request.description}"""

        raise HTTPException(status_code=500, detail=error_message)

    return response


@app.post("/save-prediction-feedback")
def save_prediction_feedback(
    recipe_feedback: RecipeFeedback,
) -> dict:
    # Validate request input
    if recipe_feedback is None:
        raise HTTPException(status_code=400, detail="Missing request body")

    errors_bq = recipe_tagging.save_prediction_feedback_bq(recipe_feedback)

    response = {"status": "success", "message": "Feedback saved successfully"}

    if len(errors_bq) > 0:
        error_message = f"""Could not save for feedback prediction_id: {recipe_feedback.prediction_id}"""
        raise HTTPException(status_code=500, detail=error_message)

    return response
