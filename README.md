# AI Data Agent

A Django application that lets an LLM answer business questions about a SaaS company's data — customers, subscriptions, product usage and product incidents — using [pydantic-ai](https://ai.pydantic.dev/).

**Status: work in progress / personal project.**

This project is being built incrementally as a learning exercise in designing LLM-powered data applications. The goal is to understand how an AI agent can interact with a relational database through well-defined Python tools, while keeping the underlying data access deterministic, testable and explainable.

## What it does

The project models a small SaaS business in a Django database using synthetic data. An AI agent can then use Python tools to query the database and answer natural-language business questions such as:

> "How many customers do we have per segment?"

> "Which customers are using the product most?"

> "Did the recent product incident affect usage?"

The project also includes a simple analyst dashboard that will eventually combine business metrics, visualisations and an AI chat interface.

The dataset is synthetic and intentionally small during development. It will grow as the project progresses.

## Tech stack

- **Django** — data models, ORM, admin, management commands and templating
- **pydantic-ai** — LLM agent and tool calling
- **Google Gemini** — LLM provider
- **SQLite** — local development database
- **PostgreSQL** — planned for deployment
- **Bootstrap 5** — dashboard UI
- **pytest / pytest-django** — automated testing
- **GitHub Actions** — CI

## Data model

The current dataset consists of four related tables:

| Model | Represents |
|---|---|
| `Customer` | Customer segment and signup date |
| `Subscription` | Subscription plan, price and status |
| `DailyUsage` | Daily product usage for each customer |
| `ProductIncident` | Product incidents, including date and severity |

The relationships are intentionally simple. The objective is not to build a complete SaaS data model, but to create a small dataset with meaningful relationships that an AI analyst can reason about.

Data is generated separately and loaded into Django through a custom management command:

```bash
python manage.py load_data --data-dir /path/to/csvs
```