"""NeuroReactor - central dispatcher for reactions with Scope Override logic."""
import logging
from typing import Any
from homeassistant.core import HomeAssistant

# Importujemy nasze adaptery
from .adapters.lighting.adaptive_lighting import AdaptiveLightingAdapter
from .adapters.presence.magic_areas import MagicAreasAdapter

_LOGGER = logging.getLogger(__name__)

class NeuroReactor:
    """Central dispatcher for reactions."""

    def __init__(self, hass: HomeAssistant, entry):
        """Inicjalizacja reaktora dla danego trybu."""
        self.hass = hass
        self.entry = entry
        
        # Inicjalizacja "rąk" wykonawczych
        self.lighting_adapter = AdaptiveLightingAdapter(hass)
        self.presence_adapter = MagicAreasAdapter(hass)
        
        # Pamiętamy poprzedni stan, żeby nie strzelać komendami co 30 sekund bez potrzeby
        self._was_active = False

    async def async_react(self, is_active: bool) -> None:
        """Główna funkcja wywoływana przez Koordynator przy każdej aktualizacji."""
        # Jeśli stan się nie zmienił, nie robimy nic
        if is_active == self._was_active:
            return

        self._was_active = is_active
        reactions_config = list(self.entry.options.get("reactions", []))

        if not reactions_config:
            return # Tryb nie ma ustawionych żadnych reakcji

        if is_active:
            _LOGGER.info("NeuroReactor: Tryb '%s' WŁĄCZONY. Aplikuję %s reakcji.", self.entry.title, len(reactions_config))
            await self._apply_reactions(reactions_config)
        else:
            _LOGGER.info("NeuroReactor: Tryb '%s' WYŁĄCZONY. Przywracam stany.", self.entry.title)
            await self._restore_reactions(reactions_config)

    async def _apply_reactions(self, reactions: list[dict[str, Any]]) -> None:
        """Aplikuje maski dla wszystkich zdefiniowanych reakcji."""
        for reaction in reactions:
            areas = reaction.get("areas", [])
            if not areas:
                continue
            
            # Odpalamy adaptery dla wybranych stref
            await self.lighting_adapter.apply_state(areas, reaction)
            await self.presence_adapter.apply_state(areas, reaction)

    async def _restore_reactions(self, reactions: list[dict[str, Any]]) -> None:
        """Cofa zmiany (przywraca tło) po zakończeniu trybu."""
        for reaction in reactions:
            areas = reaction.get("areas", [])
            restore_action = reaction.get("restore_action", "restore_previous")
            if not areas:
                continue
            
            await self.lighting_adapter.restore(areas, restore_action)
            await self.presence_adapter.restore(areas, restore_action)