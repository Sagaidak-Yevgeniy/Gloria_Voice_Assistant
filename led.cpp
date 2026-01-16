void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == '1') {
      digitalWrite(13, HIGH); // ВКЛ
    }
    else if (cmd == '0') {
      digitalWrite(13, LOW);  // ВЫКЛ
    }
  }
}
