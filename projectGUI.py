#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 10:18:44 2021

@author: hubal
"""
import tkinter as tk

# Create the master object
master = tk.Tk()
master.title('Project Manager')


# Create the menu bar
mainMenu= tk.Menu(master)
master.config(menu=mainMenu)
mainMenu.add_cascade(label="Proje")
mainMenu.add_cascade(label="MR Parametre")

            

# Create the project name label and entry
labelProjectName = tk.Label(master, text="Proje İsmi:").grid(row=0, column=0)
entryProjectName = tk.Entry(master).grid(row=0, column=1)

# Create the group name label and listbox
labelGroup = tk.Label(master, text="Katılımcı Grupları").grid(row=1, column=0)
listboxGroup = tk.Listbox(master).grid(row=2, column=0)



# Create the MR sequences name label and listbox
labelSequence = tk.Label(master, text="MR Sekansları").grid(row=3, column=0)
listboxSequence = tk.Listbox(master).grid(row=4, column=0)
listboxDeneme = tk.Listbox(master).grid(row=5, column=0)


# The mainloop
tk.mainloop()
