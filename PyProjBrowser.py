# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 18:58:18 2021

@author: benal
"""


from tkinter import *
from tkinter.ttk import *
import sqlite3
from sqlite3 import Error

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()


    def create_widgets(self):
        
        self.master.title("GUIexample")
        self.pack(fill=BOTH, expand=True)
        
        frame_ust = Frame(self)
        frame_ust.pack(fill=X)
        # Label örneği: başlık
        self.proj_bagla()
        self.Baslik = Label(frame_ust, text="Projenizi seçiniz:",
                                   font=('bold',12))
        self.Baslik.pack(side=LEFT,pady=20 )
        self.selected_proj = StringVar()
        self.ProjList_dropdown = Combobox(frame_ust, textvariable=self.selected_proj)
        self.ProjList_dropdown['state'] = 'readonly'  # normal
        self.ProjList_dropdown['values'] = self.db.fetch2("SELECT isim FROM projeler")
        self.ProjList_dropdown.pack(fill=X, padx=5, expand=True)
        # _________________________________
        frame_iki = Frame(self)
        frame_iki.pack(fill=X)
        # Yeni girişi ekle
        self.Proj_ekle = Button(frame_iki)
        self.Proj_ekle["text"] = "Ekle"
        self.Proj_ekle["command"] = self.proj_ekle # Proj_name eklenecek
        self.Proj_ekle.pack(side=LEFT, padx=5, pady=5)
        # Yeni giriş ismi
        self.Proj_name = StringVar()
        self.Proj_name.set("...")
        self.Projd_name = Entry(frame_iki, textvariable=self.Proj_name)
        self.Projd_name.pack(fill=X, padx=5, expand=True)
        #____________________________________
        frame_uc = Frame(self)
        frame_uc.pack(fill=X)
        # Çıkış
        self.quit = Button(frame_uc, text="QUIT", command=self.master.destroy)
        self.quit.pack(fill=X, padx=5, expand=True)
        #____________________________________
        # Listele
        
        frame_dort = Frame(self)
        frame_dort.pack(fill=BOTH, side=RIGHT)
        self.Projdb_list = Button(frame_dort)
        self.Projdb_list["text"] = "Yenile"
        self.Projdb_list["command"] = self.populate_list2
        self.Projdb_list.pack(side=TOP, padx=5, pady=5)
        
        # Sil
        self.Proj_sil = Button(frame_dort, text="Sil", command=self.proj_sil)
        self.Proj_sil.pack(side=TOP, padx=5, pady=5)
        
        #____________________________________
        # List
        frame_bes = Frame(self)
        frame_bes.pack(fill=BOTH, side=RIGHT)
        columns = ['id', 'isim']
        self.proj_tree_view = Treeview(frame_bes, columns=columns, show="headings")
        self.proj_tree_view.column(0, width=30)
        for col in columns[1:]:
            self.proj_tree_view.column(col, width=120)
            self.proj_tree_view.heading(col, text=col)
        self.proj_tree_view.bind('<<TreeviewSelect>>', self.proj_sec)
        self.scrollbar = Scrollbar(frame_bes, orient='vertical')
        self.scrollbar.configure(command=self.proj_tree_view.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.proj_tree_view.config(yscrollcommand=self.scrollbar.set)
        self.proj_tree_view.pack(side=RIGHT, fill=BOTH, padx=5, pady=5, expand=True)

        
    def proj_bagla(self, db_file='deneme.db'):
        self.db = self.Database(db_file)
    
    def proj_ekle(self):
        print("Eklenen:", self.Proj_name.get())
        self.db.insert(self.Proj_name.get())
        self.populate_list2()
        
    def populate_list2(self, query='select * from projeler'):
        for i in self.proj_tree_view.get_children():
            self.proj_tree_view.delete(i)
        for row in self.db.fetch2(query):
            self.proj_tree_view.insert('', 'end', values=row)
    
    def proj_sec(self, action):
        secilen_index = self.proj_tree_view.selection()[0]
        self.secilen = self.proj_tree_view.item(secilen_index)['values']
    
    def proj_sil(self):
        # print(self.secilen)
        self.db.remove(self.secilen[0])
        self.populate_list2()
        
    class Database:
        def __init__(self, db):
            self.conn = None
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS projeler (id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, isim text)")
            self.conn.commit()
        
        def fetch(self, isim=''):
            self.cur.execute(
                "SELECT * FROM projeler WHERE isim LIKE ?", ('%'+isim+'%',))
            rows = self.cur.fetchall()
            return rows
        
        def fetch2(self, query):
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows
        
        def insert(self, isim):
            self.cur.execute("INSERT INTO projeler VALUES (NULL, ?)", [isim])
            self.conn.commit()
            
        def remove(self, id):
            self.cur.execute("DELETE FROM projeler WHERE id=?", [id])
            self.conn.commit()
        
        def update(self, id, isim):
            self.cur.execute("UPDATE projeler SET isim = ? WHERE id = ?", (isim, id))
            self.conn.commit()
        
        def __del__(self):
            self.conn.close()

root = Tk()
app = Application(master=root)
app.master.geometry("700x550+%d+%d" %( ( (root.winfo_screenwidth() - 700) / 2.), ( (root.winfo_screenheight() - 550) / 2.) ) )
app.master.minsize(350, 225)
app.mainloop()