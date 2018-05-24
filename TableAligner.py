import sys, logging
from lib.ParameterChecking import checkType, checkString

class TableAligner(object):
    def __init__(self, fields, useLog=True, moduleName=__name__):
        checkType('fields', (list,), fields)
        self._fields = []
        self._fieldNames = []
        for field in fields:
            checkString('id', field['id'])
            checkString('name', field['name'])
            checkString('headerformat', field['headerformat'])
            checkString('valueformat', field['valueformat'])
            fieldName = field['headerformat'].format(field['name'])
            self._fields.append({ 'id':field['id'], 'name':fieldName, 'format':field['valueformat'] })
            self._fieldNames.append(fieldName)
        self.useLog = useLog
        self.moduleName = moduleName

    def printLine(self, data):
        if(self.useLog):
            logger = logging.getLogger(self.moduleName)
            logger.info(data)
        else:
            print(data)
            sys.stdout.flush()

    def printHeaders(self):
        self.printLine('   '.join(self._fieldNames))

    def printValues(self, fieldValues):
        checkType('fieldValues', (dict,), fieldValues)
        values = []
        for field in self._fields:
            fieldId = field['id']
            fieldFormat = field['format']
            if(not fieldValues.has_key(fieldId)):
                raise Exception('No value has not been provided for field "%s"' % fieldId)
            
            value = fieldValues[fieldId]
            value = fieldFormat.format(value)
            values.append(value)
        self.printLine('   '.join(values))
