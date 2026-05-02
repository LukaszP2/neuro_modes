# Release checklist (manual)

- [ ] `python3 -m pytest custom_components/neuro_modes/tests -q`
- [ ] Smoke test config flow (engine -> mode -> modifier)
- [ ] Smoke test options flow (manage sources add/edit/delete)
- [ ] Verify selector only shows base modes
- [ ] Verify diagnostics endpoint payload and redaction
- [ ] Bump version in `manifest.json`
- [ ] Update `CHANGELOG.md`
