import re, collections
from datetime import datetime
 
strRE_MACAddr    = '[0-9a-fA-F]{2}(\:[0-9a-fA-F]{2}){5}'
strRE_IPv4       = '(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])'
strRE_Port       = '([0-9]|[1-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-5][0-9][0-9][0-9][0-9]|6[0-4][0-9][0-9][0-9]|65[0-4][0-9][0-9]|655[0-2][0-9]|6553[0-5])'
strRE_IPv4Port   = '%s\:%s' % (strRE_IPv4, strRE_Port)
strRE_IPv4Prefix = '%s(\/([0-9]|[1-2][0-9]|3[0-2]))?' % (strRE_IPv4)
 
_re_MACAddr    = re.compile('^%s$' % strRE_MACAddr) # aa:bb:cc:dd:ee:ff
_re_IPv4       = re.compile('^%s$' % strRE_IPv4)    # aaa.bbb.ccc.ddd
_re_Port       = re.compile('^%s$' % strRE_Port)
_re_IPv4Port   = re.compile('^%s$' % strRE_IPv4Port) # aaa.bbb.ccc.ddd:eee
_re_IPv4Prefix = re.compile('^%s$' % strRE_IPv4Prefix) # aaa.bbb.ccc.ddd/ee
 
def checkType(name, types, value, allowNone=False):
    if not allowNone or value is not None:
        if(not isinstance(name, (basestring, str, unicode))): raise Exception('Invalid Parameter Name(%s)' % str(name))
        if(not isinstance(types, (tuple,))): raise Exception('Parameter(%s): Invalid Types' % str(name))
        if(not isinstance(value, types)): raise Exception('Parameter(%s): Invalid Value(%s) for Type(%s)' % (name, str(value), str(types)))
         
    return value
 
def checkValue(name, types, value, minValue=None, maxValue=None, minValueIncluded=True, maxValueIncluded=True, allowNone=False):
    if not allowNone or value is not None:
        checkType(name, types, value)
         
        if(minValue is not None):
            if(not isinstance(minValue, types)):
                raise Exception('Parameter(%s): Invalid minValue(%s)' % (name, str(minValue)))
 
            if minValueIncluded is not None:
                if(not isinstance(minValueIncluded, bool)):
                    raise Exception('Parameter(%s): Invalid minValueIncluded(%s)' % (name, str(minValueIncluded)))
                 
                if not minValueIncluded:
                    if(value == minValue): raise Exception('Parameter(%s): Invalid Value(%s) = minValue(%s)' % (name, str(value), str(minValue)))
 
            if(value < minValue): raise Exception('Parameter(%s): Invalid Value(%s) < minValue(%s)' % (name, str(value), str(minValue)))
             
        if(maxValue is not None):
            if(not isinstance(maxValue, types)):
                raise Exception('Parameter(%s): Invalid maxValue(%s)' % (name, str(maxValue)))
 
            if maxValueIncluded is not None:
                if(not isinstance(maxValueIncluded, bool)):
                    raise Exception('Parameter(%s): Invalid maxValueIncluded(%s)' % (name, str(maxValueIncluded)))
                 
                if not maxValueIncluded:
                    if(value == maxValue): raise Exception('Parameter(%s): Invalid Value(%s) = maxValue(%s)' % (name, str(value), str(maxValue)))
 
            if(value > maxValue): raise Exception('Parameter(%s): Invalid Value(%s) > maxValue(%s)' % (name, str(value), str(maxValue)))
 
    return value
 
def checkOptions(name, value, choices, allowNone=False):
    if not allowNone or value is not None:
        if(not isinstance(name, (basestring, str, unicode))): raise Exception('Invalid Parameter Name(%s)' % str(name))
        if(not isinstance(choices, (list,))): raise Exception('Parameter(%s): Invalid Choices(%s)' % (str(name), str(choices)))
        if(value not in choices): raise Exception('Parameter(%s): Invalid Value(%s) not in Choices(%s)' % (name, str(value), str(choices)))
     
    return value
 
def checkBoolean(name, value, allowNone=False):
    if not allowNone or value is not None:
        checkType(name, (bool,), value)
     
    return value
 
def checkInteger(name, value, minValue=None, maxValue=None, minValueIncluded=True, maxValueIncluded=True, allowNone=False):
    if not allowNone or value is not None:
        checkValue(name, (int, long), value, minValue, maxValue, minValueIncluded, maxValueIncluded)
 
    return value
 
def checkFloat(name, value, minValue=None, maxValue=None, minValueIncluded=True, maxValueIncluded=True, allowNone=False):
    if not allowNone or value is not None:
        checkValue(name, (float, int, long), value, minValue, maxValue, minValueIncluded, maxValueIncluded)
 
    return value
 
def checkString(name, value, minLength=None, maxLength=None, allowBlank=True, allowNone=False):
    if not allowNone or value is not None:
        checkType(name, (basestring, str, unicode), value)
         
        checkBoolean('allowBlank', allowBlank, allowNone=False)
        checkInteger('minLength', minLength, minValue=0, allowNone=True)
        checkInteger('maxLength', maxLength, minValue=0, allowNone=True)
         
        if not allowBlank:
            value = value.strip()
 
        if minLength is not None:            
            if(len(value) < minLength):
                raise Exception('Parameter(%s): Len(Value(%s)) < minLength(%d)' % (name, value, str(minLength)))
             
        if maxLength is not None:            
            if(len(value) > maxLength):
                raise Exception('Parameter(%s): Len(Value(%s)) > maxLength(%d)' % (name, value, str(maxLength)))
     
    return value
 
def checkMACAddr(name, value, allowNone=False):
    if not allowNone or value is not None:
        checkString(name, value)
        if(_re_MACAddr.match(value) is None): raise Exception('Parameter(%s): Invalid Value(%s) for MAC_Regex(%s)' % (name, value, strRE_MACAddr))
         
    return value
 
def checkIPv4(name, value, allowNone=False):
    if not allowNone or value is not None:
        checkString(name, value)
        if(_re_IPv4.match(value) is None): raise Exception('Parameter(%s): Invalid Value(%s) for IPv4_Regex(%s)' % (name, value, strRE_IPv4))
         
    return value
 
def checkPort(name, value, allowNone=False):
    if not allowNone or value is not None:
        if(isinstance(value, (int, long))):
            checkInteger(name, value, 0, 65535)
        else:
            checkString(name, value)
            if(_re_Port.match(value) is None): raise Exception('Parameter(%s): Invalid Value(%s) for Port_Regex(%s)' % (name, value, strRE_Port))
             
    return value
 
def checkIPv4Port(name, value, allowNone=False):
    if not allowNone or value is not None:
        checkString(name, value)
        if(_re_IPv4Port.match(value) is None): raise Exception('Parameter(%s): Invalid Value(%s) for IPv4&Port_Regex(%s)' % (name, value, strRE_IPv4Port))
         
    return value
 
def checkIPv4Prefix(name, value, allowNone=False):
    if not allowNone or value is not None:
        checkString(name, value)
        if(_re_IPv4Prefix.match(value) is None): raise Exception('Parameter(%s): Invalid Value(%s) for IPv4&Prefix_Regex(%s)' % (name, value, strRE_IPv4Prefix))
         
    return value
 
def checkRegex(name, regex, value, allowNone=False):
    if not allowNone or value is not None:
        checkString(name, value)
        if(re.match('^%s$' % regex, value) is None): raise Exception('Parameter(%s): Invalid Value(%s) for Regex(%s)' % (name, value, regex))
         
    return value
 
def checkIsHashable(name, value, allowNone=False):
    if not allowNone or value is not None:
        checkType(name, (collections.Hashable,), value)
         
    return value
 
def checkIsDerivedClassFrom(name, classes, value, allowNone=False):
    if not allowNone or value is not None:
        if(not isinstance(name, (basestring, str, unicode))): raise Exception('Invalid Parameter Name(%s)' % str(name))
        if(not isinstance(classes, (tuple,))): raise Exception('Parameter(%s): Invalid Classes' % str(name))
        if(not isinstance(value, classes)): raise Exception('Parameter(%s): Class(%s) is not derived from one of classes(%s)' % (name, str(value), str(classes)))
     
    return value
 
def checkIsSubClassOf(name, classes, value, allowNone=False):
    if not allowNone or value is not None:
        if(not isinstance(name, (basestring, str, unicode))): raise Exception('Invalid Parameter Name(%s)' % str(name))
        if(not isinstance(classes, (tuple,))): raise Exception('Parameter(%s): Invalid Classes' % str(name))
        if(not issubclass(value, classes)): raise Exception('Parameter(%s): Class(%s) is not a subclass of one of classes(%s)' % (name, str(value), str(classes)))
     
    return value
 
def checkAttr(name, container):
    checkString(name, name)
    checkIsHashable(name, name)
    checkType(name, (dict,), container)
    elem = container.get(name)
    if(elem is None): raise Exception('Parameter(%s): Container does not contain/or is None element' % name)
    return(elem)
 
def checkDateTime(name, value, allowNone=False):
    if not allowNone or value is not None:
        checkString(name, name)
        checkString(name, value)
        try:
            return(datetime.strptime(value, '%Y/%m/%d %H:%M:%S'))
        except:
            raise Exception('Parameter(%s): strDate(%s) for not fulfill format(YYYY/MM/DD HH:MM:SS)' % (name, str(value)))
     
    return value