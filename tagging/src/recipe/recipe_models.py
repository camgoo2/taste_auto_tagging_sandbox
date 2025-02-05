from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional


@dataclass
class RecipeTaggingRequest:
    title: str
    description: str
    ingredients: List[str]
    method_steps: List[str]
    max_num_of_tags: Optional[int] = 10

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "ingredients": self.ingredients,
            "method_steps": self.method_steps,
            "max_num_of_tags": self.max_num_of_tags,
        }


@dataclass
class PredictedTag:
    tag: str
    tag_category: str
    confidence_score: float
    explanation: str

    def to_dict(self) -> Dict:
        return {
            "tag": self.tag,
            "tag_category": self.tag_category,
            "confidence_score": self.confidence_score,
            "explanation": self.explanation,
        }


@dataclass
class RecipeTaggingResponse:
    prediction_id: str
    tags: List[PredictedTag]


@dataclass
class SavedTag:
    tag: str
    tag_category: str

    def to_dict(self) -> Dict:
        return {
            "tag": self.tag,
            "tag_category": self.tag_category,
        }


@dataclass
class RecipeFeedback:
    prediction_id: str
    saved_tags: List[SavedTag]
    overall_feedback: int


RECIPE_TAGGING_LLM_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "classification": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "category": {
                        "type": "STRING",
                        "enum": [
                            "recipe",
                            "recipe-type",
                            "cuisine",
                            "main-ingredient",
                            "ingredient-category",
                        ],
                    },
                    "tags": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "tag": {
                                    "type": "STRING"  # Freeform string for dynamic tags
                                },
                                "confidence": {"type": "NUMBER"},
                                "salience": {"type": "NUMBER"},
                                "explanation": {"type": "STRING"},
                            },
                            "required": [
                                "tag",
                                "confidence",
                                "salience",
                                "explanation",
                            ],  # Essential fields are required
                        },
                    },
                },
                "required": [
                    "category",
                    "tags",
                ],  # Ensure category and tags are always present
            },
        }
    },
}
