from shutil import copy
import json
import codecs
import os
import sys
import Tkinter as tk
import SendSounds_Theme
sys.path.append(os.path.join(
    os.path.dirname(__file__), '../SendSounds-Classes'))
from SendSounds_LoggerClass import Logger as log
from SendSounds_DatabaseClass import Database as db

global dbLogger, dbSettingsFile, scriptSettingsFile, soundsDB, helpFile, helpText
dbLogger = log('dashboard')
dbLogger.logInit()
dbSettingsFile = os.path.relpath(os.path.join(os.path.dirname(
    __file__), '../SendSound-Classes/SendSounds_dbSettings.json'))
scriptSettingsFile = os.path.relpath(os.path.join(
    os.path.dirname(__file__), '../SendSounds_Settings.json'))
helpFile = os.path.relpath(os.path.join(
    os.path.dirname(__file__), 'assets/SendSounds_Help.json'))


def printLog(msg):
    print(msg)
    if dbLogger:
        dbLogger.logWrite(msg)
    return


def initDb():
    global soundsDB
    soundsDB = db(dbSettingsFile, scriptSettingsFile)
    startDBMsg = soundsDB.createTable()
    printLog(startDBMsg)
    return soundsDB


def createSettings(data, file):
    global dbLogger
    try:
        with codecs.open(file, mode='w+', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=2,
                      sort_keys=True, encoding='utf-8')
        msg = '[{time}] (SUC) - Required file "{file}" created with success!'
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to create required file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=file, err=e)
    printLog(msg)
    return


def saveFile(filename, cb1, cb2):
    global dbLogger, soundsDB, scriptSettingsFile
    data = cb1()
    try:
        with codecs.open(filename, mode='w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
        msg = '[{time}] (SUC) - New information saved to  file "{file}" '
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to save file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=filename, err=e)
    printLog(msg)
    cb2()
    return soundsDB


def createFileBackup(fileName):
    global dbLogger
    backFileName = '{file}.bk'.format(file=fileName)
    try:
        copy(fileName, backFileName)
        msg = '[{time}] (SUC) - Saved backup of "{file}" to {backup}'
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to create backup of file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(file=fileName, backup=backFileName,
                     err=e, time=dbLogger.getTime())
    printLog(msg)
    return


def restoreFileBackup(fileName, cb):
    global dbLogger, soundsDB, scriptSettingsFile
    backFileName = '{file}.bk'.format(file=fileName)
    try:
        copy(backFileName, fileName)
        msg = '[{time}] (SUC) - Previously saved backup of "{file}" using "{backup}" restored'
        cb()
        e = None
    except Exception as e:
        msg = '[{time}] (ERR) - Unable to restore backup of file "{file}" ...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=fileName,
                     err=e, backup=backFileName)
    printLog(msg)
    return soundsDB


def readJson(jsonFile):
    global dbLogger
    try:
        with codecs.open(jsonFile, mode='r', encoding='utf-8-sig') as f:
            jsonData = json.load(f)
        msg = '[{time}] (SUC) - Required file "{file}" loaded with success!'
        e = None
    except Exception as e:
        jsonData = None
        msg = '[{time}] (ERR) - Unable to load the required file "{file}"...'
        msg += '\n[{time}] (ERR) - System message: {err})'
        pass
    msg = msg.format(time=dbLogger.getTime(), file=jsonFile, err=e)
    printLog(msg)
    return jsonData


def changeTabStatus(tab, bar, *args):
    global dbLogger
    tabIndex = tab.index(tab.select())
    barText = ' {text}'
    barText = barText.format(text=tab.tab(tabIndex, 'text'))
    bar.configure(text=barText)
    msg = '[{time}] (INF) - Now displaying {tab}...'
    msg = msg.format(time=dbLogger.getTime(), tab=barText)
    printLog(msg)
    return


def openDashboardLogs():
    folder = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '../SendSound-Logs/Dashboard'))
    os.startfile(folder)
    return


def deleteDashboardLogs():
    dbLogger.folderLogDelete('dashboard')
    return


def openScriptLogs():
    folder = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '../SendSound-Logs/Script'))
    os.startfile(folder)
    return


def deleteScriptLogs():
    dbLogger.folderLogDelete('script')
    return


def openLogs():
    folder = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '../SendSound-Logs'))
    os.startfile(folder)
    return


def deleteAllLogs():
    deleteDashboardLogs()
    deleteScriptLogs()
    return


def setVolume(label, var, *args):
    label['text'] = '{:.0f}%'.format(var.get())
    return var.get()


def getTriggers(db):
    msg = '[{time}] (INF) - Creating list of triggers...'
    try:
        results = db.getTriggersList()
        if len(results) > 0:
            list = results
        else:
            list = []
        e = None
    except Exception as e:
        msg += '\n[{time}] (ERR) - Unable to create a list of triggers...'
        msg += '\n[{time}] (ERR) - System message: {err}'
    msg = msg.format(time=dbLogger.getTime(), err=e)
    printLog(msg)
    return list


def updateSound(index, data):
    global soundsDB
    msg = soundsDB.updateSound(index, data)
    printLog(msg)
    return


def deleteSound(index):
    global soundsDB
    msg = soundsDB.deleteSound(index)
    printLog(msg)
    return


def checkIntegrity():
    check = soundsDB.checkIntegrity()
    msg = check[0]
    hasPassed = check[1]
    issueCount = check[2]
    printLog(msg)
    return [hasPassed, issueCount]


def unselect(root, *args):
    widget = root.tk_focusPrev()
    widget.selection_clear()
    return


def dbIssueFix(mode, cb):
    msg = soundsDB.fixIntegrity(mode)
    cb()
    printLog(msg)
    return


def dbClear(*args):
    if args and len(args) == 2:
        clear = soundsDB.clearDB(args[0])
        args[1]()
    else:
        clear = soundsDB.clearDB()
    msg = clear[0]
    toClear = clear[1]
    printLog(msg)
    return toClear


def dbDisconnect():
    soundsDB.conn.close()
    return


helpText = readJson(helpFile)


def changeHelp(e, root, textZone, *args):
    try:
        widget = root.focus_get()
        if widget:
            key = widget.winfo_name()
        textZone.config(state='normal')
        textZone.delete('0.0', tk.END)
        textZone.insert(tk.END, helpText[key])
        textZone.config(state='disabled', selectbackground=SendSounds_Theme.darkGray,
                        selectforeground=SendSounds_Theme.darkWhite, cursor='arrow')
    except Exception as e:
        if e.args[0] != 'popdown':
            text = 'Quick help fpr this field was not found. Please contact the developer'
            textZone.config(state='normal')
            textZone.delete('0.0', tk.END)
            textZone.insert(tk.END, text)
            textZone.config(state='disabled', selectbackground=SendSounds_Theme.darkGray,
                            selectforeground=SendSounds_Theme.darkWhite, cursor='arrow')
        else:
            pass
        pass
    return
