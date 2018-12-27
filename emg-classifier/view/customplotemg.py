# Description: Custom plot class for pyqtgraph embedded in PyQt Designer
# Author: github.com/PauloCamargos
# Dat: 08/12/2018

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.ptime import time
import pyqtgraph as pg
import numpy as np
from numpy import clip
import time as py_time
import serial
from collections import deque
from controller import ArduinoHandler
import logging

class CustomPlotEMG(pg.GraphicsWindow):
    """
    Implementing a custom class for the pyqtgraph module. 
    For more information, check out pyqtgraph documentation on 
    "Embedding widgets inside PyQt applications".
    """

    def __init__(self, parent=None, arduino_handler=None):
        """
        __init__
        
        Initilizaes a new class.
        
        Initializes a new CustomPlotEMG class. This class implements 
        a pyqtgraph realtime graph. 
        
        Parameters
        ----------
        parent : QWidget, optional
            the mother object (the default is None)
        arduino_handler : ArduinoHandler, 
            An ArduinoHandler object through which data 
            will arrive
        
        """

        #pg.setConfigOption('background', 'k')
        #pg.setConfigOption('foreground', 'k')
        pg.GraphicsWindow.__init__(self, parent=None)
        
        pg.setConfigOptions(antialias=True)          
        self.useOpenGL
        pg.setConfigOptions(useOpenGL=True)

        self.arduino_handler = arduino_handler
        self.arduino_handler.start_acquisition()
        
        # signal sampling frequency [Hz]
        self.sample_frequecy = 2000    
        # signal sample period [s] 
        self.sample_period = 1 / self.sample_frequecy 
         # window time [s] to show the signal
        self.show_time_window = 3 
        # obs.: Window time depends on FPS rate and other factors. 
        # It's a mere aproximation.

        # calculating the number of points that are going
        # to be plotted
        self.amount_of_points = int(self.show_time_window / (1 / self.sample_frequecy))
        
        # index of each point
        self.sample_index= self.amount_of_points   

        # array (deque) holding each channel value (y axis values)
        self.values_ch1 = deque([0]*self.amount_of_points,maxlen=self.amount_of_points) # [0] * self.amount_of_points 
        self.values_ch2 = deque([0]*self.amount_of_points,maxlen=self.amount_of_points) # [0] * self.amount_of_points 
        # x axis values
        self.x_tick = deque([x * self.sample_period for x in range(self.amount_of_points)], maxlen=self.amount_of_points)

        # frames per second 
        self.fps = 0
        self.show_fps = False
        self.lastTime = 0
       
        # creating each channel curve
        self.plot_ch1 = self.addPlot(title="CH1", row=1, col=1) 
        self.plot_ch2 = self.addPlot(title="CH2", row=2, col=1)

        # y axis limits
        limit = [-250,250]
        self.plot_ch1.setRange(yRange=limit)
        self.plot_ch2.setRange(yRange=limit)

        # adding legend
        # self.plot_ch1.addLegend()
        # self.plot_ch2.addLegend()
        
        # channel y labels
        self.plot_ch1.setLabel('left', 'CH1 [V]')
        self.plot_ch2.setLabel('left', 'CH2 [V]')

        # channels x labels
        self.plot_ch1.setLabel('bottom', 'Time', units='s')
        self.plot_ch2.setLabel('bottom', 'Time', units='s')


        # channels curves
        self.curva_ch1 = self.plot_ch1.plot(pen=pg.mkPen(color='g',width=0.9),name='CH1',)
        self.curva_ch2 = self.plot_ch2.plot(pen=pg.mkPen(color='r',width=0.9),name='CH2')
        
         # hiding x axis from ch1
        self.plot_ch1.hideAxis('bottom')

        # PyQt timer
        timer = pg.QtCore.QTimer(self)
        # Graph updater and arduino handler consumer
        timer.timeout.connect(self.update)  
        # interval between graph updates
        timer.start(0)

        # setting up a logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        st = logging.StreamHandler()
        st.setLevel(logging.DEBUG)
        st.setFormatter(logging.Formatter('[%(levelname)s] in %(name)s(%(lineno)d): %(message)s'))
        self.logger.addHandler(st)
        
    def consume_data(self):
        # num = queue.get(timeout=0.1)
        # # obtains the new value
        # num =  queue.popleft()
        # self.logger.info('Consumed')
        # queue.task_
        # self.values_ch1.append(num[0] - 500)
        # self.values_ch2.append(num[1] - 500)
        # # updating time axis tick 
        # self.x_tick.append(self.sample_index* self.sample_period)

        # # remove the oldest values                                
        # if len(self.values_ch1) > self.amount_of_points: 
        #     self.values_ch1.popleft()
        # if len(self.values_ch2) > self.amount_of_points:
        #     self.values_ch2.popleft()
        # if len(self.x_tick) > self.amount_of_points:
        #     self.x_tick.popleft()

        # # incresing the sample index
        # self.sample_index+= 1
        print('shittt')


    def update(self):
        """
        update
        
        Updates the graph plotting the points inside a vector
        
        Updates the data and the graph. This method acts like a 
        consumer of Arduino buffer data. 
        Important: Don't call this method by yourself. It's 
        running on a thread built by pyqtgraph.
        
        """

        if self.show_fps:
            self.calculate_fps()
            self.plot_ch1.setTitle('<font color="red">%0.2f fps</font>' % self.fps)

        # number of points to be updated
        points_to_add = len(self.arduino_handler.buffer_acquisition)
        # self.logger.info('points: {}'.format(points_to_add))

        if points_to_add > 0:
            for n in range(points_to_add): 
                 # obtains the new value
                num =  self.arduino_handler.buffer_acquisition.popleft()
                self.values_ch1.append(num[0] - 500)
                self.values_ch2.append(num[1] - 500)
                # updating time axis tick 
                self.x_tick.append(self.sample_index* self.sample_period)

                # remove the oldest values                                
                if len(self.values_ch1) > self.amount_of_points: 
                    self.values_ch1.popleft()
                if len(self.values_ch2) > self.amount_of_points:
                    self.values_ch2.popleft()
                if len(self.x_tick) > self.amount_of_points:
                    self.x_tick.popleft()

                # incresing the sample index
                self.sample_index+= 1
                
            # passing the array of values to plot       
            self.curva_ch1.setData(
                x=np.array(list(self.x_tick),dtype='float'), 
                y=np.array(list(self.values_ch1),dtype='float'))
            
            self.curva_ch2.setData(
                x=np.array(list(self.x_tick),dtype='float'), 
                y=np.array(list(self.values_ch2),dtype='float'))



    def calculate_fps(self):
        """
        If defined, it this method is called automatically by the update function.
        Updating the value of the fps attribute.
        """
        now = time()
        dt = now - self.lastTime
        self.lastTime = now
        if self.fps is None:
            self.fps = 1.0 / dt
        else:
            s = clip(dt * 3., 0, 1)
            self.fps = self.fps * (1 - s) + (1.0 / dt) * s


if __name__ == '__main__':
    arduino_handler = ArduinoHandler.ArduinoHandler.instance(port_name='COM3', baudrate=115200, qnt_ch=2)

    w = CustomPlotEMG(arduino_handler=arduino_handler)
    w.show()
    QtGui.QApplication.instance().exec_()
    arduino_handler.stop_acquisition()

