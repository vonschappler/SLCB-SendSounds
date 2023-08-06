import ttk
import Tkinter as tk

global teal, darkWhite, darkGray, lightBlack
darkGray = "#333333"
lightGray = "#666666"
lightBlack = "#1b1c1d"
darkWhite = "#eeeeee"
teal = "#16b2ab"


def CreateStyle():
    style = ttk.Style()
    style.theme_create('vonSchappler')
    style.theme_settings('vonSchappler', {
        'TScale': {
            'configure': {
                'background': teal,
                'borderwidth': 0,
                'foreground': darkGray,
                'sliderrelief': tk.FLAT,
                'troughcolor': lightBlack,
                'sliderthickness': 20
            },
            'map': {
                'sliderrelief': [
                    ('focus', tk.GROOVE),
                    ('active', tk.GROOVE)
                ],
                'troughcolor': [
                    ('focus', lightBlack)
                ],
                'borderwidth': [
                    ('focus', 1)
                ]
            }
        },
        'TCheckbutton': {
            'configure': {
                'background': darkGray,
                'font': ('calibri', 15),
                'foreground': darkWhite,
                'indicatordiameter': 18,
                'indicatorrelief': tk.FLAT,
                'indicatorcolor': lightBlack,
            },
            'map': {
                'indicatorcolor': [
                    ('selected', teal)
                ],
                'indicatorrelief': [
                    ('focus', tk.GROOVE),
                    ('selected', tk.FLAT)
                ],
                'focuscolor': [
                    ('selected', darkGray),
                    ('!selected', darkGray)
                ]
            }
        },
        'TButton': {
            'configure': {
                'borderwidth': 0,
                'padding': 10,
                'background': teal,
                'foreground': darkWhite,
                'anchor': tk.CENTER,
                'font': ('Calibri', 12, 'bold'),
            },
            'map': {
                'background': [
                    ('disabled', lightBlack),
                    ('pressed', darkWhite),
                    ('active', lightBlack),
                    ('focus', lightBlack)
                ],
                'foreground': [
                    ('disabled', darkWhite),
                    ('pressed', lightBlack),
                    ('active', teal),
                    ('focus', darkWhite)
                ],
                'relief': [
                    ('pressed', tk.SUNKEN),
                    ('!pressed', tk.FLAT),
                ],
                'focuscolor': [
                    ('disabled', darkGray),
                    ('pressed', 'white'),
                    ('active', lightBlack)
                ]
            }
        },
        'TLabel': {
            'configure': {
                'background': darkGray,
                'foreground': darkWhite,
                'font': ('Calibri', 15),
            }
        },
        'status.TLabel': {
            'configure': {
                'background': darkGray,
                'foreground': darkWhite,
                'font': ('Calibri', 12),
            }
        },
        'TEntry': {
            'configure': {
                'foreground': darkWhite,
                'insertcolor': darkWhite,
                'fieldbackground': lightBlack,
                'borderwidth': 0,
                'selectbackground': darkWhite,
                'selectforeground': darkGray,
                'padding': 5
            },
            'map': {
                'relief': [
                    ('focus', tk.ACTIVE)
                ],
                'borderwidth': [
                    ('focus', 2)
                ],
                'darkcolor': [
                    ('focus', teal)
                ],
                'lightcolor': [
                    ('focus', teal)
                ]
            }
        },
        'TLabelframe': {
            'configure': {
                'foreground': darkWhite,
                'relief': tk.SOLID,
                'background': darkGray,
                'borderwidth': 1,
                'padding': [10, 10, 10, 10]
            }
        },
        'TLabelframe.Label': {
            'configure': {
                'font': ('Calibri', 15, 'bold'),
                'background': darkGray,
                'foreground': darkWhite
            }
        },
        'TFrame': {
            'configure': {
                'background': darkGray,
                'foreground': darkWhite
            }
        },
        'TNotebook': {
            'configure': {
                'tabmargins': [1, 0, 0, 2],
                'background': darkGray,
                'foreground': darkWhite,
                'borderwidth': 0
            }
        },
        'TNotebook.Tab': {
            'configure': {
                'padding': 4,
                'background': lightGray,
                'foreground': darkWhite,
                'anchor': 'center',
                'borderwidth': 1,
                'font': ('Calibri', 15, 'bold'),
                'focusthickness': 0
            },
            'map': {
                'background': [
                    ('selected', darkGray),
                    ('active', lightGray),
                ],
                'focuscolor': [
                    ('selected', darkGray),
                ]
            },
        },
        'TCombobox': {
            'configure': {
                'background': darkGray,
                'foreground': darkWhite,
                'insertcolor': darkWhite,
                'arrowsize': 15,
                'arrowcolor': darkWhite,
                'fieldbackground': lightBlack,
                'selectbackground': lightBlack,
                'selectforeground': darkWhite,
                'borderwidth': 0,
                'relief': tk.FLAT,
                'padding': 5
            },
            'map': {
                'relief': [
                    ('focus', tk.ACTIVE)
                ],
                'background': [
                    ('focus', teal)
                ],
                'arrowcolor': [
                    ('focus', lightBlack)
                ]
            }
        },
        'TScrollbar': {
            'configure': {
                'background': darkGray,
                'relief': tk.FLAT,
                'borderwidth': 0,
                'troughcolor': lightBlack,
                'arrowcolor': darkWhite
            }
        },
        'TSeparator': {
            'configure': {
                'background': teal,
                'relief': tk.SUNKEN
            }
        }
    })
    return style


def AddRootOptions(main):
    main.option_add('*TCombobox*font', ('Calibri', 12))
    main.option_add('*TCombobox*Listbox*background', darkGray)
    main.option_add('*TCombobox*Listbox*foreground', darkWhite)
    main.option_add('*TCombobox*Listbox*selectBackground', darkWhite)
    main.option_add('*TCombobox*Listbox*selectForeground', darkGray)
    main.option_add('*TCombobox*Listbox*font', ('Calibri', 12))
    main.option_add('*TCombobox*Listbox*borderwidth', 0)
    main.option_add('*Text*background', darkGray)
    main.option_add('*Text*foreground', darkWhite)
    main.option_add('*Text*relief', tk.FLAT)
    main.option_add('*Text*font', ('Calibri', 12))
    main.option_add('*Canvas*background', darkGray)
    main.option_add('*Canvas*bordercolor', teal)
    main.option_add('*Canvas*foreground', darkWhite)
    main.option_add('*Canvas*relief', tk.FLAT)
    main.option_add('*Canvas*highlightbackground', darkGray)
    return
