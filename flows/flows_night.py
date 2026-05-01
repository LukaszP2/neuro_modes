import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_night(flow, user_input=None):
    if user_input is not None:
        sources = [{"entity_id": user_input["sun_entity"], "state": "below_horizon", "weight": 40}]
        if "chargers" in user_input:
            for charger in user_input["chargers"]:
                sources.append({"entity_id": charger, "state": "charging", "weight": 30})
        return flow.async_create_entry(title="", data={"sources": sources})
    return flow.async_show_form(step_id="template_night", data_schema=vol.Schema({
        vol.Required("sun_entity", default="sun.sun"): selector.EntitySelector(selector.EntitySelectorConfig(domain="sun")),
        vol.Optional("chargers"): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True))
    }))