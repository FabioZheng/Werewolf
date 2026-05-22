CREATE TABLE IF NOT EXISTS games (
  game_id TEXT PRIMARY KEY,
  started_at TEXT,
  finished_at TEXT,
  winning_team TEXT,
  config_json TEXT,
  seed INTEGER
);
CREATE TABLE IF NOT EXISTS players (
  game_id TEXT,
  player_id TEXT,
  role TEXT,
  model_id TEXT,
  alive INTEGER,
  death_phase TEXT,
  death_reason TEXT
);
CREATE TABLE IF NOT EXISTS messages (
  game_id TEXT, phase TEXT, day_number INTEGER, round_number INTEGER,
  player_id TEXT, model_id TEXT, message TEXT, reasoning_summary TEXT,
  raw_response_json TEXT, parse_success INTEGER, latency_ms INTEGER
);
CREATE TABLE IF NOT EXISTS votes (
  game_id TEXT, day_number INTEGER, voter_id TEXT, target_id TEXT, reasoning_summary TEXT
);
CREATE TABLE IF NOT EXISTS night_actions (
  game_id TEXT, night_number INTEGER, actor_id TEXT, role TEXT, action_type TEXT,
  target_id TEXT, resolved_result TEXT
);
CREATE TABLE IF NOT EXISTS events (
  game_id TEXT, event_type TEXT, phase TEXT, payload_json TEXT, timestamp TEXT
);
