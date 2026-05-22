from dataclasses import dataclass


@dataclass(frozen=True)
class RoleDef:
    name: str
    team: str
    has_night_action: bool


ROLES = {
    "villager": RoleDef("villager", "village", False),
    "werewolf": RoleDef("werewolf", "werewolf", True),
    "seer": RoleDef("seer", "village", True),
    "doctor": RoleDef("doctor", "village", True),
}
