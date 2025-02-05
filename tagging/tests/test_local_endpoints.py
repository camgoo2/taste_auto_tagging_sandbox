from app import app  # Import your FastAPI app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_app_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_recipe_tags():
    # Sample request payload
    request_payload = {
        "title": "Spaghetti Bolognese",
        "description": "A simple classic Italian dish",
        "ingredients": ["beef", "tomato", "garlic", "onion", "pasta"],
        "method_steps": ["Cook pasta", "Prepare sauce", "Mix together"],
    }

    response = client.post("/predict-recipe-tags", json=request_payload)

    # Ensure the response is 200 OK
    assert response.status_code == 200

    # Extract JSON response
    response_json = response.json()

    # Example structure validation (update based on actual `RecipeTaggingResponse`)
    assert (
        "prediction_id" in response_json
    )  # Check if response includes 'prediction_id'
    assert "tags" in response_json  # Check if response includes 'tags'
    assert isinstance(response_json["tags"], list)  # Ensure 'tags' is a list
    assert len(response_json["tags"]) > 0  # Ensure at least one tag is returned


def test_invalid_data_type():
    request_payload = {
        "title": 123,  # Invalid type (should be a string)
        "description": "A simple classic Italian dish",
        "ingredients": ["beef", "tomato", "garlic", "onion", "pasta"],
        "method_steps": ["Cook pasta", "Prepare sauce", "Mix together"],
    }
    response = client.post("/predict-recipe-tags", json=request_payload)

    assert response.status_code == 422


def test_save_prediction_feedback():
    # Sample request payload
    request_payload = {
        "prediction_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "overall_feedback": 1,
        "saved_tags": [
            {"tag": "chicken breast", "tag_category": "main-ingredient"},
            {"tag": "rice", "tag_category": "ingredient-category"},
            {"tag": "mango", "tag_category": "ingredient-category"},
        ],
    }

    response = client.post("/save-prediction-feedback", json=request_payload)

    # Ensure the response is 200 OK
    assert response.status_code == 200

    # Extract JSON response
    response_json = response.json()

    # Example structure validation
    assert "message" in response_json  # Ensure response includes 'message'
    assert response_json["message"] == "Feedback saved successfully"
