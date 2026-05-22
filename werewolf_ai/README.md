# Werewolf AI Benchmark Platform (MVP)

Research platform for running deterministic Werewolf/Mafia simulations where LLM agents play against each other through OpenRouter's OpenAI-compatible API.

## Setup
1. Create virtual env and install dependencies:
   ```bash
   pip install -r werewolf_ai/requirements.txt
   ```
2. Create `.env`:
   ```bash
   OPENROUTER_API_KEY=your_key_here
   ```
3. Model list is editable in `werewolf_ai/config/models.yaml`.

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
