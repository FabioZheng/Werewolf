import pandas as pd


def load_game_timeline(conn, game_id: str):
    return pd.read_sql_query("SELECT * FROM events WHERE game_id=? ORDER BY timestamp", conn, params=[game_id])
