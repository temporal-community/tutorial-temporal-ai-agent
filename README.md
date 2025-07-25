# Tutorial - Temporal AI Agent

_This repository is the companion repository for the tutorial [How To Build a Durable Agentic AI with Temporal and Python](https://learn.temporal.io/tutorials/ai/durable-ai-agent/)._

The code in this repository supports learning how to build a durable agentic AI with Temporal.
It is inspired by Steve Androulakis' [agengit AI implementation](https://github.com/temporal-community/temporal-ai-agent/) using Temporal.
This tutorial currently is the first step in building out an application similar to Steve's.

**Want to learn how to build this application from scratch?
[Check out the tutorial](https://learn.temporal.io/tutorials/ai/durable-ai-agent/)**

## Why Temporal?
There are a lot of AI and Agentic AI tools out there, and more on the way. 
But why Temporal? 
Temporal gives this system reliablity, state management, a code-first approach that we really like, built-in observability and easy error handling.

## What is "Agentic AI"?
These are the key elements of an agentic framework:
1. Goals that a system can accomplish, made up of tools that can execute individual steps
2. Agent loops - executing an LLM, executing tools, and eliciting input from an external source such as a human: repeat until goal(s) are done
3. Support for tool calls that require input and approval
4. Use of an LLM to check human input for relevance before calling the 'real' LLM
5. Use of an LLM to summarize and compact the conversation history
6. Prompt construction made of system prompts, conversation history, and tool metadata - sent to the LLM to create user questions and confirmations
7. Ideally high durability (done in this system with Temporal Workflow and Activities)

## Setup and Configuration

To run the code in this repository, use the [`uv`](https://docs.astral.sh/uv/) package and project manager.

Setup the development environment:

```bash
uv sync
```

Make a copy of `.env.example` and configure the environment variables.

```bash
cp .env.example .env
```

You can get started by only setting these two variables. 
If you want to use the [Sky Scrapper API](https://rapidapi.com/apiheya/api/sky-scrapper) or [Stripe APIs](https://stripe.com/lp/start-now), you will need to create accounts and provide the keys.
(more information in the [tutorial](#))

```bash
LLM_MODEL=openai/gpt-4o  # or any other model supported by LiteLLM
LLM_KEY=your-api-key-here
```

## Running the application

In one terminal, run the Temporal development server.
Alternatively you can set the configuration options in your `.env` file to connect to Temporal cloud.

```bash
temporal server start-dev
```

In another terminal, run the worker

```bash
uv run worker/worker.py
```

In another terminal, run the API

```bash
uv run uvicorn api.main:app --reload
```

Finally, in another terminal, install and run the frontend

```bash
npm install
npx vite
```

Test the agent in the web browser `localhost:5173`

## Testing individual parts

You can also test each individual tool using the testing scripts found in the `scripts` directory.
You would call them similarly to how you called the worker code above.

```bash
uv run scripts/find_events_test.py
uv run scripts/search_flights_test.py
uv run scripts/create_invoice_test.py
```
