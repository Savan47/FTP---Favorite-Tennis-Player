import re
from typing import List

def name_tokens(s: str) -> List[str]:
    return re.findall(r"[a-z]+", (s or "").lower())

def is_doubles(p1: str, p2: str) -> bool:
    return ("/" in (p1 or "")) or ("/" in (p2 or ""))

def is_player_match(player_input: str, p1: str, p2: str) -> bool:
    player = (player_input or "").strip().lower()
    if not player:
        return False

    p1_tokens = name_tokens(p1)
    p2_tokens = name_tokens(p2)

    parts = player.split()

    # Full name: "grigor dimitrov" -> last + first initial must match tokens
    if len(parts) >= 2:
        first, last = parts[0], parts[-1]
        first_initial = first[0]
        return (
            (last in p1_tokens and first_initial in p1_tokens) or
            (last in p2_tokens and first_initial in p2_tokens)
        )

    # Single word: match as a whole token (prevents fils matching monfils)
    key = parts[0]
    if key in p1_tokens or key in p2_tokens:
        return True

    # Optional: allow first-name-only match by initial (safer with min length)
    if len(key) >= 3 and (key[0] in p1_tokens or key[0] in p2_tokens):
        return True

    return False