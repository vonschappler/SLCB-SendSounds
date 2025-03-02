import sqlite3
import json
import codecs
import os
from collections import OrderedDict as od
from SendSounds_LoggerClass import Logger as log

global databaseLog, table, cListTrigger, cTrigger, cFilePath, cMessage, cSendAs, cVolume, cEnable, cUsesCount, cPassIntegrity, cIntegrityFixed
databaseLog = log('dashboard')

class Database():
    def __init__(self, dbSettingsFile=None, scriptSettingsFile=None):
        global newFiles, skipped, updated
        newFiles = 0
        skipped = 0
        updated = 0
        self.startMsg = '[{time}] (INF) - Starting database...'
        try:
            with codecs.open(dbSettingsFile, encoding='utf-8-sig', mode='r') as f:
                self.dbSettings = json.load(f, encoding='utf-8', object_pairs_hook=od)
                self.startMsg += '\n[{time}] (INF) - Required asset "SendSounds_dbSettings.json" file found!'
            with codecs.open(scriptSettingsFile, encoding='utf-8-sig', mode='r') as f:
                self.scriptSettings = json.load(f, encoding='utf-8', object_pairs_hook=od)
                self.startMsg += '\n[{time}] (INF) - Required asset "SendSounds_Settings.json" file found!'
            self.dbFolder = self.dbSettings['dbFolder']
            self.dbFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '../{folder}')).format(folder=self.dbFolder)
            self.dbFileName = self.dbSettings['dbFileName']
            self.dbColumns = self.dbSettings['dbColumns']
            self.dbTable = self.dbSettings['dbTable']
            self.soundsFolder = self.scriptSettings['sndFolderSFX'].lower()
            e = None
        except Exception as e:
            self.startMsg += '\n[{time}] (WAR) - Unable to find one or more required assets or the required files are not in the right format. The script is creating a new files.'
            self.startMsg += '\n[{time}] (ERR) - System message: {err}'
            self.dbFolder = 'SendSounds-Database'
            self.dbFileName = 'SendSounds_Database.sqlite'
            self.dbFilePath = os.path.realpath(os.path.join(os.path.dirname(__file__), '../{folder}')).format(folder=self.dbFolder)
            self.dbColumns = [
                "sndListTrigger",
                "sndTrigger",
                "sndFilePath",
                "sndVolume",
                "sndSendMsg",
                "sndSendAs",
                "sndEnable",
                "sndUsesCount",
                "passIntegrity",
                "integrityFixed"
            ]
            self.dbTable = 'soundsSettings'
            self.soundsFolder = os.path.realpath(os.path.join(
                os.path.dirname(__file__), '../SendSounds-Sounds'))
            with codecs.open(os.path.realpath(os.path.join(os.path.dirname(__file__), 'SendSounds_dbSettings.json')), mode='w+', encoding='utf-8-sig') as f:
                settings = {
                    "dbColumns": self.dbColumns,
                    "dbFileName": self.dbFileName,
                    "dbFolder": self.dbFolder,
                    "dbTable": self.dbTable
                }
                json.dump(settings, f, ensure_ascii=False, indent=2)
                self.startMsg += '\n[{time}] (SUC) - Required asset "SendSounds_dbSettings.json" file created with success!'
            pass
        self.startMsg += '\n[{time}] (SUC) - Database initialized with success!'
        self.startMsg = self.startMsg.format(time=databaseLog.getTime(), err=e)
        self.dbFile = os.path.join(self.dbFilePath, self.dbFileName)
        return

    def dbConns(self):
        self.conn = sqlite3.connect(self.dbFile)
        return self.conn

    def createTable(self):
        global table, cListTrigger, cTrigger, cFilePath, cMessage, cVolume, cSendAs, cEnable, cUsesCount, cPassIntegrity, cIntegrityFixed
        table = self.dbTable
        cListTrigger = self.dbColumns[0]
        cTrigger = self.dbColumns[1]
        cFilePath = self.dbColumns[2]
        cVolume = self.dbColumns[3]
        cMessage = self.dbColumns[4]
        cSendAs = self.dbColumns[5]
        cEnable = self.dbColumns[6]
        cUsesCount = self.dbColumns[7]
        cPassIntegrity = self.dbColumns[8]
        cIntegrityFixed = self.dbColumns[9]
        msg = '[{time}] (INF) - Starting connection with the sounds database...'
        conn = self.dbConns()
        try:
            createQ = 'create table if not exists {table} (id integer primary key autoincrement, {col0} text not null unique, {col1} text not null, {col2} text not null, {col3} integer not null default 50, {col4} text default "", {col5} text not null default "Chat", {col6} boolean default 1, {col7} integer default 0, {col8} boolean not null default 1, {col9} boolean)'
            createQ = createQ.format(table=table, col0=cListTrigger, col1=cTrigger, col2=cFilePath, col3=cVolume, col4=cMessage, col5=cSendAs, col6=cEnable, col7=cUsesCount, col8=cPassIntegrity, col9=cIntegrityFixed)
            addIndexFile = 'create unique index if not exists {col1} on {table} ({col1})'
            addIndexFile = addIndexFile.format(col1=cFilePath, table=table)
            cursor = conn.cursor()
            cursor.execute(createQ)
            cursor.execute(addIndexFile)
            conn.close()
            msg += '\n[{time}] (SUC) - Database connection created with success!'
            e = None
        except Exception as e:
            msg += '\n[{time}] (ERR) - An error occured while trying to connect to the databasabe'
            msg += '\n[{time}] (ERR) - System message: {err}'
        msg = msg.format(time=databaseLog.getTime(), err=e)
        return msg

    def autoAddSounds(self, *args):
        msg = '[{time}] (INF) - Creating database entries for files...'
        try:
            if args and args[0] != '':
                for fileName in os.listdir(args[0]):
                    trigger = fileName.split('.mp3')[0].replace(' ', '-').replace('_', '-')
                    filePath = os.path.realpath(os.path.join(args[0], fileName))
                    msg += '\n{result}'.format(result=self.addSound(trigger, filePath))
            else:
                for fileName in os.listdir(self.soundsFolder):
                    trigger = fileName.split('.mp3')[0].replace(' ', '-').replace('_', '-')
                    filePath = os.path.realpath(os.path.join(self.soundsFolder, fileName))
                    msg += '\n{result}'.format(result=self.addSound(trigger, filePath))
            e = None
        except Exception as e:
            msg = '[{time}] (ERR) - Unable to add new sounds to the database'
            msg += '\n[{time}] (ERR) - System error: {err}'
            pass
        msg = msg.format(time=databaseLog.getTime(), err=e)
        return msg

    def addSound(self, trigger, filePath):
        global newFiles, skipped, updated
        msg = ""
        conn = self.dbConns()
        cursor = conn.cursor()
        listTrigger = '{trigger} ({path})'
        listTrigger = listTrigger.format(trigger=trigger, path=os.path.realpath(filePath))
        addSoundQ = 'insert into {table} ({col0}, {col1}, {col2}) values ("{listTrigger}", "{trigger}", "{filePath}")'
        addSoundQ = addSoundQ.format(table=table, col0=cListTrigger, listTrigger=listTrigger, col1=cTrigger, trigger=trigger, col2=cFilePath, filePath=filePath)
        updateSoundQ = 'update {table} set {col1}=1 where {col2}="{listTrigger}"'
        updateSoundQ = updateSoundQ.format(table=table, col1=cEnable, col2=cListTrigger, listTrigger=listTrigger)
        findQ = 'select {col1} from {table} where {col1}="{value}"'
        findQ = findQ.format(col1=cListTrigger, table=table, value=listTrigger)
        try:
            cursor.execute(addSoundQ)
            msg += '[{time}] (SUC) - A new sound was added to the database...'
            msg += '\n[{time}] (INF) - Sound trigger: "{trigger}" / Sound file: "{filePath}"'
            newFiles += 1
            e = None
        except Exception as e:
            result = cursor.execute(findQ).fetchone()[0]
            if result and result == listTrigger:
                cursor.execute(updateSoundQ)
                msg += '[{time}] (SUC) - An existing sound was updated in the database...'
                msg += '\n[{time}] (INF) - Sound trigger: "{trigger}" / Sound file: "{filePath}"'
                updated += 1
            else:
                msg += '[{time}] (ERR) - Unable to add sound using "{trigger}" as trigger because it already exists on the database'
                skipped += 1
            pass
        msg = msg.format(time=databaseLog.getTime(), trigger=trigger, filePath=filePath, err=e)
        conn.commit()
        conn.close()
        return msg

    def getCount(self):
        conn = self.dbConns()
        cursor = conn.cursor()
        countQ = 'select count() from {table}'.format(table=table)
        rows = cursor.execute(countQ).fetchone()[0]
        conn.close()
        return rows

    def checkIntegrity(self):
        self.passed = 0
        self.notPassed = 0
        self.toFixList = []
        self.hasPassed = True
        folder = self.soundsFolder
        conn = self.dbConns()
        cursor = conn.cursor()
        msg = '[{time}] (INF) - Starting database integrity check...'
        msg += '\n[{time}] (INF) - Collecting information about database integrity...'
        fileListQ = 'select {col1}, {col2}, {col3}, {col4} from {table} order by id'
        fileListQ = fileListQ.format(col1=cFilePath, col2=cEnable, col3=cPassIntegrity, col4=cIntegrityFixed, table=table)
        results = cursor.execute(fileListQ).fetchall()
        soundsFileList = os.listdir(folder)
        for result in results:
            try:
                fileToCheck = os.path.realpath(result[0])
                fileName = fileToCheck.split('\\')[-1:][0]
                if fileName in soundsFileList:
                    compareFile = os.path.realpath(os.path.join(folder, fileName))
                else:
                    compareFile = None
                if (fileToCheck != compareFile):
                    if not bool(result[3]):
                        notPassQ = 'update {table} set {col1}=0, {col2}=0 where {col3}="{value}"'
                        notPassQ = notPassQ.format(table=table, col1=cPassIntegrity, col2=cIntegrityFixed, col3=cFilePath, value=result[0])
                        cursor.execute(notPassQ)
                        conn.commit()
                        self.toFixList.append(result[0])
                        self.notPassed += 1
                    elif bool(result[4]):
                        self.passed += 1
                else:
                    notPassQ = 'update {table} set {col1}=0, {col2}=Null where {col3}="{value}"'
                    notPassQ = notPassQ.format(table=table, col1=cPassIntegrity, col2=cIntegrityFixed, col3=cFilePath, value=result[0])
                    cursor.execute(notPassQ)
                    conn.commit()
                    self.passed += 1
                e = None
            except Exception as e:
                msg +='\n[{time}] (ERR) - An error has happened while checking the database integrity...'
                msg +='\n[{time}] (ERR) - System message: {err}'
                msg = msg.format(time=databaseLog.getTime(), err=e, folder=None)
                pass
        msg += '\n[{time}] (SUC) - Database integrity check completed...'
        msg += '\n[{time}] (INF) - Entries passed the check: {passed} / Entries rejected in the check: {notPassed}'
        if len(self.toFixList) > 0:
            msg += '\n[{time}] (WAR) - Your sounds database needs attention to keep its integrity'
            msg += '\n[{time}] (INF) - List of entries which need to be fixed:'
            self.hasPassed = False
            for entry in self.toFixList:
                msg += '\n[{time}] (INF) - {entry}'.format(time=databaseLog.getTime(), entry=entry)
        msg = msg.format(time=databaseLog.getTime(), passed=self.passed, notPassed=self.notPassed, folder=folder)
        conn.commit()
        conn.close()
        return [msg, self.hasPassed, self.notPassed]

    def fixIntegrity(self, action):
        msg = ''
        conn = self.dbConns()
        cursor = conn.cursor()
        if len(self.toFixList) > 0:
            msg += '[{time}] (INF) - Working on database integrity fixes using \"{mtd}\"...'
            try:
                if action == 'disable' and len(self.toFixList) > 0:
                    toFixQ = 'update {table} set {col1}=0, {col2}=1, {col3}=1 where {col3}=0'
                    toFixQ = toFixQ.format(table=table, col1=cEnable, col2=cPassIntegrity, col3=cIntegrityFixed)
                    cursor.execute(toFixQ)
                    msg += '\n[{time}] (SUC) - Fixed database integrity by disabling triggers for missing sound files'
                elif action == 'delete' and len(self.toFixList) > 0:
                    toFixQ = 'delete from {table} where {col1}=0'
                    toFixQ = toFixQ.format(table=table, col1=cIntegrityFixed)
                    cursor.execute(toFixQ)
                    msg += '\n[{time}] (SUC) - Fixed database integrity by deleting entries with missing sound files'
                e = None
            except Exception as e:
                msg += '\n[{time}] (ERR) - Unable to fix database integrity usigng "{mtd}"'
                msg += '\n[{time}] (ERR) - System message: {err}'
            msg = msg.format(time=databaseLog.getTime(), mtd=action, err=e)
        else:
            msg += '[{time}] (INF) - There are no entries to be {mtd}d'
        msg = msg.format(time=databaseLog.getTime(), mtd=action)
        conn.commit()
        conn.close()
        return msg

    def clearDB(self, *args):
        deleteCount = 0
        updateCount = 0
        conn = self.dbConns()
        cursor = conn.cursor()
        disabledListQ = 'select {col1} from {table} where {col2}="{value}"'
        disabledListQ = disabledListQ.format(table=table, col1=cListTrigger, col2=cEnable, value=0)
        disabledList = cursor.execute(disabledListQ).fetchall()
        countDisableQ = 'select count() from {table} where {col1}=0'
        countDisableQ = countDisableQ.format(table=table, col1=cEnable)
        countFix = cursor.execute(countDisableQ).fetchone()[0]
        msg = '[{time}] (INF) - Checking for entries disabled entries / sounds in the database...'
        if args and args[0] == 'delete':
            for item in disabledList:
                msg = '[{time}] (INF) - Clearing databasabe by removing disabled entries...'
                try:
                    deleteQ = 'delete from {table} where {col1}="{value}"'
                    deleteQ = deleteQ.format(table=table, col1=cListTrigger, value=item[0])
                    cursor.execute(deleteQ)
                    msg += '\n[{time}] (SUC) - Entry {entry}  deleted with success'
                    msg = msg.format(time=databaseLog.getTime(), entry=item[0])
                    deleteCount += 1
                    e = None
                except Exception as e:
                    msg += '\n[{time}] (ERR) - An error has occurred while trying to execute the database cleaning...'
                    msg += '\n[{time}] (ERR) - System error: {err}'
                    pass
                msg = msg.format(time=databaseLog.getTime(), err=e)
        if args and args[0] == 'enable':
            for item in disabledList:
                msg = '[{time}] (INF) - Enabling disabled sounds...'
                try:
                    updateQ = 'update {table} set {col1}=1 where {col2}="{value}"'
                    updateQ = updateQ.format(table=table, col1=cEnable, col2=cListTrigger, value=item[0])
                    cursor.execute(updateQ)
                    msg += '\n[{time}] (SUC) - Entry {entry}  enabled with success'
                    msg = msg.format(time=databaseLog.getTime(), entry=item[0])
                    updateCount += 1
                    e = None
                except Exception as e:
                    msg += '\n[{time}] (ERR) - An error has occurred while trying to execute the update process...'
                    msg += '\n[{time}] (ERR) - System error: {err}'
                    pass
                msg = msg.format(time=databaseLog.getTime(), err=e)
        if countFix == 0:
            msg += '\n[{time}] (INF) - There are no entries to be removed. Skipping the database cleaning process...'
        else:
            msg += '\n[{time}] (WAR) - One or more entries / sounds are disabled on the database'
            msg += '\n[{time}] (INF) - Total entries detected: {toFix}'
        if deleteCount > 0:
            msg += '\n[{time}] (INF) - Total entries deleted: {deleteCount}'
        if updateCount > 0:
            msg += '\n[{time}] (INF) - Total entries deleted: {updateCount}'
        msg = msg.format(time=databaseLog.getTime(), deleteCount=deleteCount, updateCount=updateCount, toFix=countFix, folder=self.soundsFolder)
        conn.commit()
        conn.close()
        return [msg, countFix]

    def findOne(self, rowid):
        conn = self.dbConns()
        cursor = conn.cursor()
        findQ = 'select rowid, {col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7} from {table} where rowid={rowid}'
        findQ = findQ.format(table=table, col1=cTrigger, col2=cFilePath, col3=cVolume, col4=cMessage, col5=cSendAs, col6=cEnable, col7=cUsesCount, rowid=rowid)
        try:
            foundTrigger = cursor.execute(findQ).fetchone()
        except:
            foundTrigger = None
        return foundTrigger

    def updateUseCount(self, trigger):
        conn = self.dbConns()
        cursor = conn.cursor()
        countQ = 'select {col1}, {col2} from {table} where {col3}="{trigger}"'
        countQ = countQ.format(col1=cUsesCount, col2=cListTrigger, table=table, col3=cTrigger, trigger=trigger)
        toUpdate = cursor.execute(countQ).fetchone()
        msg = ''
        if toUpdate:
            count = toUpdate[0]
            listTrigger = toUpdate[1]
            try:
                updateQ = 'update {table} set {col1}={newCount} where {col2}="{trigger}"'
                updateQ = updateQ.format(table=table, col1=cUsesCount, newCount=count+1, col2=cListTrigger, trigger=listTrigger)
                cursor.execute(updateQ)
                msg += '[{time}] (SUC) - Entry linked to "{trigger}" has uses count updated with success!'
                msg += '\n[{time}] (INF) - New use count for "{trigger}" is "{newCount}"'
                e = None
            except Exception as e:
                msg += '[{time}] (ERR) - Could not update usage count for  {trigger}...'
                msg += '\n[{time}] (ERR) - System message: {err}'
                pass
            msg = msg.format(time=databaseLog.getTime(), trigger=trigger, err=e, newCount=count+1)
        else:
            msg += '[{time}] (INF) - The database search for {trigger} returned no results'
            msg = msg.format(time=databaseLog.getTime(), trigger=trigger)
        conn.commit()
        conn.close()
        return msg

    def deleteSound(self, item):
        conn = self.dbConns()
        cursor = conn.cursor()
        msg = '[{time}] (INF) - Deleting selected sound...'
        try:
            deleteQ = 'delete from {table} where {col0}="{item}"'
            deleteQ = deleteQ.format(table=table, col0=cListTrigger, item=item)
            cursor.execute(deleteQ)
            updateQ = 'update sqlite_sequence set seq=(select max(id) from {table}) where name="{table}"'
            updateQ = updateQ.format(table=table)
            cursor.execute(updateQ)
            msg += '\n[{time}] (SUC) - Sound deleted with success!'
            e = None
        except Exception as e:
            msg += '\n[{time}] (ERR) - Error while trying to delete selected sound'
            msg += '\n[{time}] (ERR) - System message: {err}'
            pass
        msg = msg.format(time=databaseLog.getTime(), err=e)
        conn.commit()
        conn.close()
        return msg

    def deleteOne(self, trigger):
        result = self.findOne(trigger)
        conn = self.dbConns()
        cursor = conn.cursor()
        msg = ''
        if result:
            try:
                deleteQ = 'delete from {table} where {col1}="{value}"'
                deleteQ = deleteQ.format(table=table, col1=cTrigger, value=trigger)
                msg += '[{time}] (SUC) - Entry linked to "{trigger}" was deleted successfully'
                cursor.execute(deleteQ)
                updateQ = 'update sqlite_sequence set seq=(select max(id) from {table}) where name="{table}"'
                updateQ = updateQ.format(table=table)
                cursor.execute(updateQ)
                e = None
            except Exception as e:
                msg += '[{time}] (ERR) - Could not delete {trigger} from database...'
                msg += '[{time}] (ERR) - System message: {err}'
                msg = msg.format(err=e)
                pass
        else:
            msg += '[{time}] (INF) - The database search for {trigger} returned no results that could be deleted'
        msg = msg.format(time=databaseLog.getTime(), trigger=trigger)
        conn.commit()
        conn.close()
        return msg

    def findSound(self, item):
        conn = self.dbConns()
        cursor = conn.cursor()
        findQ = 'select {col0}, {col1}, {col2}, {col3}, {col4}, {col5}, {col6}, {col7} from {table} where {col0}="{item}"'
        findQ = findQ.format(table=table, col0=cListTrigger, col1=cTrigger, col2=cFilePath, col3=cVolume, col4=cMessage, col5=cSendAs, col6=cEnable, col7=cUsesCount, item=item)
        try:
            foundTrigger = cursor.execute(findQ).fetchone()
        except:
            foundTrigger = None
        return foundTrigger

    def updateSound(self, item, data):
        conn = self.dbConns()
        cursor = conn.cursor()
        msg = '[{time}] (INF) - Updating information for selected sound...'
        try:
            item = item
            newTrigger = data[1]
            newListTrigger = '{newTrigger} ({path})'
            newListTrigger = newListTrigger.format(newTrigger=newTrigger, path=os.path.realpath(data[2]))
            newVolume = data[3]
            if data[4] == None:
                newMessage = ''
            else:
                newMessage = data[4]
            newSendAs = data[5]
            if data[6] == True:
                newEnable = 1
            else:
                newEnable = 0
            updateQ = 'update {table} set {col0}="{val0}", {col1}="{val1}", {col2}={val2}, {col3}="{val3}", {col4}="{val4}", {col5}={val5} where {col0}="{item}"'
            updateQ = updateQ.format(table=table, col0=cListTrigger, val0=newListTrigger, col1=cTrigger, val1=newTrigger, col2=cVolume, val2=newVolume, col3=cMessage, val3=newMessage, col4=cSendAs, val4=newSendAs, col5=cEnable, val5=newEnable, item=item)
            cursor.execute(updateQ)
            msg += '\n[{time}] (SUC) - Information updated with success!'
            e = None
        except Exception as e:
            msg += '\n[{time}] (ERR) - Unable to update information for the selected sound'
            msg += '\n[{time}] (ERR) - System message: {err}'
            pass
        msg = msg.format(time=databaseLog.getTime(), err=e)
        conn.commit()
        conn.close()
        return msg

    def getTriggersList(self):
        conn = self.dbConns()
        cursor = conn.cursor()
        data = []
        triggerListQ = 'select {col1} from {table} order by id'
        triggerListQ = triggerListQ.format(col1=cListTrigger, table=table)
        results = cursor.execute(triggerListQ).fetchall()
        for result in results:
            data.append(result[0])
        return data

    def getInfoDB(self, col):
        conn = self.dbConns()
        cursor = conn.cursor()
        data = []
        triggerListQ = 'select {col1} from {table} where {col2}=1 order by id'
        triggerListQ = triggerListQ.format(col1=col, col2=cEnable, table=table)
        results = cursor.execute(triggerListQ).fetchall()
        for result in results:
            data.append(result[0])
        return data
