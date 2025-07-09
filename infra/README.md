# LLM Gateway Infrastructure

This directory contains the shared LLM gateway infrastructure that provides:
- Multi-provider LLM proxy with cost tracking (LiteLLM)
- Usage analytics and logging (Helicone)
- Model selection with hot-reloadable rules
- Budget management and spend limits
- FastAPI helper endpoints for UI integration

## Quick Start

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

2. **Start the services**:
   ```bash
   cd infra
   docker compose up -d
   ```

3. **Verify the gateway**:
   ```bash
   curl http://localhost:4000/v1/models
   ```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Agents    │────▶│  LiteLLM     │────▶│  LLM APIs   │
│             │     │  Gateway     │     │  (OpenAI,   │
└─────────────┘     │  :4000       │     │  Anthropic) │
                    └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Helicone    │
                    │  Analytics   │
                    │  :3210       │
                    └──────────────┘
```

## Services

### LiteLLM Proxy (Port 4000)
- Unified API for multiple LLM providers
- Budget management and spend tracking
- Key-based access control
- Model routing and fallbacks

### Helicone Analytics (Port 3210)
- Cost tracking and usage analytics
- Request logging and debugging
- Performance monitoring

### FastAPI Helper (Optional)
- `/models` - List available models
- `/estimate` - Real-time cost estimation

## Configuration

### Budget Settings (`lite_llm/config.yaml`)
- Master keys with spend limits
- Per-user sub-budgets
- Monthly reset schedules
- Provider endpoint configuration

### Model Selection Rules (`lite_llm/rules.yaml`)
- Task-based model routing
- Temperature and token settings
- Cost-based fallback models
- Hot-reloadable without restart

## Usage in Agents

```python
from llm_selector.mixin import LLMChoiceMixin

class MyAgent(LLMChoiceMixin):
    def process(self, task: str):
        # Automatically selects best model based on task type
        config = self.llm_choice(
            prompt=task,
            task_type="research_paper_summary",
            max_cost_usd=0.05
        )
        # Use config["model"], config["temperature"], etc.
```

## Adding New Models

1. Add provider key to `.env`
2. Update `lite_llm/config.yaml` with endpoint
3. Add routing rules to `lite_llm/rules.yaml`
4. No restart needed - rules hot-reload every 10 seconds

## Monitoring

- Check logs: `docker compose logs -f lite_proxy`
- View analytics: http://localhost:3210
- Monitor costs: Check Helicone dashboard

## Troubleshooting

**Gateway not responding**:
```bash
docker compose ps
docker compose restart lite_proxy
```

**Model not found**:
- Verify model name in rules.yaml
- Check provider key is set in .env
- Ensure model is listed in config.yaml

**Budget exceeded**:
- Update spend_limit in config.yaml
- Reset manually: `docker compose exec lite_proxy litellm --reset-budget`