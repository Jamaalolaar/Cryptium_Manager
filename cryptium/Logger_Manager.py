import logging

class LoggerManager:
    """
    Manages and configures separate loggers for info and error messages
    """
    def __init__(self, config):
        """
        Initialize Logger_Manager with separate info and error loggers

        self: Instance of Logger_Manager
        info_log_file: Path to the info log file
        error_log_file: Path to the error log file
        """
        self.config_data = config.config_data.get('log_files', {})
        info_log_file = self.config_data.get('log_files', {}).get('Info_log', 'Info Logs.log')
        error_log_file = self.config_data.get('log_files', {}).get('Error_log', 'Error logs.log')
        self.info_logger = self._setup_logger("info_logger", info_log_file)
        self.error_logger = self._setup_logger("error_logger",error_log_file)
    def _setup_logger(self, name, log_file):
        """
        Create and configure a logger that writes debug messages to a specified file

        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        #Handler Creation
        handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
    def log_info(self, message):
        """Logs info"""
        self.info_logger.info(message)
    def log_error(self, message):
        """Logs error"""
        self.error_logger.error(message)