from Lib.ParameterChecking import checkType, checkAttr, checkString, checkIPv4

class _Object(object):
    def __init__(self, name):
        checkString('name', name)
        self._name = name
        self._configured = False
        self._running = False

    def getName(self):      return(self._name)
    def isConfigured(self): return(self._configured)
    def isRunning(self):    return(self._running)

    @staticmethod
    def checkConfiguration(config):
        checkType('config', (dict,), config)
        pass

    def configure(self, config, updateConfigured=True):
        _Object.checkConfiguration(config)
        if(updateConfigured): self._configured = True

    def start(self, updateRunning=True):
        if(not self._configured): raise Exception('[%s] not configured' % self._name)
        if(self._running): raise Exception('[%s] already running' % self._name)
        if(updateRunning): self._running = True

    def stop(self, updateRunning=True):
        if(not self._running): raise Exception('[%s] not running' % self._name)
        if(updateRunning): self._running = False
