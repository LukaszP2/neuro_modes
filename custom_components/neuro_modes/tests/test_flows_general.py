import asyncio
from types import SimpleNamespace

from custom_components.neuro_modes.const import CONF_ENTRY_TYPE, CONF_SOURCES, ENTRY_TYPE_MODE, ENTRY_TYPE_MODIFIER
from custom_components.neuro_modes.flows.flows_general import async_step_setup_mode, async_step_setup_modifier


class _FakeFlow:
    def __init__(self):
        self.hass = SimpleNamespace()

    def async_create_entry(self, title, data):
        return {"type": "create_entry", "title": title, "data": data}

    def async_show_form(self, step_id, data_schema):
        return {"type": "form", "step_id": step_id, "data_schema": data_schema}


def test_setup_mode_creates_mode_entry_with_sources_list():
    flow = _FakeFlow()
    user_input = {"name": "Dom", "threshold": 70, "delta": 20, "override_timeout": 120}

    result = asyncio.run(async_step_setup_mode(flow, user_input))

    assert result["type"] == "create_entry"
    assert result["data"][CONF_ENTRY_TYPE] == ENTRY_TYPE_MODE
    assert result["data"][CONF_SOURCES] == []


def test_setup_modifier_creates_modifier_entry_with_sources_list():
    flow = _FakeFlow()
    user_input = {"name": "Noc", "threshold": 70, "delta": 20, "override_timeout": 120}

    result = asyncio.run(async_step_setup_modifier(flow, user_input))

    assert result["type"] == "create_entry"
    assert result["data"][CONF_ENTRY_TYPE] == ENTRY_TYPE_MODIFIER
    assert result["data"][CONF_SOURCES] == []
