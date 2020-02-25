const int echoPin = 2;
const int trigPin = 3;

long duration;
int distance;

void setup() 
{
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.begin(9600);
}

void loop() 
{
  // clear the trig pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // set the trig pin HIGH for 10us
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // read from the echo pin and get duration (seconds)
  duration = pulseIn(echoPin, HIGH);

  // calculate the distance
  distance = duration*(0.034/2);

  // print the distance
  Serial.print("Distance: ");
  Serial.println(distance);
}
