from types import SimpleNamespace

from custom_components.neuro_modes.const import (
    CONF_ENTRY_TYPE,
    CONF_NAME,
    DOMAIN,
    ENTRY_TYPE_MODE,
    ENTRY_TYPE_MODIFIER,
)
from custom_components.neuro_modes.select import NeuroBaseSelect


class _FakeConfigEntries:
    def __init__(self, entries):
        self._entries = entries

    def async_entries(self, domain):
        if domain == DOMAIN:
            return self._entries
        return []


class _FakeCoordinator:
    def __init__(self, entries):
        self.entry = SimpleNamespace(entry_id="engine-1")
        self.hass = SimpleNamespace(config_entries=_FakeConfigEntries(entries))

    def async_add_listener(self, update_callback, context=None):
        return lambda: None


def _entry(entry_type, name, title):
    return SimpleNamespace(
        data={CONF_ENTRY_TYPE: entry_type, CONF_NAME: name},
        title=title,
        entry_id=f"id-{name}",
    )


def test_select_shows_only_base_modes():
    entries = [
        _entry(ENTRY_TYPE_MODE, "Dom", "Mode: Dom"),
        _entry(ENTRY_TYPE_MODE, "Poza domem", "Mode: Poza domem"),
        _entry(ENTRY_TYPE_MODIFIER, "Noc", "Modifier: Noc"),
    ]
    select = NeuroBaseSelect(_FakeCoordinator(entries))

    assert select.options == ["Dom", "Poza domem"]


def test_select_fallback_when_no_base_mode():
    entries = [_entry(ENTRY_TYPE_MODIFIER, "Noc", "Modifier: Noc")]
    select = NeuroBaseSelect(_FakeCoordinator(entries))

    assert select.options == ["No base mode configured"]
