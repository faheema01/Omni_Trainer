# Multimodal Content Moderation System

AI-powered content moderation for customer service training — built with Google Gemini, FastAPI, Gradio, and Pydantic AI.

---

## About

This system simulates a customer service training environment for a fictional company (ACME Enterprise). A trainee agent chats with an LLM-powered angry customer, and every message — text, image, video, or audio — is moderated in real time before being sent.

**What it detects:**
- PII (personally identifiable information)
- Unprofessional or unfriendly tone
- Disturbing images/videos
- Low-quality media

Flagged content is blocked with a detailed explanation of why.

---

## Architecture

| Component | Description | File |
|-----------|-------------|------|
| Text Agent | Moderates text for PII, tone, professionalism | `agents/text_agent.py` |
| Image Agent | Checks images for disturbing or inappropriate content | `agents/image_agent.py` |
| Video Agent | Analyzes video content and quality | `agents/video_agent.py` |
| Audio Agent | Evaluates audio content and quality | `agents/audio_agent.py` |
| Customer Agent | LLM simulating an angry customer | `agents/customer_agent.py` |
| Frontend | Gradio chat UI with file upload support | `gradio_app.py` |
| Backend | FastAPI REST API (`/moderate/text`, `/moderate/image`, etc.) | `fastapi_app.py` |
| Observability | Arize Phoenix tracing and monitoring | `tracing.py` |

Each moderation agent uses **Google Gemini** and returns structured results via **Pydantic** models with specific flags and rationale.

---

## Tech Stack

- **AI:** Google Gemini, Pydantic AI
- **Backend:** FastAPI
- **Frontend:** Gradio
- **Observability:** Arize Phoenix
- **Package Management:** uv

---

## Setup

```bash
# Install dependencies
uv sync --dev

# Install app in editable mode
uv pip install -e .

# Configure credentials
cp env.example .env
# Fill in GEMINI_API_KEY and USER_API_KEY in .env
```

---

## Usage

```bash
# Start all services (backend, frontend, Phoenix)
uv run multimodal-moderation
```

- **Chat UI:** http://localhost:7860
- **API Docs:** http://localhost:8000/docs
- **Tracing:** http://localhost:6006/projects

---

## Testing

```bash
# Run all tests
uv run pytest tests/ -vv

# Run evals
uv run evals/text/test_cases.py
uv run evals/image/test_cases.py
uv run evals/audio/test_cases.py
uv run evals/video/test_cases.py
```
