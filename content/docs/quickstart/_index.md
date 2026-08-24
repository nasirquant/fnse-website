---
title: "Quickstart"
description: "Get up and running with FNSE in 5 minutes"
weight: 1
---

## Prerequisites

- **Python 3.11+**
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
    "convergence_threshold": 0.01
  }'
```

Response:
```json
{
  "epoch_id": "ep_abc123",
  "status": "running",
  "num_agents": 10,
  "max_ticks": 100,
  "global_objective": "minimize_loss",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Monitor Progress

### WebSocket Streaming (Real-time)

```bash
# Install websocat for testing
# Then connect to the epoch stream
websocat ws://localhost:8000/epochs/ep_abc123/stream
```

### REST Polling

```bash
# Check epoch status
curl http://localhost:8000/epochs/ep_abc123

# Get agent states
curl http://localhost:8000/epochs/ep_abc123/agents

# Get loss history
curl http://localhost:8000/epochs/ep_abc123/loss-history
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key for GPT models |
| `ANTHROPIC_API_KEY` | Yes* | - | Anthropic API key for Claude models |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis connection string |
| `FNSE_LOG_LEVEL` | No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `FNSE_MAX_CONCURRENT_EPOCHS` | No | `5` | Maximum parallel epochs |
| `FNSE_DEFAULT_MODEL` | No | `gpt-4-turbo` | Default LLM model for agents |

*At least one LLM API key is required.

## Next Steps

- [Architecture Overview](/docs/architecture/) — Understand the system design
- [API Reference](/docs/api-reference/) — Complete API documentation
- [MacroSwarm Guide](/docs/architecture/macroswarm/) — Agent roles and orchestration
- [GraphRAG Guide](/docs/architecture/graphrag/) — Knowledge retrieval and memory