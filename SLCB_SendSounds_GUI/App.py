import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../SLCB_SendSounds_Classes'))
import ttk, Tkinter as tk, theme
import dbFunctions as fn
import tabAbout, tabSettings

global scriptName, version, icofile, runAs
scriptName = fn.dbLogger.scriptName
version = fn.dbLogger.version
icoFile = os.path.realpath(os.path.join(os.path.dirname(__file__), 'assets/icon.ico'))

#---------------------------
#   Dashboard Creation
#---------------------------
def Init():
    global root, style, mainFrame
    root = tk.Tk()
    screenW = root.winfo_screenwidth()
    windowW = int(screenW/2)
    centerX = int(screenW/2 - windowW/2)
    screenH = root.winfo_screenheight()
    windowH = int(screenH/2)
    centerY = int(screenH/2 - windowH/2)
    geometry = '{width}x{height}+{posX}+{posY}'
    geometry = geometry.format(width=str(windowW), height=str(windowH), posX=str(centerX), posY=str(centerY))
    root.geometry(geometry)
    root.columnconfigure(0, weight=2)
    root.rowconfigure(0, weight=2)
    root.resizable(False, False)
    root.configure(bg=theme.darkGray)
    statusBarFrame = ttk.Frame(root, takefocus=0)
    statusBarFrame.grid(column=0, row=2, sticky=tk.W+tk.E, columnspan=3)
    statusBarFrame.columnconfigure(0, weight=10)
    statusBarFrame.columnconfigure(1, weight=2)
    statusBarLeft = ttk.Label(statusBarFrame, anchor=tk.W, relief=tk.GROOVE, justify=tk.RIGHT, style='status.TLabel', takefocus=0)
    statusBarLeft.grid(column=0, row=0, sticky=tk.W+tk.E, columnspan=2)
    statusBarLeft.grid_propagate(False)
    statusBarRightText = ' {script} {version} '
    statusBarRightText = statusBarRightText.format(script=scriptName, version=version)
    statusBarRight = ttk.Label(statusBarFrame, text=statusBarRightText, anchor=tk.E, relief=tk.GROOVE, justify=tk.RIGHT, style='status.TLabel', takefocus=0)
    statusBarRight.grid(column=2, row=0, sticky=tk.W+tk.E, ipadx=10)
    statusBarRight.grid_propagate(False)
    title = statusBarRightText + '- dashboard'
    root.iconbitmap(icoFile)
    root.title(title)
    root.bind_all('<FocusOut>', lambda e, root=root: fn.unselect(root))
    root.bind_all('<Button-1>', lambda e: 'break')
    style=theme.CreateStyle()
    style.theme_use('vonSchappler')
    theme.AddRootOptions(root)
    mainFrame = ttk.Notebook(root, takefocus=0)
    mainFrame.grid(column=0, row=0, sticky=tk.E+tk.W+tk.N+tk.S, ipadx=10)
    mainFrame.add(tabSettings.createTab(mainFrame), text='Settings')
    mainFrame.add(tabAbout.createTab(mainFrame), text='About')
    mainFrame.bind('<<NotebookTabChanged>>', lambda e, frame=mainFrame, bar=statusBarLeft: fn.changeTabStatus(frame, bar))
    root.bind_all('<FocusIn>', lambda e, root=root, textZone=tabSettings.tabHelpText : fn.changeHelp(e, root, textZone))
    return

Init()

#---------------------------
#   Tab styling to fit window
#---------------------------
style.configure('TNotebook.Tab', width=root.winfo_screenwidth()/len(mainFrame.tabs()))

root.mainloop()
fn.dbLogger.logEnd()