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

# Should I use radio buttons to select the category of image??? Maybe, yes.
#
# radio_var = strVar()
# radio_var.get()
# radio_button = Radiobutton(root, text="Categoria X", variable=radio_var,
# value="categoriax").pack()
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image  # Para mostrar otros formatos de imagen
import sqlite3
import copy


# Function to choose the image
def open_file():
    global path
    global new_img
    button.configure(text="Save", command=lambda: save())
    button.place(rely=.92)
    back_btn.place(relx=.11, rely=0.04, anchor="c")
    img_frame.place(relx=.5, rely=.33, anchor="c")
    side_note.place(relx=.47, rely=.72, anchor="e")
    cat.place(relx=.53, rely=.72, anchor="w")

    dir_path = open('dir.txt', 'r')
    path = root.filename = filedialog.askopenfilename(
        initialdir=dir_path.readline(),
        filetypes=(
            ("All files", "*.*"),
            ("JPG Files", "*.jpg"),
            ("PNG Files", "*.png")
        )
    )
    dir_path.close()

    my_img = Image.open(root.filename)
    img_thumb = copy.copy(my_img)
    img_thumb.thumbnail(MAX_SIZE)
    new_img = ImageTk.PhotoImage(img_thumb)
    frame_lbl.configure(image=new_img)
    frame_lbl.place(relx=.5, rely=.5, anchor="c")


def save():
    # Will save: image, side note & category into db with SQL
    db_img = to_binary()
    db_note = side_note.get(1.0, "end-1c")
    db_cat = radio_var.get()

    func_conn = sqlite3.connect('ideas.db')
    c = func_conn.cursor()
    data_tuple = (db_img, db_note, db_cat)
    c.execute(insert, data_tuple)
    func_conn.commit()
    c.close()
    func_conn.close()

    restore()


# Converts choosed image into a binary object in order to save it into db
def to_binary():
    with open(path, 'rb') as file:
        blob_data = file.read()
    return blob_data


# To clear the window and bring button back to its original place
def restore():
    radio_var.set(None)
    side_note.delete('1.0', END)
    frame_lbl.place_forget()
    img_frame.place_forget()
    cat.place_forget()
    side_note.place_forget()
    back_btn.place_forget()
    button.configure(text="Add an idea!", command=open_file)
    button.place(relx=.5, rely=.5, anchor="c")


bGround = "#2A2D37"
hlbGround = "#4B5062"
wbGround = "#FFFFFF"
gbGround = "#555A5B"
MAX_SIZE = (265, 245)
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
root.resizable(0, 0)
root.configure(bg=bGround)

back_btn = Button(root, text="< Back  ", padx=20, command=restore)
img_frame = LabelFrame(root, text="Image", height=280, width=280)
frame_lbl = Label(img_frame)
side_note = Text(root, width=23, height=8, padx=8, pady=5)
button = Button(root, text="Add an idea!", padx=40, command=open_file)
button.place(relx=.5, rely=.5, anchor="c")

# Frame for the categories
cat = Frame(root, width=210, height=150, bg=bGround)
# End of window creation ---------------------

# To create buttons with the categories dictionary
radio_var = StringVar()
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
        [image] BLOB,
        [side_note] TEXT,
        [category] VARCHAR(250)
    )"""
)

conn.commit()
cursor.close()
conn.close()

insert = """ INSERT INTO ideas (image, side_note, category) VALUES (?, ?, ?) """
# End of database ----------------------------

# Always at the end
root.mainloop()
