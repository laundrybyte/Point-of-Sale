from tkinter import *
from tkinter import font
import sqlite3



with sqlite3.connect("main.db") as db:
    cursor = db.cursor()


def login_window():
    def login():
        userID = login_userID_input.get()
        passcode = login_passcode_input.get()
        login_query_user = ("SELECT * FROM userdb WHERE userID = ? AND passcode = ?")
        cursor.execute(login_query_user, [(userID), (passcode)])
        login_query_results = cursor.fetchone()

        if login_query_results:
            # Set username variables
            global login_username
            login_username = str(login_query_results[1])
            global transaction_user
            transaction_user = login_username

            # Open main menu window
            import pos_mainmenu
            pos_mainmenu.main_menu_window()

            # Provide feedback
            login_feedback = ("Welcome, " + login_username)
            login_feedback_label = Label(root, font="Arial 10", fg="green", text=login_feedback)
            login_feedback_label.grid(row=4)

            # Clear input fields
            login_userID_input.delete(0, 'end')
            login_passcode_input.delete(0, 'end')





        else:
            login_passcode_input.delete(0, 'end')
            login_feedback = ("User ID/Passcode incorrect.")
            login_feedback_label = Label(root, font="Ariel 10", fg="red", text=login_feedback)
            login_feedback_label.grid(row=4)


    ####################### Window Definitions #######################
    global root
    root = Tk()
    root.title("Login")
    root.geometry('800x600')

    headerfont = font.Font(family='Helvetica', size=16, weight='bold')
    labelfont = font.Font(family='Helvetica', size=11, weight='normal')
    monofont = font.Font(family='Lucida Console', size=11)

    # Create main frame
    frame = Frame(root, height=600, width=500)
    frame.grid(row=0, column=0)

    # Create header frame
    header_frame = Frame(frame, height=100, width=500)
    header_frame.grid(row=0, column=0)

    # Create input frame
    input_frame = Frame(frame)
    input_frame.grid(row=1)

    # Create button frame
    button_frame = Frame(frame)
    button_frame.grid(row=2)

    # Grid configure settings
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure((0), weight=1)
    root.grid_rowconfigure((1,2), weight=1)
    #header_frame.grid_rowconfigure((1), weight=0)
    #input_frame.grid_rowconfigure((1), weight=1)
    header_frame.grid_columnconfigure((0), weight=1)

    # Create header label
    header = Label(header_frame, font=headerfont, text="Login", pady=10, padx=10)
    header.grid(row=0, column=0, columnspan=2)

    # Create "User ID:" label
    login_userID_prompt = Label(input_frame, font=labelfont, text="User ID: ", pady=10, padx=10)
    login_userID_prompt.grid(row=2, column=0)

    # Create "User ID" entry
    global login_userID_input
    login_userID_input = Entry(input_frame)
    login_userID_input.grid(row=2, column=1)

    # Create "Passcode:" label
    login_passcode_prompt = Label(input_frame, font=labelfont, text="Passcode: ", pady=10, padx=10)
    login_passcode_prompt.grid(row=3, column=0)

    # Create "Passcode" entry
    global login_passcode_input
    login_passcode_input = Entry(input_frame, show='*')
    login_passcode_input.grid(row=3, column=1)

    # Create "Login" button
    login_button = Button(button_frame, text="Login", command=login, width=10)
    login_button.grid(row=4, column=1, columnspan=2)

    # Empty login label
    login_feedback = ""
    login_feedback_label = Label(input_frame, font="Ariel 12", text=login_feedback)
    login_feedback_label.grid(row=5, column=1)

    root.mainloop()




