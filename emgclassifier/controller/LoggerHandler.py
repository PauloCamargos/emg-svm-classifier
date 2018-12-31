import logging

class LoggerHandler:

    def __init__(self, level='DEBUG', name='', log_file='', print_console=True):
        self.logger = logging.getLogger(name if name else 'undefined')

        self.logger.setLevel(getattr(logging, level.upper()))
        
        self.formatter =  '[%(levelname)s] in %(name)s: %(message)s'

        if log_file:
            self.file_handler.setLevel(level)
            self.file_handler =  logging.FileHandler(log_file)
            self.file_handler.setFormatter(logging.Formatter(self.formatter))
            self.logger.addHandler(self.file_handler)

        if print_console:
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(logging.Formatter(self.formatter))
            self.logger.addHandler(self.stream_handler)
        
    def debug(self, message):
        self.stream_handler.setLevel(logging.DEBUG)
        self.logger.debug(message)

    def info(self, message):
        self.stream_handler.setLevel(logging.INFO)
        self.logger.info(message)

    def warning(self, message):
        self.stream_handler.setLevel(logging.WARNING)
        self.logger.warning(message)

    def error(self, message):
        self.stream_handler.setLevel(logging.ERROR)
        self.logger.error(message)

    def critical(self, message):
        self.stream_handler.setLevel(logging.CRITICAL)
        self.logger.critical(message)

    
    