from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, CONF_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    # Pomijamy silnik główny, bo on nie ma własnej "pewności"
    if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
        return
        
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NeuroConfidence(coordinator)])

class NeuroConfidence(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "%"
    _attr_translation_key = "confidence"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._name = coordinator.entry.data.get(CONF_NAME)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_conf_sensor"
        self._engine_id = None

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        for entry in self.coordinator.hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
                self._engine_id = entry.entry_id
                break

    @property
    def device_info(self) -> DeviceInfo:
        info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.entry.entry_id)},
            name=f"Neuro Modes: {self._name}",
            manufacturer="Neuro Home",
        )
        if self._engine_id:
            info["via_device"] = (DOMAIN, self._engine_id)
        return info

    @property
    def native_value(self):
        return int((self.coordinator.data or {}).get("confidence", 0))