import pygame
import os
import ttk
import Tkinter as tk
import tkFileDialog as dialog
import SendSounds_Functions as fn

global scriptSettings, settingsVars, soundVars, chatOptions, soundList, database, soundEditVars, pygameLoaded, passCheck, emtpyEntriesCheck
chatOptions = ['Chat', 'Announcement (/announce)',
               'Action (/me)', 'Announcement+Action (/announce /me)']
scriptSettings = fn.readJson(fn.scriptSettingsFile)
database = fn.initDb()
soundList = fn.getTriggers(database)
if len(soundList) > 0:
    passCheck = fn.checkIntegrity()
    emtpyEntriesCheck = fn.dbClear()
else:
    passCheck = [0, 0]
    emtpyEntriesCheck = [0]
soundList.insert(0, 'Select one...')


def createTab(page):
    global settingsTab, fontOpts, variables, sfxOpts, passCheck, emtpyEntriesCheck, database, scriptSettings, soundList
    settingsTab = ttk.Frame(page)
    settingsTab.pack()
    createVars()
    checkPygame()
    configureTab(settingsTab)
    addCanvas(settingsTab)
    addHelp(settingsTab)
    return settingsTab


def createVars():
    global settingsVars, soundVars, soundEditVars, scriptSettings, database
    settingsVars = []
    soundVars = []
    soundEditVars = []
    if scriptSettings == None:
        msg = '[{time}] (WAR) - It seems this is the firt time you make use of this script. A default "{file}" is being created with some default options.'
        msg += '\n[{time}] (WAR) - If you still see this message after the file is created, please contact the developer.'
        msg = msg.format(time=fn.dbLogger.getTime(),
                         file=fn.scriptSettingsFile)
        fn.printLog(msg)
        defData = {
            'sndCommandTrigger': '#',
            'sndFolderSFX': os.path.realpath(os.path.join(os.path.dirname(__file__), '../SendSounds-Sounds')).lower(),
            'sndGlobalVolume': 50,
            'saveScriptLogs': True
        }
        fn.createSettings(defData, fn.scriptSettingsFile)
        currentSettings = defData
    else:
        currentSettings = scriptSettings
    sndCommandTrigger = tk.StringVar(
        value=currentSettings['sndCommandTrigger'])
    sndFolderSFX = tk.StringVar(value=currentSettings['sndFolderSFX'])
    sndGlobalVolume = tk.IntVar(value=currentSettings['sndGlobalVolume'])
    saveScriptLogs = tk.BooleanVar(value=currentSettings['saveScriptLogs'])
    settingsVars.append(sndCommandTrigger)
    settingsVars.append(sndFolderSFX)
    settingsVars.append(sndGlobalVolume)
    settingsVars.append(saveScriptLogs)
    sndListTrigger = tk.StringVar()
    sndTrigger = tk.StringVar()
    sndFilePath = tk.StringVar()
    sndVolume = tk.IntVar()
    sndSendMsg = tk.StringVar()
    sndSendAs = tk.StringVar()
    sndEnable = tk.BooleanVar()
    sndUsesCount = tk.IntVar()
    soundVars.append(sndListTrigger)
    soundVars.append(sndTrigger)
    soundVars.append(sndFilePath)
    soundVars.append(sndVolume)
    soundVars.append(sndSendMsg)
    soundVars.append(sndSendAs)
    soundVars.append(sndEnable)
    soundVars.append(sndUsesCount)
    return [settingsVars, soundVars, soundEditVars]


def configureTab(tab):
    tab.columnconfigure(0, weight=30)
    tab.columnconfigure(1, weight=0)
    tab.columnconfigure(2, weight=10)
    tab.rowconfigure(0, weight=10)
    return


def addCanvas(tab):
    global settingsFrame
    canvas = tk.Canvas(tab, takefocus=0, highlightthickness=0)
    canvas.grid(column=0, row=0, sticky=tk.W+tk.N+tk.S +
                tk.E, padx=10, columnspan=2, pady=10)
    canvas.columnconfigure(0, weight=10)
    canvas.columnconfigure(1, weight=0)
    settingsFrame = addComponents(canvas)
    canvas.create_window((0, 0), window=settingsFrame, anchor=tk.N+tk.E)
    scrollY = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=canvas.yview)
    scrollY.grid(row=0, column=1, padx=[0, 0],
                 sticky=tk.N+tk.S+tk.E, pady=[20, 10])
    canvas['yscrollcommand'] = scrollY.set
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox('all'))
    canvas.yview_moveto(0)
    return


def addComponents(place):
    frame = tk.Frame(place, width=place.winfo_width())
    addScriptSettings(frame, 0)
    addIndividualSoundSettings(frame, 1)
    addDBManager(frame, 2)
    addLogController(frame, 3)
    return frame


def addScriptSettings(canvas, row):
    global globalSndFolder
    labelFrame = ttk.Labelframe(
        canvas, text=" Script Settings: ", takefocus=0)
    labelFrame.grid(row=row, column=0, sticky=tk.E +
                    tk.W+tk.N+tk.S, padx=10, pady=10)
    labelFrame.config(border=1, relief=tk.SOLID)
    labelFrame.columnconfigure(0, weight=0)
    labelFrame.columnconfigure(1, weight=0)
    labelFrame.columnconfigure(2, weight=30)
    ttk.Label(labelFrame, text='Sounds/Commands custom trigger: ').grid(row=0,
                                                                        column=0, sticky=tk.E+tk.W, pady=[0, 5])
    globalCommandTrigger = ttk.Entry(
        labelFrame, name='soundsTrigger', textvariable=settingsVars[0], font=('Calibri', 12))
    globalCommandTrigger.grid(
        row=0, column=1, columnspan=2, sticky=tk.E+tk.W, ipadx=5, ipady=2, pady=[0, 5])
    globalCommandTrigger.focus_set()
    ttk.Label(labelFrame, text='Sounds folder: ').grid(
        row=1, column=0, sticky=tk.E+tk.W, pady=[0, 5])
    globalSndFolder = ttk.Entry(
        labelFrame, name='soundsFolder', textvariable=settingsVars[1], font=('Calibri', 12))
    globalSndFolder.grid(row=2, column=0, sticky=tk.E +
                         tk.W, ipadx=5, ipady=2, pady=[0, 5])
    ttk.Label(labelFrame, text=' or ').grid(row=2, column=1)
    folderSelectButton = ttk.Button(
        labelFrame, text='Select a folder...', name='soundsFolderBtn')
    folderSelectButton.grid(row=2, column=2, sticky=tk.E+tk.W, pady=[0, 5])
    folderSelectButton.configure(command=selectFolder)
    ttk.Label(labelFrame, text='Global sound volume (overlay): ').grid(
        row=3, column=0, sticky=tk.E+tk.W, pady=[5, 0])
    globalSndVolumeLabel = ttk.Label(labelFrame, text='{vol}%'.format(
        vol=settingsVars[2].get()), anchor=tk.E)
    globalSndVolumeLabel.grid(row=3, column=1, pady=[5, 0], padx=[0, 10])
    globalSndVolumeScale = ttk.Scale(
        labelFrame, variable=settingsVars[2], from_=0, to=100, name='soundsVolume')
    globalSndVolumeScale.configure(
        command=lambda e,  label=globalSndVolumeLabel, var=settingsVars[2]: fn.setVolume(label, var))
    globalSndVolumeScale.grid(
        row=3, column=2, columnspan=2, sticky=tk.E+tk.W, ipadx=5, ipady=5, pady=[5, 0])
    scriptLogsCheck = ttk.Checkbutton(labelFrame, text='Save logs from Streamlabs Chatbot when running the script?                         ',
                                      name='saveScriptLogs', onvalue=True, offvalue=False, variable=settingsVars[3])
    scriptLogsCheck.grid(row=4, column=0, columnspan=3,
                         pady=5, sticky=tk.E+tk.W)
    buttonsFrame = tk.Frame(labelFrame, width=labelFrame.winfo_width())
    buttonsFrame.grid(row=5, column=0, columnspan=3,
                      sticky=tk.E+tk.W, pady=[5, 0])
    buttonsFrame.columnconfigure(0, weight=1)
    buttonsFrame.columnconfigure(1, weight=2)
    buttonsFrame.columnconfigure(2, weight=2)
    restoreBckBtn = ttk.Button(
        buttonsFrame, text='Restore backup', name='restoreBackBtn')
    restoreBckBtn.grid(row=0, column=0, sticky=tk.E+tk.W, padx=[0, 5])
    restoreBckBtn.config(command=lambda file=fn.scriptSettingsFile,
                         cb=setSettings: fn.restoreFileBackup(file, cb))
    createBckBtn = ttk.Button(
        buttonsFrame, text='Create backup', name='createBackBtn')
    createBckBtn.grid(row=0, column=1, sticky=tk.E+tk.W, padx=[5, 5])
    createBckBtn.config(
        command=lambda file=fn.scriptSettingsFile: fn.createFileBackup(file))
    saveBtn = ttk.Button(buttonsFrame, text='Save settings',
                         name='saveSettingsBtn')
    saveBtn.grid(row=0, column=2, sticky=tk.E+tk.W, padx=[5, 0])
    saveBtn.config(command=lambda file=fn.scriptSettingsFile,
                   cb1=getScriptSettings, cb2=setSettings: fn.saveFile(file, cb1, cb2))
    return


def addIndividualSoundSettings(canvas, row):
    global soundList, soundSelect, soundChat, soundTrigger, chatSelect, soundVolumeLabel, sndEnableCheck, soundUseCount, pygameLoaded
    labelFrame = ttk.Labelframe(
        canvas, text=" Individual Sound Adjustments: ", takefocus=0)
    labelFrame.grid(row=row, column=0, sticky=tk.E +
                    tk.W+tk.N+tk.S, padx=10, pady=10)
    labelFrame.config(border=1, relief=tk.SOLID)
    labelFrame.columnconfigure(3, weight=20)
    labelFrame.columnconfigure(4, weight=20)
    ttk.Label(labelFrame, text='Change settings for sound: ').grid(
        row=0, column=0, pady=[0, 5], sticky=tk.E+tk.W)
    refreshListBnt = ttk.Button(
        labelFrame, text='Refresh list', name='soundRefreshBtn')
    refreshListBnt.grid(row=0, column=1, padx=[0, 10], pady=[
                        0, 5], sticky=tk.E+tk.W)
    refreshListBnt.configure(command=lambda db=database: updateList(db))
    soundSelect = ttk.Combobox(labelFrame, values=soundList, state='readonly', font=(
        'Calibri', 12), textvar=soundVars[0], name='soundSelect')
    soundSelect.grid(row=0, column=2, sticky=tk.E +
                     tk.W, pady=[0, 5], columnspan=3)
    soundSelect.current(0)
    soundSelect.bind('<<ComboboxSelected>>', lambda e,
                     triggerSelector=soundSelect: selectSound(triggerSelector))
    ttk.Label(labelFrame, text='Sound trigger: ').grid(
        row=1, column=0, pady=[5, 5], sticky=tk.E+tk.W)
    soundTrigger = ttk.Entry(labelFrame, font=(
        'Calibri', 12), textvariable=soundVars[1], name='soundTrigger')
    soundTrigger.grid(row=1, column=1, sticky=tk.E+tk.W,
                      pady=[5, 5], columnspan=4, ipadx=5, ipady=2)
    ttk.Label(labelFrame, text='Chat message sent with sound: ').grid(
        row=2, column=0, pady=[5, 5], sticky=tk.E+tk.W)
    soundChat = ttk.Entry(labelFrame, font=('Calibri', 12),
                          textvariable=soundVars[4], name='soundChat')
    soundChat.grid(row=2, column=1, sticky=tk.E+tk.W,
                   pady=[5, 5], columnspan=4, ipadx=5, ipady=2)
    ttk.Label(labelFrame, text='Send chat as: ').grid(
        row=3, column=0, pady=[5, 5], sticky=tk.E+tk.W)
    chatSelect = ttk.Combobox(labelFrame, values=chatOptions, state='readonly', font=(
        'Calibri', 12), textvariable=soundVars[5], name='soundSendAs')
    chatSelect.grid(row=3, column=1, sticky=tk.E +
                    tk.W, pady=[5, 5], columnspan=4)
    chatSelect.current(0)
    ttk.Label(labelFrame, text='Selected Sound volume: ').grid(
        row=4, column=0, sticky=tk.E+tk.W, pady=[5, 5])
    previewSnd = ttk.Button(
        labelFrame, text='Preview sound', name='soundPreviewBtn')
    previewSnd.grid(row=4, column=1, padx=[0, 10], pady=[
                    5, 5], sticky=tk.E+tk.W)
    if pygameLoaded:
        previewSnd.configure(state='enabled')
    else:
        previewSnd.configure(state='disabled')
    previewSnd.configure(
        command=lambda sound=soundVars[2], vol=soundVars[3]: previewSound(sound, vol))
    soundVolumeLabel = ttk.Label(labelFrame, text='{vol}%'.format(
        vol=soundVars[3].get()), anchor=tk.E)
    soundVolumeLabel.grid(row=4, column=2, pady=[5, 5], padx=[10, 5])
    soundVolumeScale = ttk.Scale(
        labelFrame, variable=soundVars[3], from_=0, to=100, name='soundVolume')
    soundVolumeScale.configure(
        command=lambda e,  label=soundVolumeLabel, var=soundVars[3]: fn.setVolume(label, var))
    soundVolumeScale.grid(row=4, column=3, sticky=tk.E +
                          tk.W, ipadx=5, ipady=5, pady=[5, 5], columnspan=2)
    sndEnableCheck = ttk.Checkbutton(labelFrame, text='Enable the use of this sound on stream?',
                                     onvalue=1, offvalue=0, variable=soundVars[6], name='soundEnable')
    sndEnableCheck.grid(row=5, column=0, columnspan=5, sticky=tk.E+tk.W)
    soundStats = ttk.LabelFrame(
        labelFrame, text=' Statistics for selected sound: ')
    soundStats.grid(row=6, sticky=tk.E+tk.W, pady=[0, 10], columnspan=5)
    soundStats.config(border=1, relief=tk.SOLID)
    soundUseCount = ttk.Label(
        soundStats, text='Total use count: {count}'.format(count=soundVars[7].get()))
    soundUseCount.grid(row=0, column=0)
    ttk.Separator(labelFrame).grid(
        row=7, column=0, sticky=tk.E+tk.W, columnspan=5)
    saveChangesBtn = ttk.Button(
        labelFrame, text='Save changes', name="soundSaveBtn")
    saveChangesBtn.grid(row=8, column=0, pady=[10, 0], padx=[
                        0, 5], sticky=tk.E+tk.W, columnspan=2)
    saveChangesBtn.configure(
        command=lambda mode='change': updateSoundSettings(mode))
    cancelChangesBtn = ttk.Button(
        labelFrame, text='Ignore changes', name='soundCancelBtn')
    cancelChangesBtn.grid(row=8, column=2, pady=[10, 0], padx=[
                          5, 5], sticky=tk.E+tk.W, columnspan=3)
    cancelChangesBtn.configure(
        command=lambda current=soundSelect: selectSound(current))
    return


def addDBManager(canvas, row):
    global passCheck, integrityCheckMsg, fixDatabaseDisable, fixDatabaseDelete, emptyEntriesMsg, clearDatabase
    labelFrame = ttk.Labelframe(
        canvas, text=" Database Manager: ", takefocus=0)
    labelFrame.grid(row=row, column=0, sticky=tk.E +
                    tk.W+tk.N+tk.S, padx=10, pady=10)
    labelFrame.config(border=1, relief=tk.SOLID)
    labelFrame.columnconfigure(0, weight=10)
    labelFrame.columnconfigure(1, weight=10)
    integrityCheckMsg = ttk.Label(labelFrame)
    integrityCheckMsg.grid(row=0, column=0, columnspan=2, sticky=tk.E+tk.W)
    fixDatabaseDisable = ttk.Button(
        labelFrame, text='Fix database Integrity - disable mode', name='fixDisableBtn')
    fixDatabaseDisable.grid(row=1, column=0, sticky=tk.E+tk.W, padx=[0, 5])
    fixDatabaseDisable.configure(
        command=lambda mode='disable', cb=fullRecheck: fn.dbIssueFix(mode, cb))
    fixDatabaseDelete = ttk.Button(
        labelFrame, text='Fix database Integrity - delete mode', name="fixDeleteBtn")
    fixDatabaseDelete.grid(row=1, column=1, sticky=tk.E +
                           tk.W, padx=[5, 0], pady=[0, 5])
    fixDatabaseDelete.configure(
        command=lambda mode='delete', cb=fullRecheck: fn.dbIssueFix(mode, cb))
    if passCheck[0]:
        integrityCheckMsg['text'] = 'No issues found on your database!'
        fixDatabaseDisable.configure(state='disabled')
        fixDatabaseDelete.configure(state='disabled')
    else:
        text = 'Total integrity issues found: {issuesCount}'
        integrityCheckMsg['text'] = text.format(issuesCount=passCheck[1])
        fixDatabaseDisable.configure(state='enabled')
        fixDatabaseDelete.configure(state='enabled')
    ttk.Separator(labelFrame).grid(row=3, column=0,
                                   columnspan=2, sticky=tk.E+tk.W, pady=5)
    emptyEntriesMsg = ttk.Label(labelFrame)
    emptyEntriesMsg.grid(row=4, column=0, columnspan=2, sticky=tk.E+tk.W)
    clearDatabase = ttk.Button(
        labelFrame, text='Remove triggers without sound from database', name="fixClearBtn")
    clearDatabase.grid(row=5, column=0, columnspan=2,
                       sticky=tk.E+tk.W, pady=[5, 0])
    clearDatabase.configure(command=lambda mode='fix',
                            cb=fullRecheck: fn.dbClear(mode, cb))
    if emtpyEntriesCheck > 0:
        text = 'Triggers disabled or with no sound: {count}'
        emptyEntriesMsg['text'] = text.format(count=emtpyEntriesCheck)
        clearDatabase.configure(state='enabled')
    else:
        emptyEntriesMsg['text'] = 'Your database is cleared from triggers with no sound, no need to worry!'
        clearDatabase.configure(state='disabled')
    return


def addLogController(canvas, row):
    labelFrame = ttk.Labelframe(canvas, text=" Logs Controller: ", takefocus=0)
    labelFrame.grid(row=row, column=0, sticky=tk.E +
                    tk.W+tk.N+tk.S, padx=10, pady=10)
    labelFrame.config(border=1, relief=tk.SOLID)
    labelFrame.columnconfigure(0, weight=0)
    labelFrame.columnconfigure(1, weight=10)
    openDashboardLogs = ttk.Button(
        labelFrame, text='Open Dashboard Logs Folder', name='logDashOpen')
    openDashboardLogs.grid(row=0, column=0, sticky=tk.E +
                           tk.W+tk.N+tk.S, padx=[0, 5], pady=5)
    openDashboardLogs.configure(command=fn.openDashboardLogs)
    deleteDashboardLogs = ttk.Button(
        labelFrame, text='Delete Dashboard Logs', name="logDashDelete")
    deleteDashboardLogs.grid(
        row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S, padx=[5, 0], pady=5)
    deleteDashboardLogs.configure(command=fn.deleteDashboardLogs)
    ttk.Separator(labelFrame).grid(row=1, column=0,
                                   columnspan=2, sticky=tk.E+tk.W, pady=5)
    openScriptLogs = ttk.Button(
        labelFrame, text='Open Script Logs Folder', name='logScriptOpen')
    openScriptLogs.grid(row=2, column=0, sticky=tk.E +
                        tk.W+tk.N+tk.S, padx=[0, 5], pady=5)
    openScriptLogs.configure(command=fn.openScriptLogs)
    deleteScriptLogs = ttk.Button(
        labelFrame, text='Delete Script Logs', name='logScriptDelete')
    deleteScriptLogs.grid(row=2, column=1, sticky=tk.E +
                          tk.W+tk.N+tk.S, padx=[5, 0], pady=5)
    deleteScriptLogs.configure(command=fn.deleteScriptLogs)
    ttk.Separator(labelFrame).grid(row=3, column=0,
                                   columnspan=2, sticky=tk.E+tk.W, pady=5)
    deleteAllLogs = ttk.Button(
        labelFrame, text='Delete All Log files', name='logDeleteAll')
    deleteAllLogs.grid(row=4, column=0, sticky=tk.E+tk.W +
                       tk.N+tk.S, pady=[5, 10], columnspan=2)
    deleteAllLogs.configure(command=fn.deleteAllLogs)
    return


def addHelp(tab):
    global tabHelpText
    tabHelpFrame = ttk.Labelframe(tab, text=' Quick Help: ', takefocus=0)
    tabHelpFrame.grid(row=0, column=2, sticky=tk.E +
                      tk.W+tk.N+tk.S, padx=10, pady=10)
    tabHelpText = tk.Text(tabHelpFrame, width=1, height=1,
                          wrap=tk.WORD, takefocus=0)
    tabHelpText.pack(fill=tk.BOTH, expand=tk.YES, pady=[5, 10])
    tabHelpFrame.columnconfigure(0, weight=10)
    tabHelpFrame.rowconfigure(0, weight=1)
    tabHelpText.grid(column=0, row=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
    scrollY = ttk.Scrollbar(
        tabHelpFrame, orient=tk.VERTICAL, command=tabHelpText.yview)
    scrollY.grid(column=1, row=0, sticky=tk.E+tk.N+tk.S)
    tabHelpText['yscrollcommand'] = scrollY.set
    return tabHelpText


# Tab specific functions
def setSettings():
    global scriptSettings, passCheck, emtpyEntriesCheck, settingsVars, database, globalSndFolder
    globalSndFolder.delete(0, tk.END)
    if settingsVars[1].get() == 'DEFAULT':
        folder = database.soundsFolder
        settingsVars[1].set('DEFAULT')
    else:
        folder = settingsVars[1].get()
        settingsVars[1].set(folder)
    database = fn.initDb()
    autoAddMsg = database.autoAddSounds(folder.lower())
    fn.printLog(autoAddMsg)
    fullRecheck()
    globalSndFolder.insert(tk.END, database.soundsFolder)
    return database


def fullRecheck():
    global database
    recheckIntegrity()
    recheckMissingFiles()
    updateList(database)
    return


def getScriptSettings():
    global database
    data = {
        'sndCommandTrigger': settingsVars[0].get(),
        'sndFolderSFX': settingsVars[1].get(),
        'sndGlobalVolume': settingsVars[2].get(),
        'saveScriptLogs': settingsVars[3].get()
    }
    return data


def selectFolder():
    global globalSndFolder
    newDir = dialog.askdirectory()
    if newDir != '':
        globalSndFolder.delete(0, tk.END)
        globalSndFolder.insert(tk.END, newDir.lower().replace('\\', '/'))
    return


def selectSound(triggerSelector):
    global soundChat
    selected = triggerSelector.current()
    msg = ''
    if selected != 0:
        trigger = soundList[selected]
        result = database.findSound(trigger)
        if result:
            msg += '[{time}] (INF) - "{trigger}" selected for customization...'
            for var in soundVars:
                var.set(result[soundVars.index(var)])
                # print(var.get()) # Delete this line for production
            updateSoundSettings()
        else:
            msg += '[{time}] (ERR) - Unable to select the requested trgger and sound for customization...'
            msg += '\n[{time}] (ERR) - System message: "{trigger}" does not exist in the database'
        msg = msg.format(time=fn.dbLogger.getTime(), trigger=result[1])
    else:
        msg += '[{time}] (WAR) - No sound was selected for customization'
        updateSoundSettings('reset')
        msg = msg.format(time=fn.dbLogger.getTime())
    fn.printLog(msg)
    return soundVars


def previewSound(sound, volSetter):
    soundFile = sound.get()
    vol = volSetter.get()
    msg = ''
    e = None
    if soundFile != '':
        try:
            pygame.mixer.music.set_volume(vol/100.0)
            pygame.mixer.music.load(soundFile)
            pygame.mixer.music.play(loops=0)
            msg = '[{time}] (SUC) - Playing preview of "{audio}" with volume "{vol}"%...'
        except Exception as e:
            msg = '[{time}] (ERR) - Unable preview "{audio}" with volume "{vol}"%...'
            msg += '\n[{time}] (ERR) - System message: {err}'
            pass
    if msg != '':
        msg = msg.format(time=fn.dbLogger.getTime(),
                         audio=soundFile, vol=vol, err=e)
    else:
        msg = '[{time}] (WAR) - Sound preview cannot be played if a sound is not selected'
        msg = msg.format(time=fn.dbLogger.getTime())
    fn.printLog(msg)
    return


def updateSoundSettings(*args):
    global soundSelect, soundTrigger, chatSelect, soundChat, soundVolumeLabel, soundUseCount, sndEnableCheck
    if not args:
        chatSelect.set(soundVars[5].get())
        soundVolumeLabel['text'] = '{vol:.0f}%'.format(vol=soundVars[3].get())
        soundUseCount['text'] = 'Total use count: {count}'.format(
            count=soundVars[7].get())
    elif args[0] == 'change':
        data = []
        for var in soundVars:
            var.set(soundVars[soundVars.index(var)].get())
            # print(var.get()) # Delete this line for production
        for value in soundVars:
            data.append(soundVars[soundVars.index(value)].get())
        fn.updateSound(soundVars[0].get(), data)
        updateList(database)
        updateSoundSettings('reset')
    elif args[0] == 'reset':
        soundVars[0].set(0)
        soundVars[1].set('')
        soundVars[2].set('')
        soundVars[3].set(0)
        soundVars[4].set(0)
        soundVars[5].set(0)
        soundVars[6].set(False)
        soundVars[7].set(0)
        soundChat.delete(0, tk.END)
        soundSelect.current(0)
        chatSelect.current(soundVars[5].get())
        soundVolumeLabel['text'] = '{vol:.0f}%'.format(vol=soundVars[3].get())
        soundUseCount['text'] = 'Total use count: {count}'.format(
            count=soundVars[7].get())
    return soundVars


def checkPygame():
    global pygameLoaded
    try:
        pygame.mixer.init()
        pygameLoaded = True
        msg = '[{time}] (SUC) - Required library for sound preview "{lib}" loaded with success'
        msg = msg.format(time=fn.dbLogger.getTime(), lib='pygame 2.0.3')
        fn.printLog(msg)
    except Exception as e:
        pygameLoaded = False
        msg = '[{time}] (ERR) - Required library for sound preview "({lib}" could not be loaded. Audio preview functionality will be disabeld.'
        msg += '\n[{time}] (INF) - To enable this feature, please refer to the script documentation and install the "{lib}" dependecy'
        msg += '\n[{time}] (ERR) - System message: {err}'
        msg = msg.format(time=fn.dbLogger.getTime(), lib='pygame 2.0.3', err=e)
        fn.printLog(msg)
        pass
    return


def updateList(db):
    global soundList, soundSelect
    soundSelect['values'] = []
    soundList = fn.getTriggers(db)
    soundList.insert(0, 'Select one')
    soundSelect['values'] = soundList
    return soundList


def recheckIntegrity():
    global integrityCheckMsg, fixDatabaseDisable, fixDatabaseDelete
    result = fn.checkIntegrity()
    if result[0]:
        integrityCheckMsg['text'] = 'No issues found on your database!'
        fixDatabaseDisable.configure(state='disabled')
        fixDatabaseDelete.configure(state='disabled')
    else:
        text = 'Total integrity issues found: {issuesCount}'
        integrityCheckMsg['text'] = text.format(issuesCount=result[1])
        fixDatabaseDisable.configure(state='enabled')
        fixDatabaseDelete.configure(state='enabled')
    return


def recheckMissingFiles():
    global emptyEntriesMsg, clearDatabase
    result = fn.dbClear()
    if result > 0:
        text = 'Triggers disabled or with no sound: {count}'
        emptyEntriesMsg['text'] = text.format(count=result)
        clearDatabase.configure(state='enabled')
    else:
        emptyEntriesMsg['text'] = 'Your database is cleared from triggers with no sound, no need to worry!'
        clearDatabase.configure(state='disabled')
    return
