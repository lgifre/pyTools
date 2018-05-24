import json
from Lib.ParameterChecking import checkType, checkString
 
class _Configuration(object):
    def __init__(self):
        self.fileName = None
        self.data = None
 
    @classmethod
    def createFromFile(cls, configFile):
        checkType('configFile', (file,), configFile)
        obj = cls()
        obj.fileName = configFile.name
        obj.data = json.loads(configFile.read())
        configFile.close()
        obj._validate()
        return(obj)
 
    @classmethod
    def createFromFileName(cls, configFileName):
        checkString('configFileName', configFileName)
        obj = cls()
        obj.fileName = configFileName
        configFile = open(configFileName, 'r')
        obj.data = json.loads(configFile.read())
        configFile.close()
        obj._validate()
        return(obj)
 
    @classmethod
    def createFromString(cls, data):
        checkString('data', data)
        obj = cls()
        obj.data = json.loads(data)
        obj._validate()
        return(obj)
     
    @classmethod
    def createFromDict(cls, data):
        checkType('data', (dict,), data)
        obj = cls()
        obj.data = data
        obj._validate()
        return(obj)
     
    def _validate(self):
        # validate configuration values, if any
        raise Exception('TO BE IMPLEMENTED BY USER')
 
    def get(self):
        return(self.data)
 
    def set(self, config):
        backup = self.data
        try:
            self.data = config
            self._validate()
            configFile = open(self.fileName, 'w')
            configFile.write(json.dumps(self.data, indent=4))
            configFile.close()
        except Exception as e:
            self.data = backup
            raise Exception('Error validating configuration provided: %s' % str(e))