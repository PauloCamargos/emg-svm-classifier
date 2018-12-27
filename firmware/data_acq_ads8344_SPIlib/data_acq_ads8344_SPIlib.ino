/***
 * PROGRAM DESCRIPTION: 
 * Program to comunicate with the ADC ADS8344 via SPI protocol.
 * This program reads data from 2 channels and returns the 
 * read values inside a package.
 * 
 * Max SPI speed: 100kHz
 * MSB first
 * Borda de descida
 * CPOL: 0
 * SPI_MODE0

ADS8344 PIN CONFIGURATION 
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
#include<SPI.h>
#include <math.h>

// OUTPUT DEFINES
#define FREQ_ACQ 2000 // F[Hz] for data sampling
#define BAUDRATE 115200
#define PACK_START '$'
#define PACK_END   '\n'
#define N_CH 2// Number of channels

#define CS_pin 10
#define AD_BUSY 9
#define NULL_SPI 0x00

// Order of the Control Bits 
// (MSB)          (LSB)
// | 15 | 14 | ... | 0 |
#define AD_CONFIG 0x86  //0b1000 0110 //CH1
#define AD_CONVERT 0x84 //0b1000 0100

#define AD_CONFIG0 0xc6  //0b1100 0110 // CH2
#define AD_CONVERT0 0xc4 //0b1100 0100

uint16_t read_adc_values[N_CH]; // holds the adcvalue for each channel
//#define AD_CONVERT 0x84 //0b1000 0100

// byte commandbits = B10000111; // command ch0
// byte commandbits = B11000111; // command ch1

void setup() {
  // pinmode configuration
 SPI.begin();

  pinMode(CS_pin, OUTPUT);
  digitalWrite(CS_pin, HIGH);
  
  Serial.begin(115200);

  setup_conversor();
  
  //T.every(ts, Aquis); //ativa o timer
  Timer1.initialize(1.0/FREQ_ACQ * pow(10,6));
  // setting the timer to work with the specified function
  Timer1.attachInterrupt(read_adc);
}

/**
   Send a packet to request a reading, waits the busy signal to become low, and send 2 null values to read the msb and lsb.
*/
void setup_conversor() {
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));

  SPI.transfer(AD_CONFIG);//0 | (channel << 4));//Enviando comando para configurar
  //esperar 100ns, que nesse caso seria o tempo de instrução(?)
  digitalWrite(CS_pin, HIGH);
  delayMicroseconds(2); //espera 2us tempo de converter
  digitalWrite(CS_pin, LOW);
  //while(digitalRead(AD_BUSY)); //tira esse e esperar 200ns, que é o tempo de instrução(?)
  SPI.transfer(NULL_SPI);
  SPI.transfer(NULL_SPI);
  SPI.transfer(NULL_SPI); //IDLE

  digitalWrite(CS_pin, HIGH);
  SPI.endTransaction();
}

void read_adc(){
  uint8_t conv_msb, conv_lsb;
  uint16_t leitura_ad;

  // READING CH1
  digitalWrite(CS_pin, LOW);
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));

  SPI.transfer(AD_CONVERT);//0 | (channel << 4));//Enviando comando para aquisição de dados
  //esperar 100ns, que nesse caso seria o tempo de instrução(?)

  digitalWrite(CS_pin, HIGH);
  delayMicroseconds(2); //espera 2us tempo de converter

  digitalWrite(CS_pin, LOW);
  //while(digitalRead(AD_BUSY)); //tira esse e esperar 200ns, que é o tempo de instrução(?)
  conv_msb = SPI.transfer(NULL_SPI);
  conv_lsb = SPI.transfer(NULL_SPI);
  SPI.transfer(NULL_SPI); //IDLE

  digitalWrite(CS_pin, HIGH);
  SPI.endTransaction();

  leitura_ad = conv_msb << 8 | conv_lsb;
  read_adc_values[0] = leitura_ad;

  // READING CH2
  digitalWrite(CS_pin, LOW);
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));

  SPI.transfer(AD_CONVERT0);//0 | (channel << 4));//Enviando comando para aquisição de dados
  //esperar 100ns, que nesse caso seria o tempo de instrução(?)

  digitalWrite(CS_pin, HIGH);
  delayMicroseconds(2); //espera 2us tempo de converter

  digitalWrite(CS_pin, LOW);
  //while(digitalRead(AD_BUSY)); //tira esse e esperar 200ns, que é o tempo de instrução(?)
  conv_msb = SPI.transfer(NULL_SPI);
  conv_lsb = SPI.transfer(NULL_SPI);
  SPI.transfer(NULL_SPI); //IDLE

  digitalWrite(CS_pin, HIGH);
  SPI.endTransaction();

  leitura_ad = conv_msb << 8 | conv_lsb;
  read_adc_values[1] = leitura_ad;
  
  send_data();
}

void send_data(){
  // Start byte
  Serial.write(PACK_START);
  for(int i=0;i<N_CH;i++){ // for each channel
  // First byte
  Serial.write(read_adc_values[i]>>8);
  Serial.write(read_adc_values[i]);
  }
  // End byte
  Serial.write(PACK_END);
}

void show_data(){
  for(int i=0; i<N_CH; i++){
        Serial.print(read_adc_values[i]+65000*i);
        Serial.print("\t");
    }
    Serial.println();
}

void loop() {

}
