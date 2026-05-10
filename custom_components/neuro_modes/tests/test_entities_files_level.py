from types import SimpleNamespace

from custom_components.neuro_modes.binary_sensor import NeuroSourceBinarySensor
from custom_components.neuro_modes.const import CONF_ENTRY_TYPE, CONF_NAME, DOMAIN, ENTRY_TYPE_MODE
from custom_components.neuro_modes.select import NeuroBaseSelect
from custom_components.neuro_modes.sensor import NeuroConfidence
from custom_components.neuro_modes.switch import NeuroModeSwitch


class _FakeConfigEntries:
    def __init__(self, entries):
        self._entries = entries
        self.updated_entry = None
        self.updated_options = None

    def async_entries(self, domain):
        if domain == DOMAIN:
            return self._entries
        return []

    def async_update_entry(self, entry, options=None, **kwargs):
        self.updated_entry = entry
        self.updated_options = options


class _FakeCoordinator:
    def __init__(self, entry, data=None, states=None, mode_name="Dom", all_entries=None):
        self.entry = entry
        self.config_entry = entry
        self.data = data or {}
        self.mode_name = mode_name
        self.engine = SimpleNamespace(states=states or {})
        self.hass = SimpleNamespace(config_entries=_FakeConfigEntries(all_entries or []))
        self.override_calls = []

    def set_override(self, is_on):
        self.override_calls.append(is_on)


def _entry(entry_id="mode-1", name="Dom", entry_type=ENTRY_TYPE_MODE, options=None):
    return SimpleNamespace(
        entry_id=entry_id,
        data={CONF_NAME: name, CONF_ENTRY_TYPE: entry_type},
        options=options or {},
        title=f"Mode: {name}",
    )


def test_binary_sensor_reports_source_activity_and_attributes():
    entry = _entry()
    coordinator = _FakeCoordinator(
        entry,
        data={"active": ["binary_sensor.motion_kitchen"]},
    )
    source = {"entity_id": "binary_sensor.motion_kitchen", "state": "on", "weight": 30}

    entity = NeuroSourceBinarySensor(coordinator, source, 0)

    assert entity.is_on is True
    assert entity.extra_state_attributes == {"expected_state": "on", "weight_points": 30}


def test_confidence_sensor_reads_engine_diagnostics():
    entry = _entry(options={"activation_threshold": 65})
    mode_name = "Dom"
    coordinator = _FakeCoordinator(
        entry,
        data={"confidence": 82},
        mode_name=mode_name,
        states={
            mode_name: {
                "confidence": 82,
                "active": ["person.lukas"],
                "human_override": True,
            }
        },
    )

    entity = NeuroConfidence(coordinator)

    assert entity.native_value == 82
    assert entity.extra_state_attributes == {
        "confidence": 82,
        "active_sources": ["person.lukas"],
        "human_override": True,
        "threshold": 65,
    }


def test_switch_reflects_state_and_calls_override_on_toggle():
    entry = _entry()
    coordinator = _FakeCoordinator(
        entry,
        data={"state": True, "confidence": 90, "human_override": False, "active": ["sensor.a"]},
    )
    entity = NeuroModeSwitch(coordinator)

    assert entity.is_on is True
    assert entity.extra_state_attributes["system_confidence"] == 90

    import asyncio

    asyncio.run(entity.async_turn_off())
    asyncio.run(entity.async_turn_on())

    assert coordinator.override_calls == [False, True]


def test_select_persists_selected_mode_to_entry_options():
    engine_entry = _entry(entry_id="engine-1", name="Engine", entry_type="engine", options={"x": 1})
    mode_a = _entry(entry_id="mode-a", name="Dom")
    mode_b = _entry(entry_id="mode-b", name="Poza domem")

    coordinator = _FakeCoordinator(
        engine_entry,
        all_entries=[mode_a, mode_b],
    )
    entity = NeuroBaseSelect(coordinator)

    assert entity.options == ["Dom", "Poza domem"]

    import asyncio

    asyncio.run(entity.async_select_option("Poza domem"))

    assert coordinator.hass.config_entries.updated_entry is engine_entry
    assert coordinator.hass.config_entries.updated_options == {"x": 1, "selected_mode": "Poza domem"}
    assert entity.current_option == "Poza domem"
