---
title: "API Reference"
description: "Complete REST API documentation for FNSE"
weight: 3
---

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production deployments, implement API key authentication via header:

```
Authorization: Bearer <your-api-key>
```

## Rate Limiting

Rate limiting is not currently implemented. For production, consider adding:
- Request rate limits per IP

## Epochs

### Create Epoch

Start a new simulation epoch.

**POST** `/epochs`

**Request Body:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `num_agents` | integer | No | 10 | Number of agents (1-100) |
| `max_ticks` | integer | No | 100 | Maximum simulation ticks (1-1000) |
| `global_objective` | string | No | "minimize_loss" | Global optimization objective |
| `loss_function` | string | No | "mse" | Loss function: "mse", "mae", "cosine", or "custom" |
| `convergence_threshold` | float | No | 0.01 | Convergence threshold (0.0-1.0) |
| `checkpoint_interval` | integer | No | 10 | Checkpoint every N ticks (1-100) |
| `agent_roles` | array[string] | No | - | Specific roles to assign (e.g., ["explorer", "optimizer"]) |
| `seed_entities` | array[object] | No | - | Initial GraphRAG entities to seed |
| `model` | string | No | - | Override default LLM model |
| `model_temperature` | float | No | - | Override default temperature |

**Example Request:**
```json
{
  "num_agents": 10,
  "max_ticks": 100,
  "global_objective": "minimize_loss",
  "loss_function": "mse",
  "convergence_threshold": 0.01,
  "checkpoint_interval": 10,
  "agent_roles": ["explorer", "optimizer", "critic", "synthesizer", "coordinator"]
}
```

**Response** (201 Created):

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

### Get Epoch Status

**GET** `/epochs/{epoch_id}`

**Response** (200 OK):

```json
{
  "epoch_id": "ep_abc123",
  "running": true,
  "tick_number": 42,
  "global_loss": 0.847,
  "convergence_rate": -0.0023,
  "converged": false,
  "agent_states": {
    "exp_001": {
      "agent_id": "exp_001",
      "role": "explorer",
      "status": "active",
      "tick_count": 42,
      "success_count": 15,
      "failure_count": 2,
      "total_tokens_used": 12500,
      "avg_latency_ms": 245.3,
      "divergence_score": 0.15,
      "current_objective": "minimize_loss",
      "active_skill_id": "skill_gradient_descent_v3"
    }
  },
  "circuit_breakers": {
    "agent_execution": "closed",
    "loss_computation": "closed"
  },
  "alerts_summary": {
    "info": 2,
    "warning": 0,
    "critical": 0,
    "emergency": 0
  },
  "checkpoints": 4,
  "uptime_seconds": 312.5
}
```



### Delete Epoch

**DELETE** `/epochs/{epoch_id}`

**Response** (200 OK):
```json
{
  "status": "deleted",
  "epoch_id": "ep_abc123"
}
```

### List All Epochs

**GET** `/epochs`

**Response** (200 OK):
```json
["ep_abc123", "ep_def456", "ep_ghi789"]
```

### Health Check

**GET** `/health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "fnse"
}
```

## Agents

### List Agents

**GET** `/epochs/{epoch_id}/agents`

**Response** (200 OK):

```json
[
  {
    "agent_id": "exp_001",
    "role": "explorer",
    "status": "active",
    "tick_count": 42,
    "success_count": 15,
    "failure_count": 2,
    "total_tokens_used": 12500,
    "divergence_score": 0.15,
    "current_objective": "minimize_loss",
    "active_skill_id": "skill_gradient_descent_v3"
  }
]
```

### Get Agent Details

**GET** `/epochs/{epoch_id}/agents/{agent_id}`

**Response** (200 OK):

```json
{
  "agent_id": "exp_001",
  "role": "explorer",
  "status": "active",
  "working_memory": {
    "dimensions": 384,
    "values": [0.1, 0.2, ...],
    "metadata": {},
    "timestamp": "2024-01-15T10:35:22Z"
  },
  "long_term_memory_ref": "fnse:epoch:ep_abc123:agent:exp_001:memory",
  "knowledge_graph_ref": "exp_001",
  "current_objective": "minimize_loss",
  "active_skill_id": "skill_gradient_descent_v3",
  "skill_stack": ["skill_gradient_descent_v3"],
  "tick_count": 42,
  "success_count": 15,
  "failure_count": 2,
  "total_tokens_used": 12500,
  "avg_latency_ms": 245.3,
  "divergence_score": 0.15,
  "last_checkpoint_tick": 40,
  "tags": {},
  "created_at": "2024-01-15T10:30:01Z",
  "updated_at": "2024-01-15T10:35:22Z"
}
```


## Safeguards

### Get Safeguard Status

**GET** `/epochs/{epoch_id}/safeguards/status`

**Response** (200 OK):

```json
{
  "epoch_id": "ep_abc123",
  "tick_count": 42,
  "circuit_breakers": {
    "agent_execution": "closed",
    "loss_computation": "closed",
    "skill_compilation": "closed",
    "graphrag_query": "closed",
    "redis_operations": "closed",
    "llm_api": "closed"
  },
  "divergence": {
    "swarm_score": 0.23,
    "max_threshold": 10.0,
    "agent_scores": {
      "exp_001": 0.15,
      "opt_002": 0.23
    }
  },
  "checkpoints": {
    "total": 4,
    "epoch_checkpoints": 4
  },
  "alerts": {
    "total": 2,
    "unacknowledged": 1,
    "by_severity": {
      "info": 2,
      "warning": 0,
      "critical": 0,
      "emergency": 0
    }
  },
  "circuit_break_count": 0,
  "rollback_count": 0
}
```



### Get Alerts

**GET** `/epochs/{epoch_id}/alerts`

**Query Parameters:**
- `severity` - Filter by severity (info, warning, critical, emergency)
- `limit` - Maximum number of alerts to return (default: 100)

**Response** (200 OK):

```json
[
  {
    "alert_id": "alt_xyz789",
    "timestamp": "2024-01-15T10:40:00Z",
    "severity": "warning",
    "source": "safeguard_system",
    "message": "Divergence score 0.52 exceeds warning threshold",
    "details": {"divergence_score": 0.52},
    "acknowledged": false,
    "resolved": false
  }
]
```

### Acknowledge Alert

**POST** `/epochs/{epoch_id}/alerts/{alert_id}/acknowledge`

**Response** (200 OK):
```json
{
  "status": "acknowledged",
  "alert_id": "alt_xyz789"
}
```

## Skills

### Compile Skill

Compile a new skill from source code.

**POST** `/epochs/{epoch_id}/skills`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Skill name |
| `description` | string | Yes | Skill description |
| `source_code` | string | Yes | Python source code |
| `author_agent_id` | string | Yes | Agent ID that authored this skill |
| `test_cases` | array[object] | No | Optional test cases |

**Example Request:**
```json
{
  "name": "gradient_descent_v3",
  "description": "Vectorized gradient descent with adaptive LR",
  "source_code": "def execute(input_data, context):\n    # ... implementation\n    return {'result': output}",
  "author_agent_id": "opt_042",
  "test_cases": [
    {"input": {"lr": 0.01}, "expected": {"loss_delta": -0.01}}
  ]
}
```

**Response** (200 OK):
```json
{
  "skill_id": "skill_gradient_descent_v3",
  "test_results": {"passed": 1, "failed": 0, "coverage": 1.0}
}
```

### List Skills

**GET** `/epochs/{epoch_id}/skills`

**Response** (200 OK):
```json
[
  {
    "skill_id": "skill_gradient_descent_v3",
    "name": "gradient_descent",
    "description": "Vectorized gradient descent with adaptive LR",
    "version": 1,
    "author_agent_id": "opt_042",
    "invocation_count": 42,
    "success_rate": 0.95,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Skill Details

**GET** `/epochs/{epoch_id}/skills/{skill_id}`

**Response** (200 OK):
```json
{
  "skill_id": "skill_gradient_descent_v3",
  "name": "gradient_descent",
  "description": "Vectorized gradient descent with adaptive LR",
  "version": 1,
  "source_code": "def execute(input_data, context):\n    ...",
  "entry_point": "execute",
  "signature": "execute(input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]",
  "author_agent_id": "opt_042",
  "parent_skill_ids": [],
  "compilation_tick": 10,
  "compilation_epoch": "ep_abc123",
  "test_cases": [{"input": {"lr": 0.01}, "expected": {"loss_delta": -0.01}}],
  "passed_tests": 1,
  "failed_tests": 0,
  "invocation_count": 42,
  "success_rate": 0.95,
  "avg_latency_ms": 12.5,
  "is_sandboxed": true,
  "allowed_imports": ["math", "random"],
  "max_execution_time_ms": 5000,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```



### Seed Graph

**POST** `/epochs/{epoch_id}/graph/seed`

**Request Body:**
```json
{
  "entities": [
    {
      "type": "skill",
      "label": "gradient_descent",
      "properties": {"version": "1", "tags": ["optimization"]}
    }
  ]
}
```

**Response** (200 OK):
```json
{
  "status": "seeded",
  "nodes_added": 1
}
```

### Query Graph

**POST** `/epochs/{epoch_id}/graph/query`

**Request Body:**
```json
{
  "query_vector": [0.1, 0.2, 0.3, ...],
  "node_types": ["skill", "concept"],
  "top_k": 10,
  "center_node": "gradient_descent",
  "radius": 2
}
```

**Response** (200 OK):
```json
{
  "results": [
    {
      "node": {
        "node_id": "ent_abc123",
        "node_type": "skill",
        "label": "gradient_descent",
        "properties": {"version": "1", "tags": ["optimization"]}
      },
      "score": 0.92
    }
  ]
}
```

### Get Graph Stats

**GET** `/epochs/{epoch_id}/graph/stats`

**Response** (200 OK):
```json
{
  "nodes": 150,
  "edges": 342,
  "node_types": {"skill": 25, "concept": 45, "function": 30},
  "last_updated": "2024-01-15T10:45:00Z"
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
  "service": "fnse"
}
```

## Next Steps

- [Quickstart](/docs/quickstart/) — Get started with FNSE
- [Architecture Overview](/docs/architecture/) — System design
- [MacroSwarm Guide](/docs/architecture/macroswarm/) — Agent orchestration
- [GraphRAG Guide](/docs/architecture/graphrag/) — Knowledge retrieval
- [SkillCompiler Guide](/docs/architecture/skillcompiler/) — Skill compilation
- [Safeguards Guide](/docs/architecture/safeguards/) — Safety systems