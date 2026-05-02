# Neuro Modes – Observability & Diagnostics

## Debug log points

Enable debug logging for the integration:

- `custom_components.neuro_modes`

Key debug logs:

1. `coordinator.async_setup`
   - setup start/end
   - number of registered source listeners
2. `coordinator._handle_state_change`
   - refresh trigger after source state change
3. `coordinator.set_override` and `_clear_override`
   - manual override set/timeout clear
4. `coordinator._recalculate`
   - recalculation result: state/confidence/active source count
5. `select.options`
   - resolved base mode option count

## Diagnostics payload (safe snapshot)

Diagnostics include:

- `entry` (data/options with sensitive field redaction)
- `runtime.summary.has_coordinator`
- `runtime.summary.active_sources_count`
- `runtime.summary.human_override`

## Suggested incident triage

1. Verify `has_coordinator == true`.
2. Check whether `active_sources_count` changes as HA entity states change.
3. Verify `human_override` is not blocking recalculation.
4. Check `Select options resolved` logs for base mode selector refresh.
