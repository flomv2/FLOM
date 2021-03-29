# Motion Sensor Setup

## What You'll Need

- Microcontroller board
- Female-to-female pin wires
- Motion sensor

The actual part specifications are located in the README file of this directory.

## Connecting The Parts

1. Retrieve 3 wires from your package of wires.
2. Locate the 3 pins on the under-side of the motion sensor. Each one has a different purpose. The label for each pin is located under the infrared-sensor plastic covering (which can simply be pulled off).
3. Locate the set of pins on the under-side of the microcontroller. Again, each one has a different purpose. Labels for each pin are on the top-side of the board (opposite the pins).
4. Connect a wire to the VCC (power) pin on the sensor to the Vin pin (provides 5V when using USB port) on the microcontroller. This will provide power to the motion sensor.
5. Connect a wire to the GND pin on the sensor to a corresponding GND pin on the microcontroller. This is the ground for the circuit.
6. Connect a wire to the OUT pin on the sensor to a corresponding data input pin on the microcontroller. This is how the senesor will send its data to the microcontroller.
7. The sensor is now connected to all its necessary parts.

## Using the Sensor

1. Using a micro-USB cable, plug the sensor into a power source (if the code has already been loaded onto the microcontroller) or a computer (if the code has not already been loaded).
2. If the motion sensor code has already been loaded, everything is good to go and it should be working properly.
3. If the motion sensor code has not been loaded, start the Arduino IDE and open the code you want to run on the microcontroller.
4. Verify that the code you want to run is error/bug free.
5. Upload the code to the microcontroller.
6. The code should now be running on the microcontroller and do so each time the microntroller has power.
7. The delay and sensitivity of the motion sensor can be adjusted. We currently have the delay knob turned to the 5 o'clock position and the sensitiviy knob in the 6 o'clock position.

## Some Helpful Diagrams

These diagram pictures were pulled from the Amazon pages for each respective part.

![Microcontroller Pin Diagram](./md_images/microcontroller_pins.jpg "Microcontroller Pin Diagram")
![Sensor Pin Diagram](./md_images/sensor_pins.jpg "Sensor Pin Diagram")
![Sensor Schematic](./md_images/sensor_schematic.jpg "Sensor Schematic")