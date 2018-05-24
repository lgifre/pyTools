class Callbacks(object):
    def __init__(self, kinds=[]):
        self.__callbacks = {}
        self.__callbackAny = []
        for kind in kinds:
            if(self.__callbacks.has_key(kind)): raise Exception('Duplicate callback kind(%s)' % str(kind))
            self.__callbacks[kind] = []

    def getCallbackKinds(self):
        return(self.__callbacks.keys())
        if(self.__callbacks.has_key(kind)): raise Exception('Duplicate callback kind(%s)' % str(kind))
        self.__callbacks[kind] = []
        for callback in self.__callbackAny: self.registerCallback(kind, callback)

    def removeCallbackKind(self, kind):
        if(self.__callbacks.has_key(kind)): raise Exception('Duplicate callback kind(%s)' % str(kind))
        self.__callbacks[kind] = []

    def registerCallback(self, kind, callback):
        if(kind not in self.__callbacks.keys()): raise Exception('Callback kind(%s) not supported' % str(kind))
        if(callback in self.__callbacks[kind]): raise Exception('Callback already registered')
        self.__callbacks[kind].append(callback)

    def unregisterCallback(self, kind, callback):
        if(kind not in self.__callbacks.keys()): raise Exception('Callback kind(%s) not supported' % str(kind))
        if(callback not in self.__callbacks[kind]): raise Exception('Callback not registered')
        self.__callbacks[kind].remove(callback)

    def registerCallbackAnyKind(self, callback):
        for kind in self.__callbacks.keys(): self.registerCallback(kind, callback)
        self.__callbackAny.append(callback)

    def unregisterCallbackAnyKind(self, callback):
        for kind in self.__callbacks.keys(): self.unregisterCallback(kind, callback)
        self.__callbackAny.remove(callback)

    def hasRegisteredCallbacks(self, kind):
        if(kind not in self.__callbacks.keys()): return(False)
        return(len(self.__callbacks[kind]) > 0)

    def _runCallbacks(self, kind, *data):
        if(kind not in self.__callbacks.keys()): raise Exception('Callback kind(%s) not supported' % str(kind))
        for callback in self.__callbacks[kind]: callback(*data)
