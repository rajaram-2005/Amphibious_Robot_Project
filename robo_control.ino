#include <Servo.h>
#include <SoftwareSerial.h>
#include <DHT.h>

// Constants
#define DHTTYPE DHT11
#define DHTPIN A2

// Pin Definitions
const int waterSensorPin = A0;
const int soilMoisturePin = A1;
const int pHSensorPin = A3;
const int thunderSensorIRQ = 2;  // AS3935 IRQ pin for lightning detection
const int elementDetectionPin = A4;  // Hypothetical pin for element detection
const int ledRedPin = 10;
const int ledGreenPin = 11;
const int ledBluePin = 12;
const int motorLandPin1 = 4;
const int motorLandPin2 = 5;
const int motorWaterPin1 = 6;
const int motorWaterPin2 = 7;
const int armServoPin = 8;
const int trigPin = 9;
const int echoPin = 13;

// Thresholds
const int waterThreshold = 500;
const int soilMoistureThreshold = 400;

// Servo and Bluetooth
Servo armServo;
SoftwareSerial BTSerial(2, 3);  // RX, TX

// DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(waterSensorPin, INPUT);
  pinMode(soilMoisturePin, INPUT);
  pinMode(pHSensorPin, INPUT);
  pinMode(thunderSensorIRQ, INPUT);
  pinMode(elementDetectionPin, INPUT);
  pinMode(ledRedPin, OUTPUT);
  pinMode(ledGreenPin, OUTPUT);
  pinMode(ledBluePin, OUTPUT);
  pinMode(motorLandPin1, OUTPUT);
  pinMode(motorLandPin2, OUTPUT);
  pinMode(motorWaterPin1, OUTPUT);
  pinMode(motorWaterPin2, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  armServo.attach(armServoPin);
  BTSerial.begin(9600);
  Serial.begin(9600);
  dht.begin();

  // Attach interrupt for thunderstorm detection
  attachInterrupt(digitalPinToInterrupt(thunderSensorIRQ), thunderstormDetected, RISING);
}

void loop() {
  int waterValue = analogRead(waterSensorPin);
  int soilMoistureValue = analogRead(soilMoisturePin);
  int pHValue = analogRead(pHSensorPin);
  float temperature = dht.readTemperature();
  int elementDetected = analogRead(elementDetectionPin);

  // Send Sensor Data to Raspberry Pi
  Serial.print("Water: "); Serial.println(waterValue);
  Serial.print("Soil Moisture: "); Serial.println(soilMoistureValue);
  Serial.print("pH: "); Serial.println(pHValue);
  Serial.print("Temperature: "); Serial.println(temperature);
  Serial.print("Element Detected: "); Serial.println(elementDetected);

  // Element Detection Logic
  if (elementDetected > 118) {
    collectSample();
    digitalWrite(ledGreenPin, HIGH);  // Indicate sample collection
  }

  // Terrain Identification and Propulsion Control
  if (waterValue > waterThreshold) {
    deactivateLandMotors();
    activateWaterMotors();
    digitalWrite(ledBluePin, HIGH);  // Indicate water mode
  } else {
    deactivateWaterMotors();
    activateLandMotors();
    digitalWrite(ledBluePin, LOW);   // Indicate land mode
  }

  // Sample Collection
  if (soilMoistureValue > soilMoistureThreshold) {
    collectSample();
    digitalWrite(ledGreenPin, HIGH);
  } else {
    digitalWrite(ledGreenPin, LOW);
  }

  // Obstacle Avoidance
  if (detectObstacle()) {
    stopMotors();
    digitalWrite(ledRedPin, HIGH);  // Indicate obstacle detected
  } else {
    digitalWrite(ledRedPin, LOW);
  }

  // Bluetooth Command Handling from Raspberry Pi
  if (BTSerial.available()) {
    char command = BTSerial.read();
    handleBluetoothCommand(command);
  }

  delay(1000);
}

// Obstacle Detection Using Ultrasonic Sensor
bool detectObstacle() {
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  return (distance < 20);
}

// Motor and Servo Functions
void activateLandMotors() {
  digitalWrite(motorLandPin1, HIGH);
  digitalWrite(motorLandPin2, LOW);
}

void deactivateLandMotors() {
  digitalWrite(motorLandPin1, LOW);
  digitalWrite(motorLandPin2, LOW);
}

void activateWaterMotors() {
  digitalWrite(motorWaterPin1, HIGH);
  digitalWrite(motorWaterPin2, LOW);
}

void deactivateWaterMotors() {
  digitalWrite(motorWaterPin1, LOW);
  digitalWrite(motorWaterPin2, LOW);
}

void stopMotors() {
  deactivateLandMotors();
  deactivateWaterMotors();
}

void collectSample() {
  armServo.write(90);  // Move arm to collect sample
  delay(1000);
  armServo.write(0);   // Return arm to original position
  delay(1000);
}

void handleBluetoothCommand(char command) {
  if (command == 'S') {
    stopMotors();
  }
}

// Thunderstorm Detection
void thunderstormDetected() {
  Serial.println("Thunderstorm detected! Stopping operations.");
  stopMotors();
  retractSamplingArm();
  // Send a signal to the Raspberry Pi for further action
  BTSerial.println("THUNDER_DETECTED");
}

void retractSamplingArm() {
  armServo.write(0);  // Retract the arm to a safe position
  delay(1000);
}
