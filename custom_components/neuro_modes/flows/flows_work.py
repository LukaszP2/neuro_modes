import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_work(flow, user_input=None):
    errors = {}
    
    # 1. Sprawdzamy czy domyślny sensor Workday jest zainstalowany w HA
    default_workday = "binary_sensor.workday_sensor"
    has_workday = flow.hass.states.get(default_workday) is not None

    if user_input is not None:
        sources = []
        
        # Punkty za dzień roboczy (jeśli użytkownik wybrał sensor)
        if "workday_sensor" in user_input:
            sources.append({"entity_id": user_input["workday_sensor"], "state": "on", "weight": 20})

        # Punkty dodatnie za osoby pracujące (wielokrotny wybór)
        for worker in user_input["workers"]:
            sources.append({"entity_id": worker, "state": "home", "weight": 30})
            
        # Punkty dodatnie za zużycie energii lub status Teams (wielokrotny wybór)
        if "activity_sensors" in user_input:
            for sensor in user_input["activity_sensors"]:
                sources.append({"entity_id": sensor, "state": "on", "weight": 40}) 
                
        # Punkty ujemne za innych domowników (kill-switch)
        if "disruptors" in user_input:
            for person in user_input["disruptors"]:
                sources.append({"entity_id": person, "state": "home", "weight": -100})
                
        # Zapisujemy wszystko do konfiguracji wraz z zakresem czasu
        return flow.async_create_entry(
            title="", 
            data={
                "sources": sources,
                "work_start_time": user_input["work_start_time"],
                "work_end_time": user_input["work_end_time"]
            }
        )

    # 2. Budujemy dynamiczny schemat formularza
    schema = {
        vol.Required("workers"): selector.EntitySelector(selector.EntitySelectorConfig(domain="person", multiple=True)),
    }
    
    # Podpowiadamy Workday jeśli istnieje, w przeciwnym razie zostawiamy puste pole
    if has_workday:
        schema[vol.Optional("workday_sensor", default=default_workday)] = selector.EntitySelector(selector.EntitySelectorConfig(domain="binary_sensor"))
    else:
        schema[vol.Optional("workday_sensor")] = selector.EntitySelector(selector.EntitySelectorConfig(domain="binary_sensor"))
        
    schema.update({
        vol.Optional("activity_sensors"): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True)),
        vol.Optional("disruptors"): selector.EntitySelector(selector.EntitySelectorConfig(domain="person", multiple=True)),
        # Wybór okna czasowego z domyślnymi wartościami (zapisane w formacie HH:MM:SS)
        vol.Required("work_start_time", default="07:00:00"): selector.TimeSelector(),
        vol.Required("work_end_time", default="17:00:00"): selector.TimeSelector(),
    })

    # 3. Informacja o braku Workday wyświetlana przez placeholdery
    workday_info = "" if has_workday else "\n\n💡 **Sugestia:** Nie wykryto integracji 'Workday'. Zainstaluj ją w Home Assistant, aby system automatycznie rozróżniał dni robocze od weekendów i świąt."

    return flow.async_show_form(
        step_id="template_work",
        errors=errors,
        data_schema=vol.Schema(schema),
        description_placeholders={"workday_info": workday_info}
    )