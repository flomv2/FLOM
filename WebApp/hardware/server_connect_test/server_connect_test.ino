/**
   Adapted code from BasicHTTPClient.ino example included in the ArduinoIDE for ESP8266 boards

   Original Created on: 24.05.2015

   Code is used to test whether or not the microcontroller can connect to WiFi and connect to the FLOM WebApp (wherever it's being hosted).

   This code is meant to be run using the ArduinoIDE with the NodeMCU microcontroller connected via micro-USB to the machine.

   To get the FLOM server up and running (and publically accessible), do the following:
    - Modify the WebApp/WebApp/settings.oy file and set ALLOWED_HOSTS = ['*']
    - Run the server in the terminal using "python manage.py runserver 0.0.0.0:8000", where 0.0.0.0 is the publically accessable IP for your machine
    - Run this code to test the microcontroller's connection to FLOM

   To view the output from this code from the microcontroller go to Tools > Serial Monitor in the ArduinoIDE while it's running. If a 200 (OK) HTTP code is returned when the FLOM server is connected to, that mean the connection is good.
*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

ESP8266WiFiMulti WiFiMulti;

void setup() {

  Serial.begin(115200);
  // Serial.setDebugOutput(true);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("SSID", "PASSWORD");

}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;

    // Insert FLOM IP address that is accessible publically from the machine it's being run on
    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, "http://0.0.0.0:8000")) {  // HTTP


      Serial.print("[HTTP] GET...\n");
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }

  delay(10000);
}
