# Description: Module joining all other separeta modulos, such as PyQt Gui interface, Unity Com and SVM processing
# Author: Paulo Camargos
# Date: 08/12/2018

from PyQt5.QtWidgets import *
from controller import MQTTHandler, ArduinoHandler, ThreadHandler
from view import main_window # qt user interface file
import sys
import os
from threading import Thread
from view import customplotemg
import time as py_time
import logging

class EmgSvmApp(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(EmgSvmApp, self).__init__(parent)
        self.setupUi(self)
        # Setting up the buttons to their respective methods
        self.setup_buttons_connections()  

        self.movements = {1:'abre', 2:'fecha', 3:'flexao', 4:'extensao', 5:'supinacao', 6:'pronacao'}              

        # MQTT client
        self.mqtt_client = MQTTHandler.MQTTHandler(
            client_name='emg_svm',
            topic='move',
            receive_message_back=True)
        self.mqtt_client.open_mosquitto_broker()

        # thread for relaying the movement code
        self.movement_thread = ThreadHandler.ThreadHandler(
            worker=self.mqtt_client.relay_message,
            is_daemon=False, # False: will be executed only once
            on_end_function=self.unlock_all_buttons)

        # Pyqtgraph custom widget for plotting 
        self.signal_plotter = customplotemg.CustomPlotEMG(
            arduino_handler=ArduinoHandler.ArduinoHandler.instance(
                port_name='/dev/ttyACM0',#'COM3', 
                baudrate=115200, 
                qnt_ch=2))
        # Adding the pyqtgraph widget to main_window
        self.GraphLayoutPlaceholder.addWidget(self.signal_plotter)

        # setting up a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        st = logging.StreamHandler()
        st.setLevel(logging.DEBUG)
        st.setFormatter(logging.Formatter('[%(levelname)s] in %(name)s(%(lineno)d): %(message)s'))
        self.logger.addHandler(st)

    def setup_buttons_connections(self):
        """
            Sets up the buttons to their respective methods and initial miscellaneous configurations. 
        """
        self.btn_rest.clicked.connect(self.execute_rest_movement)
        self.btn_open.clicked.connect(self.execute_open_movement)
        self.btn_close.clicked.connect(self.execute_close_movement)
        self.btn_extension.clicked.connect(self.execute_extension_movement)
        self.btn_flexion.clicked.connect(self.execute_flexion_movement)
        self.btn_supination.clicked.connect(self.execute_supination_movement)
        self.btn_pronation.clicked.connect(self.execute_pronation_movement)

    ### clicked.connect methods
    def execute_rest_movement(self):
        self.statusBar.showMessage('Retornando ao descanso')
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.movement_thread.start(args=(self.movements.get(1),))
        self.logger.info("Executing 'REST' movement...")

    def execute_open_movement(self):
        self.statusBar.showMessage('Executando movimento de abertura')
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.movement_thread.start(args=(self.movements.get(1),))
        self.logger.info("[INFO] Executing 'OPEN' movement...")


    def execute_close_movement(self):
        self.statusBar.showMessage('Executando movimento de fechamento')
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.movement_thread.start(args=(self.movements.get(2),))
        self.logger.info("[INFO] Executing 'CLOSE' movement...")

    def execute_flexion_movement(self):
        self.statusBar.showMessage('Executando movimento de flexão')
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.movement_thread.start(args=(self.movements.get(3),))
        self.logger.info("[INFO] Executing 'FLEXION' movement...")
        
    def execute_extension_movement(self):
        self.statusBar.showMessage('Executando movimento de extensão')
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.movement_thread.start(args=(self.movements.get(4),))
        self.logger.info("[INFO] Executing 'FLEXION' movement...")

    def execute_supination_movement(self):
        self.statusBar.showMessage('Executando movimento de supinação')
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.movement_thread.start(args=(self.movements.get(5),))
        self.logger.info("[INFO] Executing 'FLEXION' movement...")

    def execute_pronation_movement(self):

        self.statusBar.showMessage('Executando movimento de pronação')
        # Blocking all buttuns until the move is not completed.
        self.lock_all_buttons() 
        # Sending the move code and starting it's thread.
        self.movement_thread.start(args=(self.movements.get(6),))
        self.logger.info("[INFO] Executing 'FLEXION' movement...")

    def lock_all_buttons(self):
        """Blocks all move buttons"""
        self.btn_rest.setEnabled(False)
        self.btn_open.setEnabled(False)
        self.btn_close.setEnabled(False)
        self.btn_extension.setEnabled(False)
        self.btn_flexion.setEnabled(False)
        self.btn_supination.setEnabled(False)
        self.btn_pronation.setEnabled(False)
    
    def unlock_all_buttons(self):
        """Unlock all buttons. This function is called at the end
        of the self.thread_executing_move"""
        self.btn_rest.setEnabled(True)
        self.btn_open.setEnabled(True)
        self.btn_close.setEnabled(True)
        self.btn_extension.setEnabled(True)
        self.btn_flexion.setEnabled(True)
        self.btn_supination.setEnabled(True)
        self.btn_pronation.setEnabled(True)


def main():
    try:
        app = QApplication(sys.argv)
        form = EmgSvmApp()
        form.show()
        app.exec_()
        # halting the signal acquisition, thus releasing the thread
        form.signal_plotter.arduino_handler.stop_acquisition()
        # ending the mosquitto server
        form.mqtt_client.close_mosquitto_broker()
    except Exception as e:
        logging.error("Unexpected error: ",e)
        raise
    finally:
        logging.warning("Finished application")


if __name__ == "__main__":
    # Executing the interface
    main()
