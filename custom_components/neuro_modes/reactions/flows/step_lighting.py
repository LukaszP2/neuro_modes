"""Step: Configure lighting behavior."""
import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_lighting(flow, user_input=None):
    """Configure adaptive lighting behavior for this reaction."""
    if user_input is not None:
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
        flow.options_data["adaptive_lighting_mode"] = user_input.get("adaptive_lighting_mode")
        flow.options_data["fallback_scene"] = user_input.get("fallback_scene")
        
        return await flow.async_step_reactions_restore()
    
    # Wczytywanie domyślnych (przy edycji)
    default_al = flow.options_data.get("adaptive_lighting_mode", "leave") if hasattr(flow, "options_data") else "leave"
    default_scene = flow.options_data.get("fallback_scene") if hasattr(flow, "options_data") else None

    schema = {
        vol.Required("adaptive_lighting_mode", default=default_al): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": "leave", "label": "Zostaw bez zmian"},
                    {"value": "disable", "label": "Wyłącz Adaptive Lighting (AL)"},
                    {"value": "sleep_mode", "label": "Wymuś w AL tryb Nocny (Sleep Mode)"},
                ],
                mode="list",
            )
        ),
    }
    
    # Warunkowe dodawanie domyślnej sceny, jeśli istnieje
    if default_scene:
        schema[vol.Optional("fallback_scene", default=default_scene)] = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="scene")
        )
    else:
        schema[vol.Optional("fallback_scene")] = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="scene")
        )

    return flow.async_show_form(
        step_id="reactions_lighting",
        data_schema=vol.Schema(schema),
    )