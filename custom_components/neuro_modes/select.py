from homeassistant.components.select import SelectEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, ENTRY_TYPE_MODE, CONF_NAME

async def async_setup_entry(hass, entry, async_add_entities):
    if entry.data.get(CONF_ENTRY_TYPE) != ENTRY_TYPE_ENGINE:
        return
        
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NeuroBaseSelect(coordinator)])

class NeuroBaseSelect(CoordinatorEntity, SelectEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "home_mode"
    _attr_should_poll = True

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_unique_id = f"{coordinator.entry.entry_id}_global_base_mode"
        self._last_option = None

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.entry.entry_id)},
            name="Engine Neuro Modes",
            manufacturer="Neuro Home",
        )

    @property
    def options(self) -> list[str]:

        modes = []
        for entry in self.coordinator.hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_MODE:
                name = entry.data.get(CONF_NAME)
                if name:
                    modes.append(name)

        return modes if modes else ["No base mode configured"]

    @property
    def current_option(self):

        options = self.options
        if self._last_option in options:
            return self._last_option
        return options[0] if options else None

    async def async_select_option(self, option: str) -> None:
        self._last_option = option
        self.async_write_ha_state()
