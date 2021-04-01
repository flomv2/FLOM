/* This program demontrates the use of two HC-SR501 PIR Motion Sensors, and connecting to wifi.
   The sensor outputs are read every half second, and are reflected by the two builtin LEDs on the board.
   A simple web server is created to show sensor and room status, and is updated every 2 seconds.
   Room status is set as occupied if there is any motion detected by either sensor,
   and is set as empty after 5 minutes of no motion at all.

   NOTE, you must set the wifi network credentials (name and password) manually below
   in order to connect the server to wifi, if you want to see the web page.
   If you don't, the program will still work normally but obviously just can't connect to the network.

   When the program starts, it will print to Serial the IP address of the server.
   Paste that address into your web browser to see the page. If you open the Serial Monitor
   too late and miss the IP address, just click the reset button on the board.

   Connections:
   (Sensor -> NodeMcu):
       Vcc -> Vin
       Gnd -> Gnd
       OUT -> D7 (for one sensor)
       OUT -> D1 (for the other sensor)
   NOTE, this is assuming you are powering the board with a microUSB cable.
   Also, this is assuming you are using a breadboard or something, and
   can connect Vcc of both sensors to the Vin pin of the board.
   The sensors can be powered externally though, but all the ground pins might still need to be tied together (not sure though).
   Either way, it's fine to just use one sensor with this example.

   If you have it plugged into your computer and want to use the Arduino IDE's
   Serial Monitor or Serial Plotter, remember to set the baud rate to 115200.
   Also, notice that setting the LED pins to LOW turns on the LED, and setting to HIGH
   turns them off. This is because the LEDs are configured as Active-Low.
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#include <ESP8266HTTPClient.h>

/* TODO: Set these to your desired credentials. */
const char *ssid = "ENTER_YOUR_WIFI";     //Enter your WIFI ssid (name of the network)
const char *password = "ENTER_PASSWORD";  //Enter your WIFI password

/* Some HTML code to display sensors and room status in web browser.
   The page will show 3 circles to simulate a red LED for each sensor, and the room.
   The page will automatically refresh every 2 seconds to get the current info.
*/
#define HTML_CODE "<!DOCTYPE html>\
<html>\
<head>\
<meta http-equiv='refresh' content='2'/>\
<title>ESP8266 Demo</title>\
</head>\
<body>\
<h1>Room Occupancy Detection</h1>\
<svg width=300 height=400>\
<text x=20 y=15 fill=black font-size=20>Sensor 1</text>\
<circle cx=55 cy=70 r=40 stroke=black stroke-width=4 fill=%s />\
<text x=0 y=130 fill=black>Time in this state:</text>\
<text x=25 y=145 fill=black>%s </text>\
<text x=205 y=15 fill=black font-size=20>Sensor 2</text>\
<circle cx=240 cy=70 r=40 stroke=black stroke-width=4 fill=%s />\
<text x=185 y=130 fill=black>Time in this state:</text>\
<text x=210 y=145 fill=black>%s </text>\
<text x=90 y=200 fill=black font-size=25>Room Status</text>\
<circle cx=150 cy=290 r=70 stroke=black stroke-width=4 fill=%s />\
<text x=95 y=385 fill=black>Time in this state:</text>\
<text x=115 y=400 fill=black>%s </text>\
Sorry, your browser does not support inline SVG.\
</svg>\
</body>\
</html>"

#define READ_INTERVAL 500           //time between reads in milliseconds
#define EMPTY_INTERVAL (5*60*1000)  //time in milliseconds of no activity to determine room is empty. 5*60*1000 is 5 minutes
#define PIR_1 D7                    //connects to output pin of sensor
#define PIR_2 D1                    //connects to output pin of sensor
#define TOP_LED D4                  //LED next to antenna
#define BOTTOM_LED D0               //LED next to USB
int motion_sense1 = 0;              //to store output of sensor
int motion_sense2 = 0;              //to store output of sensor
unsigned long previousMillis = 0;   //to store time since last read
unsigned long sensorMillis1 = 0;    //to store time since last state change
unsigned long sensorMillis2 = 0;    //to store time since last state change
unsigned long motionMillis = 0;     //to store time since last state change
unsigned long roomMillis = 0;       //to store time since last state change
bool motion = false;                //current status of a room based on movement
bool occupied = false;              //determine if a room is occupied or not

ESP8266WebServer server(80);


/*takes in an int array of size 4, and a time in milliseconds,
  fills the array with time values like [hr, min, sec, mil]*/
void time_vals(int *_array, unsigned long _millis) {
  int mil = millis() - _millis;
  int sec = mil / 1000;
  int min = sec / 60;
  int hr = min / 60;
  _array[0] = hr;
  _array[1] = min % 60;
  _array[2] = sec % 60;
  _array[3] = mil % 1000;
}

/*takes in cstring (char array) of size 13, and a time in milliseconds,
  fills the cstring with the time formatted as HH:MM:SS.MIL */
void time_string(char *string, unsigned long _millis) {
  int mil = millis() - _millis;
  int sec = mil / 1000;
  int min = sec / 60;
  int hr = min / 60;
  snprintf(string, 13, "%02d:%02d:%02d.%03d", hr, min % 60, sec % 60, mil % 1000);
}


/*this function is called everytime a browser requests to access the page*/
void handleRoot() {
  char html[1000];  //will hold the HTML code
  char time1[13];   //will hold the time for sensor1
  char time2[13];   //will hold the time for sensor2
  char time3[13];   //will hold the time for room status

  time_string(time1, sensorMillis1); //format millis into HH:MM:SS.MIL
  time_string(time2, sensorMillis2);
  time_string(time3, roomMillis);

  //fill in the HTML code with the current values
  snprintf(html, 1000, HTML_CODE,
           motion_sense1 ? "red" : "white",
           time1,
           motion_sense2 ? "red" : "white",
           time2,
           occupied ? "red" : "white",
           time3
          );
  server.send(200, "text/html", html);
}


void setup() {
  //configure the data pins
  pinMode(TOP_LED, OUTPUT);
  pinMode(BOTTOM_LED, OUTPUT);
  pinMode(PIR_1, INPUT);
  pinMode(PIR_2, INPUT);

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
  int response = 0;

  //determine status of the room (occupied or empty)
  //The room is empty if there has been no motion for 5 minutes (EMPTY_INTERVAL)
  if (!motion && currentMillis - motionMillis >= EMPTY_INTERVAL) {
    if (occupied) {
      roomMillis = currentMillis;
      occupied = false;
      response = send_roomUpdate(); //send EXIT request
    }
  }
  else {
    if (!occupied) {
      roomMillis = currentMillis;
      occupied = true;
      response = send_roomUpdate(); //send ENTER request
    }
  }
  if (response < 0) {
    response = send_roomUpdate();
  }


  //if READ_INTERVAL milliseconds have passed since last reads, take new readings
  if (currentMillis - previousMillis >= READ_INTERVAL) {
    previousMillis = currentMillis;   //update current time

    //take readings
    int reading1 = digitalRead(PIR_1);
    int reading2 = digitalRead(PIR_2); //can be set to 0 if only using one sensor

    bool active_reading = reading1 || reading2;

    //if the sensor1 state has changed, reset the state timer
    if (motion_sense1 != reading1) {
      sensorMillis1 = currentMillis;
    }

    //if the sensor2 state has changed, reset the state timer
    if (motion_sense2 != reading2) {
      sensorMillis2 = currentMillis;
    }

    //if the total motion state has changed, reset the state timer
    if (motion != active_reading) {
      motionMillis = currentMillis;
    }

    motion_sense1 = reading1;
    motion_sense2 = reading2;
    motion = active_reading;
    Serial.println(int(motion)); //if connected to serial, output can be logged with Tools -> Serial Plotter
    digitalWrite(BOTTOM_LED, !motion_sense1); //if sensor output is HIGH, LED by USB port will turn on (and vice versa)
    digitalWrite(TOP_LED, !motion_sense2); //if sensor output is HIGH, LED by antenna will turn on (and vice versa)
  }

  server.handleClient();  //this is required for the server to work correctly
}

//pass 0 to exit room; pass 1 to enter room
int send_roomUpdate() {
  WiFiClient client;

  HTTPClient http;

  char url[48];

  //TODO: change the IP address to your own (of the machine running the server)
  snprintf(url, 48, "http://192.168.1.24:8000/floor/%s/3/311/pass", occupied ? "enter" : "exit");
  Serial.printf("URL string is: %s\n", url);

  Serial.print("[HTTP] begin...\n");
  if (http.begin(client, url)) {  // HTTP


    Serial.print("[HTTP] GET...\n");
    // start connection and send HTTP header
    int httpCode = http.GET();

    // httpCode will be negative on error
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] GET... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
        Serial.printf("Payload:\n<<%s\n>>\n", http.getString().c_str());
      } else {
        Serial.println("TODO: handle this response code");
      }

    } //http>0
    else {
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      Serial.println("trying again...");
      httpCode = http.GET();

      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          Serial.printf("Payload:\n<<%s\n>>\n", http.getString().c_str());
        } else {
          Serial.println("TODO: handle this response code");
        }

      } else {
        Serial.printf("[HTTP] GET... failed AGAIN, error: %s\n", http.errorToString(httpCode).c_str());
        Serial.println("don't try again"); //TODO: should we keep trying? This should be handled somehow
      }

    }//else (if http>0)

    Serial.println("[HTTP] end...");
    http.end();
    return httpCode;
  } //begin http
  else {
    Serial.printf("[HTTP] Unable to connect\n");
    return -1;
  }
}
