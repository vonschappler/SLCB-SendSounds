#!/usr/bin/env python
# encoding: utf-8

# ---------------------------
#   Import Libraries
# ---------------------------
from collections import deque
import sys
import os
import codecs
import json
import clr
import re
from random import randint
clr.AddReference("IronPython.Modules.dll")
sys.path.append(os.path.join(
    os.path.dirname(__file__), './SendSounds-Classes'))
sys.path.append(os.path.join(os.path.dirname(
    __file__), './SendSounds-Database'))
from SendSounds_LoggerClass import Logger as log
from SendSounds_DatabaseClass import Database as db


global scriptLogger, startMsg
scriptLogger = log('script')

# ---------------------------
#   [Required] Script Information
# ---------------------------
ScriptName = scriptLogger.scriptName
Website = 'http://rebrand.ly/vonWebsite'
Description = 'Sends the sound files added to Streamlabs Chatbot to an Overlay, simulating a virtual input'
Creator = 'von_Schappler'
Version = scriptLogger.version

# ---------------------------
#   Define Global Variables
# ---------------------------
global scriptSettingsFile, scriptSettings, dbSettingsFile, soundsDB, guiFile

scriptSettingsFile = os.path.join(
    os.path.dirname(__file__), 'SendSounds_Settings.json')
dbSettingsFile = os.path.join(os.path.dirname(
    __file__), './SendSounds-Classes/SendSounds_dbSettings.json')
guiFile = os.path.realpath(os.path.join(os.path.dirname(
    __file__), './SendSounds-GUI/SendSounds_App.py'))

# ---------------------------
#   [Required] Initialize Data (Only called on load)
# ---------------------------


def Init():
    global startMsg, soundsDB, sndGlobalVolume, saveScriptLogs, sndFolderSFX, sndCommandTrigger
    global triggerList, volumeList, pathList, msgList, sendAsList, commandList, sfxQ
    global streamer
    try:
        streamer = Parent.GetChannelName()
        startMsg = scriptLogger.logInit()
        sfxQ = deque()
        with codecs.open(scriptSettingsFile, mode='r', encoding='utf-8-sig') as f:
            scriptSettings = json.load(f)
        sndGlobalVolume = scriptSettings['sndGlobalVolume']
        saveScriptLogs = scriptSettings['saveScriptLogs']
        sndFolderSFX = scriptSettings['sndFolderSFX']
        sndCommandTrigger = scriptSettings['sndCommandTrigger']
        soundsDB = db(dbSettingsFile, scriptSettingsFile)
        startDBMsg = soundsDB.createTable()
        if saveScriptLogs:
            printLog(startDBMsg)
        triggerList = soundsDB.getInfoDB('sndTrigger')
        volumeList = soundsDB.getInfoDB('sndVolume')
        pathList = soundsDB.getInfoDB('sndFilePath')
        msgList = soundsDB.getInfoDB('sndSendMsg')
        sendAsList = soundsDB.getInfoDB('sndSendAs')
        commandList = ['play', 'opendb', 'reload', 'list']
    except Exception as e:
        Parent.SendStreamMessage('Script failed starting')
        Parent.SendStreamMessage(str(e))
    return

# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------


def Execute(data):
    global sndCommandTrigger, triggerList, saveScriptLogs
    if data.IsChatMessage() and data.IsFromTwitch():
        chatMsg = data.Message
        user = data.User
        if chatMsg.startswith(sndCommandTrigger):
            sndTrigger = chatMsg.replace(sndCommandTrigger, '')
            logMsg = '[{time}] (INF) - "{trigger}" was triggered by {user}'
            if sndTrigger in triggerList:
                logMsg += '\n[{time}] (SUC) - "{trigger}" is being sent to the overlay'
                RunCommand(user, 'play', sndTrigger)
            else:
                logMsg += '\n[{time}] (ERR) - "{trigger}" could not be sent to the overlay'
            logMsg = logMsg.format(
                time=scriptLogger.getTime(), trigger=sndTrigger, user=user)
            if saveScriptLogs:
                printLog(logMsg)
    return

# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------


def Tick():
    global sfxQ, sfxDuration
    if sfxQ and not Parent.IsOnCooldown(ScriptName, 'delay'):
        payload = sfxQ[0]
        sfx = payload['sfx']
        toPlay = payload['audio']
        if Parent.PlaySound(toPlay, 0):
            Parent.BroadcastWsEvent("EVENT_SENDSOUNDS", json.dumps(payload))
            SendChat(sfx)
            soundsDB.updateUseCount(sfx)
            sfxQ.popleft()
    return

# ---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
# ---------------------------


def Parse(parseString, userid, username, targetid, targetname, message):
    if '$sendsounds' in parseString:
        parseString = parseString.lower()
        regex = re.search(r'\$sendsounds\((.*)\)', parseString)
        if regex:
            if len(regex.group(1).split(' ')) > 1:
                command = regex.group(1).split(' ')[0]
                sound = regex.group(1).split(' ')[1]
                RunCommand(username, command, sound)
            else:
                command = regex.group(1).split(' ')[0]
                RunCommand(username, command)
            return parseString.replace(regex.group(0), "")
    return parseString

# ---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
# ---------------------------


def ReloadSettings():
    global scriptLogger
    scriptLogger.logEnd()
    Init()
    return

# ---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
# ---------------------------


def Unload():
    global scriptLogger
    scriptLogger.logEnd()
    return

# ---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
# ---------------------------


def ScriptToggled(state):
    global streamer
    if state:
        status = 'enabled'
    else:
        status = 'disabled'
    msg = '/me : @{streamer}, ({script} - {version}) is {status}...'
    msg = msg.format(streamer=streamer, script=ScriptName,
                     version=Version, status=status)
    SendInfo(streamer, 'whisper', msg)
    return

# ---------------------------
#   Script Functions
# ---------------------------


def printLog(msg):
    global scriptLogger
    scriptLogger.logWrite(msg)
    return


def RunCommand(user, command, *args):
    global sfxQ, streamer
    if command in commandList:
        if command == 'play' and user == streamer:
            sfxQ.append(SendAudioToOverlay(args[0]))
        if command == 'opendb' and user == streamer:
            OpenGUI()
        if command == 'reload' and user == streamer:
            ReloadSettings()
        if command == 'list':
            PrintSoundList(user)
    return


def SendInfo(user, mode, msg):
    if mode == 'whisper':
        Parent.SendStreamWhisper(user, msg)
    elif mode == 'chat':
        Parent.SendStreamMessage(msg)
    elif mode == 'both':
        Parent.SendStreamMessage(msg)
        Parent.SendStreamWhisper(user, msg)
    return


def SendAudioToOverlay(sfx):
    global payLoad
    index = triggerList.index(sfx)
    payload = {
        'sfx': sfx,
        "audio": pathList[index],
        "volume": (sndGlobalVolume * volumeList[index])/100
    }
    return payload


def SendChat(sfx):
    index = triggerList.index(sfx)
    toSend = msgList[index]
    sendAs = sendAsList[index]
    msg = ''
    if sendAs == 'Chat':
        msg = '{toSend}'
    elif sendAs == 'Announcement (/announce)':
        msg = '/announce {toSend}'
    elif sendAs == 'Action (/me)':
        msg = '/me : {toSend}'
    elif sendAs == 'Announcement+Action (/announce /me)':
        msg = '/announce /me : {toSend}'
    msg = msg.format(toSend=toSend)
    Parent.SendStreamMessage(msg)
    return


def PrintSoundList(user):
    msg = '/me : @{user} , those are the sounds you can pick from:'
    msg = msg.format(user=user)
    list = GetList()
    while len(list) != 0:
        if len(list) > 0:
            msg += '\n/me : {list}'.format(list=list[0])
            list.pop(0)
        else:
            list = []
    msg += '\n/me : in order to play any of the sounds, use {trigger} followed by the sound name to be played. Try out for example {trigger}{sound} on chat and enjoy!'
    msg = msg.format(trigger=sndCommandTrigger,
                     sound=triggerList[randint(0, len(triggerList))])
    Parent.SendStreamMessage(msg)
    return


def GetList():
    global triggerList
    msg = ''
    listToProcess = []
    for trigger in triggerList:
        msg += '{trigger}, '.format(trigger=trigger)
    msg = msg[:-2]
    while len(msg) != 0:
        listToProcess.append(msg[0:500])
        msg = msg[500:]
    return listToProcess

# ---------------------------
#   Streamlabs Chatbot GUI buttons functions
# ---------------------------


def OpenReadMe():
    ReadMe = 'https://github.com/vonschappler/SLCB-SendSounds#readme'
    os.startfile(ReadMe)
    return


def OpenUserGuide():
    Guide = 'https://github.com/vonschappler/SLCB-SendSounds/wiki/User-Guide'
    os.startfile(Guide)
    return


def OpenGUI():
    global guiFile
    try:
        command = 'py -2 \"{file}\"'.format(file=guiFile)
        os.system(command)
    except:
        command = 'python \"{file}"'.format(file=guiFile)
        os.system(command)
    return


def OpenDiscord():
    Discord = "http://rebrand.ly/vonDiscord"
    os.startfile(Discord)
    return


def OpenReleases():
    Release = "https://github.com/vonschappler/SLCB-SendSounds/releases"
    os.startfile(Release)
    return


def OpenDonation():
    PayPal = 'https://rebrand.ly/vonPayPal'
    os.startfile(PayPal)
    return


def OpenTwitch():
    Twitch = "http://rebrand.ly/vonTwitch"
    os.startfile(Twitch)
    return


def OpenSite():
    os.startfile(Website)
    return
