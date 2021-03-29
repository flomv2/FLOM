**Selected Board:**
HiLetgo NodeMCU LUA ESP8266 CP2102 ESP-12E Development Board

http://hiletgo.com/ProductDetail/1906570.html
https://www.amazon.com/HiLetgo-Internet-Development-Wireless-Micropython/dp/B081CSJV2V?th=1


**Steps of How to use the NodeMCU with Arduino core:**

Follow instructions below, and/or reference: https://github.com/esp8266/Arduino

1. Download and install the Arduino IDE. Refer to https://www.arduino.cc/en/Guide
2. Open the Arduino IDE and on the menubar go to File > Preferences
3. Copy the URL below and paste it into the "Additional Boards Manager URLs" field to get the ESP board manager extensions: 
  http://arduino.esp8266.com/stable/package_esp8266com_index.json
  
4. Click OK.
5. On the menubar go to Tools > Board > Boards Manager > Type "esp8266" and download the Community esp8266 and install.
6. Configure the board by setting these fields:

    Tools -> Board -> NodeMCU 1.0 (ESP-12E Module)
  
    Tools -> Flash Size -> 4MB (FS:3MB OTA:~512KB)

    Tools -> CPU Frequency -> 80 Mhz
  
    Tools -> Upload Speed -> 921600
    
    (You canleave other default settings for now)

**Now to test the board:**

7. You can use the provided example Blink program to make the on-board LED blink. Go to: 
  File > Examples > Examples for NodeMCU 1.0 (ESP-12E Module) > ESP8266 > Blink
  
8. Connect the board to your computer via USB, and figure out what COM port it's on.
  (On Windows you can see the COM ports from the Device Manager app)
9. Select the correct port on the Arduino IDE in the menu:
  Tools > Port > (whatever port it's on)
10. Compile and upload the Blink sketch just like you would a regular Arduino
  (by click the Upload button, which is a circle with an arrow in it).

**That's it.** 
Once the program is done uploading, the blue LED will start blinking slowly. You can now program the board just like a regular Arduino, but you will probably need to import some ESP8266 Libraries for most programs. There are a lot more Examples other than Blink that show more interesting things, like ESP8266WiFi > WiFiScan for example. Also take a look at the Github page (at the top of this document) for more information.

**Notes:**

With the Arduino core and IDE, you will not be using the actual NodeMCU firmware. That is being overwritten with the Arduino core. You also don't need to install the NodeMCU flasher.


