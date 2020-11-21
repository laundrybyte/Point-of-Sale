import sqlite3
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tabulate import tabulate


with sqlite3.connect("main.db") as db:
    cursor = db.cursor()

def user_maintenance_window():

    # Display main list of existing users
    def get_existing_users():
        user_listbox.delete(0, 'end')
        cursor.execute("SELECT userID, name FROM userdb")
        existing_users_array = cursor.fetchall()
        temp_table = []
        for i in existing_users_array:
            user_list_userID = i[0]
            user_list_name = i[1]
            temp_table.append([user_list_userID, user_list_name])

        temp_table = (tabulate(temp_table, headers=["ID", "Name"]))

        n = 0
        for line in temp_table.split('\n'):
            user_listbox.insert(n, line)
            n += 1


    def add_new_user():

        # When submit button of "add user" menu is clicked
        def add_new_user_submit():
            # Pull input from fields
            add_user_ID_input = user_ID_field.get()
            add_user_name_input = user_name_field.get()
            add_user_pass_input = user_passcode_field.get()

            # If user ID non-numeric
            if (str(add_user_ID_input)).isdigit() is False:
                user_ID_label_feedback = Label(user_input_frame, font='Helvetica 8', text="User ID invalid.", fg="red")
                user_ID_label_feedback.grid(row=1, column=1)

            # If user ID not between 1-9999
            if str(add_user_ID_input).isdigit() is True and (int(add_user_ID_input) < 1 or int(add_user_ID_input) > 9999):
                user_ID_label_feedback = Label(user_input_frame, font='Helvetica 8', text="User ID must be between 1 and 9999.", fg="red")
                user_ID_label_feedback.grid(row=1, column=1)

            # If passcode non-numeric
            if (str(add_user_pass_input)).isdigit() is False:
                user_passcode_label_feedback = Label(user_input_frame, font='Helvetica 8', text="Passcode invalid.", fg="red")
                user_passcode_label_feedback.grid(row=5, column=1)

            # If passcode not between 1-9999
            if str(add_user_pass_input).isdigit() is True and (int(add_user_pass_input) < 1 or int(add_user_pass_input) > 9999):
                user_passcode_label_feedback = Label(user_input_frame, font='Helvetica 8', text="Passcode must be between 1 and 9999.", fg="red")
                user_passcode_label_feedback.grid(row=5, column=1)

            # If no user name provided
            if not add_user_name_input:
                user_name_label_feedback = Label(user_input_frame, font='Helvetica 8', text="Name required.", fg="red")
                user_name_label_feedback.grid(row=3, column=1)

            # If all values provided correctly
            if (str(add_user_ID_input).isdigit() is True and int(add_user_ID_input) > 0 and int(add_user_ID_input) < 9999) \
                    and (str(add_user_pass_input).isdigit() and int(add_user_pass_input) > 0 and int(add_user_pass_input) < 9999)\
                    and add_user_name_input:

                # Check if new user exists
                new_user_check_if_exists = ("SELECT * FROM userdb WHERE userID = ?")
                cursor.execute(new_user_check_if_exists, [(add_user_ID_input)])

                # If user ID is already listed in database
                if cursor.fetchall():
                    user_ID_label_feedback = Label(user_input_frame, font='Helvetica 8', text="User ID already in use.", fg="red")
                    user_ID_label_feedback.grid(row=1, column=1)

                # If user ID is available
                else:
                    insert_new_user_query = '''INSERT INTO userdb(userID, name, passcode)
                                        VALUES(?,?,?)'''
                    cursor.execute(insert_new_user_query, [(add_user_ID_input), (add_user_name_input), (add_user_pass_input)])
                    db.commit()
                    user_root.destroy()
                    get_existing_users()




        ####################### Add user Window Definitions #######################
        user_root = Tk()
        user_root.title("Add New user")
        user_root.geometry('400x400')
        user_root.grid_columnconfigure(0, weight=1)


        # Create main frame
        user_frame = Frame(user_root, height=600, width=800)
        user_frame.grid()

        # Create header frame
        user_header_frame = Frame(user_frame, height=30, width=800)
        user_header_frame.grid(row=0, column=0)

        # Create input frame
        user_input_frame = Frame(user_frame, height=400, width=800)
        user_input_frame.grid(row=1, column=0)

        # Display header
        user_header = Label(user_header_frame, font=headerfont, text="Add User")
        user_header.grid(row=0, column=0)

        # Display input labels and fields
        user_ID_label = Label(user_input_frame, font=labelfont, text="User ID: ")
        user_ID_label.grid(row=0, column=0)

        user_ID_field = Entry(user_input_frame)
        user_ID_field.grid(row=0, column=1)

        user_ID_label_feedback = Label(user_input_frame, font='Helvetica 8', text="")
        user_ID_label_feedback.grid(row=1, column=1)

        user_name_label = Label(user_input_frame, font=labelfont, text="User Name: ")
        user_name_label.grid(row=2, column=0)

        user_name_field = Entry(user_input_frame)
        user_name_field.grid(row=2, column=1)

        user_name_label_feedback = Label(user_input_frame, font='Helvetica 8', text="")
        user_name_label_feedback.grid(row=3, column=1)

        user_passcode_label = Label(user_input_frame, font=labelfont, text="Passcode: ")
        user_passcode_label.grid(row=4, column=0)

        user_passcode_field = Entry(user_input_frame, show="*")
        user_passcode_field.grid(row=4, column=1)

        user_passcode_label_feedback = Label(user_input_frame, font='Helvetica 8', text="")
        user_passcode_label_feedback.grid(row=5, column=1)

        user_submit_button = Button(user_input_frame, text="Submit", command=add_new_user_submit, height=1, width=10)
        user_submit_button.grid(row=6, column=1)

        user_root.mainloop()



    def edit_user():

        # Query details on highlighted user
        def get_selected_user_details():
            selected_user_line = user_listbox.curselection()
            selected_user_line = user_listbox.get(selected_user_line).split(" ")
            while ("" in selected_user_line):
                selected_user_line.remove("")
            selected_user_ID = selected_user_line[0]

            # Confirms valid line is highlighted
            if str(selected_user_ID).isdigit():
                get_selected_user_name_query = "SELECT name FROM userdb WHERE userID = ?"
                cursor.execute(get_selected_user_name_query, [selected_user_ID])
                selected_user_name = cursor.fetchone()

                # When submit button of "edit user" menu is clicked
                def edit_user_submit():
                    edit_user_ID_input = selected_user_ID
                    edit_user_name_input = user_name_field.get()
                    edit_user_pass_input = user_pass_field.get()

                    # If user edits name but not pass
                    if edit_user_name_input and not edit_user_pass_input:
                        edit_user_query = '''UPDATE userdb SET name = ? WHERE userID = ?'''
                        cursor.execute(edit_user_query, [(edit_user_name_input), (edit_user_ID_input)])
                        db.commit()
                        user_root.destroy()
                        get_existing_users()

                    # If user edits pass but not name
                    elif edit_user_pass_input and not edit_user_name_input:
                        # If passcode non-numeric
                        if (str(edit_user_pass_input).isdigit() is False):
                            user_pass_label_feedback = Label(user_input_frame, font='Helvetica 8', text="Passcode invalid", fg="red")
                            user_pass_label_feedback.grid(row=5, column=1)

                        # If passcode not between 1-9999
                        if int(edit_user_pass_input) < 1 or int(edit_user_pass_input) > 9999:
                            user_pass_label_feedback = Label(user_input_frame, font='Helvetica 8', text="Passcode must be between 1 and 9999", fg="red")
                            user_pass_label_feedback.grid(row=5, column=1)

                        # If passcode provided correctly
                        if (str(edit_user_pass_input).isdigit() is True and (int(edit_user_pass_input) > 1 and int(edit_user_pass_input) < 9999)):
                            edit_user_query = '''UPDATE userdb SET passcode = ? WHERE userID = ?'''
                            cursor.execute(edit_user_query, [(edit_user_pass_input), (edit_user_ID_input)])
                            db.commit()
                            user_root.destroy()
                            get_existing_users()

                    # If user edits pass AND name
                    elif edit_user_pass_input and edit_user_name_input:
                        # If passcode non-numeric
                        if (str(edit_user_pass_input).isdigit() is False):
                            user_pass_label_feedback = Label(user_input_frame, font='Helvetica 8', text="Passcode invalid", fg="red")
                            user_pass_label_feedback.grid(row=5, column=1)

                        # If passcode not between 1-9999
                        if int(edit_user_pass_input) < 1 or int(edit_user_pass_input) > 9999:
                            user_pass_label_feedback = Label(user_input_frame, font='Helvetica 8', text="Passcode must be between 1 and 9999", fg="red")
                            user_pass_label_feedback.grid(row=5, column=1)

                        # If passcode provided correctly
                        if (str(edit_user_pass_input).isdigit() is True and (int(edit_user_pass_input) > 1 and int(edit_user_pass_input) < 9999)):
                            edit_user_query = '''UPDATE userdb SET passcode = ?, name = ? WHERE userID = ?'''
                            cursor.execute(edit_user_query, [(edit_user_pass_input), (edit_user_name_input), (edit_user_ID_input)])
                            db.commit()
                            user_root.destroy()
                            get_existing_users()



                ####################### Edit user Window Definitions #######################
                user_root = Tk()
                user_root.title("Edit user")
                user_root.geometry('400x400')
                user_root.grid_columnconfigure(0, weight=1)

                # Create main frame
                user_frame = Frame(user_root, height=600, width=800)
                user_frame.grid()

                # Create header frame
                user_header_frame = Frame(user_frame, height=30, width=800)
                user_header_frame.grid(row=0, column=0)

                # Create input frame
                user_input_frame = Frame(user_frame, height=400, width=800)
                user_input_frame.grid(row=1, column=0)

                # Display header
                user_header = Label(user_header_frame, font=headerfont, text="Edit user")
                user_header.grid(row=0, column=0)

                user_info = Label(user_header_frame, text=("Editing " + selected_user_name[0]))
                user_info.grid(row=1, column=0)

                user_name_label = Label(user_input_frame, font=labelfont, text="User Name: ")
                user_name_label.grid(row=2, column=0)

                user_name_field = Entry(user_input_frame)
                user_name_field.grid(row=2, column=1)

                user_name_label_feedback = Label(user_input_frame, font='Helvetica 8', text="")
                user_name_label_feedback.grid(row=3, column=1)

                user_pass_label = Label(user_input_frame, font=labelfont, text="User Passcode: ")
                user_pass_label.grid(row=4, column=0)

                user_pass_field = Entry(user_input_frame, show="*")
                user_pass_field.grid(row=4, column=1)

                user_pass_label_feedback = Label(user_input_frame, font='Helvetica 8', text="")
                user_pass_label_feedback.grid(row=5, column=1)

                user_submit_button = Button(user_input_frame, text="Submit", command=edit_user_submit, height=1, width=10)
                user_submit_button.grid(row=6, column=1)

                user_root.mainloop()

            else:
                input_feedback_label = Label(feedback_frame, text="Invalid row selected", fg="red")
                input_feedback_label.grid(row=0, column=0)

        get_selected_user_details()



    def remove_user():
        # Query details on highlighted user
        def get_selected_user_details():
            selected_user_line = user_listbox.curselection()
            selected_user_line = user_listbox.get(selected_user_line).split(" ")
            while ("" in selected_user_line):
                selected_user_line.remove("")
            selected_user_ID = selected_user_line[0]



            # Confirms valid line is highlighted
            from tkinter import messagebox
            if str(selected_user_ID).isdigit():
                get_selected_user_name_query = "SELECT name FROM userdb WHERE userID = ?"
                cursor.execute(get_selected_user_name_query, [selected_user_ID])
                selected_user_name = cursor.fetchone()
                global remove_user_verify_window
                remove_user_verify_window = messagebox.askokcancel("Verify Removal", ("Are you sure you want to delete " + selected_user_name[0] + "?"))
                # If user clicks "OK"
                if remove_user_verify_window is True:
                    remove_existing_user_query = "DELETE FROM userdb WHERE userID = ?"
                    cursor.execute(remove_existing_user_query, [(selected_user_ID)])
                    db.commit()
                    remove_user_successful_window = messagebox.showinfo("Removal successful", ("Successfully removed " + selected_user_name[0] + "."))
                    get_existing_users()

                # If user clicks "Cancel"
                else:
                    print("Cancel")
                    get_existing_users()

        get_selected_user_details()

    ####################### Main Window Definitions #######################
    root = Tk()
    root.title("Manage users")
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

    # Create list frame
    user_frame = Frame(frame, height=500, width=800)
    user_frame.grid(row=1, column=0)

    # Create input frame
    input_frame = Frame(frame, height=50, width=800)
    input_frame.grid(row=2, column=0)

    # Create feedback frame
    feedback_frame = Frame(frame, height=20, width=800)
    feedback_frame.grid(row=3, column=0)


    # Display header
    user_maintenance_header = Label(header_frame, font=headerfont, text="Manage Users")
    user_maintenance_header.grid(row=0, column=0)

    # Display user listbox
    user_listbox = Listbox(user_frame, width=50, height=30, font=monofont)
    user_listbox.grid(row=0, column=0)

    # Display input buttons
    user_add_button = Button(input_frame, text="Add New User", command=add_new_user, height=2, width=20)
    user_add_button.grid(row=0, column=0)

    user_edit_button = Button(input_frame, text="Edit Selected User", command=edit_user, height=2, width=20)
    user_edit_button.grid(row=0, column=1)

    user_remove_button = Button(input_frame, text="Remove Selected User", command=remove_user, height=2, width=20)
    user_remove_button.grid(row=0, column=2)

    input_feedback_label = Label(feedback_frame, text="")
    input_feedback_label.grid(row=0, column=0)



    get_existing_users()
    root.mainloop()
