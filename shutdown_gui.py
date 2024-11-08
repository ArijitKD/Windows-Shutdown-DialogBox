from tkinter import messagebox as mbox
import tkinter as tk
import tkinter.ttk as ttk
import distro, os, webbrowser as wb

distro_name = distro.name()
WD=536
HT=278
action = 'Turn off'

root=tk.Tk()

root.title('Shut Down '+distro_name)
root.configure(bg='white')
root.attributes('-topmost',True)
root.resizable(0,0)
root.after_idle(root.attributes,'-topmost',False)

screenWidth = root.winfo_screenwidth() 
screenHeight = root.winfo_screenheight() 	
left = (screenWidth / 2) - (WD / 2) 		
top = (screenHeight / 2) - (HT /2) 		
root.geometry('%dx%d+%d+%d' % (WD, HT, left, top-80))

icon = tk.PhotoImage(file='assets/computer_icon.gif')
iconpanel= tk.Label(root, image = icon, borderwidth=0)
iconpanel.place(x=20, y=HT/2+8-30)

img = tk.PhotoImage(file='assets/distro_logo.gif')
panel = tk.Label(root, image = img, borderwidth=0)
panel.place(y=30, x=80)

label=ttk.Label(root, text='What do you want the computer to do?', background='white')
label.place(x=80, y=HT/2-20)

label2=ttk.Label(root, text='Closes all apps and turns off the PC.', background='white')
label2.place(x=80, y=HT/2+60-18)

n = tk.StringVar() 
choosen = ttk.Combobox(root, width = 50, textvariable = n, state='readonly')
choosen['values'] = ['Switch user', 'Lock', 'Sign out', 'Suspend', 'Turn off', 'Restart']   
choosen.place(x=80, y=HT/2+25-15 ) 
choosen.current(4)

ok=ttk.Button(text='OK')
ok.place(y=HT-(20*2)-5, x=((80+34)*2)+30)
ok.focus_set()

cancel=ttk.Button(text='Cancel')
cancel.place(y=(HT-(20*2)-5), x=((80+34)*2)+85+30+5)

def cancel_callback():
    root.destroy()

cancel.configure(command = cancel_callback)

help=ttk.Button(text='Help')
help.place(y=(HT-(20*2)-5), x=((80+34)*2)+85+85+30+10)

def help_callback():
    root.withdraw()
    wb.open("https://forums.linuxmint.com/")
    cancel_callback()

help.configure(command = help_callback)


def setVal(event):
    action = n.get()
    ok.configure(text='OK')
    ok.focus_set()
    if action == 'Turn off':
        label2.configure(text='Closes all apps and turns off the PC.')
    elif action == 'Restart':
        label2.configure(text='Closes all apps, turns off the PC, and then turns it on again.')
    elif action == 'Sign out':
        label2.configure(text='Closes all apps and signs you out.')
    elif action == 'Suspend':
        label2.configure(text='PC stays on but uses low power. Apps stay open so that when\nthe PC wakes up you\'re instantly back to where you left off.')
    elif action == 'Switch user':
        label2.configure(text='Switch users without closing apps. You need to lock the PC first\nand then switch users from available options.')
        ok.configure(text = 'Lock')
    elif action == 'Lock':
        label2.configure(text='Locks the PC to prevent unauthorised access.')
    else:
        label2.configure(text='')


def no_highlight(event):
    event.widget.master.selection_clear()

choosen.bind("<<ComboboxSelected>>", setVal)
choosen.bind("<FocusIn>", no_highlight)


def ok_callback():
    action = n.get()
    root.withdraw()
    if action == 'Turn off':
        os.system('poweroff')
    elif action == 'Restart':
        os.system('reboot')
    elif action == 'Sign out':
        os.system('gnome-session-quit --no-prompt')
    elif action == 'Suspend':
        os.system('systemctl suspend')
    elif action == 'Switch user' or action == 'Lock':
        os.system('cinnamon-screensaver-command --lock')
    cancel_callback()


def on_enter(event):
    if (event.widget.master.focus_get() == ok):
        ok_callback()
    elif (event.widget.master.focus_get() == cancel):
        cancel_callback()
    elif (event.widget.master.focus_get() == help):
        help_callback()


def on_esc(event):
    cancel_callback()


def on_uparrow(event):
    n.set(choosen['values'][choosen['values'].index(n.get())-1])
    setVal(event)


def on_downarrow(event):
    option_index = choosen['values'].index(n.get())+1
    if (option_index == len(choosen['values'])):
        option_index = 0
    n.set(choosen['values'][option_index])
    setVal(event)


def on_focusout(event):
    try:
        if (event.widget.master.focus_displayof() == choosen):
            ok.focus_set()
        if (event.widget.master.focus_displayof() == None):
            cancel_callback()
    except:
        ok.focus_set()


ok.configure(command=ok_callback)

root.bind('<Return>', on_enter)
root.bind('<KP_Enter>', on_enter)
root.bind('<Escape>', on_esc)
root.bind('<Up>', on_uparrow)
root.bind('<Down>', on_downarrow)
root.bind('<FocusOut>', on_focusout)
root.mainloop()