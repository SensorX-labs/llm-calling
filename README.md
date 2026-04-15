# LLM Calling Service

FastAPI service for calling Large Language Models with support for prompt building and content scoring.

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── api/
│   └── routes.py          # API endpoint definitions
├── schemas/
│   ├── request.py         # Request data models
│   └── response.py        # Response data models
├── services/
│   ├── llm_client.py      # LLM API client
│   ├── prompt_builder.py  # Prompt construction utility
│   └── scoring_service.py # Content scoring service
└── core/
    └── config.py          # Configuration management

requirements.txt  # Project dependencies
.env             # Environment variables (not in version control)
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Copy `.env` file and add your API keys and settings
   - Update `LLM_API_KEY` with your LLM provider credentials

3. **Run the service:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   - Interactive API docs: `http://localhost:8000/docs`
   - ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- **GET** `/api/v1/health` - Service health status

### LLM Completion
- **POST** `/api/v1/llm/complete` - Complete a prompt
  - **Body:**
    ```json
    {
      "prompt": "Your prompt here",
      "model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 2000
    }
    ```

### Content Scoring
- **POST** `/api/v1/score` - Score content
  - **Body:**
    ```json
    {
      "content": "Content to score",
      "scoring_type": "quality"
    }
    ```

### Completion with Context
- **POST** `/api/v1/llm/complete-with-context` - Complete with context
  - Same as `/api/v1/llm/complete`

## Configuration

Environment variables in `.env`:
- `LLM_API_KEY` - API key for LLM provider
- `LLM_MODEL` - Default model to use (default: gpt-4)
- `LLM_API_BASE` - LLM API base URL
- `LLM_TIMEOUT` - Request timeout in seconds
- `MAX_TOKENS` - Default max tokens for responses
- `TEMPERATURE` - Default temperature for generation
- `DEBUG` - Enable debug mode (default: False)

## Development

### Add new endpoints:
1. Create request/response schemas in `app/schemas/`
2. Add route handlers in `app/api/routes.py`
3. Implement business logic in `app/services/`

### Testing:
```bash
pytest
```

## Next Steps

- [ ] Implement actual LLM API integration in `llm_client.py`
- [ ] Add authentication and authorization
- [ ] Implement caching for responses
- [ ] Add logging and monitoring
- [ ] Write unit and integration tests
- [ ] Deploy to production environment
