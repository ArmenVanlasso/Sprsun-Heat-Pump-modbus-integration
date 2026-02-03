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
REG_status_2 = 217 # modbus 40218
REG_wersja_programu_1 = 325 # modbus 40326
REG_wersja_programu_2 = 326 # modbus 40327
REG_wersja_programu_3 = 327 # modbus 40328
REG_pompa_model_1 = 328 # modbus 40329
REG_pompa_model_2 = 329 # modbus 40330
REG_moc_pobierana = 333 # modbus 40334
REG_napiecie_falownika = 334 # modbus 40335
REG_prad_falownika = 335 # modbus 40336

# binary_sensors:

REG_zasilanie = 0 # modbus 10001
REG_czujnik_przeplywu = 1 # modbus 10002
REG_we_sterowania_zewn = 2 # modbus 10003
REG_we_sterowania_ac = 3 # modbus 10004
REG_we_faza_zasilania = 4 # modbus 10005
REG_wy_wysoka_predkosc_went = 5 # modbus 10006
REG_wy_niska_predkosc_went = 6 # modbus 10007
REG_wy_zawor_4d = 7 # modbus 10008
REG_wy_pompa_obiegowa = 8 # modbus 10009
REG_wy_grzalka_obudowy = 9 # modbus 10010
REG_wy_ggrzalka_sprezarki = 10 # modbus 10011
REG_wy_zawor_3d = 11 # modbus 10012
REG_wy_grzalka = 12 # modbus 10013
REG_al001 = 13 # modbus 10014
REG_al002 = 14 # modbus 10015 jeżeli odczyta wartość 0 to ok, jeżeli wartość 1 to pokaż tekst i zmień ikonę na 
REG_al003 = 15 # modbus 10016
REG_al004 = 16 # modbus 10017
REG_al005 = 17 # modbus 10018
REG_al006 = 18 # modbus 10019
REG_al007 = 19 # modbus 10020
REG_al008 = 20 # modbus 10021
REG_al009 = 21 # modbus 10022
REG_al010 = 22 # modbus 10023
REG_al011 = 22 # modbus 10023
REG_al012 = 23 # modbus 10024
REG_al013 = 24 # modbus 10025
REG_al014 = 25 # modbus 10025
REG_al015 = 26 # modbus 10027
REG_al016 = 27 # modbus 10028
REG_al017 = 28 # modbus 10028
REG_al018 = 29 # modbus 10029
REG_al019 = 30 # modbus 10030
REG_al020 = 31 # modbus 10032
REG_al021 = 32 # modbus 10033
REG_al022 = 33 # modbus 10034
REG_al023 = 34 # modbus 10035
REG_al024 = 35 # modbus 10036
REG_al025 = 36 # modbus 10037
REG_al026 = 37 # modbus 10038
REG_al027 = 38 # modbus 10039
REG_al028 = 39 # modbus 10040
REG_al029 = 40 # modbus 10040
REG_al030 = 41 # modbus 10042
REG_al031 = 42 # modbus 10043
REG_al032 = 43 # modbus 10003
REG_al033 = 44 # modbus 10045
REG_al034 = 45 # modbus 10046
REG_al035 = 46 # modbus 10047
REG_al036 = 47 # modbus 10048
REG_al037 = 48 # modbus 10049
REG_al038 = 49 # modbus 10050
REG_al039 = 50 # modbus 10051
REG_pompa_obiegowa = 178 # modbus 10179
REG_sprezarka = 179 # modbus 10180
REG_wentylator = 180 # modbus 10181
REG_we_chlodzenie = 181 # modbus 10182
REG_we_ogrzewania = 182 # modbus 10183
REG_wy_pompa_obiegowa_2 = 183 # modbus 10184

# Platformy obsługiwane przez integrację
PLATFORMS: list[str] = ["sensor"]
