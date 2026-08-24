---
title: "FNSE - Fractal Neural Simulation Engine"
description: "A production-grade, self-evolving multi-agent simulation framework with recursive skill compilation, graph-based memory, and enterprise safeguards."
layout: "landing"
---

![Fractal Neural Simulation Engine](/apple-touch-icon.png)
{{< hextra/hero-headline >}}
{{< /hextra/hero-headline >}}

{{< hextra/hero-subtitle >}}
**Fractal Neural Simulation Engine**

A production-grade, self-evolving multi-agent simulation framework with recursive skill compilation, graph-based memory, and enterprise safeguards.
{{< /hextra/hero-subtitle >}}

{{< badge content="Version 1.0.0" color="blue" >}}
{{< badge content="AGPL-3.0 License" color="orange" >}}
{{< badge content="Python 3.11+" color="blue" >}}
{{< badge content="FastAPI 0.109+" color="green" >}}
{{< badge content="Redis 7.0+" color="red" >}}
{{< badge content="Docker Ready" color="blue" >}}

---

## 🏗️ The Five Engine Pillars

{{< cards cols="2" >}}
{{< card
  link="/docs/architecture/macroswarm/"
  title="🏭 MacroSwarm"
  subtitle="Hierarchical multi-agent orchestration with role-based agents (Explorer, Optimizer, Critic, Synthesizer, Coordinator), dynamic scaling, tick-based execution, and cross-agent consensus."
  icon="tabler:cpu"
>}}
{{< card
  link="/docs/architecture/graphrag/"
  title="🧠 GraphRAG"
  subtitle="Graph-based retrieval-augmented generation with vector similarity search, knowledge graph traversal, entity linking, episodic memory, and semantic clustering."
  icon="tabler:database"
>}}
{{< card
  link="/docs/architecture/skillcompiler/"
  title="⚙️ SkillCompiler"
  subtitle="Recursive self-improving skill system with dynamic code generation, sandboxed execution, test-driven compilation, skill versioning, and dependency tracking."
  icon="tabler:code"
>}}
{{< card
  link="/docs/architecture/safeguards/"
  title="🛡️ SafeguardSystem"
  subtitle="Enterprise-grade safety with computational circuit breakers, divergence monitoring, automated state rollback, and multi-level alerting."
  icon="tabler:shield"
>}}
{{< card
  link="/docs/api-reference/"
  title="🚀 REST API"
  subtitle="Full-featured FastAPI server with epoch lifecycle management, real-time WebSocket streaming, GraphRAG query interface, and skill compilation endpoints."
  icon="tabler:rocket"
>}}
{{< /cards >}}

---

## 🚀 Quick Start

Get up and running in minutes with Docker:

```bash
# Clone and start
git clone https://github.com/nasirquant/fractal-neural-engine
cd fractal-neural-engine
docker-compose up -d

# Create your first epoch
curl -X POST http://localhost:8000/epochs \
  -H "Content-Type: application/json" \
  -d '{"num_agents": 10, "max_ticks": 100, "global_objective": "minimize_loss"}'
```

{{< callout type="info" >}}
**Requires:** Python 3.11+, Redis, OpenAI API key (or Anthropic). See [Environment Variables](/docs/quickstart/#environment-variables) for full configuration.
{{< /callout >}}

---

## 📚 Documentation

{{< tabs >}}
{{< tab name="🚀 Quickstart" >}}
### 5-Minute Quickstart

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OPENAI_API_KEY
   ```

3. **Start Redis**
   ```bash
   docker run -d -p 6379:6379 redis:7-alpine
   ```

4. **Run the API server**
   ```bash
   python main.py
   ```

5. **Create an epoch**
   ```bash
   curl -X POST http://localhost:8000/epochs \
     -H "Content-Type: application/json" \
     -d '{"num_agents": 10, "max_ticks": 100}'
   ```

**Next:** Explore [Architecture](/docs/architecture/) or [API Reference](/docs/api-reference/)
{{< /tab >}}

{{< tab name="🏗️ Architecture" >}}
### System Architecture

FNSE follows a layered architecture:

| Layer | Components |
|-------|------------|
| **Client** | CLI, REST API, Python SDK |
| **Gateway** | FastAPI, WebSocket, Auth |
| **Core** | MacroSwarm, Tick Scheduler, State Manager |
| **Runtime** | 5 Agent Roles (Explorer, Optimizer, Critic, Synthesizer, Coordinator) |
| **Intelligence** | GraphRAG, SkillCompiler, LiteLLM Router |
| **Safety** | Circuit Breakers, Rollback, Alerting |
| **Persistence** | Redis Cache, Checkpoints |

See [Architecture Overview](/docs/architecture/) for detailed diagrams.
{{< /tab >}}

{{< tab name="🔌 API Reference" >}}
### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/epochs` | POST | Create new simulation epoch |
| `/epochs/{id}` | GET | Get epoch status |
| `/epochs/{id}/ticks` | GET | Stream tick events (WebSocket) |
| `/epochs/{id}/agents` | GET | List all agents |
| `/epochs/{id}/graph/query` | POST | Query GraphRAG |
| `/skills/compile` | POST | Compile new skill |

Full docs: [API Reference](/docs/api-reference/)
{{< /tab >}}

{{< tab name="🐳 Deployment" >}}
### Docker Deployment

```yaml
# docker-compose.yml
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
  
  fnse-api:
    build: .
    ports: ["8000:8000"]
    environment:
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on: [redis]
```

Production: See [Monitoring](/docs/monitoring/) for Prometheus/Grafana setup.
{{< /tab >}}
{{< /tabs >}}

---

## 🔬 How It Works

### The Simulation Loop

```mermaid
graph LR
    A[Spawn Agents] --> B[Tick Scheduler]
    B --> C[Agent Think]
    C --> D[GraphRAG Query]
    D --> E[Skill Execute]
    E --> F[Message Pass]
    F --> G[Evaluate Loss]
    G --> H{Converged?}
    H -- No --> B
    H -- Yes --> I[Checkpoint & Exit]
```

Each epoch runs for `max_ticks` or until global loss converges below `convergence_threshold`. Agents operate in parallel, sharing knowledge through GraphRAG and evolving skills through the SkillCompiler.

---

## 🏢 Enterprise Ready

{{< cards cols="3" >}}
{{< card
  title="🔒 Circuit Breakers"
  subtitle="Automatic failure isolation with configurable thresholds, half-open testing, and state-change callbacks."
>}}
{{< card
  title="📊 Observability"
  subtitle="Prometheus metrics, Grafana dashboards, structured JSON logging, and distributed tracing ready."
>}}
{{< card
  title="🔄 Auto Rollback"
  subtitle="Periodic checkpointing with instant rollback on divergence detection or critical alerts."
>}}
{{< card
  title="🌐 Multi-Model"
  subtitle="LiteLLM router with fallback chains, cost tracking, and per-agent model selection."
>}}
{{< card
  title="📦 Skill Versioning"
  subtitle="Git-like skill registry with semantic versioning, dependency graph, and rollback."
>}}
{{< card
  title="⚡ Horizontal Scale"
  subtitle="Stateless agents, Redis-backed state, and Kubernetes-ready deployment manifests."
>}}
{{< /cards >}}

---

## 📖 Learn More

{{< cards cols="2" >}}
{{< card
  link="/docs/quickstart/"
  title="📖 Quickstart Guide"
  subtitle="Step-by-step installation, configuration, and your first simulation run."
>}}
{{< card
  link="/docs/architecture/"
  title="🏗️ Architecture Deep Dive"
  subtitle="Detailed system design, data flows, and component interactions."
>}}
{{< card
  link="/docs/api-reference/"
  title="🔌 API Reference"
  subtitle="Complete REST API documentation with request/response examples."
>}}
{{< card
  link="/docs/architecture/macroswarm/"
  title="🏭 MacroSwarm Guide"
  subtitle="Agent roles, tick lifecycle, message passing, and consensus protocols."
>}}
{{< card
  link="/docs/architecture/graphrag/"
  title="🧠 GraphRAG Guide"
  subtitle="Knowledge graph operations, semantic search, and multi-hop reasoning."
>}}
{{< card
  link="/docs/architecture/skillcompiler/"
  title="⚙️ SkillCompiler Guide"
  subtitle="Failure analysis, code generation, sandboxing, and skill lifecycle."
>}}
{{< card
  link="/docs/architecture/safeguards/"
  title="🛡️ Safeguards Guide"
  subtitle="Circuit breakers, divergence monitoring, alerts, and rollback procedures."
>}}
{{< card
  link="/docs/monitoring/"
  title="📊 Monitoring & Observability"
  subtitle="Prometheus metrics, Grafana dashboards, health checks, and alerting."
>}}
{{< /cards >}}

---

## 🤝 Community & Support

{{< callout type="default" emoji="💬" >}}
**Join the conversation:**
- **GitHub Discussions** — Ask questions, share ideas
- **Issues** — Bug reports and feature requests  
- **Discord** — Real-time community chat (invite in repo)
{{< /callout >}}

{{< cards cols="3" >}}
{{< card
  link="https://github.com/nasirquant/fractal-neural-engine"
  title="⭐ GitHub Repository"
  subtitle="Source code, releases, and issue tracker"
  icon="tabler:brand-github"
>}}
{{< card
  link="https://github.com/nasirquant/fractal-neural-engine/discussions"
  title="💬 Discussions"
  subtitle="Community Q&A, ideas, and showcases"
  icon="tabler:messages"
>}}
{{< card
  link="mailto:contact@fnse.dev"
  title="📧 Enterprise Contact"
  subtitle="Commercial licensing and support inquiries"
  icon="tabler:mail"
>}}
{{< /cards >}}

---

## 📄 License

FNSE is licensed under **AGPL-3.0** — free for commercial use, modification, and distribution. Network use requires source disclosure.

[View License](https://github.com/nasirquant/fractal-neural-engine/blob/main/LICENSE) • [Commercial Licensing](mailto:contact@fnse.dev)

---

<p align="center">
  <strong>Built with ❤️ for the future of autonomous AI systems</strong>
</p>