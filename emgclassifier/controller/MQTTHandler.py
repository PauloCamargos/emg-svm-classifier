# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLÂNDIA
# FEELT- Faculty of Electrical Engineering
# GRVA - Augumented and Virtual Reality Group
# ------------------------------------------------------------------------------
# Author: Paulo Camargos
# Date: 23/12/2018
# Contact: paulocamargoss@outlook.com
# Class: MQTTHandler
# ------------------------------------------------------------------------------
# Description: Module containing a handler class for the MQTT protocol for 
# Python and Mosquitto broker. The paho-mqtt module and the Mosquitto broker
# should already be installed.
# To test the module, simply run it.
# To install paho-mqtt module, visit https://pypi.org/project/paho-mqtt/ and
# follow the given instructions.
# To install the Mosquitto broker, visit 
# http://www.steves-internet-guide.com/install-mosquitto-broker/ 
# and follow the given instructions. 
# ------------------------------------------------------------------------------
import os
import platform
import paho.mqtt.client as mqtt
from time import sleep
import logging
# ------------------------------------------------------------------------------



class MQTTHandler:
    """
    MQTTHandler
    
    Class for handling MQTT protocol with the Mosquitto broker.
    
    MQTTHandler Class for handling connections and messagens using the MQTT 
    protocol with the Mosquitto broker. For example of use, checkout 
    the test() function at the end of this module.
    """

    def __init__(self, broker='127.0.0.1', client_name='client', topic='topic', port=1883, receive_message_back=False):
        """
        __init__
        
        Initializes the class.
        
        Initializes the class with the passed parameters or the default ones.
        
        Parameters
        ----------
        broker : str, optional
            The Mosquitto broker addres (the default is '127.0.0.1', which is most used)
        client_name : str, optional
            Name of the client (the default is 'client', which can be set to anything)
        topic : str, optional
            Topic under which all messages are going to be published 
            (the default is 'topic', which can be set to anything)
        port : int, optional
            The broker port to be opened (the default is 1883, which is the MQTT default)
        receive_message_back : bool, optional
            Signalizes if the publised messages should also be shown after reception
            (the default is False, which will not show received messages)
        """

        self.broker = broker
        self.client = mqtt.Client(client_name)
        self.topic = topic
        self.receive_message_back = receive_message_back
        self.port = port

        self.setup_callback_methods()

        # setting up a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        st = logging.StreamHandler()
        st.setLevel(logging.DEBUG)
        st.setFormatter(logging.Formatter('[%(levelname)s] in %(name)s(%(lineno)d): %(message)s'))
        self.logger.addHandler(st)
    
    def setup_callback_methods(self):
        """
        setup_callback_methods
        
        Sets up the callback functions.
        
        These functions are called after an event is finished.
        """

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnet
        self.client.on_log = self.on_log
        self.client.on_message = self.on_message  

    def open_mosquitto_broker(self):
        """
        open_mosquitto_broker
        
        Opens a new Mosquitto server
        
        Opens a new Mosquitto server with defined broker address and port.
        This should be called once after instatiation of the class.
        This step might be skipped if a broker is already running.
        """

        self.logger.info('Opening Mosquitto broker...')
        if platform.system() == 'Linux':
            self.mosquitto_broker = os.popen('mosquitto -d')
        else:
            self.mosquitto_broker = os.popen('mosquitto')

        self.logger.info('Success! Mosquitto sever running.')

    def close_mosquitto_broker(self):
        """
        close_mosquitto_broker
        
        Closes the opened Mosquitto server.
        
        Closes the opened Mosquitto server. This should be called 
        if the object is not going to be used anymore.
        
        """

        code =  self.mosquitto_broker.close()
        self.logger.info('Finished Mosquitto broker. Code: {}'.format(code))
        
    def on_log(self, client, userdata, level, buf):
        """
        on_log
        
        mqtt class overwrite. 
        
        Show log messages. This class is set to be a callback method.
        
        Parameters
        ----------
        client : mqtt.Client
            An initialized client.
        userdata : [type]
            [description]
        level : [type]
            [description]
        buf : string
            The returned log message
        
        """

        self.logger.info(buf)

    def on_connect(self, client, userdata, flags, rc):
        """
        on_connect
        
        mqtt class overwrite.
        
        Confirms if a connection was made. This class is set to be a callback method.
        
        Parameters
        ----------
        client : mqtt.Client
            An initialized client.
        userdata : [type]
            [description]
        flags : [type]
            [description]
        rc : int
            Confirmation code.
        
        """

        if rc==0:
            self.logger.info('Connection made with Mosquitton broker')
        else:
            self.logger.error('Connection NOT made with Mosquitton broker. Code: {}'.format(rc))

    def on_disconnet(self, client, userdata, flags, rc=0):
        """
        on_disconnet
        
        mqtt class overwrite.
        
        Confirms if a disconnection was made. This class is set to be a callback method.
        
        Parameters
        ----------
        client : mqtt.Client
            An initialized client.
        userdata : [type]
            [description]
        flags : [type]
            [description]
        rc : int, optional
            Confirmation code (the default is 0, which represents success).
        
        """

        self.logger.info('Disconnected. Code: {}'.format(rc))

    def on_message(self, client,userdata, msg):
        """
        on_message
        
        mqtt class overwrite.
        
        Prints the received message under the subscribed topic.
        
        Parameters
        ----------
        client : mqtt.Client
            An initialized client.
        userdata : [type]
            [description]
        msg : MQTTMessage
            The received message.
        
        """
        
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        self.logger.info('Received message') 
        self.logger.info('\n> Topic: {}\n> Message: {}'.format(topic, m_decode))

    def relay_message(self, message):
        """
        relay_message
        
        Publishes a message under the topic given on object construction.
        
        Connects the client, publishes a message and 
        disconnect the client.
        
        Parameters
        ----------
        message : string
            The message to be published.
        
        """
        
        if message is not None:
            self.connect_client()
            self.client.publish(self.topic, message)            
            self.disconnet_client()
        else:
            self.logger.error('No messagem to relay')

    def connect_client(self):
        """
        connect_client
        
        Connects and subscribe the client.
        
        Creates a new connection and subscribes the client
        to the specified topic on class construction. Case 
        the received_message_back is set to True, starts
        a new loop for showing the received messages.
        
        """

        self.client.connect(self.broker,port=self.port)
        # subscribing to topic
        self.client.subscribe(self.topic)
        if self.receive_message_back:
            # if wants to see the received message.
            self.client.loop_start()
            sleep(0.001)

    def disconnet_client(self):
        """
        disconnet_client
        
        Disconnects the client.
        
        Disconnects the client and stops the loop for showing message, 
        case the receive_message_back is set to True.
        
        """


        if self.receive_message_back:
            sleep(0.001)
            self.client.loop_stop()
        self.client.disconnect()

def test():
    """
    test
    
    Testing function.
    
    Instatiates a new MQTTHandler object, 
    publishes and shows a message.
    
    """

    mqtt_connection = MQTTHandler(topic='testing',receive_message_back=True)
    mqtt_connection.open_mosquitto_broker()
    mqtt_connection.relay_message("This message will sure be passed on!")
    mqtt_connection.close_mosquitto_broker()


if __name__ == '__main__':
    test()    
