from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from custom_components.neuro_modes.reactions.reactor import NeuroReactor


def _entry(title="Mode: Kino", reactions=None):
    return SimpleNamespace(
        title=title,
        options={
            "reactions": reactions
            or [
                {
                    "areas": ["salon"],
                    "adaptive_lighting_mode": "sleep_mode",
                    "restore_action": "restore_previous",
                    "fallback_scene": "scene.movie_time",
                }
            ]
        },
    )


@pytest.mark.asyncio
async def test_reactor_activation_runs_adapters_and_scene():
    hass = SimpleNamespace(services=SimpleNamespace(async_call=AsyncMock()))
    reactor = NeuroReactor(hass, _entry())

    reactor.ma_adapter.apply_state = AsyncMock()
    reactor.al_adapter.apply_state = AsyncMock()

    await reactor.async_react(True)

    reactor.ma_adapter.apply_state.assert_awaited_once()
    reactor.al_adapter.apply_state.assert_awaited_once()
    hass.services.async_call.assert_awaited_once_with(
        "scene", "turn_on", {"entity_id": "scene.movie_time"}
    )


@pytest.mark.asyncio
async def test_reactor_deactivation_restores_adapters():
    hass = SimpleNamespace(services=SimpleNamespace(async_call=AsyncMock()))
    reactor = NeuroReactor(hass, _entry())
    reactor._was_active = True

    reactor.ma_adapter.restore = AsyncMock()
    reactor.al_adapter.restore = AsyncMock()

    await reactor.async_react(False)

    reactor.ma_adapter.restore.assert_awaited_once_with(["salon"], "restore_previous", "Mode: Kino")
    reactor.al_adapter.restore.assert_awaited_once_with(["salon"], "restore_previous", "Mode: Kino")


@pytest.mark.asyncio
async def test_reactor_skips_empty_areas_reaction():
    hass = SimpleNamespace(services=SimpleNamespace(async_call=AsyncMock()))
    entry = _entry(
        reactions=[
            {"areas": [], "adaptive_lighting_mode": "sleep_mode", "restore_action": "restore_previous"}
        ]
    )
    reactor = NeuroReactor(hass, entry)

    reactor.ma_adapter.apply_state = AsyncMock()
    reactor.al_adapter.apply_state = AsyncMock()

    await reactor.async_react(True)

    reactor.ma_adapter.apply_state.assert_not_called()
    reactor.al_adapter.apply_state.assert_not_called()
    hass.services.async_call.assert_not_called()


@pytest.mark.asyncio
async def test_reactor_idempotency_does_not_run_twice_for_same_state():
    hass = SimpleNamespace(services=SimpleNamespace(async_call=AsyncMock()))
    reactor = NeuroReactor(hass, _entry())
    reactor._was_active = True

    reactor.ma_adapter.apply_state = AsyncMock()
    reactor.al_adapter.apply_state = AsyncMock()

    await reactor.async_react(True)

    reactor.ma_adapter.apply_state.assert_not_called()
    reactor.al_adapter.apply_state.assert_not_called()
    hass.services.async_call.assert_not_called()
