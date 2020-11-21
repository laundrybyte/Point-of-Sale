import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import font
from tabulate import tabulate


with sqlite3.connect("main.db") as db:
    cursor = db.cursor()


def journal_viewer_window():


    def journal_viewer():
        journal_listbox.delete(0, 'end')
        cursor.execute("SELECT * FROM transactiondb")
        transactions_array = cursor.fetchall()
        temp_table = []
        for i in transactions_array:
            journal_list_ID = str(i[0])
            journal_list_date = str(i[1])
            journal_list_items = str(i[2])
            journal_list_amount = ("$" + format((i[3]), ',.2f'))
            journal_list_method = str(i[4])
            journal_list_user = str(i[5])
            temp_table.append([journal_list_ID, journal_list_date, journal_list_items, journal_list_amount, journal_list_method, journal_list_user])

        temp_table = (tabulate(temp_table, headers=["ID", "Date", "Item(s)", "Amt", "Method", "User"]))

        n = 0
        for line in temp_table.split('\n'):
            journal_listbox.insert(n, line)
            n += 1


    # Apply filters
    def journal_viewer_filter():

        journal_listbox.delete(0, 'end')
        journal_viewer_filter_date = journal_filter_date_field.get()
        journal_viewer_filter_item = journal_filter_item_field.get()

        # If user supplies both a filter date and a filter item
        if journal_viewer_filter_date and journal_viewer_filter_item:
            journal_viewer_filter_query = "SELECT * FROM transactiondb WHERE transactiontime LIKE ? AND transactionitem LIKE ?"
            cursor.execute(journal_viewer_filter_query, [(journal_viewer_filter_date + "%"), ("%" + journal_viewer_filter_item + "%")])
            journal_viewer_filter_results = cursor.fetchall()

            if journal_viewer_filter_results:
                temp_table = []
                for i in journal_viewer_filter_results:
                    journal_list_ID = str(i[0])
                    journal_list_date = str(i[1])
                    journal_list_items = str(i[2])
                    journal_list_amount = ("$" + format((i[3]), ',.2f'))
                    journal_list_method = str(i[4])
                    journal_list_user = str(i[5])
                    temp_table.append([journal_list_ID, journal_list_date, journal_list_items, journal_list_amount, journal_list_method, journal_list_user])

                temp_table = (tabulate(temp_table, headers=["ID", "Date", "Item(s)", "Amt", "Method", "User"]))
                n = 0
                for line in temp_table.split('\n'):
                    journal_listbox.insert(n, line)
                    n += 1

            elif not journal_viewer_filter_results:
                journal_filter_item_feedback = Label(filter_frame, text="No results found", fg="red", font='Helvetica 8')
                journal_filter_item_feedback.grid(row=2, column=1)

        # If user supplies just a filter date and NOT a filter item
        if journal_viewer_filter_date and not journal_viewer_filter_item:
            journal_viewer_filter_query = "SELECT * FROM transactiondb WHERE transactiontime LIKE ? "
            cursor.execute(journal_viewer_filter_query, [(journal_viewer_filter_date + "%")])
            journal_viewer_filter_results = cursor.fetchall()

            if journal_viewer_filter_results:
                temp_table = []
                for i in journal_viewer_filter_results:
                    journal_list_ID = str(i[0])
                    journal_list_date = str(i[1])
                    journal_list_items = str(i[2])
                    journal_list_amount = ("$" + format((i[3]), ',.2f'))
                    journal_list_method = str(i[4])
                    journal_list_user = str(i[5])
                    temp_table.append([journal_list_ID, journal_list_date, journal_list_items, journal_list_amount, journal_list_method, journal_list_user])

                temp_table = (tabulate(temp_table, headers=["ID", "Date", "Item(s)", "Amt", "Method", "User"]))
                n = 0
                for line in temp_table.split('\n'):
                    journal_listbox.insert(n, line)
                    n += 1

            elif not journal_viewer_filter_results:
                journal_filter_item_feedback = Label(filter_frame, text="No results found", fg="red", font='Helvetica 8')
                journal_filter_item_feedback.grid(row=2, column=1)

        # If user supplies just a filter item and NOT a filter date
        if not journal_viewer_filter_date and journal_viewer_filter_item:
            journal_viewer_filter_query = "SELECT * FROM transactiondb WHERE transactionitem LIKE ?"
            cursor.execute(journal_viewer_filter_query, [("%" + journal_viewer_filter_item + "%")])
            journal_viewer_filter_results = cursor.fetchall()

            if journal_viewer_filter_results:
                temp_table = []
                for i in journal_viewer_filter_results:
                    journal_list_ID = str(i[0])
                    journal_list_date = str(i[1])
                    journal_list_items = str(i[2])
                    journal_list_amount = ("$" + format((i[3]), ',.2f'))
                    journal_list_method = str(i[4])
                    journal_list_user = str(i[5])
                    temp_table.append([journal_list_ID, journal_list_date, journal_list_items, journal_list_amount, journal_list_method, journal_list_user])

                temp_table = (tabulate(temp_table, headers=["ID", "Date", "Item(s)", "Amt", "Method", "User"]))
                n = 0
                for line in temp_table.split('\n'):
                    journal_listbox.insert(n, line)
                    n += 1

            elif not journal_viewer_filter_results:
                journal_filter_item_feedback = Label(filter_frame, text="No results found", fg="red", font='Helvetica 8')
                journal_filter_item_feedback.grid(row=2, column=1)

        elif not journal_viewer_filter_date and not journal_viewer_filter_item:
            journal_filter_item_feedback = Label(filter_frame, text="No filter settings provided", fg="red", font='Helvetica 8')
            journal_filter_item_feedback.grid(row=2, column=1)


    def refund_by_transactionID():
        refund_get_selected_line = journal_listbox.curselection()
        refund_get_selection = journal_listbox.get(refund_get_selected_line).split(" ")
        refund_transactionID = refund_get_selection[3]
        print(refund_transactionID)

        # Confirms whether transaction ID exists in transactiondb
        refund_transaction_check_if_exists = ("SELECT * FROM transactiondb WHERE transactionID = ?")
        cursor.execute(refund_transaction_check_if_exists, [(refund_transactionID)])
        refund_transaction_info = cursor.fetchone()

        # If transaction ID exists...
        if refund_transaction_info:
            refund_transaction_info = ("Are you sure you want to delete the following transaction?\n"
                                       "\tID: " + str(refund_transaction_info[0]) + "\n" +
                                       "\tTimestamp: " + str(refund_transaction_info[1]) + "\n" +
                                       "\tItem(s): " + str(refund_transaction_info[2]) + "\n" +
                                       "\tPrice: $" + format(refund_transaction_info[3], ',.2f') + "\n" +
                                       "\tMethod: " + str(refund_transaction_info[4]) + "\n" +
                                       "\tUser: " + str(refund_transaction_info[5]) + "\n")
            refund_confirmation_box = messagebox.askyesno("Confirmation", refund_transaction_info)
            if refund_confirmation_box is True:
                remove_transaction_query = "DELETE FROM transactiondb WHERE transactionID = ?"
                cursor.execute(remove_transaction_query, [(refund_transactionID)])
                db.commit()
                print("Transaction successfully removed from journal.")
                journal_viewer()

            else:
                print("Aborted.")
                journal_viewer()


        else:
            print("Transaction ID not found.")
            refund_by_transactionID()



    ####################### Window Definitions #######################
    root = Tk()
    root.title("Journal Viewer")
    root.geometry('1000x800')

    from tkinter import font

    labelfont = 'Helvetica 12'
    monofont = 'TkFixedFont'

    # Grid configure settings
    root.grid_columnconfigure((0), weight=1)
    root.grid_rowconfigure((0), weight=1)

    # Create main frame
    frame = Frame(root, height=600, width=800)
    frame.grid()

    # Create header frame
    header_frame = Frame(frame, height=30, width=800)
    header_frame.grid(row=0, column=0)

    # Create journal frame
    journal_frame = Frame(frame, height=500, width=800)
    journal_frame.grid(row=1, column=0)

    # Create input frame
    input_frame = Frame(frame, height=50, width=800)
    input_frame.grid(row=2, column=0)

    # Create filter frame
    filter_frame = Frame(input_frame, height=50, width=300)
    filter_frame.grid(row=0, column=0)

    # Create option frame
    option_frame = Frame(input_frame, height=50, width=300)
    option_frame.grid(row=0, column=1)



    # Display header
    journal_header = Label(header_frame, font='Helvetica 16 bold', text="Journal Viewer")
    journal_header.grid(row=0, column=0)

    # Display journal listbox
    journal_listbox = Listbox(journal_frame, width=100, height=30, font=monofont)
    journal_listbox.grid(row=0, column=0)

    # Display filter labels and fields
    journal_filter_date_label = Label(filter_frame, font=labelfont, text="Filter date (YYYY-MM-DD): ")
    journal_filter_date_label.grid(row=0, column=0)

    journal_filter_date_field = Entry(filter_frame)
    journal_filter_date_field.grid(row=0, column=1)

    journal_filter_item_label = Label(filter_frame, font=labelfont, text="Filter item by name: ")
    journal_filter_item_label.grid(row=1, column=0)

    journal_filter_item_field = Entry(filter_frame)
    journal_filter_item_field.grid(row=1, column=1)

    journal_filter_item_feedback = Label(filter_frame, text="", font="Ariel 12")
    journal_filter_item_feedback.grid(row=2, column=1)


    # Display option frame

    journal_filter_item_button = Button(option_frame, text="Apply Filters", command=journal_viewer_filter, height=1, width=20)
    journal_filter_item_button.grid(row=0, column=0)

    journal_clear_filter_button = Button(option_frame, text="Clear Filters", command=journal_viewer, height=1, width=20)
    journal_clear_filter_button.grid(row=1, column=0)

    journal_clear_refund_button = Button(option_frame, text="Refund Transaction", command=refund_by_transactionID, height=1, width=20)
    journal_clear_refund_button.grid(row=2, column=0)


    journal_viewer()
    root.mainloop()
