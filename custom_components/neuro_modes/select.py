from homeassistant.components.select import SelectEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE, ENTRY_TYPE_MODE, CONF_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    if entry.data.get(CONF_ENTRY_TYPE) != ENTRY_TYPE_ENGINE:
        return
        
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NeuroBaseSelect(coordinator)])

class NeuroBaseSelect(CoordinatorEntity, SelectEntity):
    _attr_has_entity_name = True
    _attr_translation_key = "home_mode"
    _attr_should_poll = False

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_unique_id = f"{coordinator.entry.entry_id}_global_base_mode"
        self._cached_options = None
        self._current_option_value = None

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        # Restore last selected option from entry options
        if "selected_mode" in self.coordinator.entry.options:
            self._current_option_value = self.coordinator.entry.options["selected_mode"]

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.entry.entry_id)},
            name="Engine Neuro Modes",
            manufacturer="Neuro Home",
        )

    @property
    def options(self) -> list[str]:
        # Cache options and invalidate on coordinator refresh
        modes = []
        for entry in self.coordinator.hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_MODE:
                name = entry.data.get(CONF_NAME)
                if name:
                    modes.append(name)

        _LOGGER.debug("Select options resolved for engine entry_id=%s count=%s", self.coordinator.entry.entry_id, len(modes))
        self._cached_options = modes
        return modes

    @property
    def current_option(self):
        options = self._cached_options or self.options
        if self._current_option_value and self._current_option_value in options:
            return self._current_option_value
        return options[0] if options else None

    async def async_select_option(self, option: str) -> None:
        _LOGGER.debug("Select option chosen for engine entry_id=%s option=%s", self.coordinator.entry.entry_id, option)
        self._current_option_value = option
        # Persist selection to entry options
        self.coordinator.hass.config_entries.async_update_entry(
            self.coordinator.entry,
            options={**self.coordinator.entry.options, "selected_mode": option}
        )
        self.async_write_ha_state()
