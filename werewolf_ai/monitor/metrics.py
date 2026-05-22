import pandas as pd


def game_metrics(conn):
    games = pd.read_sql_query("SELECT * FROM games", conn)
    messages = pd.read_sql_query("SELECT * FROM messages", conn)
    if games.empty:
        return {}
    return {
        "games": len(games),
        "total_messages": len(messages),
        "avg_message_length": float(messages.message.str.len().mean()) if not messages.empty else 0.0,
    }
