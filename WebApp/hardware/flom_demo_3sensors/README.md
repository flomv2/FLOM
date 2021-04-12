# General Description:
This program goes on the NodeMCU and demontrates the use of three HC-SR501 PIR Motion Sensors, hosting a server, and connecting to the FLOM server.
The sensor outputs are read every half second.
A simple web server is created to show sensor and room status, and updates every 2 seconds.
Room status is set as occupied if there is a full minute of motion detected by any sensor,
and is set as empty after 5 minutes of no motion at all.

NOTE, you must set the wifi network credentials (name and password) manually below
in order to connect to the network (if you want to see the web page and update FLOM).
If you don't, the program will still run normally but obviously just can't connect to the network.

If you have it plugged into your computer and want to use the Serial Monitor, remember to set the baud rate to 115200.

# Sensor Webpage/Server:
When the program starts, it will print to Serial the IP address of the ESP8266 server (not FLOM).

Paste that address into your web browser to see the page. If you open the Serial Monitor
too late and miss the IP address, just click the reset button on the board.

The page shows a circle indicator for each sensor, and one for the room status. An indicator will be red if motion has been detected, and white when there is no motion. The sensor modules have adjustible timers on them to have the signal stay high for a set period of time after each trigger. Turn the timer knob to about 4 o'clock for a period of around 10-30 seconds. This takes some experimenting.

# FLOM Server:
This demo assumes you have a FLOM server running on your local network.
Change the IP address in the URL of the GET request to the IP address
of the device hosting the FLOM server (i.e., your laptop). 

For example if your laptop's IP Address is 192.168.1.24, the URL format is:

"http://192.168.1.24:8000/floor/%s/3/311/pass" (where "%s" will be filled with "enter" or "exit").

To run the FLOM server over the local network, run it in your
terminal as you normally would, and just add the IP address and port number at the end:

`path_to_flom/FLOM/WebApp$ python manage.py runserver 0.0.0.0:8000`

(you can use the zeros or your actual IP address, either is fine).

You might need to adjust firewall settings of your laptop for this to work.

# Connections:
The table below shows the pin connections of the devices.

| PIR Module |  <->  | NodeMCU |                                                                   |
| ---------: | :---: | :------ | ----------------------------------------------------------------- |
|        Vcc |  <->  | Vin     | (there is only one Vin pin that all sensors will be connected to) |
|        Gnd |  <->  | Gnd     | (there are multiple Gnd pins. They are all the same)              |
|        OUT |  <->  | D5      | (for the first sensor)                                            |
|        OUT |  <->  | D6      | (for the second sensor)                                           |
|        OUT |  <->  | D7      | (for the third sensor)                                            |


NOTE, this is assuming you are powering the board with a microUSB cable.
Also, this is assuming you are using a breadboard or something, and
can connect Vcc of all sensors to the Vin pin of the board.
The sensors can be powered externally, but all the grounds (Gnd of the sensor, power source, and board),
might still need to be tied together (not sure though). 
You can try powering the sensors from a 3v3 pin (which supplies 3.3V) and it might work, but the rated minimum is 4.5V. 
Either way, it's fine to just use one sensor with this example, 
but you should either ground the unused input pins, or set its value to 0 in the main loop of the code.