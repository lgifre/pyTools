import logging, os
from Lib.ParameterChecking import checkAttr, checkOptions, checkString
from logging import _levelNames

class LoggerConfigurator(object):
    SEVERITY = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
        logging.getLevelName(logging.CRITICAL),
        logging.getLevelName(logging.ERROR),
        logging.getLevelName(logging.WARNING),
        logging.getLevelName(logging.INFO),
        logging.getLevelName(logging.DEBUG)
    ]
    DEFAULT_SEVERITY = logging.DEBUG
    DEFAULT_FORMATTER = '[%(asctime)s] %(levelname)-7s %(name)-15s : %(message)s'
    
    def __init__(self):
        self.__logger = logging.getLogger('')
        self.__logger.setLevel(LoggerConfigurator.DEFAULT_SEVERITY)

        self.__screenHandler = logging.StreamHandler()
        self.__screenHandler.setLevel(LoggerConfigurator.DEFAULT_SEVERITY)
        self.__screenHandler.setFormatter(logging.Formatter(LoggerConfigurator.DEFAULT_FORMATTER))
        self.__logger.addHandler(self.__screenHandler)

        self.__fileHandler = None
    
    @staticmethod
    def checkConfiguration(config):
        checkOptions('screenSeverity', checkAttr('screenSeverity', config), LoggerConfigurator.SEVERITY)
        if('screenFormatter' in config): checkString('screenFormatter', config['screenFormatter'])

        checkOptions('fileSeverity', checkAttr('fileSeverity', config), LoggerConfigurator.SEVERITY)
        checkString('fileName', checkAttr('fileName', config))
        if('fileFormatter' in config): checkString('fileFormatter', config['fileFormatter'])

    @staticmethod
    def getDefaultConfig(logFilePath):
        return({
            'screenSeverity': 'INFO',
            'screenFormatter': '[%(asctime)s] %(levelname)-7s %(name)-10s: %(message)s',
            'fileSeverity': 'INFO',
            'fileFormatter': '[%(asctime)s] %(levelname)-7s %(name)-10s: %(message)s',
            'fileName': logFilePath
        })

    def configure(self, config):
        LoggerConfigurator.checkConfiguration(config)

        if(self.__screenHandler is not None): self.__logger.removeHandler(self.__screenHandler)
        self.__screenHandler.setLevel(config['screenSeverity'])
        self.__screenHandler.setFormatter(logging.Formatter(config.get('screenFormatter', LoggerConfigurator.DEFAULT_FORMATTER)))
        self.__logger.addHandler(self.__screenHandler)

        if(self.__fileHandler is not None): self.__logger.removeHandler(self.__fileHandler)
        self.__fileHandler = logging.FileHandler(config['fileName'])
        self.__fileHandler.setLevel(config['fileSeverity'])
        self.__fileHandler.setFormatter(logging.Formatter(config.get('fileFormatter', LoggerConfigurator.DEFAULT_FORMATTER)))
        self.__logger.addHandler(self.__fileHandler)

    def getConfig(self):
        return({
            'screenSeverity': _levelNames[self.__screenHandler.level],
            'screenFormatter': self.__screenHandler.formatter._fmt,
            'fileSeverity': _levelNames[self.__fileHandler.level],
            'fileFormatter': self.__fileHandler.formatter._fmt,
            'fileName': os.path.relpath(self.__fileHandler.baseFilename)
        })

    def deconfigure(self):
        if(self.__screenHandler is not None):
            self.__logger.removeHandler(self.__screenHandler)
        
        if(self.__fileHandler is not None):
            self.__logger.removeHandler(self.__fileHandler)
