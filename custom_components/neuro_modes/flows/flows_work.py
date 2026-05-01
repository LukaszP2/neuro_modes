import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_work(flow, user_input=None):
    errors = {}
    if user_input is not None:
        sources = []
        # Punkty dodatnie za osoby pracujące (wielokrotny wybór)
        for worker in user_input["workers"]:
            sources.append({"entity_id": worker, "state": "home", "weight": 30})
            
        # Punkty dodatnie za zużycie energii lub status Teams (wielokrotny wybór)
        if "activity_sensors" in user_input:
            for sensor in user_input["activity_sensors"]:
                sources.append({"entity_id": sensor, "state": "on", "weight": 40}) # np. pobór > 50W można ustawić potem
                
        # Punkty ujemne za innych domowników (kill-switch)
        if "disruptors" in user_input:
            for person in user_input["disruptors"]:
                sources.append({"entity_id": person, "state": "home", "weight": -100})
                
        # (Czas zrobimy na razie jako zmienne pomocnicze lub instrukcję, bo Neuro ocenia stany, a nie zegarki)
        return flow.async_create_entry(title="", data={"sources": sources})

    return flow.async_show_form(
        step_id="template_work",
        errors=errors,
        data_schema=vol.Schema({
            vol.Required("workers"): selector.EntitySelector(selector.EntitySelectorConfig(domain="person", multiple=True)),
            vol.Optional("activity_sensors"): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True)),
            vol.Optional("disruptors"): selector.EntitySelector(selector.EntitySelectorConfig(domain="person", multiple=True)),
        })
    )