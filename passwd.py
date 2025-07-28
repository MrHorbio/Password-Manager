import json
import random
import string
import os
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
from PIL import Image, ImageTk

# === Key Management ===
KEY_FILE = "key.key"
DATA_FILE = "data.json"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as file:
        file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, 'rb') as file:
        return file.read()

fernet = Fernet(load_key())

# === Password Generator ===
def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(12))
    password_entry.delete(0, END)
    password_entry.insert(0, password)

# === Save Credentials ===
def save_password():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        messagebox.showwarning("Oops", "Website and Password can't be empty.")
        return

    new_data = {
        website: {
            "email": email,
            "password": fernet.encrypt(password.encode()).decode()
        }
    }

    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)
    messagebox.showinfo("Success", f"Credentials saved for {website}.")

# === Search Credentials ===
def find_password():
    website = website_entry.get().strip()
    if not website:
        messagebox.showwarning("Oops", "Please enter a website to search.")
        return

    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found.")
        return

    if website in data:
        email = data[website]['email']
        decrypted_password = fernet.decrypt(data[website]['password'].encode()).decode()
        messagebox.showinfo(website, f"Email: {email}\nPassword: {decrypted_password}")
    else:
        messagebox.showinfo("Not Found", f"No credentials found for {website}.")

# === GUI Setup ===
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50,bg="yellow")


# === Canvas for Logo ===
logo_path = "logo.png"
if os.path.exists(logo_path):
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((150, 150))  # Resize to fit well
    logo_img = ImageTk.PhotoImage(logo_image)
    
    canvas = Canvas(width=150, height=150, highlightthickness=0)
    canvas.create_image(75, 75, image=logo_img)
    canvas.grid(row=0, column=1)
else:
    canvas = Canvas(height=100, width=100)
    canvas.grid(row=0, column=1)

# === Labels ===
Label(text="Website:",bg="Yellow",fg="Black",).grid(row=1, column=0, sticky=E)
Label(text="Email/Username:",bg="Yellow").grid(row=2, column=0, sticky=E)
Label(text="Password:",bg="Yellow").grid(row=3, column=0, sticky=E)

# === Entries ===
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, sticky=W,pady=10)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky=W,pady=10)
email_entry.insert(0, "your_email@example.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky=W,pady=10)

# === Buttons ===
Button(text="Search", width=13, command=find_password).grid(row=1, column=2, sticky=W)
Button(text="Generate Password", command=generate_password).grid(row=3, column=2, sticky=W)
Button(text="Add", width=36, command=save_password).grid(row=4, column=1, columnspan=2, pady=10)


#=======Watermark=========
Label(text="Created By Mr.Horbio",bg="Yellow").grid(row=6, column=1, sticky=E)

# === Start GUI Loop ===
window.mainloop()
