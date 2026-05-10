"""Magic Areas adapter with Smart Discovery."""
import logging
from typing import Any
from custom_components.neuro_modes.reactions.discovery import AreaDiscovery

_LOGGER = logging.getLogger(__name__)

class MagicAreasAdapter:
    """Adapter obsługujący Magic Areas na podstawie Area Registry."""
    
    def __init__(self, hass):
        self.hass = hass
        self.discovery = AreaDiscovery(hass)

    async def apply_state(self, area_ids: list[str], mode_config: dict[str, Any], mode_name: str) -> None:
        for area_id in area_ids:
            try:
                # 1. Automatyczny Tryb Nocny (Synchronizacja z NM)
                if any(kw in mode_name.lower() for kw in ["noc", "night", "nocny"]):
                    night_switch = self.discovery.find_integration_switch(area_id, "magic_areas", "sleep_mode")
                    if night_switch:
                        await self.hass.services.async_call("switch", "turn_on", {"entity_id": night_switch})
                        _LOGGER.debug("MA: Synchronizacja trybu nocnego dla obszaru '%s'", area_id)

                # 2. Blokowanie Auto-światła (np. dla Trybu Filmowego)
                block_lights = mode_config.get("adaptive_lighting_mode") == "disable"
                if block_lights:
                    light_control = self.discovery.find_integration_switch(area_id, "magic_areas", "light_control")
                    if light_control:
                        await self.hass.services.async_call("switch", "turn_off", {"entity_id": light_control})
                        _LOGGER.debug("MA: Zablokowano wyzwalacz światła dla obszaru '%s'", area_id)

            except Exception as err:
                _LOGGER.warning("MA Adapter Error dla '%s': %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str, mode_name: str) -> None:
        for area_id in area_ids:
            try:
                if any(kw in mode_name.lower() for kw in ["noc", "night", "nocny"]):
                    night_switch = self.discovery.find_integration_switch(area_id, "magic_areas", "sleep_mode")
                    if night_switch:
                        await self.hass.services.async_call("switch", "turn_off", {"entity_id": night_switch})

                light_control = self.discovery.find_integration_switch(area_id, "magic_areas", "light_control")
                if light_control:
                    await self.hass.services.async_call("switch", "turn_on", {"entity_id": light_control})

            except Exception as err:
                _LOGGER.warning("MA Restore Error dla '%s': %s", area_id, err)