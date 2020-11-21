import sqlite3
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tabulate import tabulate


with sqlite3.connect("main.db") as db:
    cursor = db.cursor()


def transaction_window():
    sales_tax_rate = float(cursor.execute("SELECT salestaxrate from salestaxdb ORDER BY salestaxID DESC").fetchone()[0])

    def transaction_refresh_variables():
        ## GLOBAL VARIABLES
        global transaction_total
        transaction_total = []
        global transaction_items_all
        transaction_items_all = []
        global transaction_post_tax_total
        transaction_post_tax_total = "$0.00"
        global transaction_payment_method
        global transaction_items_all_db
        transaction_items_all_db = []
        # Clear whatever is currently present in the listboxes
        item_list_box.delete(0, 'end')
        selection_cart_listbox.delete(0, 'end')

    def transaction_gather_item_list():
        transaction_refresh_variables()
        # Clear out the entries in the input boxes
        item_selection_field.delete(0, 'end')
        item_quantity_field.delete(0, 'end')

        # SQL stuff
        cursor.execute("SELECT * FROM itemdb")
        transaction_list_items = cursor.fetchall()
        cursor.execute("SELECT itemID FROM itemdb")

        temp_table = []

        for i in transaction_list_items:
            transaction_item_list_itemID = i[0]
            transaction_item_list_name = i[1]
            transaction_item_list_price = format(i[2], ',.2f')
            temp_table.append([transaction_item_list_itemID, transaction_item_list_name, ("$" + transaction_item_list_price)])


        temp_table = (tabulate(temp_table, headers=["ID", "Name", "Price"]))

        n = 0
        for line in temp_table.split('\n'):
            item_list_box.insert(n, line)
            n += 1



    def transaction_get_values():
        transaction_item_choice = str(item_selection_field.get())
        transaction_item_quantity_choice = str(item_quantity_field.get())
        if str(transaction_item_choice).isdigit() is True and str(transaction_item_quantity_choice).isdigit() is True:
            transaction_item_check_if_exists = "SELECT * FROM itemdb WHERE itemID = ?"
            cursor.execute(transaction_item_check_if_exists, [(transaction_item_choice)])
            transaction_item_in_cart = cursor.fetchone()
            # If query yields a result
            if transaction_item_in_cart:
                transaction_item_name = transaction_item_in_cart[1]
                transaction_item_price = transaction_item_in_cart[2]
                transaction_item_total = (transaction_item_price * float(transaction_item_quantity_choice))

                # Append to transaction total list
                transaction_total.append(transaction_item_total)

                # Calculate current items
                transaction_items_all_entry = str(transaction_item_name) + " x" + str(transaction_item_quantity_choice) + " - $" + format((transaction_item_total), ',.2f')
                transactions_items_all_db_entry = str(transaction_item_name) + " x" + str(transaction_item_quantity_choice)
                global transaction_items_all
                transaction_items_all.append(transaction_items_all_entry)

                # What gets inserted into the SQL database under "items"
                global transaction_items_all_db
                transaction_items_all_db.append(transactions_items_all_db_entry)

                # Show current items
                selection_cart_listbox.delete(0, 'end')
                n = 1
                for i in transaction_items_all:
                    selection_cart_listbox.insert(n, i)
                    n += 1

                print(transaction_items_all_db)

                # Preview total
                transaction_post_tax_total = ((sum(transaction_total) + (sum(transaction_total) * sales_tax_rate)))
                transaction_post_tax_total = ("$" + format(transaction_post_tax_total, ',.2f'))

                selection_total_amt = Label(selection_total_frame, font="Arial 12", text=transaction_post_tax_total)
                selection_total_amt.grid(row=0, column=1)



            # If query yields no result
            else:
                item_selection_feedback = Label(selection_input_frame, text="Item ID not found.", fg="red")
                item_selection_feedback.grid(row=1, column=1)

        elif str(transaction_item_choice).isdigit() is False:
            item_selection_feedback = Label(selection_input_frame, text="Item ID invalid.", fg="red")
            item_selection_feedback.grid(row=1, column=1)

        elif str(transaction_item_quantity_choice).isdigit() is False:
            item_quantity_feedback = Label(selection_input_frame, text="Quantity invalid.", fg="red")
            item_quantity_feedback.grid(row=3, column=1)

    def transaction_verify_box():
        # Pop-up box asking to verify transaction
        transaction_verify_popup = messagebox.askyesno("Verify Transaction", "Verify Transaction?")
        if transaction_verify_popup is True:
            # Log transaction in transactiondb
            from pos_login import login_username
            from datetime import datetime
            fulldate = datetime.now()
            transaction_timestamp = str(fulldate)[0:19]
            # Clean up the string that gets inserted into the database
            transaction_items_all_db_insert = (str(transaction_items_all_db)).replace("[","").replace("]","")

            log_transaction_query = '''INSERT INTO transactiondb(transactiontime,transactionitem,transactionprice,transactionmethod,transactionuser)
                        VALUES(?,?,?,?,?)'''
            log_transaction_total = ((sum(transaction_total) + (sum(transaction_total) * sales_tax_rate)))
            cursor.execute(log_transaction_query,[(transaction_timestamp), (transaction_items_all_db_insert), (log_transaction_total), (transaction_payment_method), (login_username)])
            db.commit()
            print("Transaction logged successfully.")
            # Clear the cart
            selection_cart_listbox.delete(0, 'end')
            transaction_gather_item_list()

        else:
            print()

    def transaction_set_payment_cash():
        global transaction_payment_method
        transaction_payment_method = "Cash"
        transaction_verify_box()

    def transaction_set_payment_credit():
        global transaction_payment_method
        transaction_payment_method = "Credit"
        transaction_verify_box()

    def transaction_set_payment_check():
        global transaction_payment_method
        transaction_payment_method = "Check"
        transaction_verify_box()

    def transaction_cancel():
        transaction_refresh_variables()
        transaction_gather_item_list()
        selection_total_amt = Label(selection_total_frame, font="Arial 12", text=transaction_post_tax_total)
        selection_total_amt.grid(row=0, column=1)

    ####################### Window Definitions #######################
    root = Tk()
    root.title("Transaction Menu")
    root.geometry('1000x800')
    from tkinter import font

    headerfont = 'Helvetica 16 bold'
    labelfont = 'Helvetica 12'
    monofont = 'TkFixedFont'

    # Create main frame
    frame = Frame(root, height=800, width=800)
    frame.grid()

    # Create header frame
    header_frame = Frame(frame, height=30, width=800)
    header_frame.grid(row=0, column=0)

    # Create input frame
    input_frame = Frame(frame, height=770, width=800)
    input_frame.grid(row=1, column=0)

    # Create item list frame
    item_list_frame = Frame(input_frame, height=400, width=300)
    item_list_frame.grid(row=0, column=0)

    # Create selection frame
    selection_frame = Frame(input_frame, height=400, width=500)
    selection_frame.grid(row=0, column=1)

    # Create selection header frame
    selection_header_frame = Frame(selection_frame, height=30, width=500)
    selection_header_frame.grid(row=0, column=0)

    # Create selection input frame
    selection_input_frame = Frame(selection_frame, height=70, width=500)
    selection_input_frame.grid(row=1, column=0)

    # Create selection cart frame
    selection_cart_frame = Frame(selection_frame, height=100, width=500)
    selection_cart_frame.grid(row=2, column=0)

    # Create selection total frame
    selection_total_frame = Frame(selection_frame, height=30, width=500)
    selection_total_frame.grid(row=3, column=0)

    # Create selection payment frame
    selection_pmt_frame = Frame(selection_frame, height=50, width=500)
    selection_pmt_frame.grid(row=4, column=0)

    # Grid configure settings
    root.grid_columnconfigure((0), weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=1)
    selection_input_frame.grid_rowconfigure(0, weight=1)


    # Display main header
    header = Label(header_frame, font=headerfont, text="Transaction")
    header.grid(row=0, column=1)

    # Display list header
    item_list_header = Label(item_list_frame, font="Arial 15", text="Available Items")
    item_list_header.grid(row=0, column=0)

    # Display item list
    item_list_box = Listbox(item_list_frame, width=50, height=40, font="Courier 10")
    item_list_box.grid(row=1, column=0)

    # Display selection header
    item_selection_header = Label(selection_header_frame, font="Arial 15", text="Item Selection")
    item_selection_header.grid(row=0, column=0)

    # Display selection input labels and fields
    item_selection_label = Label(selection_input_frame, font=labelfont, text="Item ID: ")
    item_selection_label.grid(row=0, column=0)

    item_selection_field = Entry(selection_input_frame)
    item_selection_field.grid(row=0, column=1)

    item_selection_feedback = Label(font="Arial 12", text="")
    item_selection_feedback.grid(row=1, column=1)

    item_quantity_label = Label(selection_input_frame, font=labelfont, text="Quantity: ")
    item_quantity_label.grid(row=2, column=0)

    item_quantity_field = Entry(selection_input_frame)
    item_quantity_field.grid(row=2, column=1)

    item_quantity_feedback = Label(font="Arial 12", text = "")
    item_quantity_feedback.grid(row=3, column=1)

    item_add_to_cart = Button(selection_input_frame, text="Add Item", command=transaction_get_values, height=2, width=15)
    item_add_to_cart.grid(row=4, column=1)

    # Display selection cart labels and fields
    selection_cart_header = Label(selection_cart_frame, font="Arial 15", text="In Cart:")
    selection_cart_header.grid(row=0, column=0)

    selection_cart_listbox = Listbox(selection_cart_frame, width=40, height=10)
    selection_cart_listbox.grid(row=1, column=0)
    selection_cart_listbox.insert(0)

    # Display selection total labels and fields
    selection_total_label = Label(selection_total_frame, font="Arial 12", text="Total: ")
    selection_total_label.grid(row=0, column=0)

    selection_total_amt = Label(selection_total_frame, font="Arial 12", text="$0.00")
    selection_total_amt.grid(row=0, column=1)

    # Display selection payment buttons
    selection_pmt_cash = Button(selection_pmt_frame, text="Cash", command=transaction_set_payment_cash, height=2, width=15)
    selection_pmt_cash.grid(row=0, column=0)

    selection_pmt_credit = Button(selection_pmt_frame, text="Credit/Debit", command=transaction_set_payment_credit, height=2, width=15)
    selection_pmt_credit.grid(row=0, column=1)

    selection_pmt_check = Button(selection_pmt_frame, text="Check", command=transaction_set_payment_check, height=2, width=15)
    selection_pmt_check.grid(row=1, column=0)

    selection_pmt_cancel = Button(selection_pmt_frame, text="Cancel", command=transaction_cancel, height=2, width=15)
    selection_pmt_cancel.grid(row=1, column=1)

    transaction_gather_item_list()


    # When listbox item is clicked
    def listbox_click(event):
        listbox_click = event.widget
        listbox_selection = int(listbox_click.curselection() [0])
        listbox_data = listbox_click.get(listbox_selection).split(" ")
        while ("" in listbox_data):
            listbox_data.remove("")
        listbox_selection_item_ID = listbox_data[0]
        # When user clicks on new item in listbox, put selected item ID in item ID input field
        item_selection_field.delete(0, 'end')
        item_selection_field.insert(0, listbox_selection_item_ID)


    # Listen for listbox clicks
    item_list_box.bind('<<ListboxSelect>>', listbox_click)

    global listbox_selection_item_ID
    listbox_selection_item_ID = 0


    root.mainloop()

def transaction_main():
    transaction_window()

#transaction_main()