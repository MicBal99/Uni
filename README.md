# Symulacja Przepływu Ciepła w Pomieszczeniu

## Opis Projektu
Projekt ten to symulacja przewodnictwa cieplnego w pomieszczeniu przy wykorzystaniu numerycznego modelu różnicowego. Symulacja uwzględnia:
- Równanie przewodnictwa cieplnego,
- Działanie grzejników ogrzewających pomieszczenie,
- Stałą temperaturę ścian na poziomie 18°C,
- Wizualizację rozkładu temperatury w czasie.

Kod napisany jest w języku Python w stylu obiektowym, a dane są prezentowane graficznie przy użyciu biblioteki Matplotlib.

## Wymagania systemowe
Aby uruchomić kod, należy zainstalować następujące pakiety Pythona:

```
numpy
matplotlib
```

Można je zainstalować za pomocą polecenia:

```
pip install numpy matplotlib
```

## Uruchamianie symulacji
Aby uruchomić symulację, wystarczy uruchomić główny plik skryptu:

```
python Heat_sim.py
```

Podczas działania skryptu na bieżąco wyświetlana jest animacja pokazująca zmieniający się rozkład temperatury w pomieszczeniu. W terminalu dodatkowo wyświetlane są informacje o średniej temperaturze oraz całkowitej ilości ciepła.

## Struktura Pliku
- **HeatSimulation** – główna klasa zarządzająca symulacją.
- **_initialize_walls()** – tworzy ściany o stałej temperaturze 18°C.
- **_initialize_heaters()** – dodaje grzejniki w pomieszczeniu.
- **total_heat()** – oblicza całkowite ciepło w pomieszczeniu.
- **run_simulation()** – uruchamia symulację i rysuje wykresy.

