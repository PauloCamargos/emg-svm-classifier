# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# Author: Italo Gustavo Sampaio Fernandes
# Contact: italogsfernandes@gmail.com
# Git: www.github.com/italogsfernandes
# Modified: Paulo Camargos
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
import serial
import serial.tools.list_ports as serial_tools
from ctypes import c_short
from .ThreadHandler import ThreadHandler, InfiniteTimer
import sys
if sys.version_info.major == 2:
    from Queue import Queue
else:
    from queue import Queue
    from collections import deque
# ------------------------------------------------------------------------------


class ArduinoConstants:
    """
    Save here the constants with the arduino communication.
    CONSTANTS:
    ---------
    PACKET_SIZE : Size of the packet including the starter and end bytes.
                For a packet being: '$' | DATA_MSB | DATA_LSB | '\n' - the size is 4 bytes.
    PACKET_START : This is what is expected to be in the beginning of each packet.
    PACKET_END : Only packets with this byte in the end is considered as valid.
    MANUFACTURER : It is used to search the arduino port between all the others serial ports.
    """
    PACKET_SIZE = 6
    PACKET_START = '$'
    PACKET_END = '\n'
    MANUFACTURER = 'Arduino (www.arduino.cc)'
    DUE_description = 'Arduino Due Prog. Port'
    UNO_description = 'ttyACM1'
    HINA_NANO_description = 'USB2.0-Serial'
    DUE_manufacturer = 'Arduino (www.arduino.cc)'
    UNO_manufacturer = 'Arduino (www.arduino.cc)'
    CHINA_NANO_manufacture = ''
    DUE_product = 'Arduino Due Prog. Port'
    UNO_product = ''
    CHINA_NANO_product = 'USB2.0-Serial'


class ArduinoHandler:
    """
    This class handles all the communication with a arduino board.

    It has a serialPort Object, a Buffer and a Thread for acquisition.
    Parameters
    ----------
    port_name : String containing the name of the serial port.
                Examples are: 'COM3', 'COM4', '/dev/ttyACM0'
                If it's not set, a compatible port will be searched.
    baudrate : The speed of the communication, in bits per second.
                As the communications is an asynchronous one, it should be
                set here the same of is in the arduino code.
    Examples
    --------
    See the code of the test function in this file for two command line examples.
    """

    __instance = None

    def __init__(self, port_name=None, baudrate=115200, qnt_ch=1):
        self.qnt_ch = qnt_ch
        if port_name is None:
            port_name = ArduinoHandler.get_arduino_serial_port()
        self.serial_tools_obj = None
        if len(serial_tools.comports()):
            self.serial_tools_obj = [s for s in serial_tools.comports() if s.device == port_name][0]
        self.serialPort = serial.Serial()
        self.serialPort.port = port_name
        self.serialPort.baudrate = baudrate
        self.thread_acquisition = ThreadHandler(self.acquire_routine, self.close)
        self.buffer_acquisition = deque(maxlen=1024*1)

    def update_port_name(self):
        self.serial_tools_obj = None
        self.serialPort.port = ArduinoHandler.get_arduino_serial_port()

        if len(serial_tools.comports()):
            self.serial_tools_obj = [s for s in serial_tools.comports() if s.device == str(self.serialPort.name)][0]
        if not self.serial_tools_obj is None:
            return self.serial_tools_obj.description + " on " + self.serialPort.port
        else:
            return "Nothing found."

    @property
    def data_waiting(self):
        """
        The size of the acquisition buffer
        """
        return len(self.buffer_acquisition)

    def open(self):
        """
        If it is not already open, it will open the serial port and flush its buffers.
        """
        if not self.serialPort.isOpen():
            self.serialPort.open()
            self.serialPort.flushInput()
            self.serialPort.flushOutput()

    def close(self):
        """
        If the serial port is open, this method will try to close it.
        """
        if self.serialPort.isOpen():
            self.serialPort.close()

    def start_acquisition(self):
        """
        Opens the serial port and starts a thread for acquisition.
        The read objects will be in the buffer_acquisition.
        """
        self.open()
        self.thread_acquisition.start()

    def stop_acquisition(self):
        """
        Let the thread for acquisition reaches its end and, when it finally happens,
        closes the serial port.
        """
        self.thread_acquisition.stop()

    @staticmethod
    def get_arduino_serial_port():
        """
        Tries to found a serial port compatible.

        If there is only one serial port available, return this one.

        Otherwise it will verify the manufacturer of all serial ports
        and compares with the manufacturer defined in the ArduinoConstants.
        This method will return the first match.

        If no one has found, it will return a empty string.
        :return: Serial Port String
        """
        serial_ports = serial_tools.comports()
        if len(serial_ports) == 0:
            return ""
        if len(serial_ports) == 1:
            return serial_ports[0].device
        for serial_port_found in serial_ports:
            if serial_port_found.manufacturer == ArduinoConstants.MANUFACTURER:
                return serial_port_found.device
        return ""

    @staticmethod
    def to_int16(msb_byte, lsb_byte):
        """
        Concatenate two bytes(8 bits) into a word(16 bits).

        It will shift the msb_byte by 8 places to the right,
        then it will sum the result with the lsb_byte.

        :param msb_byte: The most significant byte.
        :param lsb_byte: The less significant byte.
        :return: The word created by the two bytes.
        """
        return c_short((msb_byte << 8) + lsb_byte).value

    def acquire_routine(self):
        """
        This routine is automatically called by the acquisition thread.
        Do not call this by yourself.

        Description
        -----------
        If the serial port is open and there is more than the size of one
        packet in the buffer. It will:
             - verify the starter byte;
             - read the data in the packet;
             - verify the end byte;
             - Put the read packet in a buffer (Queue).
        """
        if self.serialPort.isOpen():
            if self.serialPort.inWaiting() >= ArduinoConstants.PACKET_SIZE:
                _starter_byte = self.serialPort.read()
                if chr(ord(_starter_byte)) == ArduinoConstants.PACKET_START:
                    if self.qnt_ch == 1:
                        _msb = self.serialPort.read()
                        _lsb = self.serialPort.read()
                        _msb = ord(_msb)
                        _lsb = ord(_lsb)
                        _value_to_put = ArduinoHandler.to_int16(_msb, _lsb)
                    else:
                        _value_to_put = []
                        for n in range(self.qnt_ch):
                            _msb = self.serialPort.read()
                            _lsb = self.serialPort.read()
                            _msb = ord(_msb)
                            _lsb = ord(_lsb)
                            _value_to_put.append(ArduinoHandler.to_int16(_msb, _lsb))
                    _end_byte = self.serialPort.read()
                    if chr(ord(_end_byte)) == ArduinoConstants.PACKET_END:
                        self.buffer_acquisition.append(_value_to_put)

    def __str__(self):
        return "ArduinoHandlerObject" +\
               "\n\tSerialPort: " + str(self.serial_tools_obj.device) +\
               "\n\tDescription: " + str(self.serial_tools_obj.description) +\
               "\n\tOpen: " + str(self.serialPort.isOpen()) +\
               "\n\tAcquiring: " + str(self.thread_acquisition.isRunning) +\
               "\n\tInWaiting: " + str(self.serialPort.inWaiting() if self.serialPort.isOpen() else 'Closed') +\
               "\n\tBufferAcq: " + str(len(self.buffer_acquisition))

    def get_buffers_status(self, separator):
        """
        Returns a string like:
            Serial:    4/1024 - Acq:    1/1024
        :param separator: Separates the strings, example ' - ', ' | ', '\n'
        :return: A string containing the status of all the buffers involved in the acquisition
        """
        return "Serial: %4d" % (self.serialPort.inWaiting()/4 if self.serialPort.isOpen() else 0) + '/' + str(4096/4) +\
               separator + "Acq: %4d" % (len(self.buffer_acquisition)) + '/' + str(self.buffer_acquisition.maxlen)

    @staticmethod
    def instance(port_name, baudrate, qnt_ch):
        """
        Creates an instance of the ArduinoHandler class:
        :return: An ArduinoHandler object.
        """

        if not ArduinoHandler.__instance:
            ArduinoHandler.__instance = ArduinoHandler(port_name=port_name, baudrate=baudrate, qnt_ch=qnt_ch)
        print('[OK] Arduino connection started successfully')
        return ArduinoHandler.__instance


def test():
    my_arduino_handler = ArduinoHandler(port_name='COM3',qnt_ch=2)

    def printer():
        if my_arduino_handler.data_waiting:
            print(my_arduino_handler.buffer_acquisition.pop())
            # time.sleep(0.01) # Uncomment if you want to see the buffer_acquisition to get full

    consumer_thr = ThreadHandler(printer)

    # Uncomment this to act as a data logger:
    # from datetime import datetime
    # horario = datetime.now()
    # arq = open("leituras-" + str(horario) + '-dados.txt', 'w')
    # arq.write("Leituras salvas com Arduino Handler - Datetime: " + str(horario) + "\n")
    # arq.write("leituras = [")
    # def saver():
    #    if my_arduino_handler.data_waiting:
    #        arq.write(str(my_arduino_handler.buffer_acquisition.pop()))
    #        arq.write(', ')
    # consumer_thr = ThreadHandler(saver)

    def show_status():
        print(my_arduino_handler)

    status_timer = InfiniteTimer(1, show_status)
    while True:
        print('-------------------------------')
        print(my_arduino_handler)
        print('-------------------------------')
        print('Menu')
        print('-------------------------------')
        print('start - Automatically Starts Everything')
        print('stop - Automatically Stops Everything')
        print('q - Quit')
        print('-------------------------------')
        print('op - open() ')
        print('cl - close()')
        print('ra - readall()')
        print('sth - start Consumer')
        print('pth - pause Consumer')
        print('rth - resume Consumer')
        print('kth - kill Consumer')
        print('sacq - start Aquisition')
        print('kacq - kill Aquisition')
        print('-------------------------------')

        if sys.version_info.major == 2:
            str_key = raw_input()
        else:
            str_key = input()

        if 'q' in str_key:
            my_arduino_handler.stop_acquisition()
            consumer_thr.stop()
            status_timer.stop()
            break
        elif 'op' in str_key:
            my_arduino_handler.open()
        elif 'cl' in str_key:
            my_arduino_handler.close()
        elif 'ra' in str_key:
            print(my_arduino_handler.serialPort.read_all())
        elif 'sth' in str_key:
            status_timer.start()
            consumer_thr.start()
        elif 'pth' in str_key:
            consumer_thr.pause()
        elif 'rth' in str_key:
            consumer_thr.resume()
        elif 'kth' in str_key:
            status_timer.stop()
            consumer_thr.stop()
        elif 'sacq' in str_key:
            status_timer.start()
            my_arduino_handler.start_acquisition()
        elif 'kacq' in str_key:
            status_timer.stop()
            my_arduino_handler.stop_acquisition()
        elif 'start' in str_key:
            status_timer.start()
            consumer_thr.start()
            my_arduino_handler.start_acquisition()
        elif 'stop' in str_key:
            status_timer.stop()
            my_arduino_handler.stop_acquisition()
            consumer_thr.stop()


if __name__ == '__main__':
    test()
