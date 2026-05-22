# Werewolf AI Benchmark Platform (MVP)

Research platform for running deterministic Werewolf/Mafia simulations where LLM agents play against each other through OpenRouter's OpenAI-compatible API.

## Setup
1. Create virtual env and install dependencies:
   ```bash
   pip install -r werewolf_ai/requirements.txt
   ```
2. Create `.env` in repo root (a mock template is included) and set your real key:
   ```bash
   OPENROUTER_API_KEY=your_real_key_here
   OPENROUTER_HTTP_REFERER=https://your-app.example
   OPENROUTER_X_TITLE=Werewolf AI Benchmark
   ```
3. The project loads `.env` automatically using `python-dotenv` when initializing the OpenRouter client.
4. Model list is editable in `werewolf_ai/config/models.yaml`.

## Run
- One simulation programmatically: import `run_once` from `werewolf_ai/run_simulation.py`.
- Streamlit UI:
  ```bash
  streamlit run werewolf_ai/app.py
  ```

## Logging and DB
SQLite schema: `werewolf_ai/storage/schema.sql` with tables for games, players, messages, votes, night actions, and events.

## Metrics
Basic metrics in `werewolf_ai/monitor/metrics.py`; extend with role/model/social metrics.

## Notes
- Engine enforces rules/state transitions.
- Agents only output JSON decisions.
- Invalid model outputs use deterministic fallback behavior.
