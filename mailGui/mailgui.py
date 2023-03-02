

from tkinter import *
import smtplib
import re

def login():
    if validate_login():
        global username
        global password

        # read credentials from GUI input fields.
        username = str(emailEntry.get())
        password = str(passEntry.get())
        print(username, password)

        global server
        # make a smtplib object
        server = smtplib.SMTP("smtp.gmail.com:587")
        # connect with default SMTP server running on our machine.
        server.ehlo()
        # make secure connection
        server.starttls()
        # login to the server
        server.login(username, password)
        f2.pack()
        logoutBtn.grid()
        # send Logged In message to the user on GUI.
        loginSuccessful["text"] = "Logged In!"
        root.after(10, root.grid)
        f1.pack_forget()
        root.after(10, root.grid)
        f3.pack()

        # removing username and password fields.
        sendSuccessful.grid_remove()
        root.after(10, root.grid)


def hide_login_label():
    f2.pack_forget()
    f3.pack_forget()
    root.after(10, root.grid)


def send_email():
    # validate message email
    if validate_message():
        sendSuccessful.grid_remove()
        root.after(10, root.grid)
        # read fields from entry fields.
        receiver = str(toEntry.get())
        subject = str(subjectEntry.get())
        msgbody = str(messageEntry.get())

        # make message string by combining.
        msg = "From: " + username + "\n" + "To: " + receiver + "\n" + "Subject: " + subject + "\n" + msgbody

        try:
            # send email method
            server.sendmail(username, receiver, msg)
            sendSuccessful.grid()
            # show success message to the user.
            sendSuccessful["text"] = "Mail Sent!"
            root.after(10, sendSuccessful.grid)
        except Exception as e:
            # in case of exception -> show failure message.
            sendSuccessful.grid()
            sendSuccessful["text"] = "Error in Sending Your Email"
            root.after(10, root.grid)


def logout():
    try:
        # off the server
        server.quit()
        f3.pack_forget()
        f2.pack()
        loginSuccessful.grid()
        # display message to user
        loginSuccessful["text"] = "Logged Out Successfully"
        logoutBtn.grid_remove()
        f1.pack()
        # end program
        passEntry.delete(0, END)
        root.after(10, root.grid)

    except Exception as e:
        loginSuccessful["text"] = "Error in Logout"


def validate_login():
    # read email and password from entry of GUI
    email_text = str(emailEntry.get())
    pass_text = str(passEntry.get())

    # check if fields are empty -> return False
    if (email_text == "") or (pass_text == ""):
        f2.pack()
        loginSuccessful.grid()
        # give proper response to user.
        loginSuccessful["text"] = "Fill all the Fields"
        logoutBtn.grid_remove()
        root.after(10, root.grid)
        # return False, because fields are empty.
        return False

    else:
        # get email regex and compile it
        email_regex = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")
        # check if email_text is not a valid email address -> return False
        if not email_regex.match(email_text):
            f2.pack()
            loginSuccessful.grid()
            # give proper response to user.
            loginSuccessful["text"] = "Enter a valid Email Address"
            logoutBtn.grid_remove()
            root.after(10, root.grid)
            # return False, because email format is invalid.
            return False

        # finally return true if both above cases are not True.
        else:
            return True


def validate_message():
    # read values from entry fields.
    email_text = str(toEntry.get())
    sub_text = str(subjectEntry.get())
    msg_text = str(messageEntry.get())

    # check if email are subject text is empty
    if (email_text == "") or (sub_text == "") or (msg_text == ""):
        sendSuccessful.grid()
        sendSuccessful["text"] = "Fill in all the Fields"
        root.after(10, root.grid)
        return False
    else:
        # check if email is in correct format
        EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")
        if not EMAIL_REGEX.match(email_text):
            f2.pack()
            sendSuccessful.grid()
            sendSuccessful["text"] = "Enter a valid Email Address"
            root.after(10, root.grid)
            return False
        else: # if all goods -> return True
            return True


# root to create Tkinter object
root = Tk()
root.title("Email Application")  # set title of window.

# setting up the first frame
f1 = Frame(root, width=10000, height=8000)
f1.pack(side=TOP)

# a label to show message to user about enter credentials
credential = Label(f1, text="Enter Your Credentials", font="Ariel")
credential.grid(row=0, columnspan=3, pady=80, padx=150)

# labels of email and password
email = Label(f1, text="Email").grid(row=1, sticky=E, pady=5, padx=10)
password = Label(f1, text="Password").grid(row=2, sticky=E, pady=5, padx=10)

# entry field of email
emailEntry = Entry(f1)
# entry field of password, hide password with * in input field
passEntry = Entry(f1, show="*")

emailEntry.grid(row=1, column=1, pady=5)
passEntry.grid(row=2, column=1)

# Button for login the user
loginBtn = Button(f1, text="Login", width=10, bg="black", fg="white", command=lambda: login())
loginBtn.grid(row=3, columnspan=3, pady=10)

# frame 2
f2 = Frame(root)
f2.pack(side=TOP, expand=NO, fill=NONE)

# label field to show message of error or success
loginSuccessful = Label(f2, width=20, bg="cyan", fg="red", text="Log in Success", font="Ariel")
loginSuccessful.grid(row=0, column=0, columnspan=2, pady=5)

# logout button
logoutBtn = Button(f2, text="Logout", bg="black", fg="white", command=lambda: logout())
logoutBtn.grid(row=0, column=4, sticky=E, pady=10, padx=(5, 0))

# frame 3
f3 = Frame(root)
f3.pack(side=TOP, expand=NO, fill=NONE)

# Message to user about compose email
composeEmail = Label(f3, width=20, text="Compose Email", font="Ariel")
composeEmail.grid(row=0, columnspan=3, pady=10)

# To, Subject, and message labels
to = Label(f3, text="To").grid(row=1, sticky=E, pady=5)
subject = Label(f3, text="Subject").grid(row=2, sticky=E, pady=5)
message = Label(f3, text="Message").grid(row=3, sticky=E)

# input fields for To, Subject, and message
toEntry = Entry(f3)
subjectEntry = Entry(f3)
messageEntry = Entry(f3)

toEntry.grid(row=1, column=1, pady=5)
subjectEntry.grid(row=2, column=1, pady=5)
messageEntry.grid(row=3, column=1, pady=5, rowspan=3, ipady=10)

# send button to send email at the destination
sendEmailBtn = Button(f3, text="Send Email", width=10, bg="black", fg="white", command=lambda: send_email())
sendEmailBtn.grid(row=6, columnspan=3, pady=10)

# message if email successfully sent, otherwise error
sendSuccessful = Label(f3, width=20, fg="white", bg="black", font="Ariel")
sendSuccessful.grid(row=7, columnspan=3, pady=5)

# call function to hide login info
hide_login_label()

# GUI not killed -> run it in loop
mainloop()
