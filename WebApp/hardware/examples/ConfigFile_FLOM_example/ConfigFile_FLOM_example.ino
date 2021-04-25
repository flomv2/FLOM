// Example: storing JSON configuration file in flash file system
//
// Uses ArduinoJson library by Benoit Blanchon.
// https://github.com/bblanchon/ArduinoJson
//
// Created Aug 10, 2015 by Ivan Grokhotkov.
//
// This example code is in the public domain.

#include <ArduinoJson.h>
#include <LittleFS.h>

//Global Variables
char floor_num[2];
char room_num[5];
char passcode[5];

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

  //fill global variables
  snprintf(floor_num, 2, doc["floor"]);
  snprintf(room, 5, doc["room"]);
  snprintf(passcode, 5, doc["pass"]);


  if (floor_num) {
    Serial.printf("Loaded floor_num: %s\n", floor_num);
  } else {
    Serial.println("Failed to load floor_num from json");
  }
  if (room_num) {
    Serial.printf("Loaded room: %s\n", room_num);
  } else {
    Serial.println("Failed to load room from json");
  }
  if (passcode) {
    Serial.printf("Loaded passcode: %s\n", passcode);
  } else {
    Serial.println("Failed to load passcode from json");
  }

  return true;
}

bool saveConfig() {
  StaticJsonDocument<200> doc;
  doc["floor"] = "3";
  doc["room"] = "311";
  doc["pass"] = "pass";

  File configFile = LittleFS.open("/room_info.json", "w");
  if (!configFile) {
    Serial.println("Failed to open config file for writing");
    return false;
  }

  serializeJson(doc, configFile);
  return true;
}

void setup() {
  Serial.begin(115200);
  Serial.println("");
  delay(1000);
  Serial.println("Mounting FS...");

  if (!LittleFS.begin()) {
    Serial.println("Failed to mount file system");
    return;
  }

  //  //if you want to write the config file from code and save it on the board
  //  if (!saveConfig()) {
  //    Serial.println("Failed to save config");
  //  } else {
  //    Serial.println("Config saved");
  //  }

  if (!loadConfig()) {
    Serial.println("Failed to load config");
  } else {
    Serial.println("Config loaded");
  }
}

void loop() {
  delay(1000);
  Serial.printf("Floor Number: %s\n", floor_num);
  //  Serial.println(floor_num);
  Serial.printf("Room Number: %s\n", room_num);
  //  Serial.println(room);
  Serial.printf("Passcode: %s\n", passcode);
  //  Serial.println(passcode);
}
