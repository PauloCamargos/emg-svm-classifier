/***
 * Max SPI speed: 100kHz
 * MSB first
 * Borda de descida
 * CPOL: 0
 * SPI_MODE0
         ___ 
CH0  1  | u |  20 +Vcc 
CH1  2  |   |  19 DCLK
CH2  3  |   |  18 CS
CH3  4  |   |  17 Din
CH4  5  |   |  16 BUSY
CH5  6  |   |  15 Dout
CH6  7  |   |  14 GND
CH7  8  |   |  13 GND
COM  9  |   |  12 Vcc
SHDN 10 |___|  11 Vref

 * DATASHEET: http://www.ti.com/lit/ds/symlink/ads8344.pdf
 * 
 * **********************
 * SERIAL OUTPUT PACKET DESCRIPTION
 * Packet description
 * For 1 channels:
 * Packet:  START | MSB  | LSB  | END
 * Exemple:  '$'  | 0x01 | 0x42 | '\n'
 * 
 * For 2 channels:
 * Packet:  START | MSB1 | LSB1 | MSB2 | LSB2 | END
 * Exemple:  '$'  | 0x01 | 0x42 | 0x01 | 0x33 | '\n'
 * 
 */

#include <TimerOne.h>
// ADC DEFINES
#define DATAOUT       11 // MOSI 11   - MASTER -> SLAVE (Data out)
#define DATAIN        12 // MISO 12   - SLAVE -> MASTER  (Data in)
#define SPICLOCK      13 // SCK  13   - CLOCK PIN
#define SELPIN        10 // CS   10   - CS = SS no ADS (selection pin)
// OUTPUT DEFINES
#define FREQ_ACQ 2000 // F[Hz] for data sampling
#define BAUDRATE 115200
#define PACK_START '$'
#define PACK_END   '\n'
#define N_CH 2// Number of channels

uint16_t readvalues[N_CH] // holds the adcvalue for each channel

void setup() {
  // pinmode configuration
  pinMode(SELPIN, OUTPUT);
  pinMode(DATAOUT, OUTPUT);
  pinMode(DATAIN, INPUT);
  pinMode(SPICLOCK, OUTPUT);
  // disabling device before start
  digitalWrite(SELPIN, HIGH);
  digitalWrite(DATAOUT, LOW);
  digitalWrite(SPICLOCK, LOW);
  
  Serial.begin(115200);
}

void read_adc(int channel){
  int adcvalue = 0;
  // PACKET DESCRIPTION | X=DONT CARE 
  // +info, pg. 13 in datasheet)=
  // | START | A2 | A1 | A0 | X | SGL/DF | PD1 | PD0 |
  byte commandbits = B10000111; // CH0
   
  //allow channel selection
  commandbits|=((channel-1)<<3);

  // setting SS (CS)  to LOW to allow data to be clocked in
  digitalWrite(SELPIN,LOW);
  
  // setting up bits to be clocked out
  for(int i=7;i>=0;i--){
    digitalWrite(DATAOUT, commandbits&1<<i);
    // clocking
    digitalWrite(SPICLOCK,HIGH);
    digitalWrite(SPICKLOCK,LOW);
  }

  // reading data (bits) from adc 
  // PACKET DESCRIPTION
  // (MSB)          (LSB)
  // | 15 | 14 | ... | 0 |
  for(int i=15;i>=0;i--){
    adcvalue+=digitalRead(DATAIN)<<i;
    // clocking
    digitalWrite(SPICLOCK,HIGH);
    digitalWrite(SPICLOCK,LOW);
  }

  // keep the read value in a array of channels
  readvalues[channel] = adcvalue;
  
  // sleeping the device
  // setting SS (CS)  to HIGH 
  digitalWrite(SELPIN,HIGH);

  // OBS.: uncomment here to send the data and coment the next line
  send_data();
  // OBS.: uncomment here to plot (PLOTER SERIAL) the data and coment the line above
  //show_data();
}

void send_data(){
  // Start byte
  Serial.write(PACK_START);
  for(int i=0;i<N_CH;i++){ // for each channel
  // First byte
  Serial.write(read_analog_value[i]>>8);
  Serial.write(read_analog_value[i]);
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
//  if (iniciar == 0) 
//  {
//      Timer3.attachInterrupt(handler);
//      Timer3.start(2000); 
//   }
}


void handler()
{
 
}
