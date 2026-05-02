from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, CONF_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    # Pomijamy silnik główny, bo on nie ma własnej "pewności"
    if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
        return
        
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NeuroConfidence(coordinator)])

class NeuroConfidence(SensorEntity):
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "%"
    _attr_translation_key = "confidence"

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._name = coordinator.entry.data.get(CONF_NAME)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_conf_sensor"

    @property
    def device_info(self) -> DeviceInfo:
        engine_id = None
        for entry in self.coordinator.hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
                engine_id = entry.entry_id
                break
                
        info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.entry.entry_id)},
            name=f"Neuro Modes: {self._name}",
            manufacturer="Neuro Home",
        )
        if engine_id:
            info["via_device"] = (DOMAIN, engine_id)
        return info

    @property
    def native_value(self):
        return int(self.coordinator.engine.states.get(self._name, {}).get("confidence", 0))

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))