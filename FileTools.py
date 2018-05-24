import os, json
from Lib.ParameterChecking import checkString

def folderExists(path):
    ''' return True/False if folder exists/does not exist '''
    return(os.path.isdir(path))

def mkdirAndParents(path):
    ''' create a folder and its parents, if needed '''
    if(folderExists(path)): return
    os.makedirs(path)

def fileExists(path):
    ''' return True/False if file exists/does not exist '''
    return(os.path.isfile(path))

def getFileSize(path):
    ''' return None if file does not exist, otherwise its size in bytes '''
    if(not fileExists(path)): return(None)
    return(os.stat(path).st_size)

def fileIsEmpty(path):
    ''' return None if file does not exist, otherwise True/False if file exists/does not exist '''
    return(getFileSize(path) == 0)

def readFile(path):
    ''' return None if file does not exist, otherwise its content '''
    strFilePath = checkString('filePath', path)
    if(not fileExists(strFilePath)): return(None)
    f = open(strFilePath, 'r')
    content = f.read()
    f.close()
    return(content)

def writeFile(path, data):
    ''' write data in file pointed by path '''
    strFilePath = checkString('filePath', path)
    f = open(strFilePath, 'w')
    f.write(data)
    f.close()

def readFileAsJSON(path):
    ''' read content of file pointed by path in JSON format '''
    strFileContent = readFile(path)
    if(strFileContent is None): raise Exception('File(%s) is empty or does not exist' % path)
    return(json.loads(strFileContent))

def writeFileAsJSON(path, jsonContent):
    ''' write jsonContent in file pointed by path in JSON format '''
    writeFile(path, json.dumps(jsonContent, indent=4))
