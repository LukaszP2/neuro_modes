"""Smart Discovery Engine for Neuro Modes."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr

_LOGGER = logging.getLogger(__name__)

class AreaDiscovery:
    """Inteligentne wykrywanie encji na podstawie Rejestru Obszarów HA."""
    
    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    def get_entities_by_domain(self, area_id: str, domain: str) -> list[str]:
        """Pobiera wszystkie encje z danej domeny dla konkretnego obszaru (Area)."""
        ent_reg = er.async_get(self.hass)
        dev_reg = dr.async_get(self.hass)
        found_entities = []

        for entity in ent_reg.entities.values():
            ent_area = entity.area_id
            
            # Jeśli encja nie ma bezpośrednio przypisanego pokoju, sprawdźmy jej urządzenie nadrzędne
            if not ent_area and entity.device_id:
                device = dev_reg.async_get(entity.device_id)
                if device:
                    ent_area = device.area_id

            if ent_area == area_id and entity.domain == domain:
                found_entities.append(entity.entity_id)

        return found_entities

    def find_integration_switch(self, area_id: str, integration: str, switch_keyword: str) -> str | None:
        """
        Szuka przełącznika z konkretnej integracji w danym pokoju.
        Pozwala na natywne wsparcie dla innych komponentów w przyszłości.
        """
        ent_reg = er.async_get(self.hass)
        switches = self.get_entities_by_domain(area_id, "switch")
        
        for entity_id in switches:
            if switch_keyword in entity_id:
                ent = ent_reg.async_get(entity_id)
                # Sprawdzamy, czy to na pewno encja z właściwej integracji
                if ent and ent.platform == integration:
                    return entity_id
                    
        # Fallback (Plan B): Oparty na standardowym wzorcu nazewnictwa, jeśli rejestr zawiedzie
        fallback = f"switch.area_{area_id}_{switch_keyword}"
        if self.hass.states.get(fallback):
            return fallback
            
        return None