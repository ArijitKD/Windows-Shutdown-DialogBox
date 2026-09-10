#!/usr/bin/env python3

# File: ./shutdown_gui.py
#
# A Windows-like Shutdown DialogBox for Linux Distros.
#
# Copyright (C) 2024-Present Arijit Kumar Das <arijitkdgit.official@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


from PIL import Image, ImageTk
from tkinter import messagebox as mbox
import tkinter as tk
import tkinter.ttk as ttk
import distro, os, webbrowser as wb
import subprocess as sbproc

## CONSTANTS
DISTRO_NAME = distro.name()
SRC_ROOT = os.path.dirname(__file__)
WIN_WIDTH = 600
WIN_HEIGHT = 300
DISTRO_ASSET_NAMES = {
                        "Debian GNU/Linux"  : "debian.gif",
                        "Linux Mint"        : "mint.gif"
}
HELP_LINKS = {
                "Debian GNU/Linux"  : "https://www.debian.org/doc/",
                "Linux Mint"        : "https://forums.linuxmint.com/"
}
COM_SEQS = {
                "Debian GNU/Linux" : {
                    "Switch user"   : "loginctl lock-session",
                    "Lock"          : "loginctl lock-session",
                    "Sign out"      : "gnome-session-quit",
                    "Suspend"       : "systemctl suspend -i",
                    "Turn off"      : "gnome-session-quit --power-off",
                    "Restart"       : "gnome-session-quit --reboot"
                },
                "Linux Mint" : {
                    "Switch user"   : "cinnamon-screensaver-command --lock",
                    "Lock"          : "cinnamon-screensaver-command --lock",
                    "Sign out"      : "gnome-session-quit --no-prompt",
                    "Suspend"       : "systemctl suspend",
                    "Turn off"      : "poweroff",
                    "Restart"       : "reboot"
                },
}

class ShutdownGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shut Down " + DISTRO_NAME)
        self.root.configure(bg = "white")
        self.root.attributes("-topmost",True)
        self.root.resizable(0, 0)
        self.root.after_idle(self.root.attributes,"-topmost", False)

        scr_width = self.root.winfo_screenwidth()
        scr_height = self.root.winfo_screenheight()
        left = (scr_width / 2) - (WIN_WIDTH / 2)
        top = (scr_height / 2) - (WIN_HEIGHT /2)

        self.root.geometry("%dx%d+%d+%d" %
        (WIN_WIDTH, WIN_HEIGHT, left, top - 80))


    def load_assets(self):
        self.distro_asset = Image.open(os.path.join(SRC_ROOT, "assets",
        DISTRO_ASSET_NAMES[DISTRO_NAME]))

        old_width, old_height = self.distro_asset.size
        new_dim = (int(old_width * 80 / old_height), 80)

        self.distro_asset = self.distro_asset.resize(new_dim,
        Image.Resampling.LANCZOS)
        self.distro_asset_img = ImageTk.PhotoImage(self.distro_asset)

        self.computer_asset = tk.PhotoImage(
        file = os.path.join(SRC_ROOT, "assets", "computer.gif"))


    def create_widgets(self):
        self.distro_widget = tk.Label(self.root, image = self.distro_asset_img,
        borderwidth = 0, background= "white")

        self.frame1 = tk.Frame(self.root, background = "white")

        self.computer_widget = tk.Label(self.frame1,
        image = self.computer_asset, borderwidth = 0)

        self.question_widget = ttk.Label(self.frame1,
        text = "What do you want the computer to do?", background = "white")

        self.frame2 = tk.Frame(self.root, background = "white")

        self.choice_var = tk.StringVar()
        self.combobox_widget = ttk.Combobox(self.frame2, width = 40,
        textvariable = self.choice_var, state = "readonly",
        values = [
                    "Switch user", "Lock", "Sign out",
                    "Suspend", "Turn off", "Restart"
        ])
        self.choice_var.set("Turn off")

        self.desc_widget = ttk.Label(self.frame2,
        text = "Closes all apps and turns off the PC.", background = "white")

        self.frame3 = tk.Frame(self.root, background = "white")

        self.ok_button = ttk.Button(self.frame3, text = "OK")
        self.cancel_button = ttk.Button(self.frame3, text = "Cancel")
        self.help_button = ttk.Button(self.frame3, text = "Help")


    def draw_widgets(self):
        self.distro_widget.pack(pady = (20, 10))
        self.frame1.pack(padx = 20, fill = tk.X)
        self.computer_widget.pack(side = tk.LEFT)
        self.question_widget.pack(side = tk.LEFT, padx = 30)
        self.frame2.pack(fill = tk.X, anchor = tk.E, padx = (100, 20))
        self.combobox_widget.pack(anchor = tk.W)
        self.desc_widget.pack(side = tk.LEFT, pady = 10)
        self.frame3.pack(
        side = tk.BOTTOM, anchor = tk.E, padx = 20, pady = (10, 20))
        self.ok_button.pack(side = tk.LEFT, padx = 5)
        self.cancel_button.pack(side = tk.LEFT, padx = 5)
        self.help_button.pack(side = tk.LEFT, padx = 5)


    def cb_update_desc(self, event):
        action = self.choice_var.get()
        self.ok_button.configure(text = "OK")
        self.ok_button.focus_set()

        if (action == "Turn off"):
            self.desc_widget.configure(
            text = "Closes all apps and turns off the PC.")

        elif (action == "Restart"):
            self.desc_widget.configure(
            text = "Closes all apps, turns off the PC, and then "
            "turns it on again.")

        elif (action == "Sign out"):
            self.desc_widget.configure(
            text = "Closes all apps and signs you out.")

        elif (action == "Suspend"):
            self.desc_widget.configure(
            text = "PC stays on but uses low power. Apps stay open so that "
            "when\nthe PC wakes up you\'re instantly back to where you left "
            "off.")

        elif (action == "Switch user"):
            self.desc_widget.configure(
            text = "Switch users without closing apps. You need to lock "
            "the PC\nfirst and then switch users from available options.")
            self.ok_button.configure(text = "Lock")

        elif (action == "Lock"):
            self.desc_widget.configure(
            text = "Locks the PC to prevent unauthorised access.")


    def cb_cycle_combobox(self, event, cycle):
        current = self.choice_var.get()
        cur_index = self.combobox_widget["values"].index(current)
        val_count = len(self.combobox_widget["values"])
        if ((cur_index == val_count - 1) and (cycle == +1)):
            self.choice_var.set(self.combobox_widget["values"][val_count - 1])
        elif ((cur_index == 0) and (cycle == -1)):
            self.choice_var.set(self.combobox_widget["values"][0])
        else:
            self.choice_var.set(
            self.combobox_widget["values"][cur_index + 1 * cycle])
        self.cb_update_desc(event)


    def cb_root_focusout(self, event):
        try:
            if (event.widget.master.focus_displayof() == self.combobox_widget):
                self.ok_button.focus_set()
            if (event.widget.master.focus_displayof() == None):
                self.cb_cancel()
        except:
            self.ok_button.focus_set()


    def cb_execute_action(self, event):
        if (event.widget.master.focus_get() == self.ok_button):
            self.cb_ok()
        elif (event.widget.master.focus_get() == self.cancel_button):
            self.cb_cancel()
        elif (event.widget.master.focus_get() == self.help_button):
            self.cb_help()


    def cb_ok(self):
        self.root.withdraw()
        command = COM_SEQS[DISTRO_NAME][self.choice_var.get()]
        sbproc.run(command.split())
        self.cb_cancel()


    def cb_cancel(self):
        self.root.destroy()


    def cb_help(self):
        self.root.withdraw()
        wb.open(HELP_LINKS[DISTRO_NAME])
        self.cb_cancel()


    def bind_callbacks(self):
        self.combobox_widget.bind(
        "<<ComboboxSelected>>", self.cb_update_desc)
        self.combobox_widget.bind(
        "<FocusIn>", lambda event : event.widget.master.selection_clear())
        self.root.bind(
        "<Up>", lambda event: self.cb_cycle_combobox(event, -1))
        self.root.bind(
        "<Down>", lambda event: self.cb_cycle_combobox(event, +1))
        self.root.bind(
        "<FocusOut>", self.cb_root_focusout)
        self.root.bind("<Escape>", lambda event: self.cb_cancel())
        self.root.bind('<Return>', self.cb_execute_action)
        self.root.bind('<KP_Enter>', self.cb_execute_action)

        self.ok_button.configure(command = self.cb_ok)
        self.cancel_button.configure(command = self.cb_cancel)
        self.help_button.configure(command = self.cb_help)


    def run(self):
        self.load_assets()
        self.create_widgets()
        self.draw_widgets()
        self.bind_callbacks()
        self.ok_button.focus_set()
        self.root.mainloop()


if (__name__ == "__main__"):
    app = ShutdownGUI()
    app.run()
