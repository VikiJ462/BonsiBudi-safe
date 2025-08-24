import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random
import os

# Fun facts
fun_facts = [
    "Bananas are berries, but strawberries aren't.",
    "Sharks existed before trees.",
    "Octopuses have three hearts.",
    "Sloths can hold their breath longer than dolphins.",
    "A day on Venus is longer than a year on Venus."
]

# Hlavní okno
root = tk.Tk()
root.title("BonziBuddy")
root.geometry("400x500")
root.config(bg="white")

canvas = tk.Canvas(root, width=400, height=500, bg="white", highlightthickness=0)
canvas.pack()

# --- GIF animace ---
gif = Image.open("animation.gif")
frames = [ImageTk.PhotoImage(frame.copy().resize((200, 200))) for frame in ImageSequence.Iterator(gif)]
gif_index = 0
gif_item = canvas.create_image(200, 300, image=frames[0])

def animate_gif():
    global gif_index
    gif_index = (gif_index + 1) % len(frames)
    canvas.itemconfig(gif_item, image=frames[gif_index])
    if root_running[0]:  # kontrola, jestli ještě jede root
        root.after(100, animate_gif)

# --- Po skončení gifu zobrazí Bonziho ---
menu_frame = None
fact_label = None
bonzi = None
bonzi_img = None

def show_bonzi():
    global bonzi, bonzi_img
    canvas.delete("all")

    img = Image.open("BonziBuddy.png")
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    bonzi_img = ImageTk.PhotoImage(img)
    bonzi = canvas.create_image(200, 300, image=bonzi_img)

    # Kliknutí na Bonziho = menu
    canvas.tag_bind(bonzi, "<Button-1>", show_menu)

# --- Menu / Fun facts / Note ---
def show_menu(event):
    global menu_frame, fact_label
    if menu_frame:
        menu_frame.destroy()
        menu_frame = None
    if fact_label:
        fact_label.destroy()
        fact_label = None

    menu_frame = tk.Frame(root, bg="lightgray", bd=2, relief="raised")
    # správná pozice – relativně k hlavnímu oknu
    menu_frame.place(x=event.x_root - root.winfo_rootx(),
                     y=event.y_root - root.winfo_rooty())

    fun_fact_btn = tk.Button(menu_frame, text="Tell me a fun fact", command=show_fun_fact)
    fun_fact_btn.pack(fill="x")

    note_btn = tk.Button(menu_frame, text="Make a note", command=make_note)
    note_btn.pack(fill="x")

def show_fun_fact():
    global fact_label, menu_frame
    if menu_frame:
        menu_frame.destroy()
    menu_frame = None
    fact = random.choice(fun_facts)
    fact_label = tk.Label(root, text=fact, bg="yellow", wraplength=300, font=("Arial", 10, "bold"))
    fact_label.place(x=50, y=100)

def make_note():
    global menu_frame
    if menu_frame:
        menu_frame.destroy()
    menu_frame = None
    with open("Note.txt", "w") as f:
        f.write("This is your note! Write something here :)")
    messagebox.showinfo("Note created", "File 'Note.txt' has been created!")

def close_menu_or_fact(event):
    global menu_frame, fact_label

    # Pokud klik byl na Bonziho → ignoruj (menu má zůstat)
    if bonzi is not None and canvas.find_withtag("current") == (bonzi,):
        return

    if menu_frame:
        if not (menu_frame.winfo_rootx() < event.x_root < menu_frame.winfo_rootx() + menu_frame.winfo_width() and
                menu_frame.winfo_rooty() < event.y_root < menu_frame.winfo_rooty() + menu_frame.winfo_height()):
            menu_frame.destroy()
            menu_frame = None

    if fact_label:
        if not (fact_label.winfo_rootx() < event.x_root < fact_label.winfo_rootx() + fact_label.winfo_width() and
                fact_label.winfo_rooty() < event.y_root < fact_label.winfo_rooty() + fact_label.winfo_height()):
            fact_label.destroy()
            fact_label = None

root.bind("<Button-1>", close_menu_or_fact)

# --- Start animace ---
root_running = [True]
animate_gif()
root.after(1000, show_bonzi)  # po 1s se zobrazí BonziBuddy.png

def on_close():
    root_running[0] = False
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
