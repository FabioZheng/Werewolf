from __future__ import annotations

import yaml
import streamlit as st

from monitor.metrics import game_metrics
from run_simulation import run_once, build_role_map, rotate_models
from storage.db import init_db
from ui.components import role_selector, validate_roles

st.set_page_config(page_title="Werewolf AI", layout="wide")
st.title("Werewolf AI Benchmark Platform")

roles_cfg = yaml.safe_load(open("werewolf_ai/config/roles.yaml"))
models_cfg = yaml.safe_load(open("werewolf_ai/config/models.yaml"))
role_defs = roles_cfg["roles"]
model_ids = [m["id"] for m in models_cfg["models"]]

page = st.sidebar.radio("Page", ["New Simulation", "Live / Latest Game", "Role Configuration", "Hidden Researcher View", "Replay", "Metrics", "Network Graph"])

db_path = st.sidebar.text_input("SQLite path", value="werewolf_ai.db")

if page == "New Simulation":
    n_games = st.number_input("Number of simulations", min_value=1, value=1)
    role_counts = role_selector(role_defs, {"villager": 3, "werewolf": 2, "seer": 1, "doctor": 1})
    allow_parity = st.checkbox("Allow werewolf parity at setup", value=False)
    errors = validate_roles(role_counts, allow_parity)
    assignment_mode = st.selectbox("Model assignment", ["same_for_all", "per_player", "random_pool"])
    temp = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    max_tokens = st.number_input("Max tokens", min_value=50, value=300)
    rounds = st.number_input("Discussion rounds/day", min_value=1, value=1)
    seed = st.number_input("Seed", min_value=0, value=42)

    if errors:
        st.error("; ".join(errors))
    if st.button("Start simulation") and not errors:
        role_map = build_role_map(role_counts, int(seed))
        players = list(role_map.keys())
        for i in range(int(n_games)):
            if assignment_mode == "same_for_all":
                m = st.selectbox("Model", model_ids, key=f"m_{i}")
                models = {p: m for p in players}
            elif assignment_mode == "random_pool":
                pool = st.multiselect("Model pool", model_ids, default=model_ids[:2], key=f"pool_{i}")
                models = rotate_models(players, pool, i)
            else:
                models = {p: st.selectbox(f"{p} model", model_ids, key=f"{p}_{i}") for p in players}
            winner = run_once(db_path, role_counts, models, temp, int(max_tokens), int(seed) + i, int(rounds))
            st.success(f"Game {i+1} winner: {winner}")

elif page == "Metrics":
    conn = init_db(db_path)
    st.json(game_metrics(conn))
else:
    st.info("MVP page placeholder. Use New Simulation and Metrics first.")
