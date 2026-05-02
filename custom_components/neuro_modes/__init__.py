from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, ENTRY_TYPE_MODE
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

    # Jeśli dodano nowy tryb bazowy po silniku, odświeżamy koordynator silnika,
    # aby selector trybu domu natychmiast zobaczył nową opcję.
    if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_MODE:
        for cfg_entry in hass.config_entries.async_entries(DOMAIN):
            if cfg_entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
                engine_coordinator = hass.data[DOMAIN].get(cfg_entry.entry_id)
                if engine_coordinator is not None:
                    engine_coordinator.async_set_updated_data(engine_coordinator.data)
    
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
