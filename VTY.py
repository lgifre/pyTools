'''
Generic VTY command interface.
    Supports custom prompt and I/O streams.
    Commands built-in:
    - exit
    - help

    Usage example:
        stdin  = sys.stdin  if(inFileHandler  is None) else open(inFilePath, 'r')
        stdout = sys.stdout if(outFileHandler is None) else open(outFilePath, 'w')
        stderr = sys.stderr if(errFileHandler is None) else stdout
        vty = VTY(handler, prompt='MyVTY> ', stdin=stdin, stdout=stdout, stderr=stderr)
            # Instantiate the VTY.
            # handler: is a handler passed to the custom commands for data management
            # prompt: defines the custom prompt
            # stdin/out/err: define the VTY standard input/output streams
        ...
        vty.addCommand(Command_XXX)
            # Add custom commands implemented in separate classes.
            # Command_XXX should inherit from _Command.
            # See examples of commands below.
        ...
        vty.run()
            # start the VTY command loop, should terminate with an "exit" command, or
            # setting self.getVTY().setTerminate() in a custom command
'''

import sys, threading, traceback
from Lib.ParameterChecking import checkString, checkIsSubClassOf, checkBoolean

class _Command(object):
    def __init__(self, vty, handler):
        self.__vty = vty
        self.__handler = handler

    def getVTY(self):     return(self.__vty)
    def getHandler(self): return(self.__handler)

    def getCommand(self):   raise Exception('Undefined command')
    def getShortHelp(self): raise Exception('Undefined command')
    def getLongHelp(self):  raise Exception('Undefined command')
    def run(self, *args):   raise Exception('Undefined command')

class Command_Dummy(_Command):
    def getCommand(self):   return('')
    def getShortHelp(self): return('')
    def getLongHelp(self):  return('')
    def run(self, *args):
        strCmd = ' '.join(args)
        if(len(strCmd) == 0): return('')
        raise Exception('Unsupported command: %s' % strCmd)

class Command_Exit(_Command):
    def getCommand(self):   return('exit')
    def getShortHelp(self): return('Exit the VTY.')
    def getLongHelp(self):  return('Exit the VTY.')
    def run(self, *args):
        self.getVTY().setTerminate()
        return('Bye!')

class Command_Help(_Command):
    def getCommand(self):   return('help')
    def getShortHelp(self): return('Retrieve help for a specific command. Try: help help')
    def getLongHelp(self):  return(
            'Retrieve help for a specific command.\n' +
            '    help <command>')
    def run(self, *args):
        commandInstance,subCommands,args = self.getVTY().getCommand(list(args))
        if(len(subCommands) == 0):
            if(commandInstance is None): return('Command(%s) not found' % ' '.join(args))
            return(commandInstance.getLongHelp())

        commandNames = sorted(subCommands.keys())

        if('exit' in commandNames):
            commandNames.remove('exit')
            commandNames.insert(0, 'exit')

        if('help' in commandNames):
            commandNames.remove('help')
            commandNames.insert(1, 'help')

        maxNameLen = max(map(len, commandNames))
        commandList = ''
        for commandName in commandNames:
            commandShortHelp = subCommands.get(commandName).get('instance').getShortHelp()
            padsize = 2 + maxNameLen - len(commandName)
            if(len(commandList) > 0): commandList += '\n'
            commandList += '%s%s%s' % (commandName, ' ' * padsize, commandShortHelp)
        return(commandList)

class VTY(object):
    def __init__(self, handler, prompt='> ', stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
        self.__handler = handler
        self.__prompt = prompt
        self.__stdin = stdin
        self.__stdout = stdout
        self.__stderr = stderr
        self.__commands = {'subCommands': {}, 'instance': Command_Dummy(self, self.__handler)}
        self.__terminate = threading.Event()
        self.__terminate.daemon = True
        self.__dumpTraceback = False
        self.addCommand(Command_Exit)
        self.addCommand(Command_Help)

    def getTerminate(self): return(self.__terminate)
    def setTerminate(self): self.__terminate.set()

    def getDumpTraceback(self): return(self.__dumpTraceback)
    def setDumpTraceback(self, value): self.__dumpTraceback = checkBoolean('dumpTraceback', value)

    def getCommand(self, commandParts): return(self.__find(commandParts, self.__commands))
    def addCommand(self, commandClass):
        checkIsSubClassOf('command', (_Command,), commandClass)
        commandInstance = commandClass(self, self.__handler)
        commandParts = self.__format(commandInstance.getCommand())
        self.__add(commandInstance, commandParts, self.__commands)
    
    def runCommand(self, commandString):
        try:
            commandParts = self.__format(commandString)
            commandInstance,subCommands,args = self.__find(commandParts, self.__commands)
            #if((commandInstance is None) or isinstance(commandInstance, Command_Dummy)): continue
            commandResult = commandInstance.run(*args)
            self.__stdout.write(commandResult)
            self.__stdout.write('\n')
            self.__stdout.flush()
            return(True)
        except Exception as e:
            self.__stderr.write(str(e))
            self.__stderr.write('\n')
            if(self.__dumpTraceback):
                traceback.print_exc(file=self.__stderr)
            self.__stderr.flush()
            return(False)

    def run(self):
        while(not self.__terminate.isSet()):
            self.__stdout.write('\n%s' % self.__prompt)
            self.__stdout.flush()
            self.runCommand(self.__stdin.readline())

    def __format(self, strCommand):
        checkString('command', strCommand)
        return(strCommand.replace('\n', '').replace('\t', ' ').split(' '))

    def __add(self, commandInstance, commandParts, commands):
        if(len(commandParts) == 0): raise Exception('Empty commandParts')
        commandPart = commandParts[0]
        subCommands = commands.get('subCommands')
        if(subCommands is None): raise Exception('Malformed command entry: missing subCommands entry')
        command = subCommands.get(commandPart)
        if(command is None):
            # commandPart not added
            if(len(commandParts) == 1):
                # last commandPart
                subCommands[commandPart] = {'subCommands': {}, 'instance': commandInstance}
            else:
                # intermediate commandPart
                subCommands[commandPart] = {'subCommands': {}, 'instance': None}
                command = subCommands.get(commandPart)
                self.__add(commandInstance, commandParts[1:], command)
        else:
            # commandPart added  
            if(len(commandParts) == 1):
                # last commandPart
                instance = commands.get('instance')
                if(instance is not None): raise Exception('CommandInstance already added')
                commands['instance'] = commandInstance
            else:
                # intermediate commandPart
                self.__add(commandInstance, commandParts[1:], command)

    def __find(self, commandParts, commands):
        instance = commands.get('instance')
        if(instance is None): raise Exception('Malformed command entry: missing instance field')

        subCommands = commands.get('subCommands')
        if(subCommands is None): raise Exception('Malformed command entry: missing subCommands field')

        # no filter specified: retrieve root
        if(len(commandParts) == 0): return(instance, subCommands, commandParts)

        # check if commandPart exists
        commandPart0 = commandParts[0]
        command = subCommands.get(commandPart0)
        if(command is None):
            # if commandPart does not exist, check if there is a single subCommand such as its beginning matches the commandPart
            matchingSCs = filter(lambda sc: sc.startswith(commandPart0), subCommands.keys())
            if(len(matchingSCs) > 1): raise Exception('Multiple subCommands(%s) match input(%s)' % (str(matchingSCs), str(commandPart0)))
            if(len(matchingSCs) == 0): return(commands.get('instance'), subCommands, commandParts)
            command = subCommands.get(matchingSCs[0])

        # commandPart exists, check if last commandPart
        if(len(commandParts) == 1): return(command.get('instance'), command.get('subCommands'), commandParts[1:])

        # intermediate commandPart, recursion required
        return(self.__find(commandParts[1:], command))
