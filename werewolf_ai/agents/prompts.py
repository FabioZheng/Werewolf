PROMPT_VERSION = "v1"

ROLE_PROMPTS = {
    "villager": "You are a villager. Identify werewolves using public behavior and voting patterns.",
    "werewolf": "You are a werewolf. Hide your identity, mislead villagers, coordinate with teammates only privately.",
    "seer": "You are the seer. Inspect one player each night and use results strategically.",
    "doctor": "You are the doctor. Protect one player each night and avoid exposing yourself too early.",
}

COMMON_RULES = (
    "Speak naturally and briefly. Return strictly valid JSON matching requested schema. "
    "Do not reveal hidden chain-of-thought; provide only short reasoning_summary."
)


def system_prompt_for_role(role: str) -> str:
    return f"{ROLE_PROMPTS.get(role, 'Play to your win condition.')} {COMMON_RULES}"
