<b>Integracja: Sprsun CGK_V3L – Home Assistant (Modbus / LAN)
Integracja pozwala na bezpośrednie podłączenie pomp ciepła Sprsun serii CGK_V3L do Home Assistanta za pomocą Modbus (np. przez bramkę Modbus TCP lub inny konwerter).
Celem integracji jest pełne, lokalne sterowanie oraz odczyt parametrów pracy bez użycia chmury.</b>

Aktualnie integracja wspiera następujące modele:
$${\color{green} CGK025V3L, CGK030V3L, CGK040V3L, CGK050V3L, CGK060V3L }$$

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

2. Sensory (sensor.*)

Sensory logiczne

Dostępne m.in.:

Czas pracy sprężarki:
daily / monthly / yearly / total
Czas pracy wentylatora:
daily / monthly / yearly / total
Czas posiadania pompy (OwnershipDays)
Liczenie oparte jest na stanach binarnych istniejących encji HA (np. sprężarka ON/OFF, wentylator ON/OFF).

3. Binary sensors (binary_sensor.*)

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

4. Switch (switch.*)

5. Button (button.*)

Przykłady:
przywracanie ustawień fabrycznych pompy
przywracanie ustawień fabrycznych parametrów sprężarki
6. Number (number.*)
Są dwa rodzaje encji:

a) Liczby rejestrowe

b) Liczniki logiczne
liczą przejścia:
(OFF → ON) dla pojedynczego sensora
złożone sekwencje defrostu (sprężarka ON, wentylator OFF przez min. 60 s)

- Encje grupowane są w HA jako jedno urządzenie:
- device_info.identifiers: (DOMAIN, entry_id)
- nazwa urządzenia: Pompa ciepła Sprsun <MODEL>
- Nazewnictwo i entity_id
- unique_id encji budowane z:
- DOMAIN, modelu, typu encji i adresu/rejestru lub klucza
- entity_id generowane na podstawie:
- wzorca sprsun_<model>_<nazwa>
- nazwa jest czyszczona z polskich znaków (ą, ć, ę, ł, ń, ó, ś, ź, ż → a, c, e, l, n, o, s, z, z)
- przestrzenie zastępowane _
- Dzięki temu encje mają stabilne, przewidywalne identyfikatory.
<br>
<b>Wymagania:</b>
<br>
- Działający dostęp Modbus do pompy Sprsun (np. przez konwerter RS485–TCP, bramkę LAN, itp.)
<br>
- Home Assistant z możliwością instalacji custom componentów (HACS lub manualne skopiowanie do custom_components/sprsun)
<br>
Instalacja (skrót):
<br>
- Skopiuj katalog sprsun do: <config>/custom_components/sprsun
<br>
- Zrestartuj Home Assistanta.
<br>
W HA:
<br>
- Ustawienia → Integracje → Dodaj integrację → wybierz „Sprsun” (lub zainstaluj przez HACS, jeśli będzie dostępne).
<br>
- Podaj parametry połączenia Modbus zgodnie z konfiguracją pompy/bramki.
<br>
- Po poprawnym połączeniu i odczycie rejestrów, encje: climate, sensor, binary_sensor, switch, select, number, button pojawią się automatycznie w HA.
<br>
<b>Logowanie i debugowanie:</b>
<br>
- Integracja korzysta z loggera homeassistant.components.sprsun (nazwa domeny)
- W przypadku problemów z zapisami/odczytami zobaczysz logi typu:
- Błędy zapisu rejestrów (switch, number, select, button)
- Błędy ładowania sensora alarmów
- Brak zdefiniowanych sensorów dla danego modelu
- Można zwiększyć poziom logowania w configuration.yaml:

```yaml


logger:
  default: warning
  logs:
    custom_components.sprsun: debug
```
<br>
<b>Uwagi:</b>b>
<br>
- Integracja jest w pełni lokalna – żadnych połączeń z chmurą.
- Logika pracy jest mocno konfigurowalna przez pliki modelowe (models/CGKxxxV3L/*), co ułatwia dodawanie nowych modeli lub dostosowywanie rejestrów.
- W miarę możliwości będę dodawał kolejne modele pomp Sprsun, które mają możliwość łączenia po modbus.
