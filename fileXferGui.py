#!/usr/bin/python3
#Written in 3.6.0 by Jordan VanWyhe
import tkinter as tk
from tkinter import *
import csv
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from newFileXfer import copyOver
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

sqlite_file = 'fileXferTimeData.sqlite'    # name of the sqlite database file

def createTable():
   
    table_name = 'date_time_file_transfer'   # name of the table to be created
    index_name = 'unique_index' # index names
    main_column = 'last_check_column' # name of the PRIMARY KEY column
    column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB, (TEXT REAL or INTEGER for Date and Time)
    
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS {tn} ({ix} INTEGER PRIMARY KEY AUTOINCREMENT, {mc} {ct})'\
          .format(tn=table_name, ix=index_name, mc=main_column, ct=column_type));
    # This is a bit complicated, but makes it easy to make new tables if you need to do that for some reason
    conn.commit()
    conn.close()

def readTime():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    last_Backup = c.execute("SELECT last_check_column FROM date_time_file_transfer WHERE unique_index = (SELECT MAX(unique_index) FROM date_time_file_transfer)").fetchone()

    if last_Backup == None:
        conn.close()
        return ("No previous data")
    
    conn.close()
    prettyTime = last_Backup[0].split(".")
    return prettyTime[0]


def updateTime():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute("INSERT INTO date_time_file_transfer (last_check_column) VALUES (?)", (str(datetime.now()),))

    conn.commit()
    conn.close()

class Feedback:

    

    def __init__(self, master):

        master.title('End of Day File Transfer')
        master.resizable(False, False)
        
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        ttk.Label(self.frame_header, text = 'Choose folders and then click run.').grid(row = 0, column = 0)

        
        self.src_entry = StringVar()
        self.des_entry = StringVar()
        self.backup_entry = StringVar()
        self.backup_entry.set(readTime())

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text = 'Source:').grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Destination:').grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'sw')
        ttk.Label(self.frame_content, text = 'Last Backup:').grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'sw')
        

        self.entry_source = ttk.Entry(self.frame_content, textvariable=self.src_entry, width = 24, font = ('Arial', 10))
        self.entry_destination = ttk.Entry(self.frame_content, textvariable=self.des_entry, width = 24, font = ('Arial', 10))
        self.entry_lastBackup = ttk.Entry(self.frame_content, textvariable=self.backup_entry, width = 24, font = ('Arial', 10))

        self.entry_source.grid(row = 0, column = 1, padx = 5)
        self.entry_destination.grid(row = 1, column = 1, padx = 5)        
        self.entry_lastBackup.grid(row = 2, column = 1, padx =5)
       ##SRC
        ttk.Button(self.frame_content, text = 'Choose Folder',
                   command = self.getSrc).grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'e')
       ##DES 
        ttk.Button(self.frame_content, text = 'Choose Folder',
                   command = self.getDes).grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'w')

        ttk.Button(self.frame_content, text = 'Run',
                   command = self.xfer).grid(row = 2, column = 2, padx = 5, pady = 5, sticky = 'w')
        

    def getSrc (self):
        src = askdirectory()
        self.src_entry.set(src)

    def getDes (self):
        des = askdirectory()
        self.des_entry.set(des)

    def xfer(self):
        print("working")
        src = self.src_entry.get() + '/'
        des = self.des_entry.get() + '/'
        copyOver(src, des) ##Imported Module for file moving code
        updateTime()
        self.backup_entry.set(readTime())
        messagebox.showinfo('File Transfer', 'New files were transferred.')

            
def main():            
    createTable()
    root = Tk()
    feedback = Feedback(root)
    root.mainloop()
    
if __name__ == "__main__": main()
