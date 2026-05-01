from homeassistant.components.select import SelectEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, ENTRY_TYPE_MODE, CONF_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    if entry.data.get(CONF_ENTRY_TYPE) != ENTRY_TYPE_ENGINE:
        return
        
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NeuroBaseSelect(coordinator)])

class NeuroBaseSelect(SelectEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Tryb domu"
        self._attr_unique_id = f"{coordinator.entry.entry_id}_global_base_mode"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.entry.entry_id)},
            name="Neuro Modes: Engine",
            manufacturer="Neuro Home",
        )

    @property
    def options(self) -> list[str]:
        """Tylko faktycznie dodane tryby bazowe."""
        modes = []
        for entry in self.coordinator.hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_MODE:
                name = entry.data.get(CONF_NAME)
                if name:
                    modes.append(name)
        # Jeśli nic jeszcze nie dodałeś, pokażemy informację
        return modes if modes else ["Dodaj tryb bazowy w integracjach"]

    @property
    def current_option(self):
        # Pobieramy stan z silnika (docelowo) - na razie unikamy błędu "Brak"
        options = self.options
        return options[0] if options else None

    async def async_select_option(self, option: str) -> None:
        self.async_write_ha_state()
