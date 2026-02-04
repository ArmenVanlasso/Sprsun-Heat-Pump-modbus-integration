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
REG_wy_grzalka_sprezarki = 10 # modbus 10011
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
REG_al011 = 23 # modbus 10024
REG_al012 = 24 # modbus 10025
REG_al013 = 25 # modbus 10026
REG_al014 = 26 # modbus 10027
REG_al015 = 27 # modbus 10028
REG_al016 = 28 # modbus 10029
REG_al017 = 29 # modbus 10030
REG_al018 = 30 # modbus 10031
REG_al019 = 31 # modbus 10032
REG_al020 = 32 # modbus 10033
REG_al021 = 33 # modbus 10034
REG_al022 = 34 # modbus 10035
REG_al023 = 35 # modbus 10036
REG_al024 = 36 # modbus 10037
REG_al025 = 37 # modbus 10038
REG_al026 = 38 # modbus 10039
REG_al027 = 39 # modbus 10040
REG_al028 = 40 # modbus 10041
REG_al029 = 41 # modbus 10042
REG_al030 = 42 # modbus 10043
REG_al031 = 43 # modbus 10044
REG_al032 = 44 # modbus 10045
REG_al033 = 45 # modbus 10046
REG_al034 = 46 # modbus 10047
REG_al035 = 47 # modbus 10048
REG_al036 = 48 # modbus 10049
REG_al037 = 49 # modbus 10050
REG_al038 = 50 # modbus 10051
REG_al039 = 51 # modbus 10052
REG_al040 = 52 # modbus 10053
REG_al041 = 53 # modbus 10054
REG_al042 = 54 # modbus 10055
REG_al043 = 55 # modbus 10056
REG_al044 = 56 # modbus 10057
REG_al045 = 57 # modbus 10058
REG_al046 = 58 # modbus 10059
REG_al047 = 59 # modbus 10060
REG_al048 = 60 # modbus 10061
REG_al049 = 61 # modbus 10062
REG_al050 = 62 # modbus 10063
REG_al051 = 63 # modbus 10064
REG_al052 = 64 # modbus 10065
REG_al053 = 65 # modbus 10066
REG_al054 = 66 # modbus 10067
REG_al055 = 67 # modbus 10068
REG_al056 = 68 # modbus 10069
REG_al057 = 69 # modbus 10070
REG_al058 = 70 # modbus 10071
REG_al059 = 71 # modbus 10072
REG_al060 = 72 # modbus 10073
REG_al061 = 73 # modbus 10074
REG_al062 = 74 # modbus 10075
REG_al063 = 75 # modbus 10076
REG_al064 = 76 # modbus 10077
REG_al065 = 77 # modbus 10078
REG_al066 = 78 # modbus 10079
REG_al067 = 79 # modbus 10080
REG_al068 = 80 # modbus 10081
REG_al069 = 81 # modbus 10082
REG_al070 = 82 # modbus 10083
REG_al071 = 83 # modbus 10084
REG_al072 = 84 # modbus 10085
REG_al073 = 85 # modbus 10086
REG_al074 = 86 # modbus 10087
REG_al075 = 87 # modbus 10088
REG_al076 = 88 # modbus 10089
REG_al077 = 89 # modbus 10090
REG_al078 = 90 # modbus 10091
REG_al079 = 91 # modbus 10092
REG_al080 = 92 # modbus 10093
REG_al081 = 93 # modbus 10094
REG_al082 = 94 # modbus 10095
REG_al083 = 95 # modbus 10096
REG_al084 = 96 # modbus 10097
REG_al085 = 97 # modbus 10098
REG_al086 = 98 # modbus 10099
REG_al087 = 99 # modbus 10100
REG_al088 = 100 # modbus 10101
REG_al089 = 101 # modbus 10102
REG_al090 = 102 # modbus 10103
REG_al091 = 103 # modbus 10104
REG_al092 = 104 # modbus 10105
REG_al093 = 105 # modbus 10106
REG_al094 = 106 # modbus 10107
REG_al095 = 107 # modbus 10108
REG_al096 = 108 # modbus 10109
REG_al097 = 109 # modbus 10110
REG_al098 = 110 # modbus 10111
REG_al099 = 111 # modbus 10112
REG_al100 = 112 # modbus 10113
REG_al101 = 113 # modbus 10114
REG_al102 = 114 # modbus 10115
REG_al103 = 115 # modbus 10116
REG_al104 = 116 # modbus 10117
REG_al105 = 117 # modbus 10118
REG_al106 = 118 # modbus 10119
REG_al107 = 119 # modbus 10120
REG_al108 = 120 # modbus 10121
REG_al109 = 121 # modbus 10122
REG_al110 = 122 # modbus 10123
REG_al111 = 123 # modbus 10124
REG_al112 = 124 # modbus 10125
REG_al113 = 125 # modbus 10126
REG_al114 = 126 # modbus 10127
REG_al115 = 127 # modbus 10128
REG_al116 = 128 # modbus 10129
REG_al117 = 129 # modbus 10130
REG_al118 = 130 # modbus 10131
REG_al119 = 131 # modbus 10132
REG_al120 = 132 # modbus 10133
REG_al121 = 133 # modbus 10134
REG_al122 = 134 # modbus 10135
REG_al123 = 135 # modbus 10136
REG_al124 = 136 # modbus 10137
REG_al125 = 137 # modbus 10138
REG_al126 = 138 # modbus 10139
REG_al127 = 139 # modbus 10140
REG_al128 = 140 # modbus 10141
REG_al129 = 141 # modbus 10142
REG_al130 = 142 # modbus 10143
REG_al131 = 143 # modbus 10144
REG_al132 = 144 # modbus 10145
REG_al133 = 145 # modbus 10146
REG_al134 = 146 # modbus 10147
REG_al135 = 147 # modbus 10148
REG_al136 = 148 # modbus 10149
REG_al137 = 149 # modbus 10150
REG_al138 = 150 # modbus 10151
REG_al139 = 151 # modbus 10152
REG_al140 = 152 # modbus 10153
REG_al141 = 153 # modbus 10154
REG_al142 = 154 # modbus 10155
REG_al143 = 155 # modbus 10156
REG_al144 = 156 # modbus 10157
REG_al145 = 157 # modbus 10158
REG_al146 = 158 # modbus 10159
REG_al147 = 159 # modbus 10160
REG_al148 = 160 # modbus 10161
REG_al149 = 161 # modbus 10162
REG_al150 = 162 # modbus 10163
REG_al151 = 163 # modbus 10164
REG_al152 = 164 # modbus 10165
REG_al153 = 165 # modbus 10166
REG_al154 = 166 # modbus 10167
REG_al155 = 167 # modbus 10168
REG_al165 = 168 # modbus 10169
REG_al166 = 169 # modbus 10170
REG_al167 = 170 # modbus 10171
REG_al168 = 171 # modbus 10172
REG_al169 = 172 # modbus 10173
REG_al170 = 173 # modbus 10174
REG_al171 = 174 # modbus 10175
REG_al172 = 175 # modbus 10176
REG_al173 = 176 # modbus 10177
REG_al174 = 177 # modbus 10178
REG_pompa_obiegowa = 178 # modbus 10179
REG_sprezarka = 179 # modbus 10180
REG_wentylator = 180 # modbus 10181
REG_we_chlodzenie = 181 # modbus 10182
REG_we_ogrzewania = 182 # modbus 10183
REG_wy_pompa_obiegowa_2 = 183 # modbus 10184

BINARY_SENSORS = [
    {
        "key": "zasilanie",
        "name": "Zasilanie",
        "register": REG_zasilanie,
        "device_class": "power",
    },
    {
        "key": "czujnik_przeplywu",
        "name": "Czujnik przepływu",
        "register": REG_czujnik_przeplywu,
        "device_class": "problem",
    },
    {
        "key": "we_sterowania_zewn",
        "name": "WE sterowania zewn",
        "register": REG_we_sterowania_zewn,
    },
    {
        "key": "we_sterowania_ac",
        "name": "We sterowania AC",
        "register": REG_we_sterowania_ac,
    },
    {
        "key": "we_faza_zasilania",
        "name": "We faza zasilania",
        "register": REG_we_faza_zasilania,
    },
    {
        "key": "wy_wysoka_predkosc_went",
        "name": "Wy wysoka prędkość went",
        "register": REG_wy_wysoka_predkosc_went,
    },
    {
        "key": "wy_niska_predkosc_went",
        "name": "Wy niska prędkość went",
        "register": REG_wy_niska_predkosc_went,
    },
    {
        "key": "wy_zawor_4d",
        "name": "Wy zawór 4D",
               "register": REG_wy_zawor_4d,
    },
    {
        "key": "wy_pompa_obiegowa",
        "name": "Wy pompa obiegowa",
        "register": REG_wy_pompa_obiegowa,
    },
    {
        "key": "wy_grzalka_obudowy",
        "name": "Wy grzałka obudowy",
        "register": REG_wy_grzalka_obudowy,
    },
    {
        "key": "wy_grzalka_sprezarki",
        "name": "Wy grzałka sprężarki",
        "register": REG_wy_ggrzalka_sprezarki,
    },
    {
        "key": "wy_zawor_3d",
        "name": "Wy zawór trójdrogowy",   # Twój wyjątek
        "register": REG_wy_zawor_3d,
    },
    {
        "key": "wy_grzalka",
        "name": "Wy grzałka",
        "register": REG_wy_grzalka,
    },
]

# Platformy obsługiwane przez integrację
PLATFORMS: list[str] = ["sensor, binary_sensor"]
