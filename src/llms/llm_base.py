from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict


@dataclass
class LLMResponse:
    response_text: str
    input_tokens: int
    output_tokens: int
    model: str
    response_time: float


class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: str, response_schema: Dict) -> str:
        ...
