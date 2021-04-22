/*
  Basic implementaion of a FLOM room/node. See README for instructions.
*/

#include <LittleFS.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>  //#include <ESP8266WebServer.h>
#include <AsyncElegantOTA.h>
#include <ArduinoJson.h>


/* TODO: Set these to your desired credentials. */
const char *ssid = "ENTER_YOUR_WIFI";     //Enter your WIFI ssid (name of the network)
const char *password = "ENTER_PASSWORD";  //Enter your WIFI password
const char *flom_ip_addr = "LAPTOP_IP_ADDR";  //IP Address of FLOM Server
const int flom_port = 8000;


/* Some HTML code to display sensors and room status in web browser.
   The page will show a circle to simulate a red LED for each sensor,
   and one for the room status. Also shows time in each state.
   The page will automatically refresh every 3 seconds to get the current info.
*/
#define HTML_CODE "<!DOCTYPE html>\
<html>\
<head>\
<meta http-equiv='refresh' content='3'/>\
<title>ESP8266 Demo</title>\
</head>\
<body>\
<h1>Room %s Occupancy Detection</h1>\
<p>Last Updated <script type=text/javascript>\
var d=new Date();\
var h=d.getHours();\
var m=d.getMinutes();\
var s=d.getSeconds();\
m=pad(m);\
s=pad(s);\
if(h>12)h=h-12;\
document.write(h+\":\"+m+\":\"+s+\" \");\
if(d.getHours()>11)document.write(\"PM\");\
else document.write(\"AM\");\
function pad(i){\
if(i<10)i=\"0\"+i;\
return i;\
}\
</script></p>\
<svg width=300 height=550>\
<text x=20 y=15 fill=black font-size=20>Sensor 1</text>\
<circle cx=55 cy=55 r=30 stroke=black stroke-width=4 fill=%s />\
<text x=0 y=105 fill=black>Time in this state:</text>\
<text x=5 y=120 fill=black>%s</text>\
<text x=205 y=15 fill=black font-size=20>Sensor 2</text>\
<circle cx=240 cy=55 r=30 stroke=black stroke-width=4 fill=%s />\
<text x=185 y=105 fill=black>Time in this state:</text>\
<text x=190 y=120 fill=black>%s</text>\
<text x=115 y=155 fill=black font-size=20>Sensor 3</text>\
<circle cx=150 cy=195 r=30 stroke=black stroke-width=4 fill=%s />\
<text x=95 y=245 fill=black>Time in this state:</text>\
<text x=100 y=260 fill=black>%s</text>\
<text x=90 y=330 fill=black font-size=25>Room Status</text>\
<circle cx=150 cy=420 r=70 stroke=black stroke-width=4 fill=%s />\
<text x=95 y=515 fill=black>Time in this state:</text>\
<text x=100 y=530 fill=black>%s</text>\
Sorry, your browser does not support inline SVG.\
</svg>\
</body>\
</html>"

/*
  Calculate max length of html code (in characters/bytes)
  5 is length of "white", 12 is length of time string (HH:MM:SS.MIL), and there are 4 groups of these
  -(2*8) is for the 8 format specifiers ("%s") being replaced
  +2 is for room number with a letter, minus the format specifier
  sizeof() function includes the terminating null character (so it adds 1 to strlen)
*/
#define MAX_HTML_LENGTH (sizeof(HTML_CODE) + (4*(5+12) - 2*8) +2)


#define READ_INTERVAL 500           //time between reads in milliseconds
#define EMPTY_INTERVAL (5*60*1000)  //time in milliseconds of no activity to determine room is empty. 5*60*1000 is 5 minutes
#define ENTER_INTERVAL (1*60*1000)  //time in milliseconds of activity to determine room is occupied. 1*60*1000 is 1 minute
#define FAIL_INTERVAL (10*1000)     //10 seconds between retries (takes 5 of those seconds to timeout though)

#define PIR_1 D5                    //connects to output pin of sensor
#define PIR_2 D6                    //connects to output pin of sensor
#define PIR_3 D7                    //connects to output pin of sensor
#define TOP_LED D4                  //LED next to antenna
#define BOTTOM_LED D0               //LED next to USB

#define FLOOR_STR_LEN 2             //length of string holding the floor number
#define ROOM_STR_LEN 5              //length of string holding the room number
#define PASSCODE_STR_LEN 5          //length of string holding the passcode

char floor_num[FLOOR_STR_LEN];      //cstring holding the floor number
char room_num[ROOM_STR_LEN];        //cstring holding the room number
char passcode[PASSCODE_STR_LEN];    //cstring holding the passcode

byte motion_sense1 = 0;             //to store output of sensor
byte motion_sense2 = 0;             //to store output of sensor
byte motion_sense3 = 0;             //to store output of sensor
unsigned long previousMillis = 0;   //to store time since last read
unsigned long sensorMillis1 = 0;    //to store time since last state change
unsigned long sensorMillis2 = 0;    //to store time since last state change
unsigned long sensorMillis3 = 0;    //to store time since last state change
unsigned long motionMillis = 0;     //to store time since last state change of total motion
unsigned long roomMillis = 0;       //to store time since last state change of room status
unsigned long requestMillis = 0;    //to store time since last GET request
bool motion = false;                //current status of a room based on movement
bool occupied = false;              //determine if a room is occupied or not
bool send_request = false;
bool request_failed = false;

AsyncWebServer server(80);


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
void handleRoot(AsyncWebServerRequest *request) {
  char html[MAX_HTML_LENGTH];  //will hold the HTML code
  char sen1[13];   //will hold the time for sensor1
  char sen2[13];   //will hold the time for sensor2
  char sen3[13];   //will hold the time for sensor3
  char room[13];   //will hold the time for room status

  time_string(sen1, sensorMillis1); //format millis into HH:MM:SS.MIL
  time_string(sen2, sensorMillis2);
  time_string(sen3, sensorMillis3);
  time_string(room, roomMillis);

  //fill in the HTML code with the current values
  snprintf(html, MAX_HTML_LENGTH, HTML_CODE,
           room_num,
           motion_sense1 ? "red" : "white",
           sen1,
           motion_sense2 ? "red" : "white",
           sen2,
           motion_sense3 ? "red" : "white",
           sen3,
           occupied ? "red" : "white",
           room
          );
  Serial.printf("Update Server: %d %s, %d %s, %d %s\n", motion_sense1, sen1, motion_sense2, sen2, motion_sense3, sen3);
  request->send(200, "text/html", html);
}


/*Send the GET Request to FLOM to enter or exit a room.*/
int send_roomUpdate() {
  WiFiClient client;
  HTTPClient http;

  byte url_size = 49; //TODO: the size of this buffer will have to be changed when the real passcode is used
  char url[url_size];

  Serial.print("Floor Number: ");
  Serial.println(floor_num);
  Serial.print("Room Number: ");
  Serial.println(room_num);
  Serial.print("Passcode: ");
  Serial.println(passcode);

  //TODO: change the IP address to your own (of the machine running the server)
  snprintf(url, url_size, "http://%s:%d/floor/%s/%s/%s/%s",
           flom_ip_addr, flom_port, occupied ? "enter" : "exit", floor_num, room_num, passcode);
  Serial.printf("URL string is: %s\n", url);

  Serial.print("[HTTP] begin...\n");
  if (http.begin(client, url)) {  // HTTP
    Serial.print("[HTTP] GET...\n");
    // start connection and send HTTP header
    int httpCode = http.GET();

    // httpCode will be negative on error
    if (httpCode > 0) {
      // HTTP header has been sent and Server response header has been handled
      Serial.printf("[HTTP] GET... code: %d\n", httpCode);

      // request successfully received by server
      if (httpCode == HTTP_CODE_OK) { //|| httpCode == HTTP_CODE_MOVED_PERMANENTLY
        Serial.printf("Payload:\n<<%s\n>>\n", http.getString().c_str());
      } else {
        Serial.println("TODO: handle this response code");
      }
    } //http>0
    else {
      Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }//else (http<0)

    Serial.println("[HTTP] end...");
    http.end();
    return httpCode;
  } //begin http
  else {
    Serial.printf("[HTTP] Unable to connect\n");
    return -1;
  }
}


/*
  Loads JSON configuration file from flash file system.
  Uses ArduinoJson library by Benoit Blanchon. https://github.com/bblanchon/ArduinoJson

  Adapted from example code in the public domain created Aug 10, 2015 by Ivan Grokhotkov.

  The json file is very basic, so we could just use a txt file and parse it manually,
  but this a fancy way to do it and will be nice if the config file grows.
*/
bool loadConfig() {
  File configFile = LittleFS.open("/room_info.json", "r");
  if (!configFile) {
    Serial.println("Failed to open config file");
    return false;
  }

  size_t size = configFile.size();
  if (size > 1024) {
    Serial.println("Config file size is too large");
    return false;
  }

  // Allocate a buffer to store contents of the file.
  std::unique_ptr<char[]> buf(new char[size]);

  // We don't use String here because ArduinoJson library requires the input
  // buffer to be mutable. If you don't use ArduinoJson, you may as well
  // use configFile.readString instead.
  configFile.readBytes(buf.get(), size);

  StaticJsonDocument<200> doc;
  auto error = deserializeJson(doc, buf.get());
  if (error) {
    Serial.println("Failed to parse config file");
    return false;
  }

  snprintf(floor_num, FLOOR_STR_LEN, doc["floor"]);
  snprintf(room_num, ROOM_STR_LEN, doc["room"]);
  snprintf(passcode, PASSCODE_STR_LEN, doc["pass"]);

  return true;
}


void setup() {
  //pull the pins low in case they are floating (not all being used)
  //maybe pull down resistors should be used instead?
  pinMode(PIR_1, OUTPUT);
  pinMode(PIR_2, OUTPUT);
  pinMode(PIR_3, OUTPUT);
  delay(200);
  digitalWrite(PIR_1, LOW);
  digitalWrite(PIR_2, LOW);
  digitalWrite(PIR_3, LOW);
  delay(200);

  //configure the data pins as input pins
  pinMode(PIR_1, INPUT);
  pinMode(PIR_2, INPUT);
  pinMode(PIR_3, INPUT);

  //set up the serial interface
  delay(1000);
  Serial.begin(115200);
  Serial.println();


  //mount filesystem and get room config data
  Serial.println("Mounting FS...");
  if (!LittleFS.begin()) {
    Serial.println("Failed to mount file system");
    //TODO: handle this
  }
  if (!loadConfig()) {
    Serial.println("Failed to load config");
    //TODO: handle this. Maybe assign example room data for demo/debug?
  } else {
    Serial.println("Config loaded");

    //TODO: handle these if they fail. Maybe assign example room data for demo/debug?
    if (floor_num) {
      Serial.printf("Loaded floor_num: %s\n", floor_num);
    } else {
      Serial.println("Failed to load floor_num from json");
    }
    if (room_num) {
      Serial.printf("Loaded room: %s\n", room_num);
    } else {
      Serial.println("Failed to load room_num from json");
    }
    if (passcode) {
      Serial.printf("Loaded passcode: %s\n", passcode);
    } else {
      Serial.println("Failed to load passcode from json");
    }
  }

  //set up the wifi connection
  Serial.printf("SSID Given: %s\n", ssid);
  Serial.print("Configuring wifi...");
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(ssid, password); //no parameters means use credentials of previous connection, which is stored in flash
  while (WiFi.status() != WL_CONNECTED) { //wait until connection is established
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.on( "/", handleRoot);
  AsyncElegantOTA.begin(&server);    // Start ElegantOTA
  server.begin();
}

void loop() {
  unsigned long currentMillis = millis();
  int response = 0;

  //determine status of the room (occupied or empty)
  //The room is empty if there has been no motion for 5 minutes (or whatever EMPTY_INTERVAL is)
  if (!motion && currentMillis - motionMillis >= EMPTY_INTERVAL) {
    if (occupied) {
      send_request = true;
    }
  }
  else if (motion && currentMillis - motionMillis >= ENTER_INTERVAL) {
    //wait for a minute of detection before setting room as occupied.
    //This is to avoid false triggers or someone just going in and out but not staying.
    if (!occupied) {
      send_request = true;
    }
  }

  //status has changed, so update the room status variables
  if (send_request) {
    roomMillis = currentMillis;
    occupied = !occupied;
  }

  //this will send a request if a change occurs or if the request failed on previous iteration of loop
  if (send_request || (request_failed && (currentMillis - requestMillis >= FAIL_INTERVAL))) {
    response = send_roomUpdate();
    requestMillis = currentMillis; //should this be millis() instead of currentMillis?
    send_request = false;

    if (response < 0) { //request did not go through
      //should currentMillis be updated since a lot of time has passed?
      //maybe this stuff could be at the end of the loop, after the reads
      request_failed = true;
      Serial.println("!!!!!!!!!\n\nREQUEST FAILED\n\n!!!!!!!!!!!");
    } else {
      request_failed = false;
    }
  }


  //if READ_INTERVAL milliseconds have passed since last reads, take new readings
  //TODO: should we be using interrupts instead of always reading?
  if (currentMillis - previousMillis >= READ_INTERVAL) {
    previousMillis = currentMillis;   //update current time

    //take readings
    byte reading1 = digitalRead(PIR_1);
    byte reading2 = digitalRead(PIR_2); //set these equal to zero and don't do the digitalRead if no sensor is attached
    byte reading3 = digitalRead(PIR_3);

    bool active_reading = reading1 || reading2 || reading3;
    char time[13];
    //if the sensor1 state has changed, reset the state timer
    if (motion_sense1 != reading1) {
      time_string(time, sensorMillis1);
      Serial.printf("Sensor_1 was %d for %s\n", motion_sense1, time);
      sensorMillis1 = currentMillis;
    }

    //if the sensor2 state has changed, reset the state timer
    if (motion_sense2 != reading2) {
      time_string(time, sensorMillis2);
      Serial.printf("Sensor_2 was %d for %s\n", motion_sense2, time);
      sensorMillis2 = currentMillis;
    }

    //if the sensor3 state has changed, reset the state timer
    if (motion_sense3 != reading3) {
      time_string(time, sensorMillis3);
      Serial.printf("Sensor_3 was %d for %s\n", motion_sense3, time);
      sensorMillis3 = currentMillis;
    }

    //if the total motion state has changed, reset the state timer
    if (motion != active_reading) {
      motionMillis = currentMillis;
    }

    motion_sense1 = reading1;
    motion_sense2 = reading2;
    motion_sense3 = reading3;
    motion = active_reading;
    Serial.printf("%d %d %d\n", reading1, reading2, reading3); //if connected to serial, output can be logged with Tools -> Serial Plotter
  }//READ_INTERVAL

  AsyncElegantOTA.loop();

}//loop
