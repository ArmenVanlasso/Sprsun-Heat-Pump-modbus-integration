import json
import os
import logging

_LOGGER = logging.getLogger(__name__)


class TranslationLoader:
    """Loader tłumaczeń sensorów dla integracji Sprsun."""

    def __init__(self, integration_path: str):
        """
        integration_path = ścieżka do folderu integracji, np.:
        /config/custom_components/sprsun
        """
        self.integration_path = integration_path
        self.lang_dir = os.path.join(self.integration_path, "lang")

    def load_language(self, language: str) -> dict:
        """
        Wczytuje plik tłumaczeń dla danego języka.
        language = "pl", "en", "ja", ...
        """

        lang_file = os.path.join(self.lang_dir, f"{language}.json")

        # Jeśli plik nie istnieje → fallback na angielski
        if not os.path.isfile(lang_file):
            _LOGGER.warning(
                "Brak pliku tłumaczeń dla języka '%s'. Używam en.json jako fallback.",
                language,
            )
            lang_file = os.path.join(self.lang_dir, "en.json")

        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
            _LOGGER.error("Błąd podczas wczytywania tłumaczeń (%s): %s", lang_file, e)
            return {}

    def get_sensor_translation(self, translations: dict, unique_id: str) -> dict:
        """
        Zwraca tłumaczenie dla konkretnego sensora.
        Jeśli brak tłumaczenia → zwraca pusty słownik.
        """

        if unique_id in translations:
            return translations[unique_id]

        # Brak tłumaczenia → fallback
        _LOGGER.debug("Brak tłumaczenia dla unique_id '%s'", unique_id)
        return {}
