# Contributing to the Temporal AI Agent Project

This document provides guidelines for contributing to `temporal-ai-agent`. All setup and installation instructions can be found in [setup.md](./setup.md).

## Getting Started

### Code Style & Formatting
We use `black` for code formatting and `isort` for import sorting to maintain a consistent codebase.
-   **Format code:**
    ```bash
    uv run poe format
    ```
    Or manually:
    ```bash
    uv run black .
    uv run isort .
    ```
    Please format your code before committing.

### Linting & Type Checking
We use `mypy` for static type checking and other linters configured via `poe the poet`.
-   **Run linters and type checks:**
    ```bash
    uv run poe lint
    ```
    Or manually for type checking:
    ```bash
    uv run mypy --check-untyped-defs --namespace-packages .
    ```
    Ensure all linting and type checks pass before submitting a pull request.

## Making Changes

### General Code Changes
-   Follow the existing code style and patterns.
-   Ensure any new code is well-documented with comments.

## Submitting Contributions

## Key Resources
-   **Project Overview**: [README.md](../README.md)
-   **Setup Instructions**: [setup.md](./setup.md)
-   **System Architecture**: [architecture.md](./architecture.md)
-   **Architecture Decisions**: [architecture-decisions.md](./architecture-decisions.md)