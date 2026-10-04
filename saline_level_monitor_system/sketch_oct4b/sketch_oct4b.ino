#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() {
  Serial.begin(9600);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  delay(1000);
}

void loop() {

  // Send ultrasonic pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  // Receive echo
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);

  // Calculate distance
  float distance = duration * 0.0343 / 2;

  // Send distance to computer
  Serial.println(distance);

  delay(1000);
}