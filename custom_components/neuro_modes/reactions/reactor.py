"""NeuroReactor - central dispatcher for reactions with Scope Override logic."""
import logging
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event

from .adapters.lighting.adaptive_lighting import AdaptiveLightingAdapter
from .adapters.presence.magic_areas import MagicAreasAdapter

_LOGGER = logging.getLogger(__name__)


class NeuroReactor:
    """Central dispatcher for reactions - implements Scope Override logic.
    
    Scope Override Logic:
    - Global (Macro): Home state determined by calculator (Home, Away, Cinema, etc.)
    - Local (Micro): Room-specific overrides for specific areas
    
    When a mode is active:
    1. Determine Global state from calculator
    2. For each configured reaction (Micro-Mode):
       - If active and has areas: apply reaction to those areas (override)
       - If not active: apply default behavior to those areas
    """

    def __init__(self, hass: HomeAssistant, entry):
        """Initialize reactor.
        
        Args:
            hass: Home Assistant instance
            entry: Config entry for this mode
        """
        self.hass = hass
        self.entry = entry
        self._unsub_listeners = []
        
        # Initialize adapters
        self.lighting_adapter = AdaptiveLightingAdapter(hass)
        self.presence_adapter = MagicAreasAdapter(hass)
        
        # Store active reactions
        self.active_reactions: dict[str, dict[str, Any]] = {}

    async def async_setup(self) -> None:
        """Setup reactor - register listeners."""
        # Listen for mode state changes from calculator
        mode_name = self.entry.data.get("name")
        if mode_name:
            # Listen to coordinator data changes
            _LOGGER.debug("Reactor setup for mode: %s", mode_name)

    @callback
    def _on_mode_state_change(self, event) -> None:
        """Handle mode state change from calculator."""
        # This will be called when coordinator updates
        # Dispatch reactions based on new state
        pass

    async def apply_reactions(
        self,
        global_state: bool,
        reactions_config: list[dict[str, Any]],
    ) -> None:
        """Apply reactions based on global state and local overrides.
        
        Args:
            global_state: Global home state (True = active, False = inactive)
            reactions_config: List of reaction configurations
        """
        for reaction in reactions_config:
            areas = reaction.get("areas", [])
            if not areas:
                continue

            try:
                # Apply lighting reactions
                await self.lighting_adapter.apply_state(areas, reaction)
                
                # Apply presence reactions
                await self.presence_adapter.apply_state(areas, reaction)
                
                # Store as active
                self.active_reactions[reaction.get("id", "")] = reaction
                
                _LOGGER.debug(
                    "Reactor: applied reaction to areas %s",
                    areas,
                )
            except Exception as err:
                _LOGGER.error("Reactor error applying reaction: %s", err)

    async def restore_reactions(
        self,
        reactions_config: list[dict[str, Any]],
    ) -> None:
        """Restore state when mode ends.
        
        Args:
            reactions_config: List of reaction configurations
        """
        for reaction in reactions_config:
            areas = reaction.get("areas", [])
            restore_action = reaction.get("restore_action", "restore_previous")
            
            if not areas:
                continue

            try:
                # Restore lighting
                await self.lighting_adapter.restore(areas, restore_action)
                
                # Restore presence
                await self.presence_adapter.restore(areas, restore_action)
                
                # Remove from active
                self.active_reactions.pop(reaction.get("id", ""), None)
                
                _LOGGER.debug(
                    "Reactor: restored areas %s with action %s",
                    areas,
                    restore_action,
                )
            except Exception as err:
                _LOGGER.error("Reactor error restoring reaction: %s", err)

    async def async_unload(self) -> None:
        """Cleanup reactor."""
        for unsub in self._unsub_listeners:
            unsub()
        self._unsub_listeners.clear()
        _LOGGER.debug("Reactor unloaded")
