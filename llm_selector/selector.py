# llm_selector/selector.py
import yaml, os, time, httpx, logging, pathlib
from functools import lru_cache

CONFIG_PATH = pathlib.Path(os.getenv("SELECTOR_RULES", "infra/lite_llm/rules.yaml"))
REFRESH_SEC = 10

logger = logging.getLogger("llm_selector")

class LLMSelector:
    """Rule-table selector with live hot-reload.
    choose(prompt, task_type, deadline_sec, max_cost_usd) → dict"""
    def __init__(self, gateway_url: str):
        self.gateway = gateway_url
        self._load_rules()
        self._last_read = time.time()

    def _load_rules(self):
        with open(CONFIG_PATH, "r") as fp:
            self.rules = yaml.safe_load(fp)

    def _maybe_reload(self):
        if time.time() - self._last_read > REFRESH_SEC:
            self._load_rules()
            self._last_read = time.time()

    @lru_cache(maxsize=256)
    def _list_models(self):
        resp = httpx.get(f"{self.gateway}/v1/models", timeout=5)
        resp.raise_for_status()
        return {m["id"]: m for m in resp.json()["data"]}

    def choose(self, prompt: str, task_type: str, *,
               deadline_sec: int = 60, max_cost_usd: float = 0.10):
        self._maybe_reload()
        rule = self.rules.get(task_type) or self.rules["default"]
        candidate = rule["model"]
        model_meta = self._list_models().get(candidate)

        # Fallback if price exceeds cap
        est_price = self._estimate_cost(prompt, candidate)
        if est_price > max_cost_usd and "fallback" in rule:
            candidate = rule["fallback"]
            est_price = self._estimate_cost(prompt, candidate)

        logger.info("Selector pick: %s ($%.4f est.)", candidate, est_price)
        return {"model": candidate,
                "temperature": rule.get("temperature", 0.7),
                "max_tokens": rule.get("max_tokens", 1024)}

    def _estimate_cost(self, prompt: str, model: str):
        try:
            r = httpx.post(f"{self.gateway}/estimate",
                           json={"prompt": prompt, "model": model}, timeout=5)
            return r.json()["estimated_cost"]
        except Exception:
            return 0.0  # optimistic if estimator down