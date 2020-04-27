const int echoPin = 2;
const int trigPin = 3;
const int irPin = A1;

long duration;
int distance;
int average;
int sonic_base;
int update_status;

void setup() 
{
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.begin(9600);

  Serial.println("Calibrating system...");

  Serial.println("Calibrating ultra-sonic sensor...");
  
  for (int i = 0; i < 1000; i++)
  {
    digitalWrite(trigPin, LOW);
    delay(2);
    digitalWrite(trigPin, HIGH);
    delay(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration*(0.0135/2);
    average += distance;
  }
  sonic_base = average / 1000;

  Serial.print("Calibrated distance is ");
  Serial.println(sonic_base);

  delay(1000);
  Serial.println("Calibration Complete\n");
  delay(2000);
}

void loop() 
{
  // clear the trig pin
  digitalWrite(trigPin, LOW);
  delay(2);

  // set the trig pin HIGH for 10us
  digitalWrite(trigPin, HIGH);
  delay(10);
  digitalWrite(trigPin, LOW);

  // read from the echo pin and get duration (seconds)
  duration = pulseIn(echoPin, HIGH);

  // calculate the distance
  distance = duration*(0.0135/2);

  int val = analogRead(irPin);

  if (distance < sonic_base || val >= 700)
  {
    // print IR Sensor output
    Serial.print("IR Sensor Value: ");
    Serial.println(val);
  
    // print the distance
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" inches\n");
  }
  
  delay(1000);
}
