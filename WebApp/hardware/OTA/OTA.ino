/*
  ORIGINAL AUTHOR INFO:
  Rui Santos
  Complete project details
   - Arduino IDE: https://RandomNerdTutorials.com/esp8266-nodemcu-ota-over-the-air-arduino/
   - VS Code: https://RandomNerdTutorials.com/esp8266-nodemcu-ota-over-the-air-vs-code/
     
  This sketch shows a Basic example from the AsyncElegantOTA library: ESP8266_Async_Demo
  https://github.com/ayushsharma82/AsyncElegantOTA

  ADDED INFO:
  I pulled out the most important information from the Arduino IDE tutorial listed above:
  - The first sketch including this code will have to be uploaded via the serial port.
  - This code will have to be included in every sketch uploaded to the microcontrollers. If not,
  then we will lose wireless access to the controllers.
  - Be sure to test/verify a new sketch works before uploading OTA. Otherwise, we may lose our
  connection if things crash.

  Libraries needed:
  - Note: the libraries with links to .zip files can be added to your library using the 
  "Add .ZIP Library" option in Sketch > Include Library. The others can be found under "Manage
  Libraries" in the same menu.
  - AsyncElegantOTA
  - ESPAsyncWebServer (https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip)
  - ESPAsyncTCP (https://github.com/me-no-dev/ESPAsyncTCP/archive/master.zip)
  - ArduinoJson
*/

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <AsyncElegantOTA.h>

const char* ssid = "REPLACE_SSID";
const char* password = "REPLACE_PWD";

AsyncWebServer server(80);

void setup(void) {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/plain", "Hi! I am ESP8266.");
  });

  AsyncElegantOTA.begin(&server);    // Start ElegantOTA
  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  AsyncElegantOTA.loop();
}
