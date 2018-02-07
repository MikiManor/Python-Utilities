
'''
Establishing SSH Connection to linux server and returning the session key
'''
def linuxConnector(i_HostName, i_UserName, i_PassWord):
    import paramiko
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(i_HostName, username=i_UserName, password=i_PassWord)
        return (ssh)
    except Exception as e:
        raise Exception("Failed to connect to host {}".format(i_HostName) + "\n"
                        + str(e.args[0]),-1)


'''
Find string in a file,
there is the ability to make it cheap search with sending flag to stop after the first found line
'''
def searchInFile(i_StringToSearch, i_FilePath, i_isOnlyFirstLine):
    foundLinesList = []
    with open(i_FilePath, 'r', encoding='utf-8', errors='ignore') as inF:
        for line in inF:
            if i_StringToSearch in line:
                foundLinesList.append(line)
                if i_isOnlyFirstLine:
                    break
                else:
                    continue
    return foundLinesList if foundLinesList else print("No lines found...")


'''
    keyPath = r"SOFTWARE\BMC Software\Control-M/Agent\CONFIG"
    hostName = "tcontrolm-lan"
    neededValue = "AGENT_DIR"
    value = getRegKeyValue(keyPath, hostName, neededValue)
    print("The Value is : " + value)
'''
def getRegKeyValue(i_keyPath, i_hostName, i_valueToFind):
    import winreg
    hostName = r"\\" + i_hostName
    reg = winreg.ConnectRegistry(hostName, winreg.HKEY_LOCAL_MACHINE)
    key = winreg.OpenKey(reg, i_keyPath)
    value = winreg.QueryValueEx(key, i_valueToFind)[0]
    return(value)


'''
This is Logger Handler Crerator, it uses the properties of the calling program and returns Logger handler
with .log and .error files handlers.
The log file is rotating every 10MB (10 files total)
'''
def loggerUtil():
    import os
    import logging
    import sys
    import logging.handlers
    import inspect

    callingProgramProps = inspect.stack()[1]
    callingProgramPath = inspect.stack()[1][1]
    executionDir = sys.argv[1]
    callingFunctionName = inspect.stack()[1][3]
    callingProgramFolderName = os.path.basename(os.path.dirname(os.path.abspath( callingProgramPath )))
    callingProgramFileName = str((os.path.basename(callingProgramPath).split("."))[:-1][0])
    logsFolderName = os.path.join(executionDir, "logs")
    if not os.path.exists(logsFolderName):
        os.makedirs(logsFolderName)
    logFile = os.path.join(logsFolderName, callingProgramFolderName + ".log")
    errorFile = os.path.join(logsFolderName, callingProgramFolderName + ".error")
    # create logger with
    loggerHandler = logging.getLogger(callingProgramFolderName + "::" + callingProgramFileName + "::" + callingFunctionName)
    loggerHandler.setLevel(logging.DEBUG)
    # create file rotating handler which logs even debug messages
    fileHandler = logging.handlers.RotatingFileHandler(logFile, maxBytes=10485760, backupCount=10)
    fileHandler.setLevel(logging.DEBUG)
    # create file handler for errors
    errorFileHandler = logging.FileHandler(errorFile)
    errorFileHandler.setLevel(logging.WARN)
    # create console handler with a higher log level
    consoleHabdler = logging.StreamHandler()
    consoleHabdler.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler.setFormatter(formatter)
    consoleHabdler.setFormatter(formatter)
    errorFileHandler.setFormatter(formatter)
    # add the handlers to the logger
    loggerHandler.addHandler(fileHandler)
    loggerHandler.addHandler(errorFileHandler)
    loggerHandler.addHandler(consoleHabdler)

    return (loggerHandler, logFile, errorFile)