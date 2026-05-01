from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
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

class NeuroSourceBinarySensor(BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, source, index):
        self.coordinator = coordinator
        self._source = source
        self._name = coordinator.entry.data.get(CONF_NAME)
        self._attr_name = f"Poszlaka: {source['entity_id']}"
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
        mode_state = self.coordinator.engine.states.get(self._name, {})
        active_sources = mode_state.get("active", [])
        return self._source["entity_id"] in active_sources

    @property
    def extra_state_attributes(self):
        """Eksport wag i stanów do UI."""
        return {
            "oczekiwany_stan": self._source.get("state"),
            "waga_punktowa": f"{self._source.get('weight')}%"
        }

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
