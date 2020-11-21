import sqlite3
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tabulate import tabulate


with sqlite3.connect("main.db") as db:
    cursor = db.cursor()

def item_maintenance_window():

    # Display main list of existing items
    def get_existing_items():
        item_listbox.delete(0, 'end')
        cursor.execute("SELECT itemID, name, price FROM itemdb")
        existing_items_array = cursor.fetchall()
        temp_table = []
        for i in existing_items_array:
            transaction_item_list_itemID = i[0]
            transaction_item_list_name = i[1]
            transaction_item_list_price = format(i[2], ',.2f')
            temp_table.append([transaction_item_list_itemID, transaction_item_list_name, ("$" + transaction_item_list_price)])

        temp_table = (tabulate(temp_table, headers=["ID", "Name", "Price"]))

        n = 0
        for line in temp_table.split('\n'):
            item_listbox.insert(n, line)
            n += 1


    def add_new_item():

        # When submit button of "add item" menu is clicked
        def add_new_item_submit():
            # Pull input from fields
            add_item_ID_input = item_ID_field.get()
            add_item_name_input = item_name_field.get()
            add_item_price_input = item_price_field.get()

            # If user chooses to provide custom item ID
            if add_item_ID_input:

                # If item ID non-numeric
                if (str(add_item_ID_input)).isdigit() is False:
                    item_ID_label_feedback = Label(item_input_frame, font='Helvetica 8', text="Item ID invalid.", fg="red")
                    item_ID_label_feedback.grid(row=1, column=1)

                # If item ID not between 1-9999
                if str(add_item_ID_input).isdigit() is True and (int(add_item_ID_input) < 1 or int(add_item_ID_input) > 9999):
                    item_ID_label_feedback = Label(input_frame, font='Helvetica 8', text="Item ID must be between 1 and 9999.", fg="red")
                    item_ID_label_feedback.grid(row=1, column=1)

                # If all values are provided correctly
                if str(add_item_ID_input).isdigit() is True and int(add_item_ID_input) > 0 and int(add_item_ID_input) < 9999:
                    try:
                        float(add_item_price_input)
                        new_item_check_if_exists = ("SELECT * FROM itemdb WHERE itemID = ?")
                        cursor.execute(new_item_check_if_exists, [(add_item_ID_input)])

                        # If item ID is already listed in database
                        if cursor.fetchall():
                            add_item_ID_label_feedback = Label(item_input_frame, font='Helvetica 8', text="Item ID already in use", fg="red")
                            add_item_ID_label_feedback.grid(row=1, column=1)

                        # If item ID is available
                        else:
                            insert_new_item_query = '''INSERT INTO itemdb(itemID, name, price)
                                                VALUES(?,?,?)'''
                            cursor.execute(insert_new_item_query, [(add_item_ID_input), (add_item_name_input), (add_item_price_input)])
                            db.commit()
                            item_root.destroy()
                            get_existing_items()
                    except ValueError:
                        item_price_label_feedback = Label(item_input_frame, font='Helvetica 8', text="Price invalid", fg="red")
                        item_price_label_feedback.grid(row=5, column=1)



            # If user does not provide a custom item ID
            elif not add_item_ID_input:
                try:
                    float(add_item_price_input)
                    insert_new_item_query = '''INSERT INTO itemdb(name, price)
                                                        VALUES(?,?)'''
                    cursor.execute(insert_new_item_query, [(add_item_name_input), (add_item_price_input)])
                    db.commit()
                    item_root.destroy()
                    get_existing_items()

                except ValueError:
                    item_price_label_feedback = Label(item_input_frame, font='Helvetica 8', text="Price invalid",
                                                          fg="red")
                    item_price_label_feedback.grid(row=5, column=1)


        ####################### Add Item Window Definitions #######################
        item_root = Tk()
        item_root.title("Add New Item")
        item_root.geometry('400x400')
        item_root.grid_columnconfigure(0, weight=1)


        # Create main frame
        item_frame = Frame(item_root, height=600, width=800)
        item_frame.grid()

        # Create header frame
        item_header_frame = Frame(item_frame, height=30, width=800)
        item_header_frame.grid(row=0, column=0)

        # Create input frame
        item_input_frame = Frame(item_frame, height=400, width=800)
        item_input_frame.grid(row=1, column=0)

        # Display header
        item_header = Label(item_header_frame, font=headerfont, text="Add Item")
        item_header.grid(row=0, column=0)

        # Display input labels and fields
        item_ID_label = Label(item_input_frame, font=labelfont, text="Item ID: ")
        item_ID_label.grid(row=0, column=0)

        item_ID_field = Entry(item_input_frame)
        item_ID_field.grid(row=0, column=1)

        item_ID_label_feedback = Label(item_input_frame, font='Helvetica 8', text="")
        item_ID_label_feedback.grid(row=1, column=1)

        item_name_label = Label(item_input_frame, font="Arial 12", text="Item Name: ")
        item_name_label.grid(row=2, column=0)

        item_name_field = Entry(item_input_frame)
        item_name_field.grid(row=2, column=1)

        item_name_label_feedback = Label(item_input_frame, font='Helvetica 8', text="")
        item_name_label_feedback.grid(row=3, column=1)

        item_price_label = Label(item_input_frame, font="Arial 12", text="Item Price: $")
        item_price_label.grid(row=4, column=0)

        item_price_field = Entry(item_input_frame)
        item_price_field.grid(row=4, column=1)

        item_price_label_feedback = Label(item_input_frame, font='Helvetica 8', text="")
        item_price_label_feedback.grid(row=5, column=1)

        item_submit_button = Button(item_input_frame, text="Submit", command=add_new_item_submit)
        item_submit_button.grid(row=6, column=1)

        item_root.mainloop()



    def edit_item():

        # Query details on highlighted item
        def get_selected_item_details():
            selected_item_line = item_listbox.curselection()
            selected_item_line = item_listbox.get(selected_item_line).split(" ")
            while("" in selected_item_line):
                selected_item_line.remove("")
            selected_item_ID = selected_item_line[0]

            # Confirms valid line is highlighted
            if str(selected_item_ID).isdigit() is True:
                get_selected_item_name_query = "SELECT name FROM itemdb WHERE itemID = ?"
                cursor.execute(get_selected_item_name_query, [selected_item_ID])
                selected_item_name = cursor.fetchone()

                # When submit button of "edit item" menu is clicked
                def edit_item_submit():
                    edit_item_ID_input = selected_item_ID
                    edit_item_name_input = item_name_field.get()
                    edit_item_price_input = item_price_field.get()

                    # If user edits name but not price
                    if edit_item_name_input and not edit_item_price_input:
                        edit_item_query = '''UPDATE itemdb SET name = ? WHERE itemID = ?'''
                        cursor.execute(edit_item_query, [(edit_item_name_input), (edit_item_ID_input)])
                        db.commit()
                        item_root.destroy()
                        get_existing_items()

                    # If user edits price but not name
                    elif edit_item_price_input and not edit_item_name_input:
                        try:
                            float(edit_item_price_input)
                            edit_item_query = '''UPDATE itemdb SET price = ? WHERE itemID = ?'''
                            cursor.execute(edit_item_query, [(edit_item_price_input), (edit_item_ID_input)])
                            db.commit()
                            item_root.destroy()
                            get_existing_items()
                        except ValueError:
                            item_price_label_feedback = Label(item_input_frame, font='Helvetica 8', text="Price invalid", fg="red")
                            item_price_label_feedback.grid(row=5, column=1)
                    # If user edits the price and the name
                    elif edit_item_name_input and edit_item_price_input:
                        try:
                            float(edit_item_price_input)
                            edit_item_query = '''UPDATE itemdb SET name = ?, price = ? WHERE itemID = ?'''
                            cursor.execute(edit_item_query, [(edit_item_name_input), (edit_item_price_input), (edit_item_ID_input)])
                            db.commit()
                            item_root.destroy()
                            get_existing_items()
                        except ValueError:
                            item_price_label_feedback = Label(item_input_frame, font='Helvetica 8', text="Price invalid.", fg="red")
                            item_price_label_feedback.grid(row=5, column=1)


                ####################### Edit Item Window Definitions #######################
                item_root = Tk()
                item_root.title("Edit Item")
                item_root.geometry('400x400')
                item_root.grid_columnconfigure(0, weight=1)

                # Create main frame
                item_frame = Frame(item_root, height=600, width=800)
                item_frame.grid()

                # Create header frame
                item_header_frame = Frame(item_frame, height=30, width=800)
                item_header_frame.grid(row=0, column=0)

                # Create input frame
                item_input_frame = Frame(item_frame, height=400, width=800)
                item_input_frame.grid(row=1, column=0)

                # Display header
                item_header = Label(item_header_frame, font=headerfont, text="Edit Item")
                item_header.grid(row=0, column=0)

                item_info = Label(item_header_frame, text=("Editing " + selected_item_name[0]))
                item_info.grid(row=1, column=0)

                item_name_label = Label(item_input_frame, font="Arial 12", text="Item Name: ")
                item_name_label.grid(row=2, column=0)

                item_name_field = Entry(item_input_frame)
                item_name_field.grid(row=2, column=1)

                item_name_label_feedback = Label(item_input_frame, font='Helvetica 8', text="")
                item_name_label_feedback.grid(row=3, column=1)

                item_price_label = Label(item_input_frame, font="Arial 12", text="Item Price: $")
                item_price_label.grid(row=4, column=0)

                item_price_field = Entry(item_input_frame)
                item_price_field.grid(row=4, column=1)

                item_price_label_feedback = Label(item_input_frame, font='Helvetica 8', text="")
                item_price_label_feedback.grid(row=5, column=1)

                item_submit_button = Button(item_input_frame, text="Submit", command=edit_item_submit)
                item_submit_button.grid(row=6, column=1)

                item_root.mainloop()

            else:
                input_feedback_label = Label(feedback_frame, text="Invalid row selected", fg="red")
                input_feedback_label.grid(row=0, column=0)

        get_selected_item_details()



    def remove_item():
        # Query details on highlighted item
        def get_selected_item_details():
            selected_item_line = item_listbox.curselection()
            selected_item_line = item_listbox.get(selected_item_line).split(" ")
            while ("" in selected_item_line):
                selected_item_line.remove("")
            selected_item_ID = selected_item_line[0]


            # Confirms valid line is highlighted
            if str(selected_item_ID).isdigit() is True:
                get_selected_item_name_query = "SELECT name FROM itemdb WHERE itemID = ?"
                cursor.execute(get_selected_item_name_query, [selected_item_ID])
                selected_item_name = cursor.fetchone()
                remove_item_verify_window = messagebox.askokcancel("Verify Removal", ("Are you sure you want to delete " + selected_item_name[0] + "?"))
                if remove_item_verify_window is True:
                    remove_existing_item_name_query = "DELETE FROM itemdb WHERE itemID = ?"
                    cursor.execute(remove_existing_item_name_query, [(selected_item_ID)])
                    db.commit()
                    remove_item_successful_window = messagebox.showinfo("Removal successful", ("Successfully removed " + selected_item_name[0] + "."))
                    get_existing_items()

                else:
                    get_existing_items()

        get_selected_item_details()

    ####################### Main Window Definitions #######################
    root = Tk()
    root.title("Manage Items")
    root.geometry('600x800')


    from tkinter import font

    headerfont = 'Helvetica 16 bold'
    labelfont = 'Helvetica 12'
    monofont = 'TkFixedFont'

    root.grid_columnconfigure(0, weight=1)

    # Create main frame
    frame = Frame(root, height=600, width=800)
    frame.grid()

    # Create header frame
    header_frame = Frame(frame, height=30, width=800)
    header_frame.grid(row=0, column=0)

    # Create journal frame
    items_frame = Frame(frame, height=500, width=800)
    items_frame.grid(row=1, column=0)

    # Create input frame
    input_frame = Frame(frame, height=50, width=800)
    input_frame.grid(row=2, column=0)

    # Create feedback frame
    feedback_frame = Frame(frame, height=20, width=800)
    feedback_frame.grid(row=3, column=0)


    # Display header
    item_maintenance_header = Label(header_frame, font=headerfont, text="Manage Items")
    item_maintenance_header.grid(row=0, column=0)

    # Display item listbox
    item_listbox = Listbox(items_frame, width=50, height=30, font=monofont)
    item_listbox.grid(row=0, column=0)

    # Display input buttons
    item_add_button = Button(input_frame, text="Add New Item", command=add_new_item, height=2, width=20)
    item_add_button.grid(row=0, column=0)

    item_edit_button = Button(input_frame, text="Edit Selected Item", command=edit_item, height=2, width=20)
    item_edit_button.grid(row=0, column=1)

    item_remove_button = Button(input_frame, text="Remove Selected Item", command=remove_item, height=2, width=20)
    item_remove_button.grid(row=0, column=2)

    input_feedback_label = Label(feedback_frame, text="")
    input_feedback_label.grid(row=0, column=0)



    get_existing_items()
    root.mainloop()
