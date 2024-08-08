import logging
from termcolor import colored


# The ColoredLogger class is a custom logging handler that extends the built-in StreamHandler.
# It overrides the emit method to add color to the output messages based on their logging level.
class ColoredLogger(logging.StreamHandler):

    # A dictionary mapping logging levels to their corresponding colors.
    COLORS = {
        logging.DEBUG: 'blue',
        logging.INFO: 'green',
        logging.WARNING: 'yellow',
        logging.ERROR: 'red',
        logging.CRITICAL: 'magenta',
    }

    # The emit method is overridden to add color to the output messages.
    # It first formats the record, then retrieves the color corresponding to the record's level,
    # and finally writes the colored message to the stream.
    def emit(self, record):
        try:
            message = self.format(record)
            color = self.COLORS.get(record.levelno)
            self.stream.write(colored(message, color) + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


# The CustomLogger class is a wrapper around the built-in Logger class.
# It sets up a colored logger with a given application name.
class CustomLogger:
    def __init__(self, application_name: str):
        """
        Initialize a new instance of the CustomLogger class.

        :param application_name: The name of the application. This will be used as the logger name.
        """
        # Get a logger with the given application name.
        self.logger = logging.getLogger(application_name)

        # Set up a colored logger handler and add it to the logger.
        handler = ColoredLogger()
        formatter = logging.Formatter('%(levelname)s - %(filename)s:%(lineno)d - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


if __name__ == '__main__':
    log = CustomLogger('Test').logger
    log.setLevel(logging.DEBUG)
    log.debug('Debug message')
    log.info('Info message')
    log.warning('Warning message')
    log.error('Error message')
    log.critical('Critical message')