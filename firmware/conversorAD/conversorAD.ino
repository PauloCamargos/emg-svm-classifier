/*
   UNIVERSIDADE FEDERAL DE UBERLÂNDIA
   FACULDADE DE ENGENHARIA ELÉTRICA
   JULHO/2017

   Autor: ADRIELLE NAZAR MORAES
   Contato: adrielle.nazar@hotmail.com

   COMUNICAÇÃO COM CONVERSOR A/D ADS8344


  Arduino - Conversor AD
  Definir:

  No AD:
  - VREF: Vcc
  - COM: GND
  No Arduino
  Pinos para: CS, DCLK, DIN, DOUT

  - CS do Arduino se liga no CS do AD

  - DIN do Arduino se liga no MOSI /Dout do AD

  - DOUT do Arduino se liga no MISO /Din do AD

  - DCLK do Arduino se liga no Dclk do AD

*/

#include<TimerOne.h>
#include<SPI.h>

#define sampFreq 2000 //frequencia de amostragem HZ
#define ts 500 /sampFreq //período em ms
#define St 0x24
#define Et 0x0A
#define EEG 0x45
#define TR 0x54
//Timer T; //timer de aquisição
int funcEvent;

//13 => sck
//12 => MISO
//11 => MOSI
//10 =>SS
#define CS_pin 10
#define AD_BUSY 9
#define NULL_SPI 0x00
#define AD_CONFIG 0x86  //0b1000 0110
#define AD_CONVERT 0x84 //0b1000 0100

#define AD_CONFIG0 0x86  //0b1000 0110
#define AD_CONVERT0 0x84 //0b1000 0100

#define CH_DFLT 0
//SPISettings settings_conv_ad(8000000, MSBFIRST, SPI_MODE0);

void setup() {
  // put your setup code here, to run once:

  SPI.begin();
  pinMode(CS_pin, OUTPUT);
  digitalWrite(CS_pin, HIGH);
  pinMode(AD_BUSY, INPUT);
  Serial.begin(115200);

  setup_conversor(0);
  
  //T.every(ts, Aquis); //ativa o timer
  Timer1.initialize(1.0/sampFreq * pow(10,6));
  // setting the timer to work with the specified function
  Timer1.attachInterrupt(Aquis);

}


/**
   Do the same of read_conversor but ignorates the result
*/
void setup_conversor(uint8_t channel) {
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


/**
   Send a packet to request a reading, waits the busy signal to become low, and send 2 null values to read the msb and lsb.
*/
void read_conversor(uint8_t channel) {
  uint8_t conv_msb, conv_lsb;
  uint16_t leitura_ad;
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
  //EnviaDados(leitura_ad);
  Serial.print(leitura_ad);
}

//envia os dados pela porta serial
void EnviaDados(uint16_t ad)
{
  Serial.write(St);
  Serial.write(EEG);
  //Serial.println(ad);//envia o valor pela porta serial
  Serial.write(ad);
  Serial.write(ad >> 8);
  Serial.write(Et);
}

void Aquis()
{
  read_conversor(CH_DFLT);
  Serial.println();
}
void loop() {
//  // put your main code here, to run repeatedly:
//  T.update();
//  if (Serial.available()) {
//    switch (Serial.read()) {
//      case 's': //setup
//        setup_conversor(CH_DFLT);
//        break;
//      case 'r': //read
//        //T.every(ts,Aquis); //ativa o timer
//        read_conversor(CH_DFLT);
//        break;
//      case 0: //pause
//        //T.stop(funcEvent); //para o timer
//        break;
//      default:
//        Serial.println("Nao existe essa opcao seu idiota");
//    }
//  }
}
