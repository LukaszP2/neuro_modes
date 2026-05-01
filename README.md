# 🧠 Neuro Modes for Home Assistant

🇬🇧 **English** | 🇵🇱 [Przejdź do polskiej wersji (Polish version)](README_pl.md)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

**Neuro Modes** is an advanced, modular engine for Home Assistant that intelligently manages your home's states, modes, and modifiers. Instead of rigid automations, it uses a dynamic "clue-based" weight system to determine the actual state of your home.

## ✨ Key Features
* **🧠 Clue-Based Logic Engine:** Assign positive or negative weights to different entities (people, sensors, media players). The mode activates only when the sum of weights crosses your defined threshold.
* **🏠 Base Modes & Modifiers:** Separate core states (like Home, Away, Night) from modifiers that run in parallel (like Guests, Cinema, Work from Home).
* **🪄 Smart Templates:** Instantly configure complex logic using built-in, one-click templates:
  * 💼 **Remote Work:** Reacts to workdays and active users, with kill-switches for returning family members.
  * 🧸 **Children Home Alone:** Automatically detects when kids are home but parents have left.
  * 🏖️ **Vacation:** Advanced long-term absence detection integrating with alarms and zones.
  * 🥂 **Guests:** Seamlessly handles public zones and guest Wi-Fi connections.
* **⚙️ Modular UI:** Fully configured through the native Home Assistant UI—no YAML required. Easy management of clues, weights, and thresholds.

## 📦 Installation via HACS

1. Open **HACS** in your Home Assistant.
2. Go to **Integrations** -> Click the three dots in the top right corner -> **Custom repositories**.
3. Paste the URL of this repository and select **Integration** as the category.
4. Click Add, then search for **Neuro Modes** in HACS and click Download.
5. Restart Home Assistant.
6. Go to **Settings -> Devices & Services -> Add Integration** and search for "Neuro Modes" to initialize the Engine.

---
*Created with passion for smart home automation.*