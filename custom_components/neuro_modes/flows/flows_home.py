import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_home(flow, user_input=None):
    if user_input is not None:
        sources = [{"entity_id": user_input["home_zone"], "state": "> 0", "weight": 80}]
        return flow.async_create_entry(title="", data={"sources": sources})
    return flow.async_show_form(step_id="template_home", data_schema=vol.Schema({
        vol.Required("home_zone", default="zone.home"): selector.EntitySelector(selector.EntitySelectorConfig(domain="zone"))
    }))