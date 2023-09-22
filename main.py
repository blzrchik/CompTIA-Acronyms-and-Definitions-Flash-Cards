import os
import pandas
import tkinter as tk
import traceback  # Import the traceback module for detailed error information
import random
from tkinter import *
import pandas as pd

# Background Image Path
BACKGROUND_COLOR = "#B1DDC6"

to_learn = {}
current_card = {}


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()


# Function to load the word list and update total_word_count
def load_word_list():
    global to_learn


# Check if the file exists
if not os.path.exists("data/words_to_learn.csv"):
    # If it doesn't exist, create it and populate it with all words from core1_acronyms.csv
    original_data = pd.read_csv("data/core1_acronyms.csv")
    original_data.to_csv("data/words_to_learn.csv", index=False)

# Load the words to learn
to_learn = pd.read_csv("data/words_to_learn.csv").to_dict(orient="records")
try:
        data = pandas.read_csv("data/words_to_learn.csv")
        to_learn = data.to_dict(orient="records")
    # total_word_count = len(to_learn)  # Update total_word_count based on loaded data
except FileNotFoundError:
    original_data = pandas.read_csv("data/core1_acronyms.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
    
original_data = pd.read_csv("data/core1_acronyms.csv")
# Get the count of words
word_count = len(original_data)

# Rest of your code...
score = 0
is_showing_definition = False

# ------------------------ Generating an Acronym ----------

# Rest of code for removing the card and displaying the next card


def is_known():
    global current_card, score
    if current_card in to_learn:
        to_learn.remove(current_card)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    # Commenting out if else here to test run
    # if is_showing_definition:
    #  card_text = current_card["Definition"]
    # card_title_text = "Definition"
    # else:
    #  card_text = current_card["Term"]
    # card_title_text = "Term"
    update_score(1)
    next_card()


def next_card():
    global current_card, score, is_showing_definition
    current_card = random.choice(to_learn)

        # Commenting out if else here to test run if is_showing_definition:
        # card_text = current_card["Definition"]
        #  card_title_text = "Definition"
        #  is_showing_definition = True
        
        # else:
        # card_text = current_card["Term"]
        # card_title_text = "Term"

    # core1_acronym = random_pair['Term']
    # canvas.itemconfig(card_title, text="Term", fill="black")
    canvas.itemconfig(card_word, text=current_card["Term"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

    
def show_answer():
    try:
        global is_showing_definition
        if is_showing_definition:
            # If currently showing Definition, switch back to Acronym
            canvas.itemconfig(card_title, text="Term", fill="black")
            canvas.itemconfig(card_word, text=current_card["Term"], fill="black")
            card_text = current_card["Term"]
            canvas.itemconfig(card_background, image=card_front_img)
            is_showing_definition = False
        else:
            # Otherwise, switch to Definition
            canvas.itemconfig(card_title, text="Definition", fill="black")
            canvas.itemconfig(card_word, text=current_card["Definition"], fill="black")
            card_text = current_card["Definition"]
            canvas.itemconfig(card_background, image=card_back_img)
            is_showing_definition = True

        
    except Exception as e:
        # Handle the exception here, log it, and provide additional information if needed
        error_message = str(e)
        traceback_info = traceback.format_exc()
        print(f"Error in show_answer(): {error_message}")
        print(f"Traceback:\n{traceback_info}")

    is_showing_definition = not is_showing_definition

    # Print the value of is_showing_definition for debugging
    print("is_showing_definition:", is_showing_definition)

# Calculate the maximum width and height for the text on the card
    max_width = 600  # Adjust this value based on your card dimensions
    max_height = 400  # Adjust this value based on your card dimensions
    
    # Start with a reasonable font size for the Definition side
    font_size = 24
    
    # Create a font with the calculated size
    font = f"Arial {font_size} bold"
    
    # Measure the text size with the current font
    text_width, text_height = canvas.bbox(card_word)[2], canvas.bbox(card_word)[3]
    
    # Decrease the font size until it fits within the max dimensions
    while text_width > max_width or text_height > max_height:
        font_size -= 1
        font = f"Arial {font_size} bold"
        canvas.itemconfig(card_word, font=font)  # Update the font
        
        text_width, text_height = canvas.bbox(card_word)[2], canvas.bbox(card_word)[3]
    
    # Update the card's text and font on click
    canvas.itemconfig(card_word, text=card_text, font=font, fill="black")
    
    # Toggle the showing state for the next click
    is_showing_definition = not is_showing_definition

def flip_card():
    global is_showing_definition
    if is_showing_definition:
        canvas.itemconfig(card_title, text = "Definition", fill = "black")
        canvas.itemconfig(card_word, text=current_card["Definition"], fill = "black")
        canvas.itemconfig(card_background, image=card_back_img)
    else:
        canvas.itemconfig(card_title, text="Term", fill="black")
        canvas.itemconfig(card_word, text=current_card["Term"], fill="black")
        # card_text = current_card["Term"]
        canvas.itemconfig(card_background, image=card_front_img)
    is_showing_definition = not is_showing_definition
#------------------------ FlashCard UI Setup -------------------------------

window = Tk()
window.title("CompTIA A+ Flashcards")
# Create a menu bar
menu_bar = Menu(window)
window.config(menu=menu_bar)

# Create a "File" menu with a submenu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add items to the "File" submenu
#file_menu.add_command(label="Open", command=menu_action)
#file_menu.add_command(label="Save", command=menu_action)
#file_menu.add_separator()  # Add a separator line
#file_menu.add_command(label="Exit", command=window.quit)

# Create a "Categories" menu with a submenu
categories_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Categories", menu=categories_menu)

# Add items to the "Categories" submenu
#categories_menu.add_command(label="Ports", command=menu_action)
#categories_menu.add_command(label="Acronyms", command=menu_action)

# Create a "Help" menu
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Add an item to the "Help" menu
#help_menu.add_command(label="About", command=menu_action)

window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(window, width=800, height=560)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
# Positions are related to canvas so 400 will be halfway in width
canvas.config (bg=BACKGROUND_COLOR, highlightthickness=0)
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"), tags="word")
# canvas should go in the middle
instruction_text = "Click the card to flip"
canvas.create_text(400, 470, text=instruction_text, font=("Ariel", 16, "italic"), fill="gray")

canvas.bind("<Button-1>", lambda event: show_answer())
canvas.grid(row=0, column=0, columnspan=3)
#score_display = canvas.create_text(650, 50, text=f"Score: {score}", font=("Ariel", 24, "bold"))


def update_score(change=None):
    global score, score_label
    if change is not None:
        score+= change
    score_label.config(text=f"Score: {score}/{word_count}")

    # Create a label to display the score
score_label = Label(text=f"Score: 0/{word_count}", font=("Ariel", 20), bg=BACKGROUND_COLOR)
#score_label.place(x=400, y=20)
score_label.grid(row=3, column=0, columnspan=3)  # Adjust the column and row as needed



cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, command = next_card)
unknown_button.grid(row=1, column=0, sticky="W")

# Add a tooltip to the "wrong" button
tooltip = Tooltip(unknown_button, "If you don't know the answer click here.")

check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, command=is_known)
known_button.grid(row=1, column=2, sticky="E")

# Add a tooltip to the "right" button
tooltip = Tooltip(known_button, "If you got it right click here.")

#show_answer_button = Button(text="Show Answer", font=("Ariel", 16), command=show_answer, bg="#d4d4d4", activebackground="#c4c4c4")
#show_answer_button.grid(row=1, column=2)

# Replace 'skip_button_image_path' with the actual path to your skip button image
skip_button_image_path = "./images/next.png"  # Example path

# Load the image
skip_button_image = PhotoImage(file=skip_button_image_path)

skip_button = Button(image=skip_button_image, command=next_card)
skip_button.grid(row=1, column=1, sticky="N")  # Adjust the row and column if needed


# Add a tooltip to the "skip" button
tooltip = Tooltip(skip_button, "Skip to the next card.")



next_card()
window.mainloop()