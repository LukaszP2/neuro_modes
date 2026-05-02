from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

TO_REDACT = {
    "entity_id",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    mode_name = entry.data.get("name")

    state_snapshot: dict[str, Any] = {}
    runtime_summary: dict[str, Any] = {
        "has_coordinator": coordinator is not None,
        "active_sources_count": 0,
        "human_override": False,
    }

    if coordinator and mode_name:
        state_snapshot = coordinator.engine.states.get(mode_name, {})
        runtime_summary["active_sources_count"] = len(state_snapshot.get("active", []))
        runtime_summary["human_override"] = bool(state_snapshot.get("human_override", False))

    payload = {
        "entry": {
            "entry_id": entry.entry_id,
            "title": entry.title,
            "data": dict(entry.data),
            "options": dict(entry.options),
        },
        "runtime": {
            "mode_name": mode_name,
            "state": state_snapshot,
            "summary": runtime_summary,
        },
    }

    return async_redact_data(payload, TO_REDACT)
