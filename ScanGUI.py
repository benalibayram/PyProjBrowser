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
        # style.theme_use("clam")
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
        
        self.nb = ttk.Notebook(mainPanel)
        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        self.nb.enable_traversal()
        self.nb.pack(fill=tk.BOTH, expand=True, padx=2, pady=3)
        # self.nb.bind("<Button-1>", self.click_tab)
        
        self._create_project_tab()
        self._create_participant_tab()
        self._create_scan_tab()
    # ========================================================================
    # ========================= OK ===========================================
    # ========================================================================
    def proj_ok(self):
        tab_index = self.nb.index(self.nb.select())
        if tab_index < 2:
            self.nb.select(tab_index+1)
            return 0
        # Subject
        if len(self.subject_name.get()) == 0:
            tk.messagebox.showerror("Error: Eksik", "Katılımcı İsmi")
            return 0
        if len(self.subject_surname.get()) == 0:
            tk.messagebox.showerror("Error: Eksik", "Katılımcı Soyismi")
            return 0
        # print("Cinsiyet:", self.gender.get())
        # print("El tercihi:", self.handedness.get())
        if self.subj_age.get() == 0:
            tk.messagebox.showerror("Error: Yanlış", "Katılımcı Yaşı")
            return 0
        if self.subjedu_combo.current() == -1:
            tk.messagebox.showerror("Error: Eksik", "Eğitim Seviyesi")
            return 0
        # print("Eğitim Yılı:", self.subj_eduyear.get())
        # print("Telefon No:", self.phone_number.get())
        # print("İlaç kullanımı:", self.subj_med.get())
        if len(self.subjillness2_txt.get(1.0, tk.END+"-1c")) == 0:
            tk.messagebox.showerror("Error: Eksik", "Kronik Hastalık")
            return 0
        if len(self.subjillness1_txt.get(1.0, tk.END+"-1c")) == 0:
            tk.messagebox.showerror("Error: Eksik", "Hastalık")
            return 0
        
        # Scan
        # print("Proje: ", self.secilen[0])
        # print("Çeken:", self.labpeople[self.ceken][0])
        # print("Çekim Tarihi:", self.scanday_dateentry.get_date())
        # print("Notlar:", self.notes_txt.get(1.0, tk.END+"-1c"))
        if self.subjgroup_combo.current() == -1:
            tk.messagebox.showerror("Error: Eksik", "Katılımcı Grubu")
            return 0
        
    # =========================================================================
    # ========================= Yeni Subject ==================================
    # =========================================================================
        querry_insertsubj = """insert into Subjects values (NULL, :Subject_Name, :Subject_Surname,
        :Subject_Sex, :Subject_Handedness, :Subject_DateOfBirth, :Subject_EduGrade,
        :Subject_EduYear, :Subject_PhoneNum, :Subject_DrugUsage, :Subject_ChronicDisease,
        :Subject_Disease)"""
        self.db.insert_update_delete(querry_insertsubj, 
        {"Subject_Name": self.subject_name.get(), "Subject_Surname": self.subject_surname.get(), 
        "Subject_Sex": self.gender.get(), "Subject_Handedness": self.handedness.get(), 
        "Subject_DateOfBirth": self.birthday_dateentry.get_date(), 
        "Subject_EduGrade": self.subjedu_combo.current(), "Subject_EduYear": self.subj_eduyear.get(), 
        "Subject_PhoneNum": self.phone_number.get(), "Subject_DrugUsage": self.subj_med.get(),
        "Subject_ChronicDisease": self.subjillness2_txt.get(1.0, tk.END+"-1c"), 
        "Subject_Disease": self.subjillness1_txt.get(1.0, tk.END+"-1c")})
        
        query_lastinsertID = "select seq from sqlite_sequence where name=:SubjTableName"
        self.subj_id = self.db.fetch_params(query_lastinsertID, {"SubjTableName": "Subjects"})[0][0]
        
    # =========================================================================
    # ========================= Yeni Çekim ====================================
    # =========================================================================
        if len(self.sequences_checklist.get_checked()) != 0:
            children_list = self.sequences_checklist.get_children("")
            children_checklist = self.sequences_checklist.get_checked()
            querry_insertscan = """insert into Scans values (NULL, :Project_ID, 
            :Subject_Type_ID, :Subject_ID, :Sequence_ID, :Lab_People_ID, 
            :Date, :Description)"""
            #insert for each sequence
            for chld in children_checklist:
                self.db.insert_update_delete(querry_insertscan, {"Project_ID": self.secilen[0], 
                "Subject_Type_ID": self.subj_types_id[self.subjgroup_combo_selectedind][1], 
                "Subject_ID": self.subj_id, "Sequence_ID": self.seqtypes_id[children_list.index(chld)][1], 
                "Lab_People_ID": self.labpeople[self.ceken][0], "Date": self.scanday_dateentry.get_date(), 
                "Description": self.notes_txt.get(1.0, tk.END+"-1c")})
        
    # def click_tab(self, event):
    #     clicked_tab = self.nb.tk.call(self.nb._w, "identify", "tab", event.x, event.y)
        # if self.nb.index(self.nb.select()) == 0:
        #     if clicked_tab != 0:
        #         self.ceken = self.labpeople_list.curselection();
        # else:
        #     if clicked_tab == 0:
        #         print(self.ceken)
                #self.labpeople_list.selection_set(self.ceken[0])
    
    # =========================================================================
    # ========================= PROJECT =======================================
    # =========================================================================
    def _create_project_tab(self):
        # frame to hold contentx
        frame = ttk.Frame(self.nb)
        # Grid Configure
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        projlist_group = ttk.Labelframe(frame, text="PROJE LİSTESİ")
        labpeople_group = ttk.Labelframe(frame, text="ÇEKİMİ YAPAN")
        
        # *********** Proj List Frame  ***********
        self.projlist_treeview = ttk.Treeview(projlist_group, selectmode="browse", columns=["id", "isim"], show="headings")
        self.projlist_treeview.column("id", width=30, stretch=tk.NO)
        self.projlist_treeview.column("isim", width=200, stretch=tk.NO)
        self.projlist_treeview.heading("isim", text="PROJE İSMİ")
        self.projlist_treeview.bind('<<TreeviewSelect>>', self.proj_sec)
        self.projlist_treeview.pack(side="left", fill="both", padx=5, pady=5, expand=True)
        
        projlist_treeview_scrollbar = ttk.Scrollbar(projlist_group, orient='vertical')
        projlist_treeview_scrollbar.configure(command=self.projlist_treeview.yview)
        projlist_treeview_scrollbar.pack(side="right", fill="y")
        self.projlist_treeview.config(yscrollcommand=projlist_treeview_scrollbar.set)
        
        # *********** Lab People Frame ***********
        self.labpeople_list = tk.Listbox(labpeople_group, selectmode="browse")
        self.labpeople_list.bind("<<ListboxSelect>>", self.labpeople_sec)
        labpeople_list_scrollbar = ttk.Scrollbar(labpeople_group, orient='vertical')
        labpeople_list_scrollbar.configure(command=self.labpeople_list.yview)
        self.labpeople_list.pack(side="left", fill="both", padx=5, pady=5, expand=True)
        labpeople_list_scrollbar.pack(side="right", fill="y")
        self.labpeople_list.config(yscrollcommand=labpeople_list_scrollbar.set)
        
        
        projlist_group.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=5)
        labpeople_group.grid(column=1, row=0, sticky=tk.NS, padx=5, pady=5)
        
        # get data
        self.db = Database()
        self.populate_projlist()
        self.populate_labpeople()
        
        self.nb.add(frame, text='Proje', underline=0, padding=2)
        
    def populate_projlist(self):
        for i in self.projlist_treeview.get_children(""):
            self.projlist_treeview.delete(i)
        for row in self.db.fetch("select * from Projects"):
            self.projlist_treeview.insert("", "end", values=row)
        chld_list = self.projlist_treeview.get_children("")
        self.secilen = self.projlist_treeview.item(chld_list[0])["values"]
        # self.projlist_treeview.focus(chld_list[0])
        self.projlist_treeview.selection_set(chld_list[0])
    def populate_labpeople(self):
        self.labpeople = self.db.fetch("select * from Lab_People")
        for row in self.labpeople:
            self.labpeople_list.insert(tk.END, row[1])
        self.labpeople_list.selection_set(0)
        self.labpeople_list.activate(0)
        self.ceken = 0
    def proj_sec(self, action):
        secilen_index = self.projlist_treeview.selection()[0]
        self.secilen = self.projlist_treeview.item(secilen_index)["values"]
        self.subjgroup_combo.set('')
        self.populate_sequencelist()
    def labpeople_sec(self, action):
        if action.widget.curselection():
            self.ceken = self.labpeople_list.curselection()[0]
        else:
            # print("labpeople_sec:", self.ceken)
            self.labpeople_list.selection_set(self.ceken)
    
    # =========================================================================
    # =========================== PARTICIPANT =================================
    # =========================================================================
    def _create_participant_tab(self):
        # Populate the second pane. Note that the content doesn't really matter, state='disabled'
        frame = ttk.Frame(self.nb)
        
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
        self.subjgroup_combo.bind("<<ComboboxSelected>>", self.subjgroup_combo_selected)
        # self.subjgroup_combo.current(0)
        self.subjgroup_combo.pack(fill="both", expand=True)
        
        self.subject_name = tk.StringVar(value="")
        self.subject_name_entry = ttk.Entry(name_group, textvariable=self.subject_name, name="subject_name")
        self.subject_name_entry.bind('<KeyRelease>', self.frmtnamechar)
        self.subject_name_entry.pack(fill="both", expand=True)
        
        self.subject_surname = tk.StringVar(value="")
        self.subject_surname_entry = ttk.Entry(surname_group, textvariable=self.subject_surname, name="subject_surname")
        self.subject_surname_entry.bind('<KeyRelease>', self.frmtsurnamechar)
        self.subject_surname_entry.pack(fill="both", expand=True)
        
        self.gender = tk.IntVar(value=0)
        ttk.Radiobutton(gender_group, text="Kadın", variable=self.gender, value=0).pack(side=tk.LEFT)
        ttk.Radiobutton(gender_group, text="Erkek", variable=self.gender, value=1).pack()
        
        self.handedness = tk.IntVar(value=0)
        ttk.Radiobutton(handedness_group, text="Sağ", variable=self.handedness, value=0).pack(side=tk.LEFT)
        ttk.Radiobutton(handedness_group, text="Sol", variable=self.handedness, value=1).pack()
        
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
        self.subjillness1_txt.bind('<KeyRelease>', self.frmtchar1)
        self.subjillness1_txt.pack(fill=tk.BOTH, expand=True)
        
        self.subjillness2_txt = tk.Text(subjillness2_group, wrap=tk.WORD, width=20, height=5)
        self.subjillness2_txt.bind('<KeyRelease>', self.frmtchar2)
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
        
        self.nb.add(frame, text='Katılımcı', underline=0)
        
    def populate_subjtypes(self):
        list = []
        subj_types = self.db.fetch("select * from Subject_Type")
        querry_joint = "select * from Projects_Subject_Type_joint where Project_ID=:projid"
        self.subj_types_id = self.db.fetch_params(querry_joint, {"projid": self.secilen[0]})
        for chld_ind in self.subj_types_id:
            list.append(subj_types[(chld_ind[1] - 1)][1])
        self.subjgroup_combo['values'] = list
        # print("noluyo:",self.subj_types_id)
    def subjgroup_combo_selected(self, event):
        self.subjgroup_combo_selectedind = self.subjgroup_combo.current()
    
    def update_chars(self, current):
        if current[-1] == 'þ':
            current = current[:-1] + 'ş'
        if current[-1] == 'Þ':
            current = current[:-1] + 'Ş'
        if current[-1] == 'ð':
            current = current[:-1] + 'ğ'
        if current[-1] == 'Ð':
            current = current[:-1] + 'Ğ'
        if current[-1] == 'ý':
            current = current[:-1] + 'ı'
        if current[-1] == 'Ý':
            current = current[:-1] + 'İ'
        return current
    
    def frmtnamechar(self, event):
        # selected_widget = self.master.focus_get()
        # print(selected_widget.widgetName)
        if event.char == "":
            current = self.subject_name.get()
            current = self.update_chars(current)
            self.subject_name.set(current)
    def frmtsurnamechar(self, event):
        if event.char == "":
            current = self.subject_surname.get()
            current = self.update_chars(current)
            self.subject_surname.set(current)
    def frmtchar1(self, event):
        if event.char == "":
            current = self.subjillness1_txt.get(1.0, tk.END+"-1c")
            current = self.update_chars(current)
            self.subjillness1_txt.delete(1.0, tk.END)
            self.subjillness1_txt.insert(1.0, current)
    def frmtchar2(self, event):
        if event.char == "":
            current = self.subjillness2_txt.get(1.0, tk.END+"-1c")
            current = self.update_chars(current)
            self.subjillness2_txt.delete(1.0, tk.END)
            self.subjillness2_txt.insert(1.0, current)
    
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
    # ============================== SCAN =========================================
    # =============================================================================
    def _create_scan_tab(self):
        # populate the third frame with a text widget 
        frame = ttk.Frame(self.nb)
        
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(2, weight=1)
        
        scandate_group = ttk.Labelframe(frame, text='Çekim Tarihi')
        sequences_group = ttk.Labelframe(frame, text='Sekanslar')
        notes_group = ttk.Labelframe(frame, text='Notlar')
        
        self.scanday_dateentry = DateEntry(scandate_group, date_pattern="dd/mm/yyyy")
        self.scanday_dateentry.pack(fill="both", expand=True)
        
        self.sequences_checklist = CheckboxTreeview(sequences_group, show="tree")
        sequences_scrollbar = ttk.Scrollbar(sequences_group, orient='vertical')
        sequences_scrollbar.configure(command=self.sequences_checklist.yview)
        sequences_scrollbar.pack(side="right", fill="y")
        self.sequences_checklist.config(yscrollcommand=sequences_scrollbar.set)
        self.sequences_checklist.pack(fill="both", expand=True)
        
        self.populate_sequencelist()
        
        self.notes_txt = tk.Text(notes_group, wrap=tk.WORD, width=40, height=10)
        self.notes_txt.bind('<KeyRelease>', self.noteschar)
        vscroll = ttk.Scrollbar(notes_group, orient=tk.VERTICAL, command=self.notes_txt.yview)
        self.notes_txt['yscroll'] = vscroll.set
        vscroll.pack(side=tk.RIGHT, fill="y")
        self.notes_txt.pack(fill=tk.BOTH, expand=True)
        
        scandate_group.grid(row=1, column=1, padx=10, sticky=tk.EW)
        sequences_group.grid(row=2, column=1, padx=10, sticky=tk.NS)
        notes_group.grid(row=1, column=2, rowspan=2, padx=10, sticky=tk.NSEW)
        
        self.nb.add(frame, text='Çekim', underline=1)
        
    def populate_sequencelist(self):
        for i in self.sequences_checklist.get_children(""):
            self.sequences_checklist.delete(i)
        sequence_types = self.db.fetch("select * from Sequence_Type")
        querry_joint = "select * from Projects_Sequence_joint where Project_ID=:projid"
        self.seqtypes_id = self.db.fetch_params(querry_joint, {"projid": self.secilen[0]})
        for chld_ind in self.seqtypes_id:
            self.sequences_checklist.insert("", "end", text=sequence_types[(chld_ind[1] - 1)][1])
        
    def noteschar(self, event):
        if event.char == "":
            current = self.notes_txt.get(1.0, tk.END+"-1c")
            current = self.update_chars(current)
            self.notes_txt.delete(1.0, tk.END)
            self.notes_txt.insert(1.0, current)
            
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()