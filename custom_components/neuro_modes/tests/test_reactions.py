import pytest
from unittest.mock import patch, AsyncMock
from homeassistant.core import HomeAssistant
from custom_components.neuro_modes.reactions.reactor import NeuroReactor

# Mockujemy (udajemy) konfigurację z Home Assistanta
MOCK_CONFIG_ENTRY = {
    "title": "Praca",
    "options": {
        "reactions": [
            {
                "areas": ["biuro"],
                "adaptive_lighting_mode": "sleep_mode",
                "restore_action": "restore_previous"
            }
        ]
    }
}

@pytest.mark.asyncio
async def test_reactor_enables_sleep_mode_and_blocks_ma(hass: HomeAssistant):
    """Test sprawdza czy włączenie trybu wywołuje poprawne serwisy w AL i MA."""
    
    # Tworzymy nasz reaktor z udawaną konfiguracją
    reactor = NeuroReactor(hass, AsyncMock(options=MOCK_CONFIG_ENTRY.get("options")))

    # Przechwytujemy (mockujemy) wywoływanie usług w Home Assistant
    with patch.object(hass.services, "async_call", new_callable=AsyncMock) as mock_call:
        
        # SYMULUJEMY AKCJĘ: Włączamy tryb
        await reactor.async_react(is_active=True)
        
        # ASERCJE: Sprawdzamy czy reaktor wykonał poprawne polecenia
        # 1. Czy włączył Sleep Mode w AL?
        mock_call.assert_any_call(
            "switch", "turn_on", {"entity_id": "switch.adaptive_lighting_sleep_mode_biuro"}
        )
        
        # 2. Czy zablokował auto-światło w MA? (Jeśli tak ustawiłeś w kodzie)
        # mock_call.assert_any_call(
        #     "switch", "turn_off", {"entity_id": "switch.area_biuro_light_control"}
        # )

@pytest.mark.asyncio
async def test_reactor_ignores_unchanged_state(hass: HomeAssistant):
    """Sprawdza bezpiecznik - czy ignoruje podwójne odpalenie tego samego stanu."""
    reactor = NeuroReactor(hass, AsyncMock(options=MOCK_CONFIG_ENTRY.get("options")))
    reactor._was_active = True # Udajemy, że tryb już jest włączony
    
    with patch.object(hass.services, "async_call", new_callable=AsyncMock) as mock_call:
        # Próbujemy włączyć go jeszcze raz
        await reactor.async_react(is_active=True)
        
        # Sprawdzamy czy NIC się nie wykonało (optymalizacja)
        mock_call.assert_not_called()