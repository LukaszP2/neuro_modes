# Neuro Modes – Observability & Diagnostics

## Debug log points

Włącz debug dla integracji:

- `custom_components.neuro_modes`

Kluczowe logi:

1. `coordinator.async_setup`
   - start/koniec setupu
   - liczba listenerów źródeł
2. `coordinator._handle_state_change`
   - trigger refresh po zmianie stanu encji
3. `coordinator.set_override` i `_clear_override`
   - ustawienie i timeout override
4. `coordinator._recalculate`
   - wynik: state/confidence/liczba aktywnych źródeł
5. `select.options`
   - liczba wyliczonych trybów bazowych

## Diagnostics payload (safe snapshot)

W diagnostics dostępne są:

- `entry` (data/options z redakcją pól wrażliwych)
- `runtime.summary.has_coordinator`
- `runtime.summary.active_sources_count`
- `runtime.summary.human_override`

## Suggested incident triage

1. Sprawdź, czy `has_coordinator == true`.
2. Sprawdź, czy `active_sources_count` rośnie/spada zgodnie ze stanami HA.
3. Zweryfikuj, czy `human_override` nie blokuje rekalkulacji.
4. Zweryfikuj log `Select options resolved` dla selectorów trybu bazowego.
