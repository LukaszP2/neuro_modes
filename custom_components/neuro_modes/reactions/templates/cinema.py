"""Cinema reaction template - predefined configuration for cinema mode."""

CINEMA_TEMPLATE = {
    "id": "cinema_default",
    "name": "Cinema",
    "description": "Disable adaptive lighting and presence tracking in cinema room",
    "areas": [],  # User will select areas
    "adaptive_lighting_mode": "disable",
    "fallback_scene": None,  # User can optionally set a scene
    "restore_action": "restore_previous",
}
