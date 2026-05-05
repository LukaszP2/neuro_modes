"""Magic Areas adapter - controls presence tracking per area."""
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

class MagicAreasAdapter:
    """Adapter for Magic Areas integration."""

    def __init__(self, hass):
        self.hass = hass

    async def apply_state(self, area_ids: list[str], mode_config: dict[str, Any]) -> None:
        """Apply presence tracking state to areas."""
        for area_id in area_ids:
            try:
                # Szukamy przełącznika light_control tworzonego przez MA
                switch_entity = f"switch.area_{area_id}_light_control"
                
                # Jeśli tryb to wyłączenie AL, najczęściej chcemy też zablokować auto-światło z MA (np. w kinie)
                if mode_config.get("adaptive_lighting_mode") == "disable":
                    await self.hass.services.async_call(
                        "switch",
                        "turn_off",
                        {"entity_id": switch_entity},
                    )
                    _LOGGER.debug("Magic Areas: Auto-światło zablokowane dla %s", area_id)
                
            except Exception as err:
                _LOGGER.debug("Magic Areas adapter: Błąd dla %s: %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str) -> None:
        """Restore presence tracking when mode ends."""
        for area_id in area_ids:
            try:
                # Przywracamy normalne działanie MA
                switch_entity = f"switch.area_{area_id}_light_control"
                
                await self.hass.services.async_call(
                    "switch",
                    "turn_on",
                    {"entity_id": switch_entity},
                )
                _LOGGER.debug("Magic Areas: Auto-światło przywrócone dla %s", area_id)
                
            except Exception as err:
                _LOGGER.debug("Magic Areas adapter błąd przywracania %s: %s", area_id, err)