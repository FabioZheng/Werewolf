def valid_vote(voter: str, target: str, alive_players: list[str]) -> bool:
    return voter in alive_players and target in alive_players and voter != ""
