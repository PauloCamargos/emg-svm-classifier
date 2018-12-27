# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# FEDERAL UNIVERSITY OF UBERLANDIA
# Faculty of Electrical Engineering
# Biomedical Engineering Lab
# ------------------------------------------------------------------------------
# Author: Andrei Nakagawa, MSc
# Contact: nakagawa.andrei@gmail.com
# Class: ThreadHander
# Modifications: Italo G S Fernandes
#                 (italogsfernandes@gmail.com, github.com/italogsfernandes)
#                Paulo Camargos
#                  (paulocamargoss@outlook.com), github.com/PauloCamargos
# ------------------------------------------------------------------------------
# Description:
# ------------------------------------------------------------------------------
from threading import Thread
from threading import Event
# ------------------------------------------------------------------------------


class ThreadHandler:
    """
    Handles a Thread Object in a way to call a worker function
    repeatedly.
    
    Parameters
    ----------
    worker : function
        The function to be called repeatedly
    on_end_function : function
        If defined, it will be called on the end of the thread.

    Example
    -------
    Creates a function to be called.
    >> def my_function():
    ...    print('Hello')
    Instantiate ThreadHandler Object
    >> my_thread_handler = ThreadHandler(my_function)
    Starts the thread:
    >> my_thread_handler.start()
    Output:
    >> Hello
    >> Hello
    ...
    """
    def __init__(self, worker=None, is_daemon=True, on_end_function=None):
        self.thread = Thread(target=self.run)
        self.worker = worker
        self.is_daemon = is_daemon # True if worker should be executed repeteadly
        self.on_end_function = on_end_function
        self.isAlive = False
        self.isRunning = False
        self.isFinished = False
        

    def start(self, args=None):
        """
        Starts to repeatedly (if it's daemon) call the worker 
        function. If it's not daemon, execute only once. 
        Argumets should be passed only for non daemon
        worker function.
        
        This method assigns a new Thread Object to the thread
        (allowing to be called more than once).
        It actives the flags isAlive and isRunning,
        calls the start method of the ThreadObject and
        sets the isFinished flag to False.
        
        Only works if the flag isAlive is False.
        
        See Also
        --------
        pause, resume, stop
        """
        if self.is_daemon:
            if not self.isAlive:
                self.thread = Thread(target=self.run)
                self.isAlive = True
                self.isRunning = True
                self.thread.start()
                self.isFinished = False
        else:
            if args is not None:
                self.thread = Thread(target=self.run, args=args)
                self.thread.start()
            else:
                self.thread = Thread(target=self.run)
                self.thread.start()

    def pause(self):
        """
        Pauses the call of the worker function.
        
        This method sets the isRunning flag to False.
        
        See Also
        --------
        resume, start, stop
        """
        self.isRunning = False

    def resume(self):
        """
        If the calling of the worker if paused,
        this method resumes the calling.
        
        This method sets the isRunning flag to True.
        
        See Also
        --------
        pause, start, stop
        """
        self.isRunning = True

    def stop(self):
        """
        Stops the calling of the worker function.
        Letting the thread to reach its end.
        
        This method sets the isAlive flag to False.
        Also sets the isRunning flag to False.
        
        See Also
        --------
        pause, start, stop
        """
        self.isAlive = False
        self.isRunning = False

    def run(self, args=None):
        """
        This is the target of the Thread Object,
        
        Do not call it by yourself, it is supposed to run
        in a separated Thread.
        
        It consists of a loop that calls the worker function
        repeatedly if the isRunning Flag is active. When the
        isAlive flag is set to False, the loop will not
        repeat, is there is a on_end_function set it will
        be called, after it the Thread will end.
        """
        if self.is_daemon:
            while self.isAlive:
                if self.isRunning:
                    if self.worker is not None:
                        self.worker()
        else:
            if args is not None:
                self.worker(args)
            else:
                self.worker()

        if self.on_end_function is not None:
            self.on_end_function()
        
        self.isFinished = True

    def __str__(self):
        return "ThreadHandler Object" +\
               "\n\tAlive: " + str(self.isAlive) +\
                "\n\tRunning: " + str(self.isRunning) +\
                "\n\tFinished: " + str(self.isFinished) +\
                "\n\tWorker: " + str(self.worker) +\
                "\n\tEndFuction: " + str(self.on_end_function)


class InfiniteTimer(ThreadHandler):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, worker, on_end_function=None, args=[], kwargs={}):
        ThreadHandler.__init__(self)
        self.interval = interval
        self.worker = worker
        self.on_end_function = on_end_function
        self.args = args
        self.kwargs = kwargs
        self.waiter = Event()

    def run(self):
        """
        This is the target of the Thread Object,

        Do not call it by yourself, it is supposed to run
        in a separated Thread.

        It consists of a loop that calls the worker function
        repeatedly if the isRunning Flag is active. When the
        isAlive flag is set to False, the loop will not
        repeat, is there is a on_end_function set it will
        be called, after it the Thread will end.
        """
        while self.isAlive:
            if self.isRunning:
                self.waiter.wait(self.interval)
                self.worker()
        if self.on_end_function is not None:
            self.on_end_function()
        self.isFinished = True


if __name__ == '__main__':              # if we're running file directly and not importing it
    from time import sleep
    from datetime import datetime

    def counter():
        print('-'*10)
        print("Next 10 seconds:")
        for n in range(10, 0, -1):
            print(str(n) + ": " + str(datetime.now()))
            sleep(1)

    myThreadHandler = ThreadHandler(counter)

    def show_time():
        print(str(datetime.now()))

    myInfiniteTimer = InfiniteTimer(1, show_time)

    while True:
        print('-------------------------------')
        print(myThreadHandler)
        print('-------------------------------')
        print('Menu')
        print('*' * 5 + 'Thread' + '*' * 5)
        print('st - start() ')
        print('sp - stop()')
        print('p - pause()')
        print('r - resume()')
        print('*' * 5 + 'Timer' + '*' *5)
        print('stt - start() ')
        print('spt - stop()')
        print('pt - pause()')
        print('rt - resume()')
        print('-------------------------------')
        print('q - Quit')
        print('-------------------------------')
        import sys
        if sys.version_info.major == 2:
            str_key = raw_input()
        else:
            str_key = input()
        if str_key == 'q':
            myThreadHandler.stop()
            myInfiniteTimer.stop()
            break
        elif str_key == 'st':
            myThreadHandler.start()
        elif str_key == 'sp':
            myThreadHandler.stop()
        elif str_key == 'p':
            myThreadHandler.pause()
        elif str_key == 'r':
            myThreadHandler.resume()
        elif str_key == 'stt':
            myInfiniteTimer.start()
        elif str_key == 'spt':
            myInfiniteTimer.stop()
        elif str_key == 'pt':
            myInfiniteTimer.pause()
        elif str_key == 'rt':
            myInfiniteTimer.resume()