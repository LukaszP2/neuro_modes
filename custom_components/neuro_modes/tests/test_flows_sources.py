import asyncio
from types import SimpleNamespace

from custom_components.neuro_modes.flows.flows_sources import (
    async_step_pick_source_for_delete,
    async_step_pick_source_for_edit,
)


class _FakeFlow:
    def __init__(self, sources):
        self._entry = SimpleNamespace(options={"sources": sources}, data={"sources": sources})
        self._selected_source_id = None
        self.hass = SimpleNamespace(states=_FakeStates())

    def async_show_form(self, step_id, data_schema=None, **kwargs):
        return {"type": "form", "step_id": step_id, "data_schema": data_schema, **kwargs}

    def async_abort(self, reason):
        return {"type": "abort", "reason": reason}

    async def async_step_edit_source_form(self):
        return {"type": "forward", "step_id": "edit_source_form", "selected": self._selected_source_id}

    async def async_step_delete_source_action(self):
        return {"type": "forward", "step_id": "delete_source_action", "selected": self._selected_source_id}


class _FakeStates:
    def get(self, entity_id):
        return SimpleNamespace(attributes={"friendly_name": f"Friendly {entity_id}"})


def test_pick_source_for_edit_no_sources_aborts():
    flow = _FakeFlow([])

    result = asyncio.run(async_step_pick_source_for_edit(flow, None))

    assert result["type"] == "abort"
    assert result["reason"] == "no_sources"


def test_pick_source_for_edit_selects_and_forwards_to_edit_form():
    flow = _FakeFlow([{"entity_id": "sensor.temp", "state": "on", "weight": 30}])

    result = asyncio.run(async_step_pick_source_for_edit(flow, {"selected_source": "sensor.temp"}))

    assert flow._selected_source_id == "sensor.temp"
    assert result["type"] == "forward"
    assert result["step_id"] == "edit_source_form"


def test_pick_source_for_delete_no_sources_aborts():
    flow = _FakeFlow([])

    result = asyncio.run(async_step_pick_source_for_delete(flow, None))

    assert result["type"] == "abort"
    assert result["reason"] == "no_sources"


def test_pick_source_for_delete_selects_and_forwards_to_confirm_delete():
    flow = _FakeFlow([{"entity_id": "binary_sensor.motion", "state": "on", "weight": 20}])

    result = asyncio.run(async_step_pick_source_for_delete(flow, {"selected_source": "binary_sensor.motion"}))

    assert flow._selected_source_id == "binary_sensor.motion"
    assert result["type"] == "forward"
    assert result["step_id"] == "delete_source_action"
