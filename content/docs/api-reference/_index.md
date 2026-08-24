---
title: "API Reference"
description: "Complete REST API and WebSocket documentation for FNSE"
weight: 3
---

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API uses API key authentication via header:

```
Authorization: Bearer <your-api-key>
```

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per minute per API key
- WebSocket connections: 50 concurrent per IP

## Epochs

### Create Epoch

Start a new simulation epoch.

**POST** `/epochs`

```json
{
  "num_agents": 10,
  "max_ticks": 100,
  "global_objective": "minimize_loss",
  "convergence_threshold": 0.01,
  "roles": ["explorer", "optimizer", "critic", "synthesizer", "coordinator"],
  "role_distribution": {
    "explorer": 0.30,
    "optimizer": 0.25,
    "critic": 0.20,
    "synthesizer": 0.15,
    "coordinator": 0.10
  },
  "config_overrides": {}
}
```

**Response** (201 Created):

```json
{
  "epoch_id": "ep_abc123",
  "status": "running",
  "num_agents": 10,
  "max_ticks": 100,
  "global_objective": "minimize_loss",
  "convergence_threshold": 0.01,
  "created_at": "2024-01-15T10:30:00Z",
  "started_at": "2024-01-15T10:30:01Z"
}
```

### Get Epoch Status

**GET** `/epochs/{epoch_id}`

**Response** (200 OK):

```json
{
  "epoch_id": "ep_abc123",
  "status": "running",
  "current_tick": 42,
  "max_ticks": 100,
  "num_agents": 10,
  "global_objective": "minimize_loss",
  "convergence_threshold": 0.01,
  "current_loss": 0.847,
  "best_loss": 0.823,
  "loss_history": [1.234, 1.156, 0.987, 0.847],
  "agent_counts": {
    "explorer": 3,
    "optimizer": 2,
    "critic": 2,
    "synthesizer": 2,
    "coordinator": 1
  },
  "created_at": "2024-01-15T10:30:00Z",
  "started_at": "2024-01-15T10:30:01Z",
  "updated_at": "2024-01-15T10:35:22Z"
}
```

### List Epochs

**GET** `/epochs`

**Query Parameters:**
- `status` - Filter by status (running, completed, failed, paused)
- `limit` - Max results (default 50, max 200)
- `offset` - Pagination offset

**Response** (200 OK):

```json
{
  "epochs": [
    {
      "epoch_id": "ep_abc123",
      "status": "completed",
      "num_agents": 10,
      "max_ticks": 100,
      "final_loss": 0.823,
      "created_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T11:15:00Z"
    }
  ],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

### Pause Epoch

**POST** `/epochs/{epoch_id}/pause`

**Response** (200 OK):

```json
{
  "epoch_id": "ep_abc123",
  "status": "paused",
  "paused_at": "2024-01-15T10:45:00Z",
  "current_tick": 42
}
```

### Resume Epoch

**POST** `/epochs/{epoch_id}/resume`

**Response** (200 OK):

```json
{
  "epoch_id": "ep_abc123",
  "status": "running",
  "resumed_at": "2024-01-15T10:46:00Z",
  "current_tick": 42
}
```

### Delete Epoch

**DELETE** `/epochs/{epoch_id}`

## Agents

### List Agents

**GET** `/epochs/{epoch_id}/agents`

**Query Parameters:**
- `role` - Filter by role
- `status` - Filter by status (active, idle, quarantined)

**Response** (200 OK):

```json
{
  "agents": [
    {
      "agent_id": "exp_001",
      "role": "explorer",
      "status": "active",
      "current_tick": 42,
      "last_loss": 0.847,
      "skills_used": ["skill_gradient_descent_v3", "skill_random_search_v1"],
      "messages_sent": 15,
      "messages_received": 23,
      "created_at": "2024-01-15T10:30:01Z"
    }
  ],
  "total": 10
}
```

### Get Agent Details

**GET** `/epochs/{epoch_id}/agents/{agent_id}`

**Response** (200 OK):

```json
{
  "agent_id": "exp_001",
  "role": "explorer",
  "status": "active",
  "state": {
    "current_params": {"lr": 0.01, "momentum": 0.9},
    "best_params": {"lr": 0.005, "momentum": 0.95},
    "best_loss": 0.823,
    "iteration": 42
  },
  "skill_history": [
    {"skill_id": "skill_gradient_descent_v3", "tick": 40, "success": true, "loss_delta": -0.012},
    {"skill_id": "skill_random_search_v1", "tick": 41, "success": true, "loss_delta": -0.008}
  ],
  "message_history": [
    {"message_id": "msg_123", "type": "proposal", "tick": 41, "recipient": "broadcast"}
  ],
  "graphrag_queries": 15,
  "skill_executions": 8,
  "errors": 0
}
```

### Scale Agents

**POST** `/epochs/{epoch_id}/agents/scale`

```json
{
  "role": "explorer",
  "delta": 5,
  "reason": "Exploration plateau detected"
}
```

**Response** (200 OK):

```json
{
  "epoch_id": "ep_abc123",
  "role": "explorer",
  "previous_count": 3,
  "new_count": 8,
  "scaled_at": "2024-01-15T10:40:00Z"
}
```

## Messages

### Get Message History

**GET** `/epochs/{epoch_id}/messages`

**Query Parameters:**
- `tick` - Filter by tick number
- `type` - Filter by message type
- `sender_id` - Filter by sender
- `limit` - Max results (default 100)
- `offset` - Pagination offset

**Response** (200 OK):

```json
{
  "messages": [
    {
      "message_id": "msg_abc123",
      "sender_id": "exp_001",
      "recipient": "broadcast",
      "type": "proposal",
      "payload": {
        "solution": "adaptive_learning_rate",
        "params": {"lr": 0.01, "decay": 0.99}
      },
      "tick": 42,
      "timestamp": "2024-01-15T10:35:22Z"
    }
  ],
  "total": 1247
}
```

### WebSocket Stream

**WS** `/epochs/{epoch_id}/stream`

Real-time stream of epoch events. Connect with WebSocket client.

**Event Types:**

```json
// Agent state update
{
  "type": "agent_update",
  "tick": 42,
  "agent_id": "exp_001",
  "data": {"loss": 0.847, "status": "active"}
}

// New message
{
  "type": "message",
  "message": {...}
}

// Safeguard alert
{
  "type": "safeguard_alert",
  "severity": "warning",
  "message": "Loss divergence detected"
}

// Epoch completed
{
  "type": "epoch_complete",
  "epoch_id": "ep_abc123",
  "final_loss": 0.823,
  "ticks": 87
}
```
**Response** (204 No Content)
## Safeguards

### Get Safeguard Status

**GET** `/epochs/{epoch_id}/safeguards/status`

**Response** (200 OK):

```json
{
  "epoch_id": "ep_abc123",
  "status": "healthy",
  "circuit_breakers": {
    "loss_divergence": {"triggered": false, "value": 0.847, "threshold": 2.0},
    "agent_stall": {"triggered": false, "idle_agents": 0},
    "memory_leak": {"triggered": false, "max_memory_mb": 452},
    "api_error_rate": {"triggered": false, "rate": 0.02},
    "skill_failure_rate": {"triggered": false, "rate": 0.05}
  },
  "divergence": {
    "score": 0.23,
    "level": "info",
    "metrics": {
      "loss": 0.847,
      "loss_velocity": -0.002,
      "agent_diversity": 0.73,
      "consensus_strength": 0.81,
      "skill_success_rate": 0.94
    }
  },
  "rollback": {
    "available": true,
    "latest_checkpoint_tick": 40,
    "max_rollback_ticks": 100
  }
}
```

### Get Divergence Metrics

**GET** `/epochs/{epoch_id}/safeguards/metrics`

**Query Parameters:**
- `start_tick` - Start tick (default: 0)
- `end_tick` - End tick (default: current)
- `interval` - Aggregation interval (default: 1)

**Response** (200 OK):

```json
{
  "metrics": [
    {
      "tick": 40,
      "loss": 0.856,
      "loss_delta": -0.011,
      "loss_velocity": -0.003,
      "agent_diversity": 0.72,
      "consensus_strength": 0.80,
      "skill_success_rate": 0.93,
      "message_throughput": 125,
      "memory_usage_mb": 448,
      "divergence_score": 0.25
    }
  ]
}
```

### Get Alert History

**GET** `/epochs/{epoch_id}/safeguards/alerts`

**Response** (200 OK):

```json
{
  "alerts": [
    {
      "alert_id": "alt_xyz789",
      "epoch_id": "ep_abc123",
      "severity": "warning",
      "type": "divergence",
      "message": "Divergence score 0.52 exceeds warning threshold",
      "metrics": {"divergence_score": 0.52},
      "timestamp": "2024-01-15T10:40:00Z",
      "acknowledged": false
    }
  ]
}
```

### Trigger Manual Rollback

**POST** `/epochs/{epoch_id}/safeguards/rollback`

```json
{
  "target_tick": 30,
  "reason": "Manual intervention required"
}
```

**Response** (200 OK):

```json
{
  "rollback_id": "rbk_abc123",
  "epoch_id": "ep_abc123",
  "target_tick": 30,
  "status": "completed",
  "started_at": "2024-01-15T10:45:00Z",
  "completed_at": "2024-01-15T10:45:05Z"
}
## Skill Compiler

### Compile Skill

**POST** `/skills/compile`

```json
{
  "failure_context": {
    "failure_id": "fail_xyz789",
    "agent_id": "opt_042",
    "error_type": "performance",
    "root_causes": [
      {"hypothesis": "Inefficient loop", "confidence": 0.85}
    ]
  },
  "target_skill": "gradient_descent",
  "requirements": ["vectorized", "adaptive_lr"]
}
```

**Response** (200 OK):

```json
{
  "compilation_id": "cmp_abc123",
  "status": "validated",
  "skill_id": "skill_gradient_descent_v3",
  "code": "class GradientDescentV3(Skill): ...",
  "manifest": {...},
  "test_results": {"passed": 15, "failed": 0, "coverage": 0.94},
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Register Skill

**POST** `/skills/register`

```json
{
  "compilation_id": "cmp_abc123",
  "skill_code": "class GradientDescentV3(Skill): ...",
  "manifest": {...},
  "test_results": {...}
}
```

**Response** (201 Created):

```json
{
  "skill_id": "skill_gradient_descent_v3",
  "version": "3.0.0",
  "status": "registered",
  "registered_at": "2024-01-15T10:30:00Z"
}
```

### List Skills

**GET** `/skills`

**Query Parameters:**
- `role` - Filter by compatible role
- `tag` - Filter by tag
- `status` - Filter by status (draft, testing, validated, registered, deprecated)

**Response** (200 OK):

```json
{
  "skills": [
    {
      "skill_id": "skill_gradient_descent_v3",
      "name": "gradient_descent",
      "version": "3.0.0",
      "description": "Vectorized gradient descent with adaptive LR",
      "status": "registered",
      "compatible_roles": ["optimizer", "synthesizer"],
      "tags": ["optimization", "core", "vectorized"],
      "test_coverage": 0.94,
      "performance": {"avg_latency_ms": 12, "memory_mb": 45},
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 42
}
```
### Get Skill Details

**GET** `/skills/{skill_id}`

**Response** (200 OK):

```json
{
  "skill_id": "skill_gradient_descent_v3",
  "name": "gradient_descent",
  "version": "3.0.0",
  "description": "Vectorized gradient descent with adaptive LR and momentum",
  "author": "skill_compiler",
  "status": "registered",
  "code": "class GradientDescentV3(Skill): ...",
  "manifest": {
    "dependencies": ["numpy>=1.24", "torch>=2.0"],
    "compatible_with": ["optimizer_role", "synthesizer_role"],
    "tags": ["optimization", "core", "vectorized"]
  },
  "test_results": {"passed": 15, "failed": 0, "coverage": 0.94},
  "performance": {"avg_latency_ms": 12, "memory_mb": 45},
  "versions": [
    {"version": "3.0.0", "status": "registered", "created_at": "2024-01-15T10:30:00Z"},
    {"version": "2.5.0", "status": "deprecated", "created_at": "2024-01-10T10:30:00Z"}
  ],
  "dependencies": ["skill_base_optimizer_v1", "skill_vectorization_v1"],
  "dependents": ["skill_adaptive_lr_v1", "skill_optimizer_ensemble_v1"]
}
```

### Run Skill Tests

**POST** `/skills/{skill_id}/test`

```json
{
  "test_suite": "full"
}
```

**Response** (200 OK):

```json
{
  "skill_id": "skill_gradient_descent_v3",
  "results": {
    "passed": 15,
    "failed": 0,
    "skipped": 0,
    "coverage": 0.94,
    "duration_ms": 1250
  },
  "tests": [
    {"name": "test_vectorized_update", "passed": true, "duration_ms": 45},
    {"name": "test_adaptive_lr", "passed": true, "duration_ms": 67}
  ]
}
```

### Rollback Skill

**POST** `/skills/{skill_id}/rollback`

```json
{
  "target_version": "2.5.0"
}
```

### Deprecate Skill

**DELETE** `/skills/{skill_id}`

```json
{
  "reason": "Superseded by v3"
}
```

## GraphRAG

### Hybrid Search

**POST** `/graphrag/search`

```json
{
  "query": "optimization strategies for neural networks",
  "vector_weight": 0.6,
  "graph_weight": 0.4,
  "max_hops": 2,
  "top_k": 15,
  "filters": {
    "epoch_id": "ep_123",
    "type": "skill"
  }
}
```

**Response** (200 OK):

```json
{
  "results": [
    {
      "entity_id": "ent_abc123",
      "type": "skill",
      "name": "gradient_descent_v3",
      "description": "Vectorized gradient descent with adaptive LR",
      "score": 0.92,
      "source": "hybrid",
      "metadata": {"epoch_id": "ep_123", "version": "3.0.0"}
    }
  ],
  "query_time_ms": 45
}
```

### Vector Search

**POST** `/graphrag/vector-search`

```json
{
  "query": "catastrophic forgetting prevention",
  "top_k": 10,
  "filters": {"type": "concept"}
}
```

### Graph Traversal

**POST** `/graphrag/graph-traverse`

```json
{
  "start_entity": "gradient_descent",
  "max_hops": 3,
  "relation_types": ["derives", "optimizes", "combines_with"]
}
```

### Multi-Hop Reasoning

**POST** `/graphrag/multi-hop`

```json
{
  "question": "What skills combine well with gradient_descent for sparse rewards?",
  "max_hops": 3,
  "synthesis_model": "gpt-4-turbo"
}
```

### Ingest Documents

**POST** `/graphrag/ingest`

```json
{
  "documents": [
    {
      "content": "New research on adaptive learning rates...",
      "source": "arxiv:2024.00123",
      "type": "research_paper",
      "metadata": {"tags": ["optimization", "adaptive_lr"]}
    }
  ]
}
```

### Get Entity

**GET** `/graphrag/entities/{entity_id}`

### Get Entity Neighbors

**GET** `/graphrag/entities/{entity_id}/neighbors`

**Query Parameters:**
- `relation_types` - Comma-separated relation types
- `max_hops` - Maximum hops (default: 1)

## Configuration

### Get Safeguard Config

**GET** `/safeguards/config`

### Update Safeguard Config

**PUT** `/safeguards/config`

```json
{
  "circuit_breaker_threshold": 5,
  "divergence_threshold": 2.0,
  "rollback_on_critical": true,
  "divergence": {
    "enabled": true,
    "check_interval_ticks": 1,
    "baseline_window_ticks": 50,
    "weights": {
      "loss_velocity": 0.35,
      "diversity": 0.20,
      "consensus": 0.20,
      "skill_success": 0.15,
      "throughput": 0.10
    },
    "thresholds": {
      "info": 0.3,
      "warning": 0.5,
      "critical": 0.7,
      "emergency": 0.9
    }
  }
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "EPOCH_NOT_FOUND",
    "message": "Epoch ep_xyz789 not found",
    "details": {"epoch_id": "ep_xyz789"}
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `EPOCH_NOT_FOUND` | 404 | Epoch does not exist |
| `AGENT_NOT_FOUND` | 404 | Agent does not exist |
| `SKILL_NOT_FOUND` | 404 | Skill does not exist |
| `INVALID_STATE` | 400 | Operation invalid for current state |
| `RATE_LIMITED` | 429 | Too many requests |
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `INTERNAL_ERROR` | 500 | Internal server error |

## Health Check

**GET** `/health`

**Response** (200 OK):

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "uptime_seconds": 3600,
  "components": {
    "redis": "connected",
    "vector_db": "connected",
    "graph_db": "connected",
    "llm_provider": "connected"
  }
}
```

## Next Steps

- [Quickstart](/docs/quickstart/) — Get started with FNSE
- [Architecture Overview](/docs/architecture/) — System design
- [MacroSwarm Guide](/docs/architecture/macroswarm/) — Agent orchestration
- [GraphRAG Guide](/docs/architecture/graphrag/) — Knowledge retrieval
- [SkillCompiler Guide](/docs/architecture/skillcompiler/) — Skill compilation
- [Safeguards Guide](/docs/architecture/safeguards/) — Safety systems