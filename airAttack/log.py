import logging

class Logger():
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger('')
    
    def debug(self, message):
        self.logger.debug(message)
        return
    def info(self, message):
        self.logger.info(message)
        return
    def warning(self, message):
        self.logger.warning(message)
        return
    def error(self, message):
        self.logger.error(message)
        return
    def critical(self, message):
        self.logger.critical(message)
        return
