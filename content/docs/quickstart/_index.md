---
title: "Quickstart"
description: "Get up and running with FNSE in 5 minutes"
weight: 1
---

## Prerequisites

- **Python 3.10+**
- **Redis 7.0+** (for state management and message passing)
- **OpenAI API key** or **Anthropic API key** (for LLM-powered agents)

## Installation

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/nasirquant/fractal-neural-engine
cd fractal-neural-engine

# Start all services
docker-compose up -d

# Verify the API is running
curl http://localhost:8000/health
```

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/nasirquant/fractal-neural-engine
cd fractal-neural-engine

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Run the API server
python main.py
```

## Your First Epoch

An **epoch** is a complete simulation run with a defined objective, agent count, and tick limit.

```bash
curl -X POST http://localhost:8000/epochs \
  -H "Content-Type: application/json" \
  -d '{
    "num_agents": 10,
    "max_ticks": 100,
    "global_objective": "minimize_loss",
    "loss_function": "mse",
    "convergence_threshold": 0.01,
    "checkpoint_interval": 10,
    "agent_roles": ["explorer", "optimizer", "critic", "synthesizer", "coordinator"]
  }'
```

Response:
```json
{
  "epoch_id": "ep_abc123",
  "status": "running",
  "config": {
    "num_agents": 10,
    "max_ticks": 100,
    "global_objective": "minimize_loss",
    "loss_function": "mse",
    "convergence_threshold": 0.01,
    "checkpoint_interval": 10,
    "agent_roles": ["explorer", "optimizer", "critic", "synthesizer", "coordinator"]
  }
}
```

## Monitor Progress

### REST Polling

```bash
# Check epoch status
curl http://localhost:8000/epochs/ep_abc123

# Get agent states
curl http://localhost:8000/epochs/ep_abc123/agents

# Get epoch result
curl http://localhost:8000/epochs/ep_abc123/result
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key for GPT models |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic API key for Claude models |
| `GOOGLE_API_KEY` | No | - | Google API key |
| `COHERE_API_KEY` | No | - | Cohere API key |
| `TOGETHER_API_KEY` | No | - | Together AI API key |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection string |
| `FNSE_LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `FNSE_LOG_FORMAT` | No | `json` | Log format (json or text) |
| `FNSE_DEFAULT_MODEL` | No | `gpt-4o-mini` | Default LLM model for agents |
| `FNSE_MODEL_TEMPERATURE` | No | `0.7` | Sampling temperature |
| `FNSE_MAX_TOKENS` | No | `2048` | Max tokens per completion |

*At least one LLM API key is required.

## Next Steps

- [Architecture Overview](/docs/architecture/) — Understand the system design
- [API Reference](/docs/api-reference/) — Complete API documentation
- [MacroSwarm Guide](/docs/architecture/macroswarm/) — Agent roles and orchestration
- [GraphRAG Guide](/docs/architecture/graphrag/) — Knowledge retrieval and memory