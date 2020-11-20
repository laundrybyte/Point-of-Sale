from tkinter import *
import sqlite3
import transaction
import journalviewer
import itemmaintenance
import usermaintenance
import globalsettings


with sqlite3.connect("main.db") as db:
    cursor = db.cursor()

def main_menu_window():
    root = Tk()
    root.title("Main Menu")
    root.geometry('1000x600')
    headerfont = font.Font(family='Helvetica', size=25, weight='bold')
    miniheaderfont = font.Font(family='Helvetica', size=16, weight='bold')
    labelfont = font.Font(family='Helvetica', size=12, weight='normal')
    # monofont = font.Font(family='TkFixedFont', size=10)
    monofont = 'TkFixedFont'
    # Create main frame
    frame = Frame(root, height=600, width=500, )
    frame.grid()

    # Create header frame
    header_frame = Frame(frame, height=30, width=500, )
    header_frame.grid(row=0, column=0)

    # Create input frame
    input_frame = Frame(frame, height=400, width=500, pady=100, padx=10, )
    input_frame.grid(row=1, column=0)

    # Grid configure settings
    root.grid_columnconfigure((0), weight=1)


    # Create header label
    header = Label(header_frame, font=headerfont, text="Main Menu", pady=50)
    header.grid(row=0)

    # Create Transaction button
    transaction_button = Button(input_frame, font=labelfont, text="Transaction", width=20, height=2, padx=10, pady=0, command=transaction.transaction_main)
    transaction_button.grid(row=1, column=0)

    # Create Refund button
    journal_viewer_button = Button(input_frame, font=labelfont, text="Journal Viewer", width=20, height=2, padx=10, pady=0, command=journalviewer.journal_viewer_window)
    journal_viewer_button.grid(row=1, column=1)

    # Create Manage Items button
    manage_items_button = Button(input_frame, font=labelfont, text="Manage Items", width=20, height=2, padx=10, pady=0, command=itemmaintenance.item_maintenance_window)
    manage_items_button.grid(row=2, column=0)

    # Create Manage Users button
    manage_users_button = Button(input_frame, font=labelfont, text="Manage Users", width=20, height=2, padx=10, pady=0, command=usermaintenance.user_maintenance_window)
    manage_users_button.grid(row=2, column=1)

    # Create Global Settings button
    global_settings_button = Button(input_frame, font=labelfont, text="Global Settings", width=20, height=2, padx=10, pady=0, command=globalsettings.global_settings_window)
    global_settings_button.grid(row=3, column=0)

    # Create Logout button
    logout_button = Button(input_frame, font=labelfont, text="Logout", width=20, height=2, padx=10, pady=0, command=root.destroy)
    logout_button.grid(row=3, column=1)


    root.mainloop()

