# Changelog

## Unreleased

- Unified entity state reads to `coordinator.data` (sensor/switch/binary_sensor).
- Switched base mode select to event-driven updates (`_attr_should_poll = False`).
- Added regression coverage for selector non-polling behavior.
- Fixed base mode selector refresh after mode removal (immediate + delayed tick refresh).
- Added/expanded test stubs for local pytest execution without full Home Assistant runtime.