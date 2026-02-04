DOMAIN = "sprsun"

# Pola konfiguracyjne
CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_MODEL = "model"

# Domyślne wartości
DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 1
DEFAULT_SCAN_INTERVAL = 30

# MODELE – lista wartości, nie słownik
MODELS = [
    "cgk_025v3l",
    "cgk_030v3l",
    "cgk_040v3l",
    "cgk_050v3l",
    "cgk_060v3l",
]

# ---------------------------------------------------------
# HOLDING REGISTERS (4xxxx)
# ---------------------------------------------------------

REG_temperatura_powrotu = 188
REG_temperatura_zasilania = 189
REG_temperatura_zewnetrzna = 190
REG_temperatura_sprezania = 191
REG_temperatura_ssania = 192
REG_cisnienie_sprezania = 193
REG_cisnienie_ssania = 194
REG_temperatura_cwu = 195
REG_temperatura_parownika = 196
REG_y1_wentylator_nastawa = 197
REG_y3_pwm_pompa_obiegowa = 198
REG_wentylator_1_sterowanie = 199
REG_wentylator_1_pomiar = 200
REG_wentylator_2_sterowanie = 201
REG_wentylator_2_pomiar = 202
REG_wymagana_wydajnosc = 203
REG_aktualna_wymagana_wydajnosc = 204
REG_obroty_sprezarki = 205
REG_zawor_eev = 207
REG_status = 209
REG_zabezpieczenie = 210   # poprawiona literówka
REG_przegrzanie = 211
REG_tryb_pracy_pompy = 215
REG_temperatura_tloczenia = 216
REG_status_2 = 217
REG_wersja_programu_1 = 325
REG_wersja_programu_2 = 326
REG_wersja_programu_3 = 327
REG_pompa_model_1 = 328
REG_pompa_model_2 = 329
REG_moc_pobierana = 333
REG_napiecie_falownika = 334
REG_prad_falownika = 335

# Lista holding registers
ALL_HOLDING_REGISTERS = [
    value
    for name, value in globals().items()
    if name.startswith("REG_") and isinstance(value, int)
    and value >= 100  # filtr: holding zaczyna się od 188 w Twoim zestawie
]

# ---------------------------------------------------------
# DISCRETE INPUT REGISTERS (1xxxx)
# ---------------------------------------------------------

REG_zasilanie = 0
REG_czujnik_przeplywu = 1
REG_we_sterowania_zewn = 2
REG_we_sterowania_ac = 3
REG_we_faza_zasilania = 4
REG_wy_wysoka_predkosc_went = 5
REG_wy_niska_predkosc_went = 6
REG_wy_zawor_4d = 7
REG_wy_pompa_obiegowa = 8
REG_wy_grzalka_obudowy = 9
REG_wy_grzalka_sprezarki = 10
REG_wy_zawor_3d = 11
REG_wy_grzalka = 12

# Alarmy al001–al174
ALL_ALARMS = list(range(13, 178))

# Dodatkowe discrete inputs
REG_pompa_obiegowa_2 = 183

ALL_DISCRETE_INPUTS = (
    [REG_zasilanie,
     REG_czujnik_przeplywu,
     REG_we_sterowania_zewn,
     REG_we_sterowania_ac,
     REG_we_faza_zasilania,
     REG_wy_wysoka_predkosc_went,
     REG_wy_niska_predkosc_went,
     REG_wy_zawor_4d,
     REG_wy_pompa_obiegowa,
     REG_wy_grzalka_obudowy,
     REG_wy_grzalka_sprezarki,
     REG_wy_zawor_3d,
     REG_wy_grzalka,
     REG_pompa_obiegowa_2]
    + ALL_ALARMS
)

# ---------------------------------------------------------
# Platformy
# ---------------------------------------------------------

PLATFORMS = ["sensor", "binary_sensor"]
