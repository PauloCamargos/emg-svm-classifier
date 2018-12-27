#include <math.h>
#include "TimerOne.h"
#define PERIOD_ACQ 500

int led_state = LOW;
volatile uint16_t last_time = 0;
volatile uint16_t now = 0;
uint16_t deltaT = 0;
uint16_t last_time_copy = 0;
uint16_t now_copy = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Timer1.initialize(1.0 / PERIOD_ACQ * pow(10, 6)); // interval time im microseconds
  Timer1.attachInterrupt(blink_led);
  Serial.begin(115200);
}

void blink_led() {
  last_time = now;
  led_state = !led_state;
  digitalWrite(LED_BUILTIN, led_state);
  now = micros();
}

void loop() {
  noInterrupts();
  last_time_copy = last_time;
  now_copy = now;
  interrupts();

  deltaT = now_copy - last_time_copy;

  Serial.print("F (Hz):");
  Serial.println(1.0 / deltaT * pow(10, 6));
}
