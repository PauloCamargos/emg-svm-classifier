#define TIPO_ARDUINO          "UNO"
#define PIN_ANALOG            0   // Definindo pinos
#define ADC_RESOLUTION        10
#define INICIAR_LEITURA       'R'   // Caracter para iniciar leitura
#define INTERROMPER_LEITURA   'S'   // Caracter para parar leitura
float escala;
bool  leitura_autorizada = false;   // Flag sinalizando se a leitura esta autorizada
int   tensao;                         // Armazena o valor da tensão
int   valor_lido;                   // valor entre 0-1023
  
void setup() {
  // inicializando a comunicação serial
  Serial.begin(115200);
  escala = 1023.0;
  if(TIPO_ARDUINO=="DUE"){
//    analogReadResolution(12);
    escala = 4095.0;
  } 
}

// the loop routine runs over and over again forever:
void loop() { 
  if (Serial.available() > 0 && Serial.read() == INICIAR_LEITURA )  // caso exista e o caracter na porta serial é 'R': (iniciar leitura)
    leitura_autorizada = true;

  // Enquuanto a leitura estiver autorizada (variavel leitura_autorizada = true)
  while (leitura_autorizada) {
    if (Serial.available() > 0 && Serial.read() == INTERROMPER_LEITURA)  // caso o caracter na porta serial seja 'S': (parar leitura)
      leitura_autorizada = false;

    valor_lido = analogRead(PIN_ANALOG); // Lendo o pino PIN_ANALOG = A0 do arduino
    tensao = 100 * (3.3 * valor_lido / escala);  // convertendo bits (0 - 1023) para tensão (0 - 5.0 * 100)
    Serial.println(tensao);        // Enviando o valor pelo pino serial
    delay(20); // aguarda 100ms para proxima leitura
  }
}
