"""Magic Areas adapter - controls presence tracking per area."""
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)


class MagicAreasAdapter:
    """Adapter for Magic Areas integration."""

    def __init__(self, hass):
        """Initialize adapter."""
        self.hass = hass

    async def apply_state(
        self,
        area_ids: list[str],
        mode_config: dict[str, Any],
    ) -> None:
        """Apply presence tracking state to areas.
        
        Args:
            area_ids: List of area IDs to apply to
            mode_config: Configuration dict
        """
        for area_id in area_ids:
            try:
                # Check if Magic Areas integration is available
                if "magic_areas" not in self.hass.data:
                    _LOGGER.debug("Magic Areas not available, skipping %s", area_id)
                    continue

                # Disable presence tracking for this area
                # This prevents false positives during specific modes (e.g., Cinema)
                presence_entity = f"binary_sensor.{area_id}_presence"
                
                # Try to disable the presence sensor
                await self.hass.services.async_call(
                    "homeassistant",
                    "turn_off",
                    {"entity_id": presence_entity},
                )
                _LOGGER.debug("Magic Areas: presence disabled for %s", area_id)
                
            except Exception as err:
                _LOGGER.debug("Magic Areas adapter: %s not available or error: %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str) -> None:
        """Restore presence tracking when mode ends.
        
        Args:
            area_ids: List of area IDs
            restore_action: Action to perform
        """
        for area_id in area_ids:
            try:
                # Re-enable presence tracking
                presence_entity = f"binary_sensor.{area_id}_presence"
                
                await self.hass.services.async_call(
                    "homeassistant",
                    "turn_on",
                    {"entity_id": presence_entity},
                )
                _LOGGER.debug("Magic Areas: presence restored for %s", area_id)
                
            except Exception as err:
                _LOGGER.debug("Magic Areas adapter restore error for %s: %s", area_id, err)
