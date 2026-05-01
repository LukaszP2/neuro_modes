from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .engine import NeuroEngine
from .coordinator import NeuroModesCoordinator

PLATFORMS = ["select", "switch", "sensor", "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if "engine" not in hass.data.setdefault(DOMAIN, {}):
        hass.data[DOMAIN]["engine"] = NeuroEngine(hass)
        
    engine = hass.data[DOMAIN]["engine"]
    coordinator = NeuroModesCoordinator(hass, entry, engine)
    
    await coordinator.async_setup()
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = hass.data[DOMAIN].get(entry.entry_id)
    if coordinator:
        await coordinator.async_unload()
        
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
