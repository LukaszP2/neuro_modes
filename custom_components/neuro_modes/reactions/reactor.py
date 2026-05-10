"""Core Neuro Reactor - The Engine."""
import logging
from homeassistant.core import HomeAssistant
from .adapters.lighting.adaptive_lighting import AdaptiveLightingAdapter
from .adapters.presence.magic_areas import MagicAreasAdapter

_LOGGER = logging.getLogger(__name__)

class NeuroReactor:
    """Mózg wykonawczy Neuro Modes - deleguje zadania do adapterów."""
    
    def __init__(self, hass: HomeAssistant, config_entry):
        self.hass = hass
        self.config_entry = config_entry
        self.options = config_entry.options
        
        # Wczytanie wtyczek (Adapterów)
        self.ma_adapter = MagicAreasAdapter(hass)
        self.al_adapter = AdaptiveLightingAdapter(hass)
        
        self._was_active = False

    async def async_react(self, is_active: bool) -> None:
        """Główny punkt wejścia. Uruchamiany, gdy koordynator zmienia stan trybu."""
        if is_active == self._was_active:
            return  # Zabezpieczenie przed podwójnym odpaleniem (Idempotentność)
        
        self._was_active = is_active
        mode_name = self.config_entry.title
        reactions_config = self.options.get("reactions", [])
        
        if is_active:
            _LOGGER.info("🧠 NeuroReactor: Start wykonywania reakcji dla '%s'", mode_name)
            for reaction in reactions_config:
                areas = reaction.get("areas", [])
                if not areas:
                    continue
                    
                # 1. Odpalamy Magic Areas
                await self.ma_adapter.apply_state(areas, reaction, mode_name)
                
                # 2. Odpalamy Adaptive Lighting
                await self.al_adapter.apply_state(areas, reaction, mode_name)
                
                # 3. Opcjonalne uruchomienie fizycznej Sceny (Zawsze na końcu)
                fallback_scene = reaction.get("fallback_scene")
                if fallback_scene:
                    await self.hass.services.async_call("scene", "turn_on", {"entity_id": fallback_scene})
                    _LOGGER.debug("🎬 Wywołano scenę: %s", fallback_scene)
                    
        else:
            _LOGGER.info("🧠 NeuroReactor: Wygaszanie reakcji i przywracanie domu dla '%s'", mode_name)
            for reaction in reactions_config:
                areas = reaction.get("areas", [])
                if not areas:
                    continue
                    
                restore_action = reaction.get("restore_action", "restore_previous")
                
                # Przywracamy systemy do domyślnego stanu
                await self.ma_adapter.restore(areas, restore_action, mode_name)
                await self.al_adapter.restore(areas, restore_action, mode_name)