#include <DHT.h>

#define DHTPIN 2      // Pin where the DHT11 sensor is connected
#define DHTTYPE DHT11 // DHT sensor type (DHT11 for this case)

DHT dht(DHTPIN, DHTTYPE);

int ldrPin = A0;      // LDR connected to analog pin A0
int ledPin = 13;      // LED connected to digital pin 13

const int moisturePin = A1;

void setup() {
  Serial.begin(9600);
  dht.begin();
  delay(2000); // Allow time for the sensor to stabilize
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);
}

void loop() {
  float temp = dht.readTemperature();
  float humid = dht.readHumidity();

  if (isnan(temp) || isnan(humid)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.print(" °C\t");
  Serial.print("Humidity: ");
  Serial.print(humid);
  Serial.println(" %");

  int lightValue = analogRead(ldrPin);   // Read the value from the LDR
  Serial.print("LDR value is: ");
  Serial.println(lightValue);            // Print the light value

  if (lightValue < 500) {
    digitalWrite(ledPin, HIGH);          // Turn on the LED
  } else {
    digitalWrite(ledPin, LOW);           // Turn off the LED
  }

  int moistureValue = analogRead(moisturePin); // Read the analog value from the soil moisture sensor
  Serial.print("Moisture Value is: ");
  Serial.println(moistureValue); // Print the value to the serial monitor
  delay(1000);

}