import asyncio
from types import SimpleNamespace

from custom_components.neuro_modes.const import CONF_ENTRY_TYPE, ENTRY_TYPE_MODE
from custom_components.neuro_modes.flows.flows_settings import async_step_edit_settings


class _FakeConfigEntries:
    def __init__(self):
        self.updated = []

    def async_update_entry(self, entry, title, data):
        self.updated.append({"entry": entry, "title": title, "data": data})


class _FakeFlow:
    def __init__(self):
        self._entry = SimpleNamespace(
            data={CONF_ENTRY_TYPE: ENTRY_TYPE_MODE, "name": "Dom", "threshold": 70, "delta": 20, "override_timeout": 120},
            options={"sources": []},
        )
        self.hass = SimpleNamespace(config_entries=_FakeConfigEntries())

    def async_create_entry(self, title, data):
        return {"type": "create_entry", "title": title, "data": data}

    def async_show_form(self, step_id, data_schema):
        return {"type": "form", "step_id": step_id, "data_schema": data_schema}


def test_edit_settings_updates_entry_and_preserves_options():
    flow = _FakeFlow()
    user_input = {"name": "Nowy Dom", "threshold": 80, "delta": 10, "override_timeout": 60}

    result = asyncio.run(async_step_edit_settings(flow, user_input))

    assert flow.hass.config_entries.updated
    assert flow.hass.config_entries.updated[0]["title"].startswith("Mode:")
    assert result["data"] == flow._entry.options
