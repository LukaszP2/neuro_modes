"""Step: Configure restore behavior when mode ends."""
import voluptuous as vol
from homeassistant.helpers import selector


async def async_step_restore(flow, user_input=None):
    """Configure what happens when this reaction mode ends."""
    if user_input is not None:
        # Store restore config
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
        flow.options_data["restore_action"] = user_input.get("restore_action")
        
        # Create entry with all collected data
        return flow.async_create_entry(
            title="Reaction",
            data=flow.options_data,
        )
    
    return flow.async_show_form(
        step_id="step_restore",
        data_schema=vol.Schema({
            vol.Required("restore_action", default="restore_previous"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": "restore_previous", "label": "Restore previous state"},
                        {"value": "turn_off_all", "label": "Turn off all"},
                        {"value": "enable_al", "label": "Enable adaptive lighting"},
                    ],
                    mode="list",
                )
            ),
        }),
        translation_key="step_restore",
    )
