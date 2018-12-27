# EMG signal Classfier based on SVM 

## About the project
The EMGClassifier is a project aiming at 
the **acquisition of EMG** (electromyographic) signal, 
processing and classification **using SVM** (Suport Vector 
Machine) to **control a virtual prosthetic hand**.  

The project uses signal collected with signal 
conditioner. The processing of the signal is made using techniques such as 
frequency filters. For the SVM code, it uses features as RMS and MAV values. 
After processing and classification, commands are sent to a serious game 
to control a virtual prosthetic hand.

## How to use
TODO

## Main tools 

The main tools used at the development of this project are:  

1. Arduino for computer/signal conditioner interface.
1. Unity, for the serious game creationg
1. Python libraries, for the signal processing and 
machine learning algorithm and.
1. MQTT protocol with Mosquitto broker for Python/Unity communication.

The libraries used in this project, as well as installation instructions 
will be found at the `docs/installs.md` file.


