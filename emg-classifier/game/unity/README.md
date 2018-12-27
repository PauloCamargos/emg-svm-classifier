This README.md contains the instructions the configure the project on Unity 3D.

# Tools
1. [Unity 3D](https://unity3d.com/pt/get-unity/download)  
1. [M2MqttUnity](https://github.com/gpvigano/M2MqttUnity) client (instructions bellow)
1. [Visual Studio 2017](https://visualstudio.microsoft.com/downloads/)  

        Obs.: The Unity version used in this project was 2018.2.17f1 (64-bit). Some stuff might need extra configurations if you use another version. Make sure to adapt correctly to you version. 

# Installs

### Unity 3D
1. Donwload [Unity 3D](https://unity3d.com/pt/get-unity/download)
1. Execute the installer
1. If asked in the installer, 

# Configuring Mqtt on Unity
In order to communicate Python with Unity (C#), you'll need to donwload and install the Mqtt libray for Unity.

1. Download or clone the [M2MqttUnity](https://github.com/gpvigano/M2MqttUnity) project.
This library can be found at `./libs/M2MqttUnity-master.zip`
1. Copy the files `M2MqttUnity-master/Assets/M2Mqtt` to your project. 
1. Create a new script in your project
1. The code to receive messages from Mqtt can be found at `Assets/Models/Scripts/Player.cs` script.