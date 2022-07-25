#!/usr/bin/env python3.9

"""This projects aims to build a little, personal DB that I'm going to use
with the development of a game, it is going to help me add images and annotate
ideas within them, or just plain ideas without an image, because MS Word can get tedious at
times."""

# TODO: 1) Update Labelframe image once selected; 2) Maybe remove that dictionary stuff,
#  it was fun as training, but I think it is giving me problems; 3) Get radio buttons, Labelframe
#  image (maybe also store it into another variable) and text box value and store them into the
#  database, rendering my app finished <3
#  Or so I believe...

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image  # Para mostrar otros formatos de imagen
import sqlite3
import copy
import base64
import csv


# Function to choose the image
def open_file():
    global new_img
    button.configure(text="Save", command=lambda: save())
    button.place(rely=.92)
    back_btn.place(relx=.11, rely=0.04, anchor="center")
    img_frame.place(relx=.5, rely=.33, anchor="center")
    side_note.place(relx=.47, rely=.72, anchor="e")
    cat.place(relx=.53, rely=.72, anchor="w")

    img_thumb = copy.copy(open_img())  # Making a copy so that returned image isn't made smaller
    img_thumb.thumbnail(DISPLAY_SIZE)
    new_img = ImageTk.PhotoImage(img_thumb)
    frame_lbl.configure(image=new_img)
    frame_lbl.place(relx=.5, rely=.5, anchor="center")


def open_img():
    global path
    global my_img

    path = filedialog.askopenfilename(
        initialdir=r"/home/misato/Imágenes",
        filetypes=(
            ("All files", "*.*"),
            ("JPG Files", "*.jpg"),
            ("PNG Files", "*.png")
        )
    )

    my_img = Image.open(path)
    if my_img.width > 720 or my_img.height > 720:
        my_img.thumbnail(MAX_SIZE)  # Resized image to max dimensions of 720x720
    my_img.save(path)
    return my_img


def save():
    # Will save: image in base64, side note, category and a zero (for "done" attribute) into db
    db_img_str = to_base64()
    db_note = side_note.get(1.0, "end-1c")
    db_cat = radio_var.get()

    save_conn = sqlite3.connect('ideas.db')
    c = save_conn.cursor()
    data_tuple = (db_img_str, db_note, db_cat, 0)
    c.execute(insert, data_tuple)
    save_conn.commit()
    c.close()
    save_conn.close()

    restore()


# Converts choosed image into base64 to save it as string into db
def to_base64():
    with open(path, 'rb') as file:
        img_encoded = base64.b64encode(file.read())
    return img_encoded.decode('UTF-8')  # Removes the first letter 'b'


# To clear the window and bring button back to its original place
def restore():
    radio_var.set(" ")
    side_note.delete('1.0', END)
    frame_lbl.place_forget()
    img_frame.place_forget()
    cat.place_forget()
    side_note.place_forget()
    back_btn.place_forget()
    button.configure(text="Add an idea!", command=open_file)
    button.place(relx=.5, rely=.5, anchor="center")


def on_closing():
    close_conn = sqlite3.connect('ideas.db')
    c = close_conn.cursor()
    ideas = c.execute("SELECT * FROM ideas")

    with open("/home/misato/Dropbox/ideas.csv", "w", newline='') as f:
        file = csv.writer(f)
        file.writerow(['id', 'image_base64', 'side_note', 'category', 'done'])
        file.writerows(ideas)

    close_conn.commit()
    c.close()
    close_conn.close()
    root.destroy()


bGround = "#2A2D37"
hlbGround = "#4B5062"
wbGround = "#FFFFFF"
gbGround = "#555A5B"
DISPLAY_SIZE = (265, 245)
MAX_SIZE = (720, 720)
categories = {
    "Clothing": "clothing",
    "Footwear": "footwear",
    "Hairstyle": "hairstyle",
    "Weapons": "weapons",
    "Actions": "actions",
    "Art & Deco": "art-deco",
    "Car Model": "cars",
    "Car Wrap": "car-skin",
    "Vehicle Parts": "vehicle-parts",
    "Reference": "reference",
    "Other": "other"
}

# Window creation
root = Tk()
root.title("IdSave")

# From here we start to declare variables
window_w = 550  # 'w' for width and 'h' for height
window_h = 600
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w / 2) - (window_w / 2)  # If we don't take out WxH of the window it would be off center
y = (screen_h / 2) - (window_h / 2)
root.geometry(f"{window_w}x{window_h}+{int(x)}+{int(y)}")
# And just above we used prior variables to center the window

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.resizable(False, False)
root.configure(bg=bGround)

back_btn = Button(root, text="< Back  ", padx=20, command=restore)
img_frame = LabelFrame(root, text="Image", height=280, width=280)
frame_lbl = Label(img_frame)
side_note = Text(root, width=23, height=8, padx=8, pady=5)
button = Button(root, text="Add an idea!", padx=40, command=open_file)
button.place(relx=.5, rely=.5, anchor="center")

# Frame for the categories
cat = Frame(root, width=210, height=150, bg=bGround)
# End of window creation ---------------------

# To create buttons with the categories dictionary
radio_var = StringVar(value=" ")
yy1 = 0
yy2 = 0
xx = 0
cont = 0
for (key, value) in categories.items():
    if cont < (len(categories)/2):
        Radiobutton(
            cat,
            text=key,
            bg=bGround,
            activebackground=hlbGround,
            activeforeground=wbGround,
            highlightthickness=0,
            selectcolor=gbGround,
            fg=wbGround,
            borderwidth=0,
            variable=radio_var,
            value=value
        ).place(relx=xx, rely=yy1)
        yy1 += .18
        cont += 1
    else:
        xx = .45
        Radiobutton(
            cat,
            text=key,
            bg=bGround,
            activebackground=hlbGround,
            activeforeground=wbGround,
            highlightthickness=0,
            selectcolor=gbGround,
            fg=wbGround,
            borderwidth=0,
            variable=radio_var,
            value=value
        ).place(relx=xx, rely=yy2)
        yy2 += .18
# End of radio buttons creation

# Database creation
conn = sqlite3.connect('ideas.db')
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS ideas (
        [id] INTEGER PRIMARY KEY AUTOINCREMENT,
        [image_base64] TEXT,
        [side_note] TEXT,
        [category] TEXT,
        [done] INTEGER
    )"""
)
# "done" to be treated as boolean

conn.commit()
cursor.close()
conn.close()

insert = """ INSERT INTO ideas (image_base64, side_note, category, done) VALUES (?, ?, ?, ?) """
# End of database ----------------------------

root.protocol("WM_DELETE_WINDOW", on_closing)
# Always at the end
root.mainloop()

