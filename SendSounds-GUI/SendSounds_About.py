import os
import ttk
import Tkinter as tk
import SendSounds_Theme
import SendSounds_Functions as fn


def createTab(page):
    global aboutTab
    aboutTab = ttk.Frame(page)
    aboutTab.pack()
    aboutTab.columnconfigure(0, weight=10)
    aboutTab.rowconfigure(0, weight=10)
    tabHelpFrame = ttk.Labelframe(
        aboutTab, text=' Aditional Information: ', takefocus=0)
    tabHelpFrame.grid(row=0, column=0, sticky=tk.E +
                      tk.W+tk.N+tk.S, padx=10, pady=10)
    tabHelpText = tk.Text(tabHelpFrame, width=1, height=1,
                          wrap=tk.WORD, takefocus=0)
    aboutFile = os.path.realpath(os.path.join(
        os.path.dirname(__file__), 'assets/SendSounds_About.txt'))
    try:
        aboutContent = open(aboutFile)
        aboutContentText = aboutContent.read()
        tabHelpText.insert(tk.END, aboutContentText)
        aboutContent.close()
        msg = '[{time}] (INF) - Required asset "{file}" loaded with success!)'
        e = None
    except Exception as e:
        aboutContentText = "File not found...\nPlease contact the developer."
        tabHelpText.insert(tk.END, aboutContentText)
        msg = '[{time}] (ERR) - Unable to read {file}...'
        msg += '\n[{time}] (ERR) - System message: {err}'
        pass
    msg = msg.format(time=fn.dbLogger.getTime(), file=aboutFile, err=e)
    fn.printLog(msg)
    tabHelpText.config(state='disabled', selectbackground=SendSounds_Theme.darkGray,
                       selectforeground=SendSounds_Theme.darkWhite, cursor='arrow')
    tabHelpText.pack(fill=tk.BOTH, expand=tk.YES, pady=[5, 10])
    tabHelpFrame.columnconfigure(0, weight=10)
    tabHelpFrame.rowconfigure(0, weight=1)
    tabHelpText.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
    scrollY = ttk.Scrollbar(
        tabHelpFrame, orient=tk.VERTICAL, command=tabHelpText.yview)
    scrollY.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)
    tabHelpText['yscrollcommand'] = scrollY.set
    return aboutTab
