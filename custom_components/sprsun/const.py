DOMAIN = "sprsun"

# Pola konfiguracyjne
CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_MODEL = "model"

# Domyślne wartości (bez domyślnego hosta — użytkownik wpisuje ręcznie)
DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 1
DEFAULT_SCAN_INTERVAL = 30  # sekundy

# Lista modeli dostępnych w config_flow
MODELS = {
    "CGK-025V3L": "cgk_025v3l",
    "CGK-030V3L": "cgk_030v3l",
    "CGK-040V3L": "cgk_040v3l",
    "CGK-050V3L": "cgk_050v3l",
    "CGK-060V3L": "cgk_060v3l",
}

# Lista sensorów:
REG_temperatura_powrotu = 188 # modbus 40189
REG_temperatura_zasilania = 189 # modbus 40190
REG_temperatura_zewnetrzna = 190 # modbus 40191
REG_temperatura_sprezania = 191 # modbus 40192
REG_temperatura_ssania = 192 # modbus 40193
REG_cisnienie_sprezania = 193 # modbus 40194
REG_cisnienie_ssania = 194 # modbus 40195
REG_temperatura_cwu = 195 # modbus 40196
REG_temperatura_parownika = 196 # modbus 40197
REG_y1_wentylator_nastawa = 197 # modbus 40198
REG_y3_pwm_pompa_obiegowa = 198 # modbus 40199
REG_wentylator_1_sterowanie = 199 # modbus 40200
REG_wentylator_1_pomiar = 200 # modbus 40201
REG_wentylator_2_sterowanie = 201 # modbus 40202
REG_wentylator_2_pomiar = 202 # modbus 40203
REG_wymagana_wydajnosc = 203 # modbus 40204
REG_aktualna_wymagana_wydajnosc = 204 # modbus 40205
REG_obroty_sprezarki = 205 # modbus 40206
REG_zawor_eev = 207 # modbus 40208
REG_status = 209 # modbus 40210
RE_zabezpieczenie = 210 # modbus 40211
REG_przegrzanie = 211 # modbus 40212
REG_tryb_pracy_pompy = 215 # modbus 40216
REG_temperatura_tloczenia = 216 # modbus 40217
REG_status = 217 # modbus 40218
REG_wersja_programu_1 = 325 # modbus 40326
REG_wersja_programu_2 = 326 # modbus 40327
REG_wersja_programu_3 = 327 # modbus 40328
REG_pompa_model_1 = 328 # modbus 40329
REG_pompa_model_2 = 329 # modbus 40330
REG_moc_pobierana = 333 # modbus 40334
REG_napiecie_falownika = 334 # modbus 40335
REG_prad_falownika = 335 # modbus 40336

# Platformy obsługiwane przez integrację
PLATFORMS: list[str] = ["sensor"]
