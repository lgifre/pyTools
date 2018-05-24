from Lib.ParameterChecking import checkString, checkType

class _RunnableObject(object):
    def __init__(self, name, *args, **kwargs):
        self._configured = False
        self._running = False
        checkString('name', name)
        self._name = name
        object.__init__(self, *args, **kwargs)
    
    def getName(self): return(self._name)

    def isConfigured(self):    return(self._configured)
    def setConfigured(self):   self._configured = True
    def unsetConfigured(self): self._configured = False

    def isRunning(self):    return(self._running)
    def setRunning(self):   self._running = True
    def unsetRunning(self): self._running = False

    @staticmethod
    def checkConfiguration(config):
        checkType('config', (dict,), config)

    @staticmethod
    def getDefaultConfig():
        return({})

    def getConfig(self):
        return({})

    def configure(self, config):
        _RunnableObject.checkConfiguration(config)
        if(self._configured): raise Exception('[%s] already configured' % self._name)

    def deconfigure(self):
        if(not self._configured): raise Exception('[%s] not configured' % self._name)

    def preStart(self, persistedData={}):
        if(not self._configured): raise Exception('[%s] not configured' % self._name)
        if(self._running): raise Exception('[%s] already running' % self._name)

    def start(self):
        if(not self._configured): raise Exception('[%s] not configured' % self._name)
        if(self._running): raise Exception('[%s] already running' % self._name)

    def preStop(self):
        if(not self._configured): raise Exception('[%s] not configured' % self._name)
        if(not self._running): raise Exception('[%s] not running' % self._name)
        return({})

    def stop(self):
        if(not self._configured): raise Exception('[%s] not configured' % self._name)
        if(not self._running): raise Exception('[%s] not running' % self._name)
