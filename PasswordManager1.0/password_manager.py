#!/usr/bin/env python3
#-----------------------------------IMPORTS-----------------------------#
import string
from tkinter import *
from tkinter import messagebox
from random import *
#import pyperclip

#-----------------------------------PASSWORD GENERATOR-----------------------------#

def generate_password():
    password_min = 8
    password_max = 32
    all_chars = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(all_chars) for x in range(randint(password_min, password_max)))
    password_entry.delete(0, END)
    password_entry.insert(0, password)
#pyperclip.copy(password)
#-----------------------------------SAVE PASSWORD-----------------------------#

def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title=website, message=f"Veuillez vous rassurer que toutes les cases soient remplies !")

    is_ok = messagebox.askokcancel(title=website, message=f"Voici les informations entrées : \nEmail: {email} \nPassword: {password}")


    if is_ok:
        with open("data.txt", "a") as data_file:
            data_file.write(f"{website} | {email } | {password}\n")
            website_entry.delete(0, END)

#-----------------------------------UI SETUP-----------------------------#

# Window creation
window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=50)
window.geometry("720x480")

# Image creation
canvas = Canvas(height=200, width=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

# Label creation
website_label = Label(text="Website URL :")
website_label.grid(row=1, column=0)
email_label = Label(text="Email / Username :")
email_label.grid(row=2, column=0)
password_label = Label(text="Password :")
password_label.grid(row=3, column=0)


# Entries / Input
website_entry = Entry(width=53)
website_entry.grid(row=1, column=1, columnspan=10)
email_entry = Entry(width=53)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "bproust14@gmail.com")
password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

# Buttons
generate_password = Button(text="Generate Password", width=14, command=generate_password)
generate_password.grid(row=3, column=2)
add_button = Button(text="Add", width=26, command=save)
add_button.grid(row=4, column=1)

window.mainloop()