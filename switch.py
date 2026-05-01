from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, CONF_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
        return
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NeuroModeSwitch(coordinator)])

class NeuroModeSwitch(SwitchEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._name = coordinator.entry.data.get(CONF_NAME)
        self._attr_name = "Stan"
        self._attr_unique_id = f"{coordinator.entry.entry_id}_state"

    @property
    def device_info(self) -> DeviceInfo:
        engine_id = None
        for entry in self.coordinator.hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
                engine_id = entry.entry_id
                break
        info = DeviceInfo(identifiers={(DOMAIN, self.coordinator.entry.entry_id)}, name=f"Neuro Modes: {self._name}", manufacturer="Neuro Home")
        if engine_id:
            info["via_device"] = (DOMAIN, engine_id)
        return info

    @property
    def is_on(self):
        return self.coordinator.engine.states.get(self._name, {}).get("state", False)
        
    @property
    def extra_state_attributes(self):
        """POPRAWKA: Przywrócone atrybuty statystyczne dla XAI."""
        data = self.coordinator.engine.states.get(self._name, {})
        return {
            "Pewność systemu": f"{data.get('confidence', 0)}%",
            "Ręczne nadpisanie": "Aktywne" if data.get('human_override') else "Brak",
            "Aktywne poszlaki": data.get("active", [])
        }

    async def async_turn_on(self, **kwargs):
        # Odpalamy czasówkę z Coordinatora
        self.coordinator.set_override(True)

    async def async_turn_off(self, **kwargs):
        self.coordinator.set_override(False)

    async def async_added_to_hass(self):
        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))
