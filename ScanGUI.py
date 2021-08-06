# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 18:58:18 2021

@author: benal
"""

import tkinter as tk
from tkinter import ttk
from ttkwidgets import CheckboxTreeview
from tkcalendar import DateEntry
from datetime import date
import re
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file="EveryThing.db"):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
        except Error as e:
            print(e)
    
    def fetch(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows
    
    def fetch_params(self, query, params):
        self.cur.execute(query, params)
        rows = self.cur.fetchall()
        return rows
    
    def insert_update_delete(self, query, params):
        self.cur.execute(query, params)
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("PyProjManager")
        self.master.geometry("550x325+%d+%d" %( ( (root.winfo_screenwidth() - 550) / 2.), ( (root.winfo_screenheight() - 325) / 2.) ) )
        self.master.minsize(550, 325)
        self.master.iconbitmap('pyPro-1-150x150.ico')
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self.master)
        #style.theme_use("clam")
        style.configure("TNotebook", tabposition="n")
        # # style.configure('Checkbox.Treeview', borderwidth=0, relief='sunken')
        # style.configure('my.DateEntry',
        #         fieldbackground='light green',
        #         background='dark green',
        #         foreground='dark blue',
        #         arrowcolor='white')
        
        self.proj_ok_btn = ttk.Button(self, text="Tamam", command=self.proj_ok)
        # self.proj_ok_btn.state(["disabled"])
        self.proj_ok_btn.pack(side=tk.BOTTOM, pady=3)
        
        mainPanel = tk.Frame(self)
        mainPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        nb = ttk.Notebook(mainPanel)
        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        nb.enable_traversal()
        nb.pack(fill=tk.BOTH, expand=True, padx=2, pady=3)
        
        self._create_project_tab(nb)
        self._create_participant_tab(nb)
        self._create_scan_tab(nb)
        
    def proj_ok(self):
        print("tamam yaşın: ")
        
    def _create_project_tab(self, nb):
        # frame to hold contentx
        frame = ttk.Frame(nb)
        # Grid Configure
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=0)
        frame.rowconfigure(0, weight=3)
        frame.rowconfigure(1, weight=0) # 0 yapınca boyut esnek degil
        
        # *********** Proj List Frame  ***********
        projlist_group = ttk.Labelframe(frame, text="PROJE LİSTESİ")

        self.projlist_treeview = ttk.Treeview(projlist_group, selectmode="browse", columns=["id", "isim"], show="headings")
        self.projlist_treeview.column("id", width=30, stretch=tk.NO)
        # self.projlist_treeview.column("isim", width=300)
        self.projlist_treeview.heading("isim", text="PROJE İSMİ")
        self.projlist_treeview.bind('<<TreeviewSelect>>', self.proj_sec)
        self.projlist_treeview.pack(side="left", fill="both", padx=5, pady=5, expand=True)
        
        projlist_treeview_scrollbar = ttk.Scrollbar(projlist_group, orient='vertical')
        projlist_treeview_scrollbar.configure(command=self.projlist_treeview.yview)
        projlist_treeview_scrollbar.pack(side="left", fill="y")
        self.projlist_treeview.config(yscrollcommand=projlist_treeview_scrollbar.set)
        
        # *********** Lab People Frame ***********
        
        labpeople_group = ttk.Labelframe(frame, text="ÇEKİMİ YAPAN")
        self.labpeople_checklist = CheckboxTreeview(labpeople_group, show="tree")
        labpeople_checklist_scrollbar = ttk.Scrollbar(labpeople_group, orient='vertical')
        labpeople_checklist_scrollbar.configure(command=self.labpeople_checklist.yview)
        self.labpeople_checklist.pack(side="left", fill="both", expand=True)
        labpeople_checklist_scrollbar.pack(side="left", fill="y")
        self.labpeople_checklist.config(yscrollcommand=labpeople_checklist_scrollbar.set)
        
        
        projlist_group.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)
        labpeople_group.grid(column=1, row=0, sticky=tk.NS, padx=5, pady=5)
        
        # get data
        self.db = Database()
        self.populate_projlist()
        self.populate_labpeople()
        
        nb.add(frame, text='Proje', underline=0, padding=2)
        
    def populate_projlist(self):
        for i in self.projlist_treeview.get_children(""):
            self.projlist_treeview.delete(i)
        for row in self.db.fetch("select * from Projects"):
            self.projlist_treeview.insert("", "end", values=row)
        chld_list = self.projlist_treeview.get_children("")
        self.secilen = self.projlist_treeview.item(chld_list[0])["values"]
    def populate_labpeople(self):
        for row in self.db.fetch("select * from Lab_People"):
            self.labpeople_checklist.insert("", "end", text=row[1])
    def proj_sec(self, action):
        secilen_index = self.projlist_treeview.selection()[0]
        self.secilen = self.projlist_treeview.item(secilen_index)["values"]
        self.subjgroup_combo.set('')
        self.populate_sequencelist()
    # =============================================================================
    def _create_participant_tab(self, nb):
        # Populate the second pane. Note that the content doesn't really matter, state='disabled'
        frame = ttk.Frame(nb)
        
        # # Grid Configure
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        # frame.rowconfigure(1, weight=1)
        # frame.rowconfigure(1, weight=0) # 0 yapınca boyut esnek degil
        
        subjgroup_group = ttk.Labelframe(frame, text='Katılımcı Grubu')
        name_group = ttk.Labelframe(frame, text='İsim')
        surname_group = ttk.Labelframe(frame, text='Soyisim')
        gender_group = ttk.Labelframe(frame, text='Cinsiyet')
        handedness_group = ttk.Labelframe(frame, text='El Tercihi')
        birthday_group = ttk.Labelframe(frame, text='Doğum Tarihi')
        age_group = ttk.Labelframe(frame, text='Yaş')
        edu_group = ttk.Labelframe(frame, text='Eğitim Durumu')
        eduyear_group = ttk.Labelframe(frame, text='Eğitim Süresi')
        phone_group = ttk.Labelframe(frame, text='Telefon Numarası\n0(212)123-4567')
        subjillness1_group = ttk.Labelframe(frame, text='Nörolojik/Psikiyatrik hastalık')
        subjillness2_group = ttk.Labelframe(frame, text='Kronik hastalık')
        
        self.subjgroup_combo = ttk.Combobox(subjgroup_group, postcommand = self.populate_subjtypes) # font = fontExample = ("Courier", 16, "bold")
        # self.subjgroup_combo.current(0)
        self.subjgroup_combo.pack(fill="both", expand=True)
        
        self.subject_name = tk.StringVar(value="")
        self.subject_name_entry = ttk.Entry(name_group, textvariable=self.subject_name)
        self.subject_name_entry.pack(fill="both", expand=True)
        
        self.subject_surname = tk.StringVar(value="")
        self.subject_surname_entry = ttk.Entry(surname_group, textvariable=self.subject_surname)
        self.subject_surname_entry.pack(fill="both", expand=True)
        
        self.gender = tk.IntVar(value=1)
        ttk.Radiobutton(gender_group, text="Kadın", variable=self.gender, value=1).pack(side=tk.LEFT)
        ttk.Radiobutton(gender_group, text="Erkek", variable=self.gender, value=2).pack()
        
        self.handedness = tk.IntVar(value=1)
        ttk.Radiobutton(handedness_group, text="Sağ", variable=self.handedness, value=1).pack(side=tk.LEFT)
        ttk.Radiobutton(handedness_group, text="Sol", variable=self.handedness, value=2).pack()
        
        self.birthday_dateentry = DateEntry(birthday_group, date_pattern="dd/mm/yyyy")
        self.birthday_dateentry.bind('<<DateEntrySelected>>', self.calculate_subjage)
        self.birthday_dateentry.pack(fill="both", expand=True)
        
        self.subj_age = tk.IntVar()
        self.age_entry = ttk.Entry(age_group, textvariable=self.subj_age, state='disabled')
        self.age_entry.pack(fill="both", expand=True)
        
        edu_types = ["İlkokul", "Ortaokul", "Lise", "Üniversite", "Y.Lisans", "Doktora"]
        self.subjedu_combo = ttk.Combobox(edu_group, values=edu_types)
        # self.subjgroup_combo.current(0)
        self.subjedu_combo.pack(fill="both", expand=True)
        
        vcmd = (self.register(self.isdigit_callback))
        self.subj_eduyear = tk.IntVar()
        self.eduyear_entry = ttk.Entry(eduyear_group, textvariable=self.subj_eduyear, validate="all", validatecommand=(vcmd, "%P"))
        self.eduyear_entry.pack(fill="both", expand=True)
        
        self.phone_number = tk.StringVar(value="0")
        self.phone_entry = ttk.Entry(phone_group, textvariable=self.phone_number, width=16)
        self.phone_entry.bind('<KeyRelease>', self.frmtphone)
        self.phone_entry.pack(fill="both", expand=True)
        
        self.subjillness1_txt = tk.Text(subjillness1_group, wrap=tk.WORD, width=20, height=5)
        self.subjillness1_txt.pack(fill=tk.BOTH, expand=True)
        
        self.subjillness2_txt = tk.Text(subjillness2_group, wrap=tk.WORD, width=20, height=5)
        self.subjillness2_txt.pack(fill=tk.BOTH, expand=True)
        
        self.subj_med = tk.IntVar(value=0)
        self.subj_med_check = ttk.Checkbutton(frame, text='İlaç kullanımı var.', variable=self.subj_med, onvalue=1, offvalue=0)
        self.subj_med_check.grid(row=5, column=3, padx=10, sticky=tk.EW)
        
        subjgroup_group.grid(row=1, column=1, padx=10, sticky=tk.EW)
        name_group.grid(row=2, column=1, padx=10, sticky=tk.EW)
        surname_group.grid(row=3, column=1, padx=10, sticky=tk.EW)
        gender_group.grid(row=4, column=1, padx=10, sticky=tk.EW)
        handedness_group.grid(row=5, column=1, padx=10, sticky=tk.EW)
        birthday_group.grid(row=1, column=2, padx=10, sticky=tk.EW)
        age_group.grid(row=2, column=2, padx=10, sticky=tk.EW)
        edu_group.grid(row=3, column=2, padx=10, sticky=tk.EW)
        eduyear_group.grid(row=4, column=2, padx=10, sticky=tk.EW)
        phone_group.grid(row=5, column=2, padx=10, sticky=tk.EW)
        subjillness1_group.grid(row=1, column=3, rowspan=2, padx=10, sticky=tk.EW)
        subjillness2_group.grid(row=3, column=3, rowspan=2, padx=10, sticky=tk.EW)
        
        nb.add(frame, text='Katılımcı', underline=0)
        
    def populate_subjtypes(self):
        list = []
        subj_types = self.db.fetch("select * from Subject_Type")
        querry_joint = "select * from Projects_Subject_Type_joint where Project_ID=:projid"
        for chld_ind in self.db.fetch_params(querry_joint, {"projid": self.secilen[0]}):
            list.append(subj_types[(chld_ind[1] - 1)][1])
        self.subjgroup_combo['values'] = list
        
    def frmtphone(self, event):
        current = self.phone_number.get()
        current = re.sub("[^0-9]", "", current) # işte burası 
        if len(current) == 0:
            current = "0"
        elif current[0] != "0":
            current = "0" + current
        elif len(current) > 11:
            current = current[:11]
        if (len(current) > 1) and (len(current) < 5):
            current = current[:1] + '(' + current[1:]
        elif (len(current) > 4) and (len(current) < 8):
            current = current[:1] + '(' + current[1:]
            current = current[:5] + ')' + current[5:]
        elif len(current) > 7:
            current = current[:1] + '(' + current[1:]
            current = current[:5] + ')' + current[5:]
            current = current[:9] + '-' + current[9:]
        self.phone_number.set(current)
        self.phone_entry.icursor("end")
        
    def calculate_subjage(self,event):
        yas = (date.today() - self.birthday_dateentry.get_date()).days / 365.25
        self.subj_age.set(int(yas))
        
    def isdigit_callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False
    
    # =============================================================================
    def _create_scan_tab(self, nb):
        # populate the third frame with a text widget
        frame = ttk.Frame(nb)
        
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(2, weight=1)
        
        scandate_group = ttk.Labelframe(frame, text='Çekim Tarihi')
        sequences_group = ttk.Labelframe(frame, text='Sekanslar')
        notes_group = ttk.Labelframe(frame, text='Notlar')
        
        self.birthday_dateentry = DateEntry(scandate_group, date_pattern="dd/mm/yyyy")
        self.birthday_dateentry.pack(fill="both", expand=True)
        
        self.sequences_checklist = CheckboxTreeview(sequences_group, show="tree")
        sequences_scrollbar = ttk.Scrollbar(sequences_group, orient='vertical')
        sequences_scrollbar.configure(command=self.sequences_checklist.yview)
        sequences_scrollbar.pack(side="right", fill="y")
        self.sequences_checklist.config(yscrollcommand=sequences_scrollbar.set)
        self.sequences_checklist.pack(fill="both", expand=True)
        
        self.populate_sequencelist()
        
        self.notes_txt = tk.Text(notes_group, wrap=tk.WORD, width=40, height=10)
        vscroll = ttk.Scrollbar(notes_group, orient=tk.VERTICAL, command=self.notes_txt.yview)
        self.notes_txt['yscroll'] = vscroll.set
        vscroll.pack(side=tk.RIGHT, fill="y")
        self.notes_txt.pack(fill=tk.BOTH, expand=True)
        
        scandate_group.grid(row=1, column=1, padx=10, sticky=tk.EW)
        sequences_group.grid(row=2, column=1, padx=10, sticky=tk.NS)
        notes_group.grid(row=1, column=2, rowspan=2, padx=10, sticky=tk.NSEW)
        
        nb.add(frame, text='Çekim', underline=1)
        
    def populate_sequencelist(self):
        for i in self.sequences_checklist.get_children(""):
            self.sequences_checklist.delete(i)
        sequence_types = self.db.fetch("select * from Sequence_Type")
        querry_joint = "select * from Projects_Sequence_joint where Project_ID=:projid"
        for chld_ind in self.db.fetch_params(querry_joint, {"projid": self.secilen[0]}):
            self.sequences_checklist.insert("", "end", text=sequence_types[(chld_ind[1] - 1)][1])
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()