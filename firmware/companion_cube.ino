/*
 * AI Companion Cube - ESP32 Firmware
 * 
 * This firmware handles:
 * - Serial communication with Python host
 * - Sensor reading (PIR, sound, temperature)
 * - LED control
 * - Speaker output
 */

#include <Arduino.h>
#include <FastLED.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>

// Pin definitions
#define PIR_PIN 26
#define SOUND_PIN 34
#define LED_PIN 27
#define SPEAKER_PIN 25
#define TEMP_SENSOR_PIN 32

// Constants
#define NUM_LEDS 12
#define BAUD_RATE 115200
#define SOUND_THRESHOLD 70
#define MOTION_THRESHOLD 0.8
#define SERIAL_TIMEOUT 1000

// Global variables
CRGB leds[NUM_LEDS];
Adafruit_MLX90614 mlx = Adafruit_MLX90614();
String inputString = "";
bool stringComplete = false;

void setup() {
    // Initialize serial communication
    Serial.begin(BAUD_RATE);
    inputString.reserve(200);
    
    // Initialize sensors
    pinMode(PIR_PIN, INPUT);
    pinMode(SOUND_PIN, INPUT);
    pinMode(TEMP_SENSOR_PIN, INPUT);
    
    // Initialize LED ring
    FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
    FastLED.setBrightness(50);
    
    // Initialize temperature sensor
    if (!mlx.begin()) {
        Serial.println("Error initializing MLX90614");
    }
    
    // Initialize speaker
    pinMode(SPEAKER_PIN, OUTPUT);
    
    // Set initial LED color to blue
    fill_solid(leds, NUM_LEDS, CRGB::Blue);
    FastLED.show();
}

void loop() {
    // Read sensors
    float pirValue = digitalRead(PIR_PIN);
    float soundLevel = analogRead(SOUND_PIN);
    float temperature = mlx.readObjectTempC();
    
    // Create sensor data JSON
    String sensorData = createSensorJson(pirValue, soundLevel, temperature);
    Serial.println(sensorData);
    
    // Process serial commands
    if (stringComplete) {
        processCommand(inputString);
        inputString = "";
        stringComplete = false;
    }
    
    // Check for security alerts
    checkSecurityAlerts(pirValue, soundLevel);
    
    delay(100);  // Small delay to prevent overwhelming serial
}

void serialEvent() {
    while (Serial.available()) {
        char inChar = (char)Serial.read();
        inputString += inChar;
        if (inChar == '\n') {
            stringComplete = true;
        }
    }
}

String createSensorJson(float pir, float sound, float temp) {
    String json = "{";
    json += "\"pir\":" + String(pir) + ",";
    json += "\"sound\":" + String(sound) + ",";
    json += "\"temperature\":" + String(temp);
    json += "}";
    return json;
}

void processCommand(String command) {
    command.trim();
    
    // LED control
    if (command.startsWith("LED")) {
        int r, g, b;
        sscanf(command.c_str(), "LED %d %d %d", &r, &g, &b);
        setLedColor(r, g, b);
    }
    // Speaker control
    else if (command.startsWith("SPEAK")) {
        String text = command.substring(6);
        speak(text);
    }
}

void setLedColor(int r, int g, int b) {
    fill_solid(leds, NUM_LEDS, CRGB(r, g, b));
    FastLED.show();
}

void speak(String text) {
    // TODO: Implement text-to-speech
    // For now, just beep
    tone(SPEAKER_PIN, 1000, 100);
}

void checkSecurityAlerts(float pir, float sound) {
    if (pir > MOTION_THRESHOLD) {
        setLedColor(255, 0, 0);  // Red for motion alert
        delay(1000);
        setLedColor(0, 0, 255);  // Back to blue
    }
    
    if (sound > SOUND_THRESHOLD) {
        setLedColor(255, 165, 0);  // Orange for sound alert
        delay(1000);
        setLedColor(0, 0, 255);  // Back to blue
    }
} 