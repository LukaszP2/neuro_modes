"""Reactions flow implementations."""
import voluptuous as vol
from homeassistant.helpers import selector

def _get_reaction_label(idx, reaction):
    """Pomocnicza funkcja do formatowania etykiet (bez [1] [2])."""
    areas = reaction.get("areas", [])
    if isinstance(areas, str):
        areas = [areas]
    areas_str = ", ".join(areas) if areas else "Brak przypisanych stref"
    
    al_mode = reaction.get("adaptive_lighting_mode", "leave")
    al_labels = {"leave": "Bez zmian", "disable": "Wyłącz AL", "sleep_mode": "AL Nocny"}
    
    return f"Pokoje: {areas_str} | Ośw: {al_labels.get(al_mode, al_mode)}"

async def async_step_pick_reaction_for_edit(flow, user_input=None):
    """Pick reaction to edit."""
    reactions = list(flow._entry.options.get("reactions", []))

    if not reactions:
        return flow.async_abort(reason="not_implemented_yet") # Docelowo błąd "Brak reakcji"

    if user_input is not None:
        idx = int(user_input["selected_reaction"])
        flow.options_data = dict(reactions[idx])
        flow.edit_reaction_index = idx
        return await flow.async_step_reactions_scope()

    options = [{"value": str(idx), "label": _get_reaction_label(idx, r)} for idx, r in enumerate(reactions)]

    return flow.async_show_form(
        step_id="pick_reaction_for_edit",
        data_schema=vol.Schema({
            vol.Required("selected_reaction"): selector.SelectSelector(
                selector.SelectSelectorConfig(options=options, mode="list")
            )
        }),
    )

async def async_step_pick_reaction_for_delete(flow, user_input=None):
    """Krok 1: Wybór reakcji do usunięcia."""
    reactions = list(flow._entry.options.get("reactions", []))

    if not reactions:
        return flow.async_abort(reason="not_implemented_yet")

    if user_input is not None:
        flow.delete_reaction_index = int(user_input["selected_reaction"])
        # Przechodzimy do kroku potwierdzenia
        return await flow.async_step_delete_reaction_action()

    options = [{"value": str(idx), "label": _get_reaction_label(idx, r)} for idx, r in enumerate(reactions)]

    return flow.async_show_form(
        step_id="pick_reaction_for_delete",
        data_schema=vol.Schema({
            vol.Required("selected_reaction"): selector.SelectSelector(
                selector.SelectSelectorConfig(options=options, mode="list")
            )
        }),
    )

async def async_step_delete_reaction_action(flow, user_input=None):
    """Krok 2: Potwierdzenie usunięcia reakcji."""
    if user_input is not None:
        if user_input.get("confirm"):
            current_options = dict(flow._entry.options)
            reactions = list(current_options.get("reactions", []))
            
            if hasattr(flow, "delete_reaction_index"):
                reactions.pop(flow.delete_reaction_index)
                
            current_options["reactions"] = reactions
            return flow.async_create_entry(title="", data=current_options)
        else:
            # Użytkownik nie zaznaczył checkboxa - wracamy do menu
            return await flow.async_step_manage_reactions()

    # Pobieramy ładną etykietę do wyświetlenia w komunikacie
    idx = flow.delete_reaction_index
    reactions = list(flow._entry.options.get("reactions", []))
    reaction_label = _get_reaction_label(idx, reactions[idx])

    return flow.async_show_form(
        step_id="delete_reaction_action",
        description_placeholders={"reaction": reaction_label},
        data_schema=vol.Schema({
            vol.Required("confirm", default=False): selector.BooleanSelector()
        }),
    )

async def async_step_select_reaction_template(flow, user_input=None):
    return flow.async_show_menu(
        step_id="select_reaction_template",
        menu_options=["reaction_template_cinema", "manage_reactions"]
    )

async def async_step_reaction_template_cinema(flow, user_input=None):
    if user_input is not None:
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
            
        areas = user_input.get("areas", [])
        if isinstance(areas, str):
            areas = [areas]
            
        flow.options_data["areas"] = areas
        flow.options_data["adaptive_lighting_mode"] = "disable"
        flow.options_data["fallback_scene"] = None
        flow.options_data["restore_action"] = "restore_previous"
        
        current_options = dict(flow._entry.options)
        reactions = list(current_options.get("reactions", []))
        reactions.append(flow.options_data)
        current_options["reactions"] = reactions
        
        return flow.async_create_entry(title="", data=current_options)

    return flow.async_show_form(
        step_id="reaction_template_cinema",
        data_schema=vol.Schema({
            vol.Required("areas", default=[]): selector.AreaSelector(
                selector.AreaSelectorConfig(multiple=True)
            ),
        }),
    )