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
# ser.write(bytes([0b00000000, 0x20]))

# Przykładowa ramka: Skręt (01), Kierunek: Prawo (1), Bajt danych: 90 (kąt)
# Pierwszy bajt = 0b01000000 => 0x40
# Drugi bajt = 90 => 0x5A
ser.write(bytes([0b00000000, 0x5A]))

# Czekamy chwilę, aby Arduino miało czas na przetworzenie danych
time.sleep(1)

# Odczytywanie wszystkich danych z portu szeregowego
print("Odczytane dane z Arduino:")

# Nieskończona pętla do ciągłego odczytu danych z bufora
while True:
    if ser.in_waiting > 0:  # Sprawdzenie, czy są dostępne dane w buforze
        dane = ser.read(ser.in_waiting)  # Odczyt całego dostępnego bufora
        print("Surowe dane:", dane)  # Wyświetlenie odebranych danych w postaci surowej (bytes)
        
        # Próbujemy zdekodować dane jako tekst UTF-8 (ignorując błędy)
        try:
            decoded_data = dane.decode('utf-8', errors='ignore')  
            print("Odebrane dane jako tekst:", decoded_data)
        except UnicodeDecodeError:
            print("Błąd dekodowania danych na tekst.")
    
    # Możesz dodać krótki czas oczekiwania, aby zmniejszyć obciążenie procesora
    time.sleep(0.1)

# Zamknięcie portu po zakończeniu (w rzeczywistym przypadku należy to umieścić po odpowiednich warunkach)
# ser.close()
