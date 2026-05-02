import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, ENTRY_TYPE_MODE, ENTRY_TYPE_MODIFIER, CONF_SOURCES
from .engine import NeuroEngine
from .coordinator import NeuroModesCoordinator

PLATFORMS = ["select", "switch", "sensor", "binary_sensor"]


def _refresh_engine_coordinators(hass: HomeAssistant) -> None:
    """Trigger refresh for all engine coordinators (selector options sync)."""
    for cfg_entry in hass.config_entries.async_entries(DOMAIN):
        if cfg_entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
            engine_coordinator = hass.data[DOMAIN].get(cfg_entry.entry_id)
            if engine_coordinator is not None:
                engine_coordinator.async_set_updated_data(engine_coordinator.data)


async def _refresh_engine_coordinators_delayed(hass: HomeAssistant) -> None:
    """Run one event loop tick later to catch async_entries state after add/remove."""
    await asyncio.sleep(0)
    _refresh_engine_coordinators(hass)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if "engine" not in hass.data.setdefault(DOMAIN, {}):
        hass.data[DOMAIN]["engine"] = NeuroEngine(hass)
        
    engine = hass.data[DOMAIN]["engine"]
    coordinator = NeuroModesCoordinator(hass, entry, engine)
    
    await coordinator.async_setup()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # If a new base mode was added after engine, refresh engine coordinator
    # so the mode selector immediately sees the new option.
    if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_MODE:
        _refresh_engine_coordinators(hass)
        hass.async_create_task(_refresh_engine_coordinators_delayed(hass))
    
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate config entry to newer versions."""
    data = dict(entry.data)

    if entry.version < 2:
        if CONF_ENTRY_TYPE not in data:
            title = (entry.title or "").lower()
            if title.startswith("mode:"):
                data[CONF_ENTRY_TYPE] = ENTRY_TYPE_MODE
            elif title.startswith("modifier:"):
                data[CONF_ENTRY_TYPE] = ENTRY_TYPE_MODIFIER
            else:
                data[CONF_ENTRY_TYPE] = ENTRY_TYPE_ENGINE

        if data.get(CONF_ENTRY_TYPE) in (ENTRY_TYPE_MODE, ENTRY_TYPE_MODIFIER) and CONF_SOURCES not in data:
            data[CONF_SOURCES] = []

        hass.config_entries.async_update_entry(entry, data=data, version=2)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    entry_type = entry.data.get(CONF_ENTRY_TYPE)

    coordinator = hass.data[DOMAIN].get(entry.entry_id)
    if coordinator:
        await coordinator.async_unload()
        
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

        # If a base mode was removed, refresh engine coordinator
        # so the selector immediately removes the option.
        if entry_type == ENTRY_TYPE_MODE:
            _refresh_engine_coordinators(hass)
            hass.async_create_task(_refresh_engine_coordinators_delayed(hass))

        # Clean up engine if this was the last entry
        if not any(e.data.get(CONF_ENTRY_TYPE) != ENTRY_TYPE_ENGINE for e in hass.config_entries.async_entries(DOMAIN)):
            hass.data[DOMAIN].pop("engine", None)

    return unload_ok
