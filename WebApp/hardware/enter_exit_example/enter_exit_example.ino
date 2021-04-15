/**
   Adapted from example:
   BasicHTTPClient.ino

   To show how a NodeMCU can enter/exit a room
   in a FLOM server running on a local network.

   Set the network credentials for your local wifi,
   and change the IP address in the URL to the IP
   of the device hosting the FLOM server (i.e., your laptop)

   To run the FLOM server over the local network, run it in your
   terminal as you normally would, and just add the IP and port at the end:
   .../FLOM/WebApp$ python manage.py runserver 0.0.0.0:8000

   (you can use the zeros or your actual IP)

*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

ESP8266WiFiMulti WiFiMulti;

bool entered = false;

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

  //TODO: add your network name and password
  WiFiMulti.addAP("YOUR_SSID", "YOUR_PASSWORD");

  /*WiFiMulti allows you to have multiple access points,
    and it automatically connects you to the strongest one.
    So you can optionally add more with WiFiMulti.addAP
   */ 
  // WiFiMulti.addAP("2nd_SSID", "2nd_PASSWORD");

}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;
  
    char url[48];
    
    //TODO: change the IP address to your own (of the machine running the server)
    snprintf(url, 48, "http://192.168.1.24:8000/floor/%s/3/311/pass", entered ? "exit" : "enter");
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
          process_payload(http.getString());
        }
      } //http>0
      else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
        Serial.println("trying again...");
        int httpCode = http.GET();

        if (httpCode > 0) {
          // HTTP header has been send and Server response header has been handled
          Serial.printf("[HTTP] GET... code: %d\n", httpCode);

          // file found at server
          if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
            process_payload(http.getString());
          }
        } else {
          Serial.printf("[HTTP] GET... failed AGAIN, error: %s\n", http.errorToString(httpCode).c_str());
          Serial.println("don't try again, just wait 30 seconds");
        }

      }//else (>0)


      Serial.println("[HTTP] end...");
      http.end();
    } //begin http
    else {
      Serial.printf("[HTTP] Unable to connect\n");
    }
  }
  else {
    Serial.println("Wifi not connected...");
  }

  Serial.println("(waiting 30 seconds)");
  delay(30000);
}

void process_payload(String payload) {
  Serial.println("Payload:\n<<");
  Serial.println(payload);
  Serial.println(">>");

  Serial.printf("room status was: %s\n", entered ? "occupied" : "empty");
  entered = !entered;
  Serial.printf("room status is: %s\n", entered ? "occupied" : "empty");
}
