import logging

def flatten(obj, level=0):
    if(level > 20): return('<Level (%d) exceeded>' % level)
    
    if(obj is None): return(None)

    if(hasattr(obj, '__dict__') and obj.__dict__):
        return(dict([(k, flatten(v, level+1)) for (k, v) in obj.__dict__.items()]))

    if(isinstance(obj, (dict,))):
        return(dict([(k, flatten(v, level+1)) for (k, v) in obj.items()]))

    if(isinstance(obj, (list,))):
        return([flatten(x, level+1) for x in obj])

    if(isinstance(obj, (tuple,))):
        return(tuple([flatten(x, level+1) for x in obj]))

    return(obj)

def dumper(obj, level=0):
    logger = logging.getLogger(__name__)
    if(obj is None):
        logger.info(('  '*level) + 'None')
        return

    if(hasattr(obj, '__dict__') and obj.__dict__):
        for name,value in obj.__dict__.iteritems():
            dumper(name, level+1)
            dumper(value, level+2)
        return

    if(isinstance(obj, (dict,))):
        for name,value in obj.iteritems():
            dumper(name, level+1)
            dumper(value, level+2)
        return

    if(isinstance(obj, (list,))):
        logger.info(('  '*level) + '[')
        for value in obj:
            dumper(value, level+1)
        logger.info(('  '*level) + ']')
        return

    if(isinstance(obj, (tuple,))):
        logger.info(('  '*level) + '(')
        for value in obj:
            dumper(value, level+1)
        logger.info(('  '*level) + ')')
        return

    logger.info(('  '*level) + str(obj))
