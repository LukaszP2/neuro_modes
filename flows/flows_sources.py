import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_manage_sources(flow, user_input=None):
    """Główna lista poszlak (Wstecz na samym dole)."""
    sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))
    
    if user_input is not None:
        if user_input["selected_source"] == "BACK":
            return await flow.async_step_init()
        if user_input["selected_source"] == "ADD_NEW":
            return await flow.async_step_add_source()
            
        flow._selected_source_id = user_input["selected_source"]
        return await flow.async_step_edit_source_menu()

    options = [{"value": "ADD_NEW", "label": "➕ Dodaj nową poszlakę"}]
    
    # Renderowanie dynamicznej listy encji
    for src in sources:
        entity_id = src["entity_id"]
        weight = src["weight"]
        state_obj = flow.hass.states.get(entity_id)
        
        if state_obj and state_obj.attributes.get("friendly_name"):
            friendly_name = state_obj.attributes.get("friendly_name")
        else:
            friendly_name = entity_id
            
        options.append({"value": entity_id, "label": f"{friendly_name} ({entity_id}) - {weight} pkt"})

    # MAGIA: Przycisk Wstecz na samym końcu listy
    options.append({"value": "BACK", "label": "⬅️ Wstecz (Powrót do menu)"})

    return flow.async_show_form(
        step_id="manage_sources",
        data_schema=vol.Schema({
            vol.Required("selected_source", default="ADD_NEW"): selector.SelectSelector(
                selector.SelectSelectorConfig(options=options, mode="list")
            )
        })
    )

async def async_step_edit_source_menu(flow, user_input=None):
    """Prawdziwe, klikalne menu dla wybranej poszlaki z przyjazną nazwą w nagłówku."""
    
    # Pobieranie Friendly Name dla nagłówka
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
        if user_input["confirm"] == "yes":
            # Potwierdzono - usuwamy
            sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))
            sources = [s for s in sources if s["entity_id"] != flow._selected_source_id]
            return flow.async_create_entry(title="", data={"sources": sources})
        else:
            # Anulowano - wracamy do menu
            return await async_step_edit_source_menu(flow)

    # Pobieramy nazwę, żeby wstawić ją w komunikat
    state_obj = flow.hass.states.get(flow._selected_source_id)
    friendly_name = state_obj.attributes.get("friendly_name") if state_obj and state_obj.attributes.get("friendly_name") else flow._selected_source_id

    return flow.async_show_form(
        step_id="delete_source_action",
        description_placeholders={"source": f"{friendly_name} ({flow._selected_source_id})"},
        data_schema=vol.Schema({
            vol.Required("confirm", default="no"): selector.SelectSelector(
                selector.SelectSelectorConfig(options=[
                    {"value": "yes", "label": "✅ TAK, usuń poszlakę"},
                    {"value": "no", "label": "❌ NIE, wracam do menu"}
                ], mode="list")
            )
        })
    )

async def async_step_edit_source_form(flow, user_input=None):
    """Formularz edycji konkretnej poszlaki."""
    sources = list(flow._entry.options.get("sources", flow._entry.data.get("sources", [])))
    # Szukamy obecnych danych wybranej poszlaki
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

    # Ładny nagłówek z Friendly Name
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