import csv
import random
import numpy as np
import matplotlib.pyplot as plt

#vragen voor sensor
def get_user_input():
    """Vraag de instellingen voor de sensor aan de gebruiker."""
    while True:
        sensor_type = input("Welk type sensor wil je gebruiken? (bijv. temperatuur/licht): ").strip()
        if sensor_type:
            break
        print("Vul een sensortype in.")
#vragen aantal metingen 
    while True:
        try:
            number_of_readings = int(input("Hoeveel metingen wil je genereren? "))
            if number_of_readings <= 0:
                print("Het aantal metingen moet groter zijn dan 0.")
                continue
            break
        except ValueError:
            print("Voer een geldig heel getal in.")
#vraag min en max waarde
    while True:
        try:
            minimum = float(input("Wat is de minimale sensorwaarde? "))
            maximum = float(input("Wat is de maximale sensorwaarde? "))
            if minimum >= maximum:
                print("De minimumwaarde moet kleiner zijn dan de maximumwaarde.")
                continue
            break
        except ValueError:
            print("Voer geldige getallen in.")
#vraag alarmgrens
    while True:
        try:
            threshold = float(input("Wat is de alarmgrens? "))
            break
        except ValueError:
            print("Voer een geldig getal in.")

    return sensor_type, number_of_readings, minimum, maximum, threshold

#random nummers maken tussen de min en max waarde
def generate_readings(number_of_readings, minimum, maximum):
    """Genereer reproduceerbare willekeurige sensorwaarden."""
    random.seed(21)
    readings = [
        random.uniform(minimum, maximum)
        for _ in range(number_of_readings)
    ]
    return np.array(readings)

#de statistieken ophalen zoals aantal getallen min en max
def calculate_statistics(readings):
    """Bereken de belangrijkste statistieken met NumPy."""
    return {
        "count": len(readings),
        "mean": np.mean(readings),
        "minimum": np.min(readings),
        "maximum": np.max(readings),
        "standard_deviation": np.std(readings)
    }

#aantal getallen boven de grenswaarde
def find_outliers(readings, threshold):
    """Geef alle metingen boven de alarmgrens terug."""
    return readings[readings > threshold]

#toon overschrijdingen en de statistieken
def display_statistics(readings, threshold, sensor_type):
    """Toon de statistieken en overschrijdingen op het scherm."""
    stats = calculate_statistics(readings)
    outliers = find_outliers(readings, threshold)

    print("\n--- Resultaten sensoranalyse ---")
    print(f"Sensortype: {sensor_type}")
    print(f"Aantal metingen: {stats['count']}")
    print(f"Gemiddelde: {stats['mean']:.2f}")
    print(f"Minimum: {stats['minimum']:.2f}")
    print(f"Maximum: {stats['maximum']:.2f}")
    print(f"Standaardafwijking: {stats['standard_deviation']:.2f}")
    print(f"Aantal metingen boven alarmgrens ({threshold}): {len(outliers)}")

    if len(outliers) > 0:
        print("Metingen boven de alarmgrens:")
        for value in outliers:
            print(f"- {value:.2f}")
    else:
        print("Er zijn geen metingen boven de alarmgrens.")

#metingen opslaan
def save_readings(readings, filename="sensor_readings.csv"):
    """Sla meetnummer en sensorwaarde op in een CSV-bestand."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Sample number", "Sensor reading"])
            for sample_number, reading in enumerate(readings, start=1):
                writer.writerow([sample_number, reading])
        print(f"De meetgegevens zijn opgeslagen in: {filename}")
        return True
    except OSError as error:
        print(f"Fout bij het opslaan van het CSV-bestand: {error}")
        return False

#lees bestand bij 2
def load_readings(filename):
    """Lees meetwaarden uit een CSV-bestand."""
    try:
        loaded_values = []
        with open(filename, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames or "Sensor reading" not in reader.fieldnames:
                print("Het CSV-bestand moet een kolom 'Sensor reading' bevatten.")
                return None

            for row in reader:
                loaded_values.append(float(row["Sensor reading"]))

        if not loaded_values:
            print("Het CSV-bestand bevat geen meetgegevens.")
            return None

        return np.array(loaded_values)

    except FileNotFoundError:
        print("Dit bestand bestaat niet.")
    except (OSError, ValueError, KeyError) as error:
        print(f"Het CSV-bestand kon niet worden gelezen: {error}")
    return None

#maak lijngrafiek
def plot_readings(readings, threshold, sensor_type):
    """Maak een lijngrafiek van de meetwaarden."""
    sample_numbers = np.arange(1, len(readings) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(sample_numbers, readings, marker="o", label="Sensor readings")
    plt.axhline(
        y=threshold,
        color="red",
        linestyle="--",
        label=f"Alarmgrens ({threshold})"
    )
    plt.title(f"{sensor_type.capitalize()}sensor - meetwaarden")
    plt.xlabel("Meetnummer")
    plt.ylabel("Sensorwaarde")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

#maken histogram
def plot_histogram(readings, sensor_type):
    """Maak een histogram van de verdeling van de meetwaarden."""
    plt.figure(figsize=(10, 5))
    plt.hist(readings, bins=10, edgecolor="black")
    plt.title(f"Verdeling van {sensor_type}metingen")
    plt.xlabel("Sensorwaarde")
    plt.ylabel("Aantal metingen")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#main programma
def main():
    print("=== Sensor Data Analysis Tool ===")
    print("1. Nieuwe sensorwaarden genereren")
    print("2. Sensorwaarden laden uit een CSV-bestand")

    while True:
        choice = input("Maak een keuze (1 of 2): ").strip()
        if choice in ("1", "2"):
            break
        print("Kies 1 of 2.")

    if choice == "1":
        sensor_type, number, minimum, maximum, threshold = get_user_input()
        readings = generate_readings(number, minimum, maximum)
        save_readings(readings)
    else:
        filename = input("Naam van het CSV-bestand (bijv. sensor_readings.csv): ").strip()
        if not filename:
            print("Je moet een bestandsnaam invoeren.")
            return

        readings = load_readings(filename)
        if readings is None:
            return

        sensor_type = input("Welk sensortype hoort bij deze gegevens? ").strip()
        if not sensor_type:
            sensor_type = "sensor"

        while True:
            try:
                threshold = float(input("Wat is de alarmgrens? "))
                break
            except ValueError:
                print("Voer een geldig getal in.")

    display_statistics(readings, threshold, sensor_type)
    plot_readings(readings, threshold, sensor_type)
    plot_histogram(readings, sensor_type)


if __name__ == "__main__":
    main()