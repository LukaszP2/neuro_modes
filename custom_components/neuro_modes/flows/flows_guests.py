import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_guests(flow, user_input=None):
    """Kreator trybu Goście."""
    if user_input is not None:
        sources = [
            {"entity_id": user_input["guest_wifi"], "state": "on", "weight": 50},
        ]
        for area in user_input["public_areas"]:
            sources.append({"entity_id": area, "state": "on", "weight": 25})
            
        return flow.async_create_entry(title="", data={"sources": sources})

    return flow.async_show_form(
        step_id="template_guests",
        data_schema=vol.Schema({
            vol.Required("guest_wifi"): selector.EntitySelector(),
            vol.Required("public_areas"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="binary_sensor", multiple=True)
            ),
        })
    )