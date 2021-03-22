#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

/* This program demontrates the use of a HC-SR501 PIR Motion Sensor, and connecting to wifi.
 * The sensor output is read every half second, and is shown by a builtin LED. 
 * A simple web server is created to show motion status, and is updated every 2 seconds.
 * 
 * NOTE, you must set the wifi network credentials (name and password) manually below.
 * 
 * When the program starts, it will print to Serial the IP address of the server.
 * Paste that address into your web browser to see the page.
 * (I think) The Default IP Address is 192.168.1.76 (but that might be different for you).
 * 
 * Connections:
 * (Sensor -> NodeMcu):
 *     Vcc -> Vin
 *     OUT -> D7
 *     Gnd -> Gnd
 * NOTE, this is assuming you are powering the board with a microUSB cable.
 * If you have it plugged into your computer and want to use the Arduino IDE's
 * Serial Monitor or Serial Plotter, remember to set the baud rate to 115200.
 * Also, notice that setting the LED pins to LOW turns on the LED, and setting to HIGH
 * turns them off. This is because the LEDs are configured as Active-Low.
*/

/* TODO: Set these to your desired credentials. */
const char *ssid = "ENTER_YOUR_WIFI"; //Enter your WIFI ssid (name of the network)
const char *password = "ENTER_PASSWORD"; //Enter your WIFI password

#define INTERVAL 500              //time between reads in milliseconds
#define PIR_PIN D7                //connects to output pin of sensor
#define TOP_LED D4                //LED next to antenna
#define BOTTOM_LED D0             //LED next to USB
int motion_sense;                 //to store output of sensor
unsigned long previousMillis = 0; //to store time since last read
unsigned long stateMillis = 0;    //to store time since last state change

ESP8266WebServer server(80);

void handleRoot() {
  digitalWrite(TOP_LED, LOW); //Turn on the LED next to antenna
  char temp[400];
  int sec = (millis() - stateMillis) / 1000;
  int min = sec / 60;
  int hr = min / 60;

  /* Some HTML code to display sensor status in web browser.
   * The page will show a circle to simulate a red LED.
   * The page will automatically refresh every 2 seconds to get the current info.
  */
  snprintf(temp, 400,
    "<html>\
     <head>\
        <meta http-equiv='refresh' content='2'/>\
        <title>ESP8266 Demo</title>\
      </head>\
      <body>\
        <h1>Hello from ESP8266!</h1>\
        <p>Time since state changed: %02d:%02d:%02d</p>\
        <h2>Motion Detector</h2>\
        <svg width=\"100\" height=\"100\">\
          <circle cx=\"50\" cy=\"50\" r=\"40\" stroke=\"black\" stroke-width=\"4\" fill=\"%s\" />sorry</svg>\
      </body>\
    </html>",
    hr, min % 60, sec % 60, motion_sense ? "red" : "white"
  );
  server.send(200, "text/html", temp);

  digitalWrite(TOP_LED, HIGH); //turn LED off. (LED flashes very quickly to show when server is updated)
}

void setup() {
  //configure the data pins
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D0, OUTPUT);
  pinMode(PIR_PIN, INPUT);

  //set up the serial interface
  delay(1000);
  Serial.begin(115200);
  Serial.println();

  //set up the wifi connection
  Serial.print("Configuring access point...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { //wait until connection is established
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.on ( "/", handleRoot );
  server.begin();
  Serial.println ( "HTTP server started" );
}

void loop() {
  unsigned long currentMillis = millis();

  //if INTERVAL milliseconds have passed since last read, take a reading
  if (currentMillis - previousMillis >= INTERVAL) {
    previousMillis = currentMillis;   //update current time
    int reading = digitalRead(PIR_PIN); //take a reading
    
    //if the state has changed, reset the state timer
    if (motion_sense != reading){
      stateMillis = currentMillis;
    }
    
    motion_sense = reading;
    Serial.println(motion_sense); //if connected to serial, output can be logged with Tools -> Serial Plotter
    digitalWrite(BOTTOM_LED, !motion_sense); //if sensor output is HIGH, LED will turn on (and vice versa) 
  }

  server.handleClient();
}
