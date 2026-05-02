from types import SimpleNamespace
import asyncio

from custom_components.neuro_modes.const import DOMAIN
from custom_components.neuro_modes.diagnostics import async_get_config_entry_diagnostics


def test_diagnostics_runtime_summary_and_redaction():
    entry = SimpleNamespace(
        entry_id="mode-1",
        title="Mode: Dom",
        data={"name": "Dom", "entity_id": "sensor.secret"},
        options={},
    )

    coordinator = SimpleNamespace(
        engine=SimpleNamespace(
            states={
                "Dom": {
                    "state": True,
                    "confidence": 80,
                    "active": ["binary_sensor.motion"],
                    "human_override": True,
                }
            }
        )
    )

    hass = SimpleNamespace(data={DOMAIN: {"mode-1": coordinator}})

    diagnostics = asyncio.run(async_get_config_entry_diagnostics(hass, entry))

    assert diagnostics["runtime"]["summary"]["has_coordinator"] is True
    assert diagnostics["runtime"]["summary"]["active_sources_count"] == 1
    assert diagnostics["runtime"]["summary"]["human_override"] is True
    assert diagnostics["entry"]["data"]["entity_id"] == "**REDACTED**"
