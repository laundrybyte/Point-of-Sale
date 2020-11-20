import sqlite3
from tkinter import *
from tkinter import font
from tkinter import messagebox


with sqlite3.connect("main.db") as db:
    cursor = db.cursor()




def global_settings_window():
    #global sales_tax_rate
    #cursor.execute("SELECT salestaxrate from salestaxdb ORDER BY salestaxID DESC")
    #sales_tax_rate = float(cursor.fetchone()[0])
    sales_tax_rate = float(cursor.execute("SELECT salestaxrate from salestaxdb ORDER BY salestaxID DESC").fetchone()[0])

    def change_sales_tax():
        sales_tax_choice = sales_tax_input.get()
        try:
            sales_tax_choice = float(sales_tax_choice)
            sales_tax_rate = sales_tax_choice
            sales_tax_feedback = Label(input_frame, fg="green", font="Arial 10", text="Sales tax rate updated successfully.")
            sales_tax_feedback.grid(row=1, column=1)
            sales_tax_update_query = "UPDATE salestaxdb SET salestaxrate = ?"
            cursor.execute(sales_tax_update_query, [(sales_tax_rate)])
            db.commit()
        except ValueError:
            sales_tax_feedback = Label(input_frame, fg="red", font="Arial 10", text="Sales tax rate must be a decimal.")
            sales_tax_feedback.grid(row=1, column=1)


    root = Tk()
    root.title("Global Settings")
    root.geometry('400x400')
    from tkinter import font

    headerfont = font.Font(family='Helvetica', size=25, weight='bold')
    miniheaderfont = font.Font(family='Helvetica', size=16, weight='bold')
    labelfont = font.Font(family='Helvetica', size=12, weight='normal')
    monofont = 'TkFixedFont'

    root.grid_columnconfigure(0, weight=1)

    # Create main frame
    frame = Frame(root, height=400, width=400)
    frame.grid()

    # Create header frame
    header_frame = Frame(frame, height=30, width=400)
    header_frame.grid(row=0, column=0)

    # Create input frame
    input_frame = Frame(frame, height=370, width=400)
    input_frame.grid(row=1, column=0)

    # Display header
    header = Label(header_frame, font=headerfont, text="Global Settings", pady=10)
    header.grid(row=0, column=0)

    # Display input labels and fields
    sales_tax_label = Label(input_frame, font=labelfont, text="Sales Tax Rate: ")
    sales_tax_label.grid(row=0, column=0)

    sales_tax_input = Entry(input_frame, font=labelfont, width=5)
    sales_tax_input.grid(row=0, column=1)
    sales_tax_input.insert(0, sales_tax_rate)

    submit_button = Button(input_frame, text="Submit", command=change_sales_tax)
    submit_button.grid(row=2, column=1)

    sales_tax_feedback = Label(input_frame, text="")
    sales_tax_feedback.grid(row=1, column=1)

    root.mainloop()
