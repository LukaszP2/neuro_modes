import sys
import types


def _ensure_module(name: str):
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)
    return sys.modules[name]


# Base package tree
_ensure_module("homeassistant")
_ensure_module("homeassistant.components")
_ensure_module("homeassistant.helpers")
_ensure_module("homeassistant.helpers.event")
_ensure_module("homeassistant.helpers.selector")


# voluptuous (minimal test stub)
vol_mod = _ensure_module("voluptuous")


def Schema(value):
    return value


def Required(key, default=None):
    return key


setattr(vol_mod, "Schema", Schema)
setattr(vol_mod, "Required", Required)


# homeassistant.components.select
select_mod = _ensure_module("homeassistant.components.select")


class SelectEntity:
    pass


setattr(select_mod, "SelectEntity", SelectEntity)


# homeassistant.components.diagnostics
diagnostics_mod = _ensure_module("homeassistant.components.diagnostics")


def async_redact_data(data, to_redact):
    def _redact(value):
        if isinstance(value, dict):
            out = {}
            for k, v in value.items():
                out[k] = "**REDACTED**" if k in to_redact else _redact(v)
            return out
        if isinstance(value, list):
            return [_redact(v) for v in value]
        return value

    return _redact(data)


setattr(diagnostics_mod, "async_redact_data", async_redact_data)


# homeassistant.helpers.device_registry
device_registry_mod = _ensure_module("homeassistant.helpers.device_registry")


class DeviceInfo(dict):
    pass


setattr(device_registry_mod, "DeviceInfo", DeviceInfo)


# homeassistant.helpers.update_coordinator
uc_mod = _ensure_module("homeassistant.helpers.update_coordinator")


class CoordinatorEntity:
    def __init__(self, coordinator):
        self.coordinator = coordinator

    def async_write_ha_state(self):
        return None


class DataUpdateCoordinator:
    def __class_getitem__(cls, _item):
        return cls

    def __init__(self, *args, **kwargs):
        self.data = {}

    async def async_refresh(self):
        return None

    def async_set_updated_data(self, data):
        self.data = data


setattr(uc_mod, "CoordinatorEntity", CoordinatorEntity)
setattr(uc_mod, "DataUpdateCoordinator", DataUpdateCoordinator)


# homeassistant.config_entries
config_entries_mod = _ensure_module("homeassistant.config_entries")


class ConfigEntry:
    pass


setattr(config_entries_mod, "ConfigEntry", ConfigEntry)


class ConfigFlow:
    pass


class OptionsFlow:
    pass


setattr(config_entries_mod, "ConfigFlow", ConfigFlow)
setattr(config_entries_mod, "OptionsFlow", OptionsFlow)
setattr(config_entries_mod, "SOURCE_IMPORT", "import")


# homeassistant.core
core_mod = _ensure_module("homeassistant.core")


class HomeAssistant:
    pass


setattr(core_mod, "HomeAssistant", HomeAssistant)


def callback(func):
    return func


setattr(core_mod, "callback", callback)


# homeassistant.helpers.event
event_mod = _ensure_module("homeassistant.helpers.event")


def async_track_state_change_event(hass, entity_ids, action):
    return lambda: None


def async_call_later(hass, delay, action):
    return lambda: None


setattr(event_mod, "async_track_state_change_event", async_track_state_change_event)
setattr(event_mod, "async_call_later", async_call_later)


# homeassistant.helpers.selector
selector_mod = _ensure_module("homeassistant.helpers.selector")


class SelectSelector:
    def __init__(self, config):
        self.config = config


class SelectSelectorConfig:
    def __init__(self, options=None, mode=None):
        self.options = options or []
        self.mode = mode


class BooleanSelector:
    pass


class EntitySelectorConfig:
    def __init__(self, domain=None, multiple=False):
        self.domain = domain
        self.multiple = multiple


class EntitySelector:
    def __init__(self, config=None):
        self.config = config


setattr(selector_mod, "SelectSelector", SelectSelector)
setattr(selector_mod, "SelectSelectorConfig", SelectSelectorConfig)
setattr(selector_mod, "BooleanSelector", BooleanSelector)
setattr(selector_mod, "EntitySelector", EntitySelector)
setattr(selector_mod, "EntitySelectorConfig", EntitySelectorConfig)
