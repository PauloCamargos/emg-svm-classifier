#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 16:06:46 2018

@author: italo
"""
#%% Importing the libraries
import pandas as pd # reading files
import numpy as np # handling numerical data
import matplotlib.pyplot as plt # Plotting

#%% Adding the path to datasets
HAND_MOVIMENTS_NAMES = ["Supinar", "Pronar", "Pincar", "Fechar", "Estender", "Flexionar"]
START_TARGET = 6
END_TARGET = 12
#%% Importing the dataset
# TODO: perguntar julia sobre os protocolos dessas coletas,
# por que 11, 12, 13, 14, 21, 22, 23, 24?
# 2 posições do eletrodo - encima(1) e embaixo(4)
# 4 baterias para cada posição
# NOTE: da pra juntar as baterias juntos pois foi separado para a pessoa nao cansar
file_name = '../../datasets/coletas/Eber/Eber11-Final.txt'
dataset = pd.read_table(file_name, sep=';', header=None)
dataset.columns = 'CH1 CH2 CH3 CH4 Trigger None'.split()
emg_channels = dataset.iloc[:, :-2].values
emg_trigger = dataset.iloc[:, -2].values

file_name_targets = '../../datasets/coletas/Eber/Eber11-Resposta.txt'
targets = pd.read_table(file_name_targets, header=None)
targets = targets.iloc[:, :].values.ravel()
targets_str = []
for target in targets:
    targets_str.append(HAND_MOVIMENTS_NAMES[target-1])

#%% Constantes dos sinais
# Tempo de atraso (em amostras) no TRIGER para sincronização SINAL/TRIGGER
delay_trigger = 500
fs = 2000  # Frequência de amostragem (Hz)fa = 

#%% Correcting the triger
# TODO: perguntar julia oq vai ser feito desse atraso
emg_trigger_corrected = np.append(arr = np.zeros(delay_trigger),
                                  values = emg_trigger[:-delay_trigger])

#%% Contraction sites
contractions_onsets = []
contractions_offsets = []
for i in range(1,emg_channels.shape[0]):
    # Borda 0 -> 1
    if emg_trigger_corrected[i-1] < 1 and emg_trigger_corrected[i] >= 1:
        contractions_onsets.append(i-500)
    # Borda 1 -> 0
    if emg_trigger_corrected[i-1] > 1 and emg_trigger_corrected[i] <= 1:
        contractions_offsets.append(i+500)
       
#%% Arduino Signals
arduino_emg_sinals = []
for i in range(START_TARGET,END_TARGET):
    arduino_emg_sinals.append([])
    for ch in range(4):
        arduino_emg_sinals[-1].append(emg_channels[contractions_onsets[i]:contractions_offsets[i],ch])

#%% plottando os sinais
'''
for i in range(START_TARGET,END_TARGET):
    fig = plt.figure()
    axes = [None for i in range(4)]
    for ch in range(4):
        axes[ch] = plt.subplot(4,1,ch+1)
        plt.plot(arduino_emg_sinals[i-START_TARGET][ch])
        plt.title('Ch ' + str(ch+1))
        plt.grid()
    
    axes[0].get_shared_x_axes().join(axes[0],axes[1],axes[2],axes[3])
    axes[0].get_shared_y_axes().join(axes[0],axes[1],axes[2],axes[3])
    plt.ylim((-1000,1000))
    axes[0].set_xticklabels([])
    axes[1].set_xticklabels([])
    axes[2].set_xticklabels([])
    fig.suptitle(targets_str[i])
plt.show()
'''
#%% Normalizando os sinais
max_emg = []
min_emg = []
for i in range(START_TARGET,END_TARGET):
    for ch in range(4):
        max_emg.append(arduino_emg_sinals[i-START_TARGET][ch].max())
        min_emg.append(arduino_emg_sinals[i-START_TARGET][ch].min())

max_emg = max(max_emg)
min_emg = min(min_emg)
scaller_factor = max(max_emg, abs(min_emg))
#%%
for i in range(START_TARGET,END_TARGET):
    for ch in range(4):
        arduino_emg_sinals[i-START_TARGET][ch] = arduino_emg_sinals[i-START_TARGET][ch] / scaller_factor

#%% Generating arduino vectors
# const float emg_estender_wave[][] PROGMEM = {
#     {0.2, 0.2, 0.2, 13.3}, {0.2, 0.2, 0.2, 13.3}, {0.2, 0.2, 0.2, 13.3},
#     {0.2, 0.2, 0.2, 13.3}, {0.2, 0.2, 0.2, 13.3}, {0.2, 0.2, 0.2, 13.3},
#     {0.2, 0.2, 0.2, 13.3}, {0.2, 0.2, 0.2, 13.3}, {0.2, 0.2, 0.2, 13.3}};
arq = open("dados_gerados.h", 'w')
#arq = open("../Firmware/emg-four-channel-simulator/dados_gerados.h", 'w')
arq.write("""
// Arquivo gerado automaticamente através do script
// arduino_signal_simulator_gen.py
""")
arq.write("#include <avr/pgmspace.h> //for IDE versions below 1.0 (2011)\n")
fd = 2 # freq divider
valores_por_linha = 4
for i in range(START_TARGET,END_TARGET):
    vector_out = ""
    vector_name = targets_str[i].lower()
    q = len(arduino_emg_sinals[i-START_TARGET][0])
    vector_header = "const float emg_" + vector_name + "_wave[" +str(np.floor(q/fd).astype(int)) + "][4] PROGMEM = {\n"
    vector_data = "    "
    
    for k in range(0,np.floor(q/fd).astype(int),fd):
        vector_data += "{"
        for ch in range(4):
            v = arduino_emg_sinals[i-START_TARGET][ch][k]
            vector_data += "%f" % (v)
            if ch != 3:
                vector_data += ", "
        vector_data += "}"
        if k != (np.floor((q/fd)).astype(int)-fd):
            vector_data += ", "
        if (k+1)%valores_por_linha == 0:
            vector_data += "\n    "
    vector_out = vector_header + vector_data + "\n};\n"
    arq.write(vector_out)
arq.close()
