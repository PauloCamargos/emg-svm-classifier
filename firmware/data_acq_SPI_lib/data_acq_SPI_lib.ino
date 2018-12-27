/***
  Author: Paulo Camargos
  Description: Program for testing data sending in high frequency on Arduino
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

#define PLOTTER_SERIAL
#define CH1_ANLG_PIN A0
#define FREQ_ACQ 2000 // F[Hz] for data sampling
#define BAUDRATE 115200
#define PACK_START '$'
#define PACK_END   '\n'
#define N_CH 2// Number of channels

uint16_t read_analog_value[N_CH];

void send_data();
void show_data();

void setup() {
   Serial.begin(BAUDRATE);
  // initializing timer with the specified frequency/
  Timer1.initialize(1.0/FREQ_ACQ * pow(10,6));
  // setting the timer to work with the specified function
  Timer1.attachInterrupt(read_value); 
}

void read_value(){
  // Simulating 2 channels
  read_analog_value[0] = analogRead(CH1_ANLG_PIN);
  read_analog_value[1] = read_analog_value[0];

  //#ifndef PLOTTER_SERIAL
  send_data(); 
  //else 
  //show_data(); 
  //#endif
}

void send_data(){
  // Start byte
  Serial.write(PACK_START);
  // First byte
  Serial.write(read_analog_value[0]>>8);
  Serial.write(read_analog_value[0]);
  // Second byte
  if(N_CH == 2){
    Serial.write(read_analog_value[1]>>8);
    Serial.write(read_analog_value[1]);
  }
  // End byte
  Serial.write(PACK_END);
}

void show_data(){
  for(int i=0; i<N_CH; i++){
        Serial.print(read_analog_value[i]+1024*i);
        Serial.print("\t");
    }
    Serial.println();
}
void loop() {

}
