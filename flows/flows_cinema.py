import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_cinema(flow, user_input=None):
    if user_input is not None:
        sources = [{"entity_id": user_input["tv_entity"], "state": "playing", "weight": 60}]
        if "lights" in user_input:
            for light in user_input["lights"]:
                sources.append({"entity_id": light, "state": "off", "weight": 20})
        return flow.async_create_entry(title="", data={"sources": sources})
    return flow.async_show_form(step_id="template_cinema", data_schema=vol.Schema({
        vol.Required("tv_entity"): selector.EntitySelector(selector.EntitySelectorConfig(domain="media_player")),
        vol.Optional("lights"): selector.EntitySelector(selector.EntitySelectorConfig(domain="light", multiple=True))
    }))