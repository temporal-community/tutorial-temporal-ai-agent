# Setup Guide
## Initial Configuration

This application uses `.env` files for configuration. Copy the [.env.example](.env.example) file to `.env` and update the values:

```bash
cp .env.example .env
```

Then add API keys, configuration, as desired.

If you want to show confirmations/enable the debugging UI that shows tool args, set
```bash
SHOW_CONFIRM=True
```
We recommend setting this to `False` in most cases, as it can clutter the conversation with confirmation messages.

### Quick Start with Makefile

We've provided a Makefile to simplify the setup and running of the application. Here are the main commands:

```bash
# Initial setup
make setup              # Creates virtual environment and installs dependencies
make setup-venv         # Creates virtual environment only
make install            # Installs all dependencies

# Running the application
make run-worker         # Starts the Temporal worker
make run-api            # Starts the API server
make run-frontend       # Starts the frontend development server

# Additional services
make run-train-api      # Starts the train API server
make run-legacy-worker  # Starts the legacy worker
make run-enterprise     # Builds and runs the enterprise .NET worker

# Development environment setup
make setup-temporal-mac # Installs and starts Temporal server on Mac

# View all available commands
make help
```

### Manual Setup (Alternative to Makefile)

If you prefer to run commands manually, see the sections below for detailed instructions on setting up the backend, frontend, and other components.

### LLM Configuration

Note: We recommend using OpenAI's GPT-4o or Claude 3.5 Sonnet for the best results. There can be significant differences in performance and capabilities between models, especially for complex tasks.

The agent uses LiteLLM to interact with various LLM providers. Configure the following environment variables in your `.env` file:

- `LLM_MODEL`: The model to use (e.g., "openai/gpt-4o", "anthropic/claude-3-sonnet", "google/gemini-pro", etc.)
- `LLM_KEY`: Your API key for the selected provider
- `LLM_BASE_URL`: (Optional) Custom base URL for the LLM provider. Useful for:
  - Using Ollama with a custom endpoint
  - Using a proxy or custom API gateway
  - Testing with different API versions

LiteLLM will automatically detect the provider based on the model name. For example:
- For OpenAI models: `openai/gpt-4o` or `openai/gpt-3.5-turbo`
- For Anthropic models: `anthropic/claude-3-sonnet`
- For Google models: `google/gemini-pro`
- For Ollama models: `ollama/mistral` (requires `LLM_BASE_URL` set to your Ollama server)

Example configurations:
```bash
# For OpenAI
LLM_MODEL=openai/gpt-4o
LLM_KEY=your-api-key-here

# For Anthropic
LLM_MODEL=anthropic/claude-3-sonnet
LLM_KEY=your-api-key-here

# For Ollama with custom URL
LLM_MODEL=ollama/mistral
LLM_BASE_URL=http://localhost:11434
```

For a complete list of supported models and providers, visit the [LiteLLM documentation](https://docs.litellm.ai/docs/providers).

## Configuring Temporal Connection

By default, this application will connect to a local Temporal server (`localhost:7233`) in the default namespace, using the `agent-task-queue` task queue. You can override these settings in your `.env` file.

### Use Temporal Cloud

See [.env.example](.env.example) for details on connecting to Temporal Cloud using mTLS or API key authentication.

[Sign up for Temporal Cloud](https://temporal.io/get-cloud)

### Use a local Temporal Dev Server

On a Mac
```bash
brew install temporal
temporal server start-dev
```
See the [Temporal documentation](https://learn.temporal.io/getting_started/python/dev_environment/) for other platforms.

You can also run a local Temporal server using Docker Compose. See the `Development with Docker` section below.

### Local Machine (no docker)

**Python Backend**

Requires [uv](https://docs.astral.sh/uv/) to manage dependencies.

1. `uv venv`

2. `source .venv/bin/activate`

3. `uv pip install -e .`

Run the following commands in separate terminal windows:

1. Start the Temporal worker:
```bash
uv run python scripts/run_worker.py
```

2. Start the API server:
```bash
uv run uvicorn api.main:app --reload
```
Access the API at `/docs` to see the available endpoints.

**React UI**
Start the frontend:
```bash
cd frontend
npm install
npx vite
```
Access the UI at `http://localhost:5173`