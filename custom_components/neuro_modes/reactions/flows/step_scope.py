"""Step: Configure reaction scope (areas)."""
import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_scope(flow, user_input=None):
    """Configure which areas this reaction applies to."""
    if user_input is not None:
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
            
        areas = user_input.get("areas", [])
        # Wymuszamy listę, nawet jeśli HA zwróci pojedynczy string
        if isinstance(areas, str):
            areas = [areas]
            
        flow.options_data["areas"] = areas
        
        return await flow.async_step_reactions_lighting()
    
    # Bezpieczne wczytywanie domyślnych wartości (dla trybu edycji)
    default_areas = flow.options_data.get("areas", []) if hasattr(flow, "options_data") else []
    if isinstance(default_areas, str):
        default_areas = [default_areas]

    return flow.async_show_form(
        step_id="reactions_scope",
        data_schema=vol.Schema({
            vol.Required("areas", default=default_areas): selector.AreaSelector(
                selector.AreaSelectorConfig(multiple=True)
            ),
        }),
    )