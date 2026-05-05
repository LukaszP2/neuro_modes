"""Adaptive Lighting adapter - controls AL switches per area."""
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

class AdaptiveLightingAdapter:
    """Adapter for Adaptive Lighting integration."""

    def __init__(self, hass):
        self.hass = hass

    async def apply_state(self, area_ids: list[str], mode_config: dict[str, Any]) -> None:
        mode = mode_config.get("adaptive_lighting_mode", "leave")
        fallback_scene = mode_config.get("fallback_scene")

        for area_id in area_ids:
            try:
                if mode == "disable":
                    switch_entity = f"switch.adaptive_lighting_{area_id}"
                    await self.hass.services.async_call("switch", "turn_off", {"entity_id": switch_entity})
                    _LOGGER.debug("AL wyłączone dla %s", area_id)
                    
                elif mode == "sleep_mode":
                    switch_entity = f"switch.adaptive_lighting_sleep_mode_{area_id}"
                    await self.hass.services.async_call("switch", "turn_on", {"entity_id": switch_entity})
                    _LOGGER.debug("AL Sleep Mode włączony dla %s", area_id)
                    
                # Jeśli użytkownik wskazał scenę (np. kino), włączamy ją od razu
                if fallback_scene:
                    await self.hass.services.async_call("scene", "turn_on", {"entity_id": fallback_scene})
                    _LOGGER.debug("Scena %s włączona", fallback_scene)
                    
            except Exception as err:
                _LOGGER.warning("Błąd AL dla %s: %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str) -> None:
        for area_id in area_ids:
            try:
                if restore_action == "restore_previous" or restore_action == "enable_al":
                    # Włączamy główny switch AL
                    switch_entity = f"switch.adaptive_lighting_{area_id}"
                    await self.hass.services.async_call("switch", "turn_on", {"entity_id": switch_entity})
                    
                    # Na wszelki wypadek wyłączamy Sleep Mode, gdyby był włączony
                    sleep_switch = f"switch.adaptive_lighting_sleep_mode_{area_id}"
                    await self.hass.services.async_call("switch", "turn_off", {"entity_id": sleep_switch})
                    
                elif restore_action == "turn_off_all":
                    # Gasimy całe światło w strefie
                    light_group = f"light.{area_id}"
                    await self.hass.services.async_call("light", "turn_off", {"entity_id": light_group})
                    
            except Exception as err:
                _LOGGER.warning("Błąd przywracania AL dla %s: %s", area_id, err)