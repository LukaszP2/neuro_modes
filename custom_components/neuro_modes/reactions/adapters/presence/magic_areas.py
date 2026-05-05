"""Magic Areas adapter - controls presence tracking per area with Smart Search."""
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

class MagicAreasAdapter:
    """Adapter for Magic Areas integration."""

    def __init__(self, hass):
        self.hass = hass

    def _find_entity(self, area_id: str) -> str | None:
        """Inteligentne wyszukiwanie encji MA (light_control)."""
        all_switches = self.hass.states.async_entity_ids("switch")
        
        for entity_id in all_switches:
            if area_id in entity_id and "light_control" in entity_id:
                return entity_id
        return None

    async def apply_state(self, area_ids: list[str], mode_config: dict[str, Any]) -> None:
        for area_id in area_ids:
            try:
                entity = self._find_entity(area_id)
                # Blokujemy auto-światło tylko gdy kazano nam wyłączyć AL
                if entity and mode_config.get("adaptive_lighting_mode") == "disable":
                    await self.hass.services.async_call("switch", "turn_off", {"entity_id": entity})
                    _LOGGER.debug("Magic Areas: Auto-światło zablokowane dla %s (%s)", area_id, entity)
            except Exception as err:
                _LOGGER.debug("Błąd MA adaptera dla %s: %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str) -> None:
        for area_id in area_ids:
            try:
                entity = self._find_entity(area_id)
                if entity:
                    await self.hass.services.async_call("switch", "turn_on", {"entity_id": entity})
                    _LOGGER.debug("Magic Areas: Auto-światło przywrócone dla %s (%s)", area_id, entity)
            except Exception as err:
                _LOGGER.debug("Błąd MA adaptera przywracania %s: %s", area_id, err)