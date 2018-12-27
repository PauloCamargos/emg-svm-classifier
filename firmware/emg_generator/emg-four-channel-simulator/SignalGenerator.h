#ifndef __SignalGenerator__
#define __SignalGenerator__

#include <avr/pgmspace.h> //for IDE versions below 1.0 (2011)
#include "dados_gerados.h"

//Tipos de ondas possiveis de se selecionar
typedef enum {
  REPOUSO_WAVE,
  SUPINAR_WAVE,
  PRONAR_WAVE,
  PINCAR_WAVE,
  FECHAR_WAVE,
  ESTENDER_WAVE,
  FLEXIONAR_WAVE
} waveforms_t;

/////////////////////////////////////////
//Classe para gerar as formas de onda //
////////////////////////////////////////
class SignalGenerator_t {
  private:
    waveforms_t _waveform; //Acessible by getter and setter

    uint16_t _actual_index; //Index de leitura do vetor de dados
    float _actual_value[4]; //Valor atual
    float _offset;
    float _amplitude;

    uint16_t _qnt_points;
    uint8_t _freq_divider;

    double get_next() {
      switch (_waveform) {
        case REPOUSO_WAVE:
          _actual_value[0] = 0;
          _actual_value[1] = 0;
          _actual_value[2] = 0;
          _actual_value[3] = 0;
        case SUPINAR_WAVE:
          _actual_value[0] = pgm_read_float_near(emg_supinar_wave + _actual_index * _freq_divider);
          _actual_value[1] = pgm_read_float_near(emg_supinar_wave + 1 + _actual_index * _freq_divider);
          _actual_value[2] = pgm_read_float_near(emg_supinar_wave + 2 + _actual_index * _freq_divider);
          _actual_value[3] = pgm_read_float_near(emg_supinar_wave + 3 + _actual_index * _freq_divider);
          break;
        case PRONAR_WAVE:
          _actual_value[0] = pgm_read_float_near(emg_pronar_wave + _actual_index * _freq_divider);
          _actual_value[1] = pgm_read_float_near(emg_pronar_wave + 1 + _actual_index * _freq_divider);
          _actual_value[2] = pgm_read_float_near(emg_pronar_wave + 2 + _actual_index * _freq_divider);
          _actual_value[3] = pgm_read_float_near(emg_pronar_wave + 3 + _actual_index * _freq_divider);
          break;
        case PINCAR_WAVE:
          _actual_value[0] = pgm_read_float_near(emg_pincar_wave + _actual_index * _freq_divider);
          _actual_value[1] = pgm_read_float_near(emg_pincar_wave + 1 + _actual_index * _freq_divider);
          _actual_value[2] = pgm_read_float_near(emg_pincar_wave + 2 + _actual_index * _freq_divider);
          _actual_value[3] = pgm_read_float_near(emg_pincar_wave + 3 + _actual_index * _freq_divider);
          break;
        case FECHAR_WAVE:
          _actual_value[0] = pgm_read_float_near(emg_fechar_wave + _actual_index * _freq_divider);
          _actual_value[1] = pgm_read_float_near(emg_fechar_wave + 1 + _actual_index * _freq_divider);
          _actual_value[2] = pgm_read_float_near(emg_fechar_wave + 2 + _actual_index * _freq_divider);
          _actual_value[3] = pgm_read_float_near(emg_fechar_wave + 3 + _actual_index * _freq_divider);
          break;
        case ESTENDER_WAVE:
          _actual_value[0] = pgm_read_float_near(emg_estender_wave + _actual_index * _freq_divider);
          _actual_value[1] = pgm_read_float_near(emg_estender_wave + 1 + _actual_index * _freq_divider);
          _actual_value[2] = pgm_read_float_near(emg_estender_wave + 2 + _actual_index * _freq_divider);
          _actual_value[3] = pgm_read_float_near(emg_estender_wave + 3 + _actual_index * _freq_divider);
          break;
        case FLEXIONAR_WAVE:
          _actual_value[0] = pgm_read_float_near(emg_flexionar_wave + _actual_index * _freq_divider);
          _actual_value[1] = pgm_read_float_near(emg_flexionar_wave + 1 + _actual_index * _freq_divider);
          _actual_value[2] = pgm_read_float_near(emg_flexionar_wave + 2 + _actual_index * _freq_divider);
          _actual_value[3] = pgm_read_float_near(emg_flexionar_wave + 3 + _actual_index * _freq_divider);
          break;
      }
      _actual_value[0] = _actual_value[0] * _amplitude + _offset;
      _actual_value[1] = _actual_value[1] * _amplitude + _offset;
      _actual_value[2] = _actual_value[2] * _amplitude + _offset;
      _actual_value[3] = _actual_value[3] * _amplitude + _offset;
      ++_actual_index %= (_qnt_points / _freq_divider); //Incremento circular
    }

  public:
    SignalGenerator_t () {
      _waveform = REPOUSO_WAVE;
      _actual_index = 0;
      _offset = 0;
      _amplitude = 100;
      _freq_divider = 1;
    }

    void generate_value(float *value_holder) {
      get_next();
      value_holder[0] = _actual_value[0];
      value_holder[1] = _actual_value[1];
      value_holder[2] = _actual_value[2];
      value_holder[3] = _actual_value[3];
    }

    ////////////////////////
    //Getters and Setters //
    ////////////////////////

    waveforms_t getWaveform() {
      return _waveform;
    }

    void setWaveform(waveforms_t waveform) {
      _waveform = waveform;
      switch (_waveform) {
        case REPOUSO_WAVE:
          break;
        case SUPINAR_WAVE:
          _qnt_points = 3521;
        case PRONAR_WAVE:
          _qnt_points = 3511;
          break;
        case PINCAR_WAVE:
          _qnt_points = 3511;
          break;
        case FECHAR_WAVE:
          _qnt_points = 3506;
          break;
        case ESTENDER_WAVE:
          _qnt_points = 3506;
          break;
        case FLEXIONAR_WAVE:
          _qnt_points = 3511;
          break;
      }
    }

    void setAmplitude(float amplitude) {
      _amplitude = amplitude;
    }

    void setOffset(float offset) {
      _offset = offset;
    }

    void setQntPointsPerInterval(uint16_t qnt_points) {
      _qnt_points = qnt_points;
    }

    void setFreqDivider(uint16_t freq_divider) {
      _freq_divider = freq_divider;
    }
};

#endif
