import serial
import time 

# Konfiguracja portu szeregowego - upewnij się, że używasz odpowiedni port (np. 'COM3' dla Windows lub '/dev/ttyUSB0' dla Linux)
ser = serial.Serial('/dev/ttyUSB0', 250000, timeout=1)  # Użyj odpowiedniego portu i prędkości transmisji

# Krótkie opóźnienie, aby upewnić się, że port jest otwarty i gotowy do komunikacji
time.sleep(2)

# Wysyłanie przykładowych ramek
# Przykładowa ramka: Ruch do przodu (00), Kierunek: Lewo (0), Bajt danych: 32
# Pierwszy bajt = 0b00000000 => 0x00
# Drugi bajt = 32 => 0x20
ser.write(bytes([0b00000000, 0x20]))

# Przykładowa ramka: Skręt (01), Kierunek: Prawo (1), Bajt danych: 90 (kąt)
# Pierwszy bajt = 0b01000000 => 0x40
# Drugi bajt = 90 => 0x5A
ser.write(bytes([0b01000000, 0x5A]))

# Czekamy chwilę, aby Arduino miało czas na przetworzenie danych
time.sleep(1)

# Odczytywanie wszystkich danych z portu szeregowego
print("Odczytane dane z Arduino:")
while ser.in_waiting > 0:  # Dopóki są dane w buforze wejściowym
    dane = ser.read(ser.in_waiting)  # Odczyt całego dostępnego bufora
    print(dane)  # Wyświetlenie odebranych danych w postaci surowej
    print(dane.decode('utf-8', errors='ignore'))  # Wyświetlenie odebranych danych jako string (jeśli to tekst)

# Zamknięcie portu po odczytaniu danych
ser.close()
