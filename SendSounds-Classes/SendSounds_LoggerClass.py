import os
import datetime

global logFolder, logFile


class Logger():
    def __init__(self, mode=None):
        self.scriptName = '[SLCB] SendSounds'
        self.version = 'b1.1.0'
        if mode == 'dashboard':
            self.logFolder = os.path.realpath(os.path.join(
                os.path.dirname(__file__), '..\SendSounds-Logs\Dashboard'))
        elif mode == 'script' or mode == None:
            self.logFolder = os.path.realpath(os.path.join(
                os.path.dirname(__file__), '..\SendSounds-Logs\Script'))
        self.logFileName = '{folder}\SLCB_SendSounds_log_{datetime}.log'.format(
            folder=self.logFolder, datetime=self.setTimeName())
        self.startLog = True
        return

    def logInit(self):
        try:
            f = open(self.logFileName, mode='w+')
            msg = '[' + self.getTime() + \
                '] (INF) - This is the beggining of the log file "{file}":'
            msg += '\n[' + self.getTime() + \
                '] (INF) - {scriptName} {version} is starting...'
            msg = msg.format(file=self.logFileName,
                             scriptName=self.scriptName, version=self.version)
            f.write(msg)
        except Exception as e:
            msg = '[' + self.getTime() + \
                '] (ERR) - Unable to init log functionalities.'
            msg += '\n[' + self.getTime() + \
                '] System error: {error}'.format(error=e)
            self.startLog = False
            pass
        return [msg, self.startLog]

    def logDelete(self):
        os.remove(self.logFileName)
        return

    def folderLogDelete(self, mode):
        if mode == 'dashboard':
            logFolder = os.path.realpath(os.path.join(
                os.path.dirname(__file__), '..\Logs\Dashboard'))
        elif mode == 'script':
            logFolder = os.path.realpath(os.path.join(
                os.path.dirname(__file__), '..\Logs\Script'))
        for f in os.listdir(logFolder):
            os.remove(os.path.join(logFolder, f))
        return

    def logEnd(self):
        f = open(self.logFileName, mode='a+')
        msg = '\n[' + self.getTime() + \
            '] (INF) - This is the end of of the log file "{file}" .'
        msg = msg.format(file=self.logFileName)
        f.write(msg)
        return

    def logWrite(self, msg):
        f = open(self.logFileName, mode='a+')
        f.write('\n' + msg)
        f.close()
        return

    def setTimeName(self):
        time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        return time

    def getTime(self):
        time = datetime.datetime.now().strftime('%Y/%m/%d@%H:%M:%S')
        return time
