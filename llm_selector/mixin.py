# llm_selector/mixin.py
from .selector import LLMSelector
import os

_selector = LLMSelector(os.getenv("GATEWAY_URL", "http://localhost:4000"))

class LLMChoiceMixin:
    def llm_choice(self, prompt: str, task_type: str = "default",
                   deadline_sec: int = 60, max_cost_usd: float = 0.10):
        return _selector.choose(prompt, task_type,
                                deadline_sec=deadline_sec,
                                max_cost_usd=max_cost_usd)