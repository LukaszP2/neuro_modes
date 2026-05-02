from __future__ import annotations

import asyncio
from types import SimpleNamespace

import custom_components.neuro_modes as nm_init
from custom_components.neuro_modes.const import (
    CONF_ENTRY_TYPE,
    DOMAIN,
    ENTRY_TYPE_ENGINE,
    ENTRY_TYPE_MODE,
)


class _FakeEngineCoordinator:
    def __init__(self):
        self.data = {"ok": True}
        self.refresh_called = False

    def async_set_updated_data(self, data):
        self.refresh_called = True
        self.data = data


class _FakeCreatedCoordinator:
    def __init__(self, hass, entry, engine):
        self.hass = hass
        self.entry = entry
        self.engine = engine

    async def async_setup(self):
        return None

    async def async_unload(self):
        return None


class _FakeFlowEntries:
    def __init__(self, entries):
        self._entries = entries

    def async_entries(self, domain):
        if domain == DOMAIN:
            return self._entries
        return []

    async def async_forward_entry_setups(self, entry, platforms):
        return None


class _FakeHass(SimpleNamespace):
    def async_create_task(self, coro):
        # Emulujemy zachowanie HA: task jest planowany na aktywnej pętli.
        return asyncio.create_task(coro)


def _make_entry(entry_id: str, entry_type: str):
    return SimpleNamespace(
        entry_id=entry_id,
        data={CONF_ENTRY_TYPE: entry_type},
        add_update_listener=lambda listener: (lambda: None),
        async_on_unload=lambda cb: None,
    )


def test_mode_added_after_engine_triggers_engine_selector_refresh(monkeypatch):
    # Given: engine entry already exists
    engine_entry = _make_entry("engine-1", ENTRY_TYPE_ENGINE)
    mode_entry = _make_entry("mode-1", ENTRY_TYPE_MODE)

    fake_engine_coordinator = _FakeEngineCoordinator()

    hass = _FakeHass(
        data={DOMAIN: {"engine": object(), "engine-1": fake_engine_coordinator}},
        config_entries=_FakeFlowEntries([engine_entry, mode_entry]),
    )

    monkeypatch.setattr(nm_init, "NeuroModesCoordinator", _FakeCreatedCoordinator)

    # When: new MODE entry is set up after engine
    result = asyncio.run(nm_init.async_setup_entry(hass, mode_entry))

    # Then: engine coordinator should be pinged to refresh selector options
    assert result is True
    assert fake_engine_coordinator.refresh_called is True
