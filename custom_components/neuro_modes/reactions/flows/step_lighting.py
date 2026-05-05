"""Step: Configure lighting behavior with dependency checking."""
import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_lighting(flow, user_input=None):
    """Configure lighting behavior based on available integrations."""
    
    # --- SPRAWDZANIE ZALEŻNOŚCI ---
    has_al = "adaptive_lighting" in flow.hass.data

    if user_input is not None:
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
            
        if has_al:
            flow.options_data["adaptive_lighting_mode"] = user_input.get("adaptive_lighting_mode")
        else:
            # Dla osób bez AL zapisujemy surowe światła
            flow.options_data["adaptive_lighting_mode"] = "not_installed"
            flow.options_data["raw_lights_off"] = user_input.get("raw_lights_off", [])
            
        flow.options_data["fallback_scene"] = user_input.get("fallback_scene")
        
        return await flow.async_step_reactions_restore()
    
    # Wczytywanie domyślnych (przy edycji)
    default_scene = flow.options_data.get("fallback_scene") if hasattr(flow, "options_data") else None

    # --- WARIANT 1: UŻYTKOWNIK MA ADAPTIVE LIGHTING ---
    if has_al:
        default_al = flow.options_data.get("adaptive_lighting_mode", "leave") if hasattr(flow, "options_data") else "leave"
        
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
        description = "Wykryto integrację Adaptive Lighting. Jak chcesz nią sterować w tym trybie?"
        
    # --- WARIANT 2: UŻYTKOWNIK NIE MA ADAPTIVE LIGHTING ---
    else:
        default_lights = flow.options_data.get("raw_lights_off", []) if hasattr(flow, "options_data") else []
        if isinstance(default_lights, str):
            default_lights = [default_lights]
            
        schema = {
            vol.Optional("raw_lights_off", default=default_lights): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="light", multiple=True)
            ),
        }
        description = "Nie wykryto Adaptive Lighting. Możesz wskazać konkretne światła, które mają zostać zgaszone w tym trybie (np. w trybie Kinowym)."

    # Wspólne pole dla obu wariantów (Scena)
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
        description_placeholders={"info": description},
        data_schema=vol.Schema(schema),
    )