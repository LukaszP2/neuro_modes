import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_manage_sources(flow, user_input=None):
    return flow.async_show_menu(
        step_id="manage_sources",
        menu_options=["add_source", "pick_source_for_edit", "pick_source_for_delete", "init"]
    )


async def async_step_pick_source_for_edit(flow, user_input=None):
    sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))

    if not sources:
        return flow.async_abort(reason="no_sources")

    if user_input is not None:
        flow._selected_source_id = user_input["selected_source"]
        return await flow.async_step_edit_source_form()

    options = []
    for src in sources:
        entity_id = src["entity_id"]
        state_obj = flow.hass.states.get(entity_id)
        if state_obj and state_obj.attributes.get("friendly_name"):
            friendly_name = state_obj.attributes.get("friendly_name")
        else:
            friendly_name = entity_id

        options.append({"value": entity_id, "label": f"{friendly_name} ({entity_id})"})

    return flow.async_show_form(
        step_id="pick_source_for_edit",
        data_schema=vol.Schema(
            {
                vol.Required("selected_source"): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=options, mode="list")
                )
            }
        ),
    )


async def async_step_pick_source_for_delete(flow, user_input=None):
    sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))

    if not sources:
        return flow.async_abort(reason="no_sources")

    if user_input is not None:
        flow._selected_source_id = user_input["selected_source"]
        return await flow.async_step_delete_source_action()

    options = []
    for src in sources:
        entity_id = src["entity_id"]
        state_obj = flow.hass.states.get(entity_id)
        if state_obj and state_obj.attributes.get("friendly_name"):
            friendly_name = state_obj.attributes.get("friendly_name")
        else:
            friendly_name = entity_id

        options.append({"value": entity_id, "label": f"{friendly_name} ({entity_id})"})

    return flow.async_show_form(
        step_id="pick_source_for_delete",
        data_schema=vol.Schema(
            {
                vol.Required("selected_source"): selector.SelectSelector(
                    selector.SelectSelectorConfig(options=options, mode="list")
                )
            }
        ),
    )

async def async_step_edit_source_menu(flow, user_input=None):
    
    state_obj = flow.hass.states.get(flow._selected_source_id)
    friendly_name = state_obj.attributes.get("friendly_name") if state_obj and state_obj.attributes.get("friendly_name") else flow._selected_source_id

    return flow.async_show_menu(
        step_id="edit_source_menu",
        menu_options=["edit_source_form", "delete_source_action", "manage_sources"],
        description_placeholders={"source": f"{friendly_name} ({flow._selected_source_id})"}
    )

async def async_step_delete_source_action(flow, user_input=None):
    """Ekran bezpiecznika: Potwierdzenie usunięcia poszlaki."""
    if user_input is not None:
        if user_input["confirm"]:

            sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))
            sources = [s for s in sources if s["entity_id"] != flow._selected_source_id]
            return flow.async_create_entry(title="", data={"sources": sources})
        else:

            return await async_step_edit_source_menu(flow)

    state_obj = flow.hass.states.get(flow._selected_source_id)
    friendly_name = state_obj.attributes.get("friendly_name") if state_obj and state_obj.attributes.get("friendly_name") else flow._selected_source_id

    return flow.async_show_form(
        step_id="delete_source_action",
        description_placeholders={"source": f"{friendly_name} ({flow._selected_source_id})"},
        data_schema=vol.Schema({
            vol.Required("confirm", default=False): selector.BooleanSelector()
        })
    )

async def async_step_edit_source_form(flow, user_input=None):
    """Formularz edycji konkretnej poszlaki."""
    sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))

    current_source = next((s for s in sources if s["entity_id"] == flow._selected_source_id), {})
    
    if user_input is not None:
        for i, s in enumerate(sources):
            if s["entity_id"] == flow._selected_source_id:
                sources[i] = {
                    "entity_id": flow._selected_source_id,
                    "state": user_input["state"],
                    "weight": user_input["weight"]
                }
                break
        return flow.async_create_entry(title="", data={"sources": sources})

    state_obj = flow.hass.states.get(flow._selected_source_id)
    friendly_name = state_obj.attributes.get("friendly_name") if state_obj and state_obj.attributes.get("friendly_name") else flow._selected_source_id

    return flow.async_show_form(
        step_id="edit_source_form",
        description_placeholders={"source": f"{friendly_name} ({flow._selected_source_id})"},
        data_schema=vol.Schema({
            vol.Required("state", default=current_source.get("state", "on")): str,
            vol.Required("weight", default=current_source.get("weight", 30)): int,
        })
    )

async def async_step_add_source(flow, user_input=None):
    """Krok dodawania nowej poszlaki."""
    if user_input is not None:
        sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))
        sources.append(user_input)
        return flow.async_create_entry(title="", data={"sources": sources})

    return flow.async_show_form(
        step_id="add_source",
        data_schema=vol.Schema({
            vol.Required("entity_id"): selector.EntitySelector(),
            vol.Required("state", default="on"): str,
            vol.Required("weight", default=30): int,
        })
    )