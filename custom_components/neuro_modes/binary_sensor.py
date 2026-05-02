from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, CONF_NAME, CONF_SOURCES

async def async_setup_entry(hass, entry, async_add_entities):
    if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
        return
        
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sources = entry.options.get(CONF_SOURCES, entry.data.get(CONF_SOURCES, []))
    
    entities = []
    for index, source in enumerate(sources):
        entities.append(NeuroSourceBinarySensor(coordinator, source, index))
        
    async_add_entities(entities)

class NeuroSourceBinarySensor(CoordinatorEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, source, index):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._source = source
        self._name = coordinator.entry.data.get(CONF_NAME)
        self._attr_name = source["entity_id"]
        self._attr_unique_id = f"{coordinator.entry.entry_id}_source_{index}_{source['entity_id']}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.entry.entry_id)},
            name=f"Neuro Modes: {self._name}",
            manufacturer="Neuro Home",
        )

    @property
    def is_on(self):
        mode_state = self.coordinator.data or {}
        active_sources = mode_state.get("active", [])
        return self._source["entity_id"] in active_sources

    @property
    def extra_state_attributes(self):
        return {
            "expected_state": self._source.get("state"),
            "weight_points": self._source.get("weight"),
        }

