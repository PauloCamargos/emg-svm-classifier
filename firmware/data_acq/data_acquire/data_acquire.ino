/***
  Author: Paulo Camargos
  Description: Program for sending data from analog pins
  with specified frequency.
  Date: 18/12/2018

  Packet description
  For 1 channels:
  Packet:  START | MSB  | LSB  | END
  Exemple:  '$'  | 0x01 | 0x42 | '\n'

  For 2 channels:
  Packet:  START | MSB1 | LSB1 | MSB2 | LSB2 | END
  Exemple:  '$'  | 0x01 | 0x42 | 0x01 | 0x33 | '\n'
*/

#include <TimerOne.h>
#include <math.h>

#define FREQ_ACQ 2000     // F[Hz] for data sampling
#define CH1_ANLG_PIN A0   // channel 1 data
#define CH2_ANLG_PIN A1   // channel 2 data
#define BAUDRATE 115200   // baudrate
#define PACK_START '$'    // symbol start of packet
#define PACK_END   '\n'   // symbol end of packet
#define N_CH 2            // Number of channels

// Uncoment here if you want to simulate sin and cos function
// Comment if you want to read analogic pins on arduino
//#define SIMULATE_TRIGONOMETRY


// Uncoment here to view data on PLOTTER SERIL
// Coment if you want to send data
// Doenst work together with SIMULATE_TRIGONOMETRY
//#define WANT_PLOT

uint16_t read_analog_value[N_CH];   // holds the ch1 and ch2 read values
uint16_t rad_angle = 0;

void send_data(); // sends data through serial.write
void show_data(); // sends data throug serial.print (for plotter serial)
void simulate_trigonometry(); // simulates sin (ch1) and cos (ch2) 

void setup() {
  Serial.begin(BAUDRATE);
  // initializing timer with the specified frequency
  Timer1.initialize(1.0 / FREQ_ACQ * pow(10, 6));  // must pass the period
  // setting the timer to work with the specified function
#ifndef SIMULATE_TRIGONOMETRY
  Timer1.attachInterrupt(read_value);
#else
  Timer1.attachInterrupt(simulate_trigonometry);
#endif
}

// simulating sin and cos function
void simulate_trigonometry() {
  // Simulating 2 channels
  read_analog_value[0] = sin(rad_angle * 3.14159 / 180.0) * 500 + 500;
  if (N_CH == 2)
    read_analog_value[1] = cos(rad_angle * 3.14159 / 180.0) * 500 + 500;

  rad_angle++;
  if (rad_angle == 361)
    rad_angle = 0;

  // checking if wants to send or see data
  // on serial plotter
#ifndef WANT_PLOT
  send_data();
#else
  show_data();
#endif
}

// reads the analog value of channels
void read_value() {
  // Simulating 2 channels
  read_analog_value[0] = analogRead(CH1_ANLG_PIN);
  if (N_CH == 2)
    read_analog_value[1] = analogRead(CH2_ANLG_PIN);

  // checking if wants to send or see data
  // on serial plotter
#ifndef WANT_PLOT
  send_data();
#else
  show_data();
#endif
}

void send_data() {
  // sends the data through serial.write as a packet
  Serial.write(PACK_START); // Start byte
  // start byte
  // shifting 8 bits to right (write() only sends 8 bits each time)
  Serial.write(read_analog_value[0] >> 8);
  Serial.write(read_analog_value[0]);
  // Second byte
  if (N_CH == 2) { // if 2 channels
    Serial.write(read_analog_value[1] >> 8);
    Serial.write(read_analog_value[1]);
  }
  // end byte
  Serial.write(PACK_END);
}

void show_data() {
  // sends data through serial.print
  // usefull for plotter serial
  for (int i=0; i<N_CH; i++) {
    Serial.print(read_analog_value[i] + 1 * i);
    Serial.print("\t");
  }
  Serial.println();
}

void loop() {
  // nothing here

}
