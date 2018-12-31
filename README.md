# EMG signal Classfier based on SVM for virtual prosthetic hand control

## About the project
The EMG Classifier is a project aiming at 
the **acquisition of EMG** (electromyographic) signal, 
processing and classification **using SVM** (Suport Vector 
Machine) to **control a virtual prosthetic hand**.  

The project uses signal collected with a signal 
conditioner. For the SVM code, it uses features as RMS and MAV values. 
After processing and classification, commands are sent to a serious game 
to control a virtual prosthetic hand.

## How to use
To **install the tools** used in this project, go to the `docs/installs.md` file and follow its instructions.

## Main tools 

The main tools used at the development of this project are:  

1. Arduino for PC and Signal Conditioner interface.
1. Unity, for the serious game development
1. Python libraries, for the signal processing and 
machine learning algorithm and.
1. MQTT protocol with Mosquitto broker for Python and Unity communication.

The libraries used in this project, as well as installation instructions 
will be found at the `docs/installs.md` file.


