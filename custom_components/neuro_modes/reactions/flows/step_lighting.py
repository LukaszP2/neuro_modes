"""Step: Configure lighting behavior."""
import voluptuous as vol
from homeassistant.helpers import selector


async def async_step_lighting(flow, user_input=None):
    """Configure adaptive lighting behavior for this reaction."""
    if user_input is not None:
        # Store lighting config
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
        flow.options_data["adaptive_lighting_mode"] = user_input.get("adaptive_lighting_mode")
        flow.options_data["fallback_scene"] = user_input.get("fallback_scene")
        
        # Move to next step
        return await flow.async_step_reactions_restore()
    
    return flow.async_show_form(
        step_id="step_lighting",
        data_schema=vol.Schema({
            vol.Required("adaptive_lighting_mode", default="leave"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": "leave", "label": "Leave as is"},
                        {"value": "disable", "label": "Disable"},
                        {"value": "sleep_mode", "label": "Sleep mode"},
                    ],
                    mode="list",
                )
            ),
            vol.Optional("fallback_scene"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="scene")
            ),
        }),
        translation_key="step_lighting",
    )
