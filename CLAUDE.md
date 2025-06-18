# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Temporal AI Agent tutorial that demonstrates multi-turn conversations with an AI agent running inside a Temporal workflow. The agent collects information towards a goal, executes tools, and manages interactive conversations with users. The system is designed to be durable, reliable, and observable using Temporal's orchestration capabilities.

## Core Architecture

The system follows an agentic AI pattern with these key components:

- **Temporal Workflow** (`workflows/agent_goal_workflow.py`): Orchestrates the main agent loop, manages conversation state, handles tool execution, and provides durability
- **Activities** (`activities/tool_activities.py`): Temporal activities that execute tools and LLM calls with automatic retry logic
- **Tools** (`tools/`): Python functions that define agent capabilities (find events, search flights, create invoices)
- **Goal Registry** (`tools/goal_registry.py`): Defines agent goals and their associated tools and prompts
- **Prompts** (`prompts/`): System prompts and conversation management for LLM interactions
- **Models** (`models/`): Pydantic models for data structures and API requests
- **Frontend** (`frontend/`): React/Vite UI for chat interface
- **API** (`api/main.py`): FastAPI backend that bridges the web UI with Temporal workflows

## Development Commands

### Backend (Python)
```bash
# Setup virtual environment and dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Run Temporal worker
uv run python scripts/run_worker.py

# Run API server
uv run uvicorn api.main:app --reload

# Test individual tools
uv run python scripts/find_events_test.py
uv run python scripts/flight_api_test.py
uv run python scripts/create_invoice_test.py
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev    # Development server
npm run build  # Production build
```

### Temporal Server
```bash
# Install and run local Temporal server (Mac)
brew install temporal
temporal server start-dev
```

## Environment Configuration

Required environment variables in `.env`:
- `LLM_MODEL`: LiteLLM model identifier (e.g., "openai/gpt-4o", "anthropic/claude-3-sonnet")
- `LLM_KEY`: API key for the LLM provider
- `SHOW_CONFIRM`: Set to "True" to enable tool confirmation UI (recommended: "False")

Optional Temporal configuration:
- `TEMPORAL_ADDRESS`: Temporal server address (default: localhost:7233)
- `TEMPORAL_NAMESPACE`: Temporal namespace (default: default)
- `TEMPORAL_TASK_QUEUE`: Task queue name (default: agent-task-queue)

## Key Patterns

### Adding New Tools
1. Create tool function in `tools/` directory
2. Register tool in `tools/tool_registry.py`
3. Add tool to relevant goal in `tools/goal_registry.py`
4. Update prompts to include tool instructions

### Workflow State Management
- Conversation history is stored in workflow state
- Tool execution results are tracked durably
- User confirmations are handled via Temporal signals
- Chat termination is managed through workflow signals

### LLM Integration
- Uses LiteLLM for multi-provider support
- Prompts are generated dynamically based on conversation state
- Tool calls are formatted according to LLM provider requirements
- Conversation history is summarized to manage token limits

## File Structure Notes

- `scripts/`: Contains utility scripts for testing and running components
- `shared/config.py`: Central configuration management
- `workflows/workflow_helpers.py`: Common utilities for workflow operations
- Frontend components follow React functional component patterns with hooks
- API endpoints are defined in `api/main.py` with FastAPI patterns