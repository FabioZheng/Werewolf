def check_win(alive_roles: list[str]) -> str | None:
    wolves = sum(1 for r in alive_roles if r == "werewolf")
    villagers = len(alive_roles) - wolves
    if wolves == 0:
        return "village"
    if wolves >= villagers:
        return "werewolf"
    return None
