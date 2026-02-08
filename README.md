# Sprsun heat pump modbus integration to Home Assistant

CGK‑025V3L

CGK‑030V3L

CGK‑040V3L

CGK‑050V3L

CGK‑060V3L

Integracja zawiera także:
- sensor zbiorczy dla wszystkich encji alarmowych, który sprawdza je po rejestrach. Gdy pojawi się z jednego, dwóch, trzech itd. to wyświetla je razem z opisem
- sensor zliczający dzienną, miesiączną, roczną i całościową ilość włączeń sprężarki,
- sensor zliczający dzienną, miesiączną, roczną i całościową ilość włączeń wentylatora,
- sensor czasu pracy pompy w ciągu dnia, miesiąca, roku i całości,
- sensor ilości defrostów w ciąu dnia, miesiąca, roku, oraz całościowy
- Zamiast każdego sensora alarmowego jest jeden zbiorczy, który sprawdza je po rejestrach. Gdy pojawi się z jednego, dwóch, trzech itd. To sensor wyświetla je razem z opisem. Gdy brak wyświetla stan Brak.
- Można używać jednocześnie dwóch pomp i więcej. Zapisy i odczyty nie kolidują ze sobą

  Jeśli twój recorder wyklucza niektóre encje z zapisu do bazy danych, dodaj je do rejestratora, w celu poprawnego działania.

  Docelowo integracja będzie zawierała wszystkie modele Pomp Sprsun, które mają możliwość połączenia po modbus.
