"""Adaptive Lighting adapter - controls AL switches per area with Smart Discovery."""
import logging
from typing import Any
from custom_components.neuro_modes.reactions.discovery import AreaDiscovery

_LOGGER = logging.getLogger(__name__)

class AdaptiveLightingAdapter:
    """Adapter obsługujący Adaptive Lighting na podstawie Area Registry."""

    def __init__(self, hass):
        self.hass = hass
        # Wstrzykujemy nasz nowy silnik wykrywania encji
        self.discovery = AreaDiscovery(hass)

    async def apply_state(self, area_ids: list[str], mode_config: dict[str, Any], mode_name: str) -> None:
        """Aplikuje ustawienia AL dla danych pokoi."""
        mode = mode_config.get("adaptive_lighting_mode", "leave")

        for area_id in area_ids:
            try:
                if mode == "disable":
                    # Szukamy głównego wyłącznika AL w danym pokoju
                    entity = self.discovery.find_integration_switch(area_id, "adaptive_lighting", "adaptive_lighting")
                    if entity:
                        await self.hass.services.async_call("switch", "turn_off", {"entity_id": entity})
                        _LOGGER.debug("AL wyłączone dla %s (%s)", area_id, entity)
                    
                elif mode == "sleep_mode":
                    # Szukamy wyłącznika Trybu Nocnego AL w danym pokoju
                    entity = self.discovery.find_integration_switch(area_id, "adaptive_lighting", "sleep_mode")
                    if entity:
                        await self.hass.services.async_call("switch", "turn_on", {"entity_id": entity})
                        _LOGGER.debug("AL Sleep Mode włączony dla %s (%s)", area_id, entity)
                    
            except Exception as err:
                _LOGGER.warning("Błąd AL Adaptera dla %s: %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str, mode_name: str) -> None:
        """Przywraca domyślny stan AL po wyłączeniu trybu."""
        for area_id in area_ids:
            try:
                if restore_action in ["restore_previous", "enable_al"]:
                    main_entity = self.discovery.find_integration_switch(area_id, "adaptive_lighting", "adaptive_lighting")
                    sleep_entity = self.discovery.find_integration_switch(area_id, "adaptive_lighting", "sleep_mode")
                    
                    if main_entity:
                        await self.hass.services.async_call("switch", "turn_on", {"entity_id": main_entity})
                    if sleep_entity:
                        await self.hass.services.async_call("switch", "turn_off", {"entity_id": sleep_entity})
                    
                elif restore_action == "turn_off_all":
                    # Znajduje wszystkie światła przypisane do pokoju i gasi je
                    lights_in_area = self.discovery.get_entities_by_domain(area_id, "light")
                    if lights_in_area:
                        await self.hass.services.async_call(
                            "light", "turn_off", {"entity_id": lights_in_area}
                        )
                        _LOGGER.debug("Zgaszono wszystkie światła w %s", area_id)
                    
            except Exception as err:
                _LOGGER.warning("Błąd przywracania AL dla %s: %s", area_id, err)