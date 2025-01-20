from typing import Dict

import vertexai
from vertexai.generative_models import GenerationConfig
from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import HarmBlockThreshold
from vertexai.generative_models import HarmCategory

from src.config import PROJECT_ID
from src.llms.llm_base import LLM


class Gemini(LLM):
    def __init__(
        self,
        project_id: str,
        model_name: str,
        prompt_instruction: str,
        temperature: float = 0.4,
        max_output_tokens: float = 1000,
    ):
        self.project_id = PROJECT_ID
        self.model_name = model_name
        self.prompt_instructions = prompt_instruction
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.model = GenerativeModel(
            model_name, system_instruction=[prompt_instruction]
        )

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }

        vertexai.init(project=self.project_id, location="australia-southeast1")

    # TODO: Change response to LLMResponse
    def generate(self, prompt: str, response_schema: Dict) -> str:
        response = self.model.generate_content(
            [prompt],
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=self.temperature,
                seed=1000,
            ),
            safety_settings=self.safety_settings,
            stream=False,
        )
        return response.text
