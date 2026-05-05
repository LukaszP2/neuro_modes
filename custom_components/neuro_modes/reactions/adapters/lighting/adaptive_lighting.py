"""Adaptive Lighting adapter - controls AL switches per area."""
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)


class AdaptiveLightingAdapter:
    """Adapter for Adaptive Lighting integration."""

    def __init__(self, hass):
        """Initialize adapter."""
        self.hass = hass

    async def apply_state(
        self,
        area_ids: list[str],
        mode_config: dict[str, Any],
    ) -> None:
        """Apply adaptive lighting state to areas.
        
        Args:
            area_ids: List of area IDs to apply to
            mode_config: Configuration with 'adaptive_lighting_mode' and 'fallback_scene'
        """
        mode = mode_config.get("adaptive_lighting_mode", "leave")
        fallback_scene = mode_config.get("fallback_scene")

        for area_id in area_ids:
            try:
                if mode == "leave":
                    # Do nothing - leave AL as is
                    _LOGGER.debug("AL adapter: leaving %s as is", area_id)
                    
                elif mode == "disable":
                    # Disable adaptive lighting
                    switch_entity = f"switch.adaptive_lighting_{area_id}"
                    await self.hass.services.async_call(
                        "switch",
                        "turn_off",
                        {"entity_id": switch_entity},
                    )
                    _LOGGER.debug("AL adapter: disabled for %s", area_id)
                    
                elif mode == "sleep_mode":
                    # Enable sleep mode
                    switch_entity = f"switch.adaptive_lighting_sleep_mode_{area_id}"
                    await self.hass.services.async_call(
                        "switch",
                        "turn_on",
                        {"entity_id": switch_entity},
                    )
                    _LOGGER.debug("AL adapter: sleep mode enabled for %s", area_id)
                    
                # Apply fallback scene if provided
                if fallback_scene:
                    await self.hass.services.async_call(
                        "scene",
                        "turn_on",
                        {"entity_id": fallback_scene},
                    )
                    _LOGGER.debug("AL adapter: fallback scene %s applied", fallback_scene)
                    
            except Exception as err:
                _LOGGER.warning("AL adapter error for %s: %s", area_id, err)

    async def restore(self, area_ids: list[str], restore_action: str) -> None:
        """Restore lighting state when mode ends.
        
        Args:
            area_ids: List of area IDs
            restore_action: Action to perform ('restore_previous', 'turn_off_all', 'enable_al')
        """
        for area_id in area_ids:
            try:
                if restore_action == "restore_previous":
                    # Re-enable adaptive lighting
                    switch_entity = f"switch.adaptive_lighting_{area_id}"
                    await self.hass.services.async_call(
                        "switch",
                        "turn_on",
                        {"entity_id": switch_entity},
                    )
                    _LOGGER.debug("AL adapter: restored for %s", area_id)
                    
                elif restore_action == "turn_off_all":
                    # Turn off all lights
                    light_group = f"light.{area_id}"
                    await self.hass.services.async_call(
                        "light",
                        "turn_off",
                        {"entity_id": light_group},
                    )
                    _LOGGER.debug("AL adapter: turned off lights in %s", area_id)
                    
                elif restore_action == "enable_al":
                    # Enable adaptive lighting
                    switch_entity = f"switch.adaptive_lighting_{area_id}"
                    await self.hass.services.async_call(
                        "switch",
                        "turn_on",
                        {"entity_id": switch_entity},
                    )
                    _LOGGER.debug("AL adapter: AL enabled for %s", area_id)
                    
            except Exception as err:
                _LOGGER.warning("AL adapter restore error for %s: %s", area_id, err)
