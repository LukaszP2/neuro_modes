# 🧠 Neuro Modes dla Home Assistant

🇵🇱 **Polski** | 🇬🇧 [Go to English version (Wersja angielska)](README.md)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

**Neuro Modes** to zaawansowany, modułowy silnik dla Home Assistant, który inteligentnie zarządza stanami, trybami i modyfikatorami w Twoim domu. Zamiast sztywnych automatyzacji, wykorzystuje dynamiczny system "poszlak" i wag punktowych, aby precyzyjnie określić, co aktualnie dzieje się w domu.

## ✨ Główne funkcje
* **🧠 Silnik Logiki Poszlak:** Przypisuj dodatnie lub ujemne wagi różnym encjom (osoby, sensory, odtwarzacze). Tryb aktywuje się dopiero, gdy suma wag przekroczy zdefiniowany przez Ciebie próg.
* **🏠 Tryby Bazowe i Modyfikatory:** Oddziel główne stany domu (np. Dom, Poza domem, Noc) od nakładających się modyfikatorów (np. Goście, Kino, Praca Zdalna).
* **🪄 Inteligentne Szablony (Smart Templates):** Błyskawicznie konfiguruj złożoną logikę za pomocą wbudowanych szablonów:
  * 💼 **Praca Zdalna:** Reaguje na dni robocze i pracujących domowników, z możliwością zablokowania trybu, gdy reszta rodziny wraca.
  * 🧸 **Dzieci same w domu:** Automatycznie wykrywa obecność dzieci przy jednoczesnym braku rodziców.
  * 🏖️ **Wakacje:** Zaawansowane wykrywanie długiej nieobecności zintegrowane z systemem alarmowym.
  * 🥂 **Goście:** Obsługa stref publicznych i połączeń z siecią Wi-Fi dla gości.
* **⚙️ Modułowy interfejs (UI):** Pełna konfiguracja odbywa się z poziomu interfejsu Home Assistant – zapomnij o YAML-u. Łatwe zarządzanie poszlakami, wagami i progami aktywacji.

## 📦 Instalacja przez HACS

1. Otwórz **HACS** w swoim Home Assistant.
2. Przejdź do **Integracje** -> Kliknij trzy kropki w prawym górnym rogu -> **Niestandardowe repozytoria (Custom repositories)**.
3. Wklej link do tego repozytorium i wybierz kategorię **Integracja**.
4. Kliknij "Dodaj", a następnie wyszukaj **Neuro Modes** w HACS i pobierz.
5. Zrestartuj Home Assistant.
6. Przejdź do **Ustawienia -> Urządzenia i usługi -> Dodaj integrację**, wpisz "Neuro Modes" i zainstaluj Główny Silnik.

---
*Stworzone z pasją do inteligentnego domu.*