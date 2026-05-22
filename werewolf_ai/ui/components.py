from __future__ import annotations
import streamlit as st


def role_selector(roles: dict, defaults: dict[str, int] | None = None):
    counts = {}
    st.subheader("Role Configuration")
    for role, meta in roles.items():
        counts[role] = st.number_input(f"{role.title()} ({meta.get('description','')})", min_value=0, value=(defaults or {}).get(role, 0), step=1)
    return counts


def validate_roles(role_counts: dict[str, int], allow_wolf_parity: bool = False):
    total = sum(role_counts.values())
    wolves = role_counts.get("werewolf", 0)
    villagers = role_counts.get("villager", 0)
    non_wolves = total - wolves
    errors = []
    if total < 5:
        errors.append("Total players must be at least 5")
    if wolves < 1:
        errors.append("At least 1 werewolf is required")
    if non_wolves < 1:
        errors.append("At least 1 non-werewolf is required")
    if not allow_wolf_parity and wolves >= villagers and villagers > 0:
        errors.append("Werewolves must be fewer than villagers unless parity is allowed")
    return errors
