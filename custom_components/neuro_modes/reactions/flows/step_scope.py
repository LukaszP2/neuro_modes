"""Step: Configure reaction scope (areas)."""
import voluptuous as vol
from homeassistant.helpers import selector


async def async_step_scope(flow, user_input=None):
    """Configure which areas this reaction applies to."""
    if user_input is not None:
        # Store scope in intermediate data
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
        flow.options_data["areas"] = user_input.get("areas", [])
        
        # Move to next step
        return await flow.async_step_reactions_lighting()
    
    return flow.async_show_form(
        step_id="step_scope",
        data_schema=vol.Schema({
            vol.Required("areas", default=[]): selector.AreaSelector(),
        }),
        translation_key="step_scope",
    )
