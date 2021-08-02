# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 18:58:18 2021

@author: benal
"""


import tkinter as tk
from tkinter import ttk
from ttkwidgets import CheckboxTreeview
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
        self.master.geometry("700x550+%d+%d" %( ( (root.winfo_screenwidth() - 700) / 2.), ( (root.winfo_screenheight() - 550) / 2.) ) )
        self.master.minsize(350, 225)
        self.master.iconbitmap('pyPro-1-150x150.ico')
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Grid Configure
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure((0, 3), weight=0) # 0 yapınca boyut esnek degil
        self.rowconfigure((1, 2), weight=3)
        
        # Proj List Frame
        self.projlist_group = ttk.Labelframe(self, text="Proj List")

        columns = ['id', 'isim']
        self.projlist_treeview = ttk.Treeview(self.projlist_group, columns=columns, show="headings")
        self.projlist_treeview.column(0, width=30)
        for col in columns[1:]:
            self.projlist_treeview.column(col, width=120)
            self.projlist_treeview.heading(col, text=col)
        self.projlist_treeview.bind('<<TreeviewSelect>>', self.proj_sec)
        self.projlist_treeview_scrollbar = ttk.Scrollbar(self.projlist_group, orient='vertical')
        self.projlist_treeview_scrollbar.configure(command=self.projlist_treeview.yview)
        self.projlist_treeview_scrollbar.pack(side="right", fill="y")
        self.projlist_treeview.config(yscrollcommand=self.projlist_treeview_scrollbar.set)
        self.projlist_treeview.pack(side="right", fill="both", padx=5, pady=5, expand=True)
        
        # Proj Name
        self.projname_group = ttk.Labelframe(self, text="Proj Name:")
        
        self.Proj_name = tk.StringVar()
        self.Proj_name.set("...")
        self.projname_entry = ttk.Entry(self.projname_group, textvariable=self.Proj_name)
        self.projname_entry.pack(fill="both", expand=True)
        
        # Subject Types
        self.subjtype_group = ttk.Labelframe(self, text="Subject Types")
        self.subjtype_checklist = CheckboxTreeview(self.subjtype_group, show="tree")
        self.subjtype_checklist_scrollbar = ttk.Scrollbar(self.subjtype_group, orient='vertical')
        self.subjtype_checklist_scrollbar.configure(command=self.subjtype_checklist.yview)
        self.subjtype_checklist_scrollbar.pack(side="right", fill="y")
        self.subjtype_checklist.config(yscrollcommand=self.subjtype_checklist_scrollbar.set)
        
        # Sequence Types
        self.sequencetype_group = ttk.Labelframe(self, text="Sequence Types")
        self.sequencetype_checklist = CheckboxTreeview(self.sequencetype_group, show="tree")
        self.sequencetype_checklist_scrollbar = ttk.Scrollbar(self.sequencetype_group, orient='vertical')
        self.sequencetype_checklist_scrollbar.configure(command=self.sequencetype_checklist.yview)
        self.sequencetype_checklist_scrollbar.pack(side="right", fill="y")
        self.sequencetype_checklist.config(yscrollcommand=self.sequencetype_checklist_scrollbar.set)
        
        style = ttk.Style(self.master)
        # remove the indicator in the treeview 
        style.layout("Checkbox.Treeview.Item",
                     [("Treeitem.padding",
                       {"sticky": tk.E+tk.W+tk.N+tk.S,
                        "children": [("Treeitem.image", {"side": "left", "sticky": ""}),
                                     ("Treeitem.focus", {"side": "left", "sticky": "",
                                                         "children": [("Treeitem.text",
                                                                       {"side": "left", "sticky": ""})]})]})])
        # make it look more like a listbox                                                               
        style.configure("Checkbox.Treeview", borderwidth=1, relief="sunken")
        
        self.subjtype_checklist.pack(fill="both", expand=True)
        self.sequencetype_checklist.pack(fill="both", expand=True)
        # self.secilenler = self.ct_checklist.get_checked()
        # self.ct_checklist.bind("<Button-1>", self.click_listitem, True)
        
        # Buttons
        self.buttons_frame = ttk.Frame(self)
        self.proj_add_btn = ttk.Button(self.buttons_frame, text="Add", command=self.proj_add)
        self.proj_add_btn.pack(side="left", expand=True)
        self.proj_update_btn = ttk.Button(self.buttons_frame, text="Update", command=self.proj_update)
        self.proj_update_btn.pack(side="left", expand=True)
        self.proj_update_btn.state(["disabled"])
        self.proj_delete_btn = ttk.Button(self.buttons_frame, text="Delete", command=self.proj_delete)
        self.proj_delete_btn.pack(side="left", expand=True)
        self.proj_delete_btn.state(["disabled"])
        
        # ************* Arrange Frame Grids ********************
        self.projlist_group.grid(column=0, row=0, rowspan=3, sticky=tk.NSEW, padx=5, pady=5)
        self.projname_group.grid(column=1, row=0, sticky=tk.NSEW, padx=5, pady=5)
        self.subjtype_group.grid(column=1, row=1, sticky=tk.NSEW, padx=5, pady=5)
        self.sequencetype_group.grid(column=1, row=2, sticky=tk.NSEW, padx=5, pady=5)
        self.buttons_frame.grid(column=0, row=3, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        
        # get data
        self.db = Database()
        self.populate_projlist()
        self.populate_subjtypes()
        self.populate_sequencetypes()
        # self.subjtype_checklist.insert("", "end", text="subj1", tags="unchecked")
        # self.subjtype_checklist.insert("", "end", text="subj2", tags="checked")
        # self.sequencetype_checklist.insert("", "end", text="seq1", tags="unchecked")
        # self.sequencetype_checklist.insert("", "end", text="seq2", tags="checked")
        
    # def click_listitem(self, event):
    #     print("Eklenen:", self.ct_checklist.get_checked())
    def populate_projlist(self):
        for i in self.projlist_treeview.get_children(""):
            self.projlist_treeview.delete(i)
        for row in self.db.fetch("select * from Projects"):
            self.projlist_treeview.insert("", "end", values=row)
    
    def populate_subjtypes(self):
        self.subj_types = self.db.fetch("select * from Subject_Type")
        for row in self.subj_types:
            self.subjtype_checklist.insert("", "end", text=row[1])
            
    def populate_sequencetypes(self):
        self.sequence_types = self.db.fetch("select * from Sequence_Type")
        for row in self.sequence_types:
            self.sequencetype_checklist.insert("", "end", text=row[1])
    
    def proj_sec(self, action):
        # secilen Projenin ismi
        secilen_index = self.projlist_treeview.selection()[0]
        self.secilen = self.projlist_treeview.item(secilen_index)["values"]
        self.Proj_name.set(self.secilen[1])
        
        # secilen Projenin denek türleri, önce temizle sonra ekle
        children_list = self.subjtype_checklist.get_children("")
        for chld in children_list:
            self.subjtype_checklist.change_state(chld, "unchecked")
        querry_joint = "select * from Projects_Subject_Type_joint where Project_ID=:projid" 
        for chld_ind in self.db.fetch_params(querry_joint, {"projid": self.secilen[0]}):
            self.subjtype_checklist.change_state(children_list[(chld_ind[1] - 1)], "checked")
        
        # secilen Projenin sekans türleri, önce temizle sonra ekle
        children_list = self.sequencetype_checklist.get_children("")
        for chld in children_list:
            self.sequencetype_checklist.change_state(chld, "unchecked")  
        querry_joint = "select * from Projects_Sequence_joint where Project_ID=:projid"
        for chld_ind in self.db.fetch_params(querry_joint, {"projid": self.secilen[0]}):
            self.sequencetype_checklist.change_state(children_list[(chld_ind[1] - 1)], "checked")
        
        self.proj_update_btn.state(["!disabled"])
        self.proj_delete_btn.state(["!disabled"])
    
    def proj_add(self):
        self.proj_add_update(True)
    
    def proj_update(self):
        self.proj_add_update(False)
    
    def proj_add_update(self, add_bool):
        pname = self.Proj_name.get()
        querry_Projcontrol = "select * from Projects where Project_Name=:pname"
        if ((len(self.db.fetch_params(querry_Projcontrol, {"pname": pname})) == 0 or not add_bool) and
            len(self.subjtype_checklist.get_checked()) != 0 and
            len(self.sequencetype_checklist.get_checked()) != 0 and
            len(pname) != 0):
            if add_bool:
                querry_insertproj = "insert into Projects (Project_Name) values (:pname)"
                self.db.insert_update_delete(querry_insertproj, {"pname": pname})
                # update selection
                self.populate_projlist()
                chld_list = self.projlist_treeview.get_children("")
                self.projlist_treeview.selection_set(chld_list[-1])
                self.secilen = self.projlist_treeview.item(chld_list[-1])["values"]
                
            Project_ID = self.secilen[0] 
            if not add_bool:
                querry_insertproj = "update Projects set Project_Name = :pname where Project_ID = :Project_ID"
                self.db.insert_update_delete(querry_insertproj, {"pname": pname, "Project_ID": Project_ID})
                # clean previous joints
                querry_joint = "delete from Projects_Subject_Type_joint where Project_ID = :Project_ID" 
                self.db.insert_update_delete(querry_joint, {"Project_ID": Project_ID})
                querry_joint = "delete from Projects_Sequence_joint where Project_ID = :Project_ID" 
                self.db.insert_update_delete(querry_joint, {"Project_ID": Project_ID})
            
            children_list = self.subjtype_checklist.get_children("")
            children_checklist = self.subjtype_checklist.get_checked()
            for chld in children_checklist:# 
                Subject_Type_ID = self.subj_types[children_list.index(chld)][0] #
                querry_insertsubjjoint = "insert into Projects_Subject_Type_joint values (:Project_ID, :Subject_Type_ID)"
                self.db.insert_update_delete(querry_insertsubjjoint,
                                      {"Project_ID": Project_ID, "Subject_Type_ID": Subject_Type_ID})
                
            children_list = self.sequencetype_checklist.get_children("")
            children_checklist = self.sequencetype_checklist.get_checked()
            for chld in children_checklist:
                Sequence_ID = self.sequence_types[children_list.index(chld)][0] # 
                querry_insertseqjoint = "insert into Projects_Sequence_joint values (:Project_ID, :Sequence_ID)"
                self.db.insert_update_delete(querry_insertseqjoint,
                                      {"Project_ID": Project_ID, "Sequence_ID": Sequence_ID})
        else:
            tk.messagebox.showerror("Error", """Aynı isimli iki proje olamaz. 
İsimsiz, denek türü seçilmemiş, çekim türü seçilmemiş proje kaydedilmez!""".replace("\n", ""))
    
    def proj_delete(self):
        Project_ID = self.secilen[0]
        if len(self.projlist_treeview.get_children("")) > 1:
            answer = tk.messagebox.askokcancel(title = "Onay",
                                  message = "Projeyi silmek istediğinizden emin misiniz?",
                                  icon = "warning")
            if answer:
                # clean previous joints
                querry_joint = "delete from Projects_Subject_Type_joint where Project_ID = :Project_ID" 
                self.db.insert_update_delete(querry_joint, {"Project_ID": Project_ID})
                querry_joint = "delete from Projects_Sequence_joint where Project_ID = :Project_ID" 
                self.db.insert_update_delete(querry_joint, {"Project_ID": Project_ID})
                querry_joint = "delete from Projects where Project_ID = :Project_ID" 
                self.db.insert_update_delete(querry_joint, {"Project_ID": Project_ID})
                tk.messagebox.showinfo(title = "Proje Sil", message = "Silindi.")
                # update selection
                self.populate_projlist()
                chld_list = self.projlist_treeview.get_children("")
                self.projlist_treeview.selection_set(chld_list[0])
                self.secilen = self.projlist_treeview.item(chld_list[0])["values"]
            else:
                tk.messagebox.showinfo(title = "Proje Sil", message = "Silme iptal.")
        else:
            tk.messagebox.showinfo(title = "Proje Sil", message = "Silme iptal. Çünkü son proje!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()