"""Adaptive Lighting adapter - controls AL switches per area with Smart Search."""
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

class AdaptiveLightingAdapter:
    """Adapter for Adaptive Lighting integration."""

    def __init__(self, hass):
        self.hass = hass

    def _find_entity(self, area_id: str, is_sleep: bool) -> str | None:
        """Inteligentne wyszukiwanie encji AL niezależnie od nazewnictwa."""
        # Pobieramy wszystkie przełączniki w Home Assistant
        all_switches = self.hass.states.async_entity_ids("switch")
        
        for entity_id in all_switches:
            if "adaptive_lighting" in entity_id and area_id in entity_id:
                has_sleep = "sleep_mode" in entity_id
                if is_sleep and has_sleep:
                    return entity_id
                elif not is_sleep and not has_sleep:
                    return entity_id
        return None

    async def apply_state(self, area_ids: list[str], mode_config: dict[str, Any]) -> None:
        mode = mode_config.get("adaptive_lighting_mode", "leave")
        fallback_scene = mode_config.get("fallback_scene")

        for area_id in area_ids:
            try:
                if mode == "disable":
                    entity = self._find_entity(area_id, False)
                    if entity:
                        await self.hass.services.async_call("switch", "turn_off", {"entity_id": entity})
                        _LOGGER.debug("AL wyłączone dla %s (%s)", area_id, entity)
                    
                elif mode == "sleep_mode":
                    entity = self._find_entity(area_id, True)
                    if entity:
                        await self.hass.services.async_call("switch", "turn_on", {"entity_id": entity})
                        _LOGGER.debug("AL Sleep Mode włączony dla %s (%s)", area_id, entity)
                    
                if fallback_scene:
                    await self.hass.services.async_call("scene", "turn_on", {"entity_id": fallback_scene})
                    _LOGGER.debug("Scena %s włączona", fallback_scene)
                    
            except Exception as err:
                _LOGGER.warning("Błąd AL dla %s: %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str) -> None:
        for area_id in area_ids:
            try:
                if restore_action in ["restore_previous", "enable_al"]:
                    main_entity = self._find_entity(area_id, False)
                    sleep_entity = self._find_entity(area_id, True)
                    
                    if main_entity:
                        await self.hass.services.async_call("switch", "turn_on", {"entity_id": main_entity})
                    if sleep_entity:
                        await self.hass.services.async_call("switch", "turn_off", {"entity_id": sleep_entity})
                    
                elif restore_action == "turn_off_all":
                    # W trybie wyłączania zakładamy standardową grupę z MA lub sam pokój
                    light_group = f"light.{area_id}"
                    await self.hass.services.async_call("light", "turn_off", {"entity_id": light_group})
                    
            except Exception as err:
                _LOGGER.warning("Błąd przywracania AL dla %s: %s", area_id, err)