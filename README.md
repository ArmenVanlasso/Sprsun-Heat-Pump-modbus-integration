Integracja: Sprsun CGK_V3L – Home Assistant (Modbus / LAN)
Integracja pozwala na bezpośrednie podłączenie pomp ciepła Sprsun serii CGK_V3L do Home Assistanta za pomocą Modbus (np. przez bramkę Modbus TCP lub inny konwerter).
Celem integracji jest pełne, lokalne sterowanie oraz odczyt parametrów pracy bez użycia chmury.

Aktualnie integracja wspiera następujące modele:

CGK025V3L
CGK030V3L
CGK040V3L
CGK050V3L
CGK060V3L

Integracja tworzy w Home Assistant następujące typy encji:

1. Climate (climate.*)

Dostępne m.in.:

Temperatury zadane:
ogrzewania
chłodzenia
CWU
Zaawansowane nastawy:
histerezy (start/stop) dla ogrzewania / chłodzenia / CWU
krzywe grzewcze / chłodzące (X1–X4, Y1–Y4)
funkcja czasowa – temperatury dla trybów czasowych
temperatura załączenia grzałki
parametr Delta T
Logika:

Tryby HVAC odczytywane z rejestrów Modbus (m.in. 215, opcjonalnie 12 i 39)
Możliwość blokowania trybów na podstawie dodatkowego rejestru (hvac_mode_register_2, hvac_mode_block_values)
Slider temperatury automatycznie włącza/wyłącza się w zależności od trybu lub wartości rejestru (slider_condition_register, slider_disable_when)
Obsługa typów danych uint16 i int16 (włącznie z wartościami ujemnymi)
Skala temperatur (np. rejestr 188 → 18.8°C przy scale = 0.1)
Zapis trybu i restore stanu

Zmiana trybu HVAC realizowana poprzez definicję write_logic:
np. dla ogrzewania: zapis do określonego rejestru wartości odpowiadającej danemu trybowi
Przy przejściu w tryb OFF:
odczytywany jest zapisany wcześniej stan wybranych rejestrów (restore_registers)
stan ten jest trzymany w lokalnym pliku state.json w katalogu modelu
Przy przejściu w HEAT/COOL:
aktualne wartości wybranych rejestrów są zapisywane do state.json (do późniejszego odtworzenia po OFF)
2. Sensory (sensor.*)
Sensory rejestrowe (Modbus)

Oparte o definicje z:

models/CGKxxxV3L/sensors.py
Cechy:

Odczyt wartości z rejestrów Modbus poprzez SprsunCoordinator
Skala (scale) oraz informacja o typie ze znakiem (signed)
Możliwe mapowanie wartości numerycznych na opisy (mapping)
Możliwe mapowanie ikon w zależności od odczytu (icon_map)
Zdefiniowane:
jednostki (unit)
device_class
state_class
ikony
Sensory logiczne

Dostępne m.in.:

Czas pracy sprężarki:
daily / monthly / yearly / total
Czas pracy wentylatora:
daily / monthly / yearly / total
Czas posiadania pompy (OwnershipDays)
Liczenie oparte jest na stanach binarnych istniejących encji HA (np. sprężarka ON/OFF, wentylator ON/OFF).

3. Binary sensors (binary_sensor.*)
Zdefiniowane per model w:

models/CGKxxxV3L/binary_sensors.py

Przykładowe encje:

Zasilanie
Czujnik przepływu
Wejścia sterujące (zewnętrzne, AC, ogrzewanie, chłodzenie)
Wyjścia:
pompa obiegowa
pompa obiegowa 2
sprężarka
wentylator
zawór 3- i 4-drogowy
grzałki (obudowy, sprężarki, główna)
sygnały prędkości wentylatora
Dodatkowo:

dynamiczna ikona zależna od stanu (icon_on / icon_off)
opcjonalny mapping opisu stanu (extra_state_attributes["description"])
Sensor aktywnych alarmów

Podczas async_setup_entry integracja próbuje dynamicznie załadować klasę SprsunActiveAlarmsSensor z:
custom_components.sprsun.models.<MODEL_FOLDER>.sensor_alarm
Dzięki temu możliwa jest obsługa modelowego sensora alarmów bez sztywnego importu
4. Switch (switch.*)
Definicje w:

models/CGKxxxV3L/switches.py
Implementacja:

SprsunSwitchEntity – prosty zapis 0/1 do rejestru Modbus
Stan odczytywany z coordinator.data[register] (0/1 → OFF/ON)
Osobne ikony dla stanu ON/OFF (np. pompa, grzałka)
5. Button (button.*)
Definicje w:

models/CGKxxxV3L/buttons.py
Implementacja:

SprsunGenericButton – jednorazowy zapis wartości 1 do wybranego rejestru
Przykłady:
przywracanie ustawień fabrycznych pompy
przywracanie ustawień fabrycznych parametrów sprężarki
6. Number (number.*)
Są dwa rodzaje encji:

a) Liczby rejestrowe (Modbus)
Zdefiniowane w:
models/CGKxxxV3L/numbers.py (wpisy zawierające register)
Implementacja:
SprsunNumberEntity
Możliwości:
ustawianie wartości rejestru z HA
tryb suwaka lub pola liczbowego (mode: slider/box)
zakres (min, max, step), jednostka (unit), ikona
b) Liczniki logiczne
Wpisy w numbers.py bez pola register
Implementacja:
SprsunCounterNumberEntity (NumberEntity + RestoreEntity)
Cechy:
oparte o istniejące w HA sensory binarne (źródłowe encje podawane w definicji jako source_sensor, source_sensor_sprezarka, source_sensor_wentylator)
liczą przejścia:
proste (OFF → ON) dla pojedynczego sensora
złożone sekwencje defrostu (sprężarka ON, wentylator OFF przez min. 60 s)
reset licznika według harmonogramu:
brak resetu (None) – stan total_increasing
reset daily, monthly, yearly o północy
stan przywracany po restarcie HA (RestoreEntity)
Struktura techniczna
Integracja oparta na:
ConfigEntry
DataUpdateCoordinator (SprsunCoordinator)
Dane z Modbus przechowywane są w:
coordinator.data (rejestry)
coordinator.data_discrete (discrete inputs)
Każdy typ encji ma dedykowaną klasę bazową:
climate: HeatPumpClimate
sensor: SprsunGenericSensor
binary_sensor: SprsunBinarySensor
switch: SprsunSwitchEntity
select: SprsunGenericSelect
number: SprsunNumberEntity, SprsunCounterNumberEntity
button: SprsunGenericButton
Encje grupowane są w HA jako jedno urządzenie:
device_info.identifiers: (DOMAIN, entry_id)
nazwa urządzenia: Pompa ciepła Sprsun <MODEL>
Nazewnictwo i entity_id
unique_id encji budowane z:
DOMAIN, modelu, typu encji i adresu/rejestru lub klucza
entity_id generowane na podstawie:
wzorca sprsun_<model>_<nazwa>
nazwa jest czyszczona z polskich znaków (ą, ć, ę, ł, ń, ó, ś, ź, ż → a, c, e, l, n, o, s, z, z)
przestrzenie zastępowane _
Dzięki temu encje mają stabilne, przewidywalne identyfikatory.
Wymagania
Działający dostęp Modbus do pompy Sprsun (np. przez konwerter RS485–TCP, bramkę LAN, itp.)
Home Assistant z możliwością instalacji custom componentów (HACS lub manualne skopiowanie do custom_components/sprsun)
Wypełniona konfiguracja integracji (adres hosta/bramki, port, ID slave, parametry Modbus – zależnie od implementacji w __init__.py / config_flow.py)
Instalacja (skrót)
Skopiuj katalog sprsun do:
<config>/custom_components/sprsun
Zrestartuj Home Assistanta.
W HA:
Ustawienia → Integracje → Dodaj integrację → wybierz „Sprsun” (lub zainstaluj przez HACS, jeśli będzie dostępne).
Podaj parametry połączenia Modbus zgodnie z konfiguracją pompy/bramki.
Po poprawnym połączeniu i odczycie rejestrów:
encje climate, sensor, binary_sensor, switch, select, number, button pojawią się automatycznie w HA.
Logowanie i debugowanie
Integracja korzysta z loggera homeassistant.components.sprsun (nazwa domeny)
W przypadku problemów z zapisami/odczytami zobaczysz logi typu:
błędy zapisu rejestrów (switch, number, select, button)
błędy ładowania sensora alarmów
brak zdefiniowanych sensorów dla danego modelu
Można zwiększyć poziom logowania w configuration.yaml:

yaml


logger:
  default: warning
  logs:
    custom_components.sprsun: debug
Uwagi
Integracja jest w pełni lokalna – żadnych połączeń z chmurą.
Logika pracy jest mocno konfigurowalna przez pliki modelowe (models/CGKxxxV3L/*), co ułatwia dodawanie nowych modeli lub dostosowywanie rejestrów.
W miarę rozwoju będzie można:
dodać kolejne modele Sprsun
rozszerzać zestaw encji i logikę (np. dodatkowe liczniki, zaawansowane alarmy, statystyki COP itp.).
