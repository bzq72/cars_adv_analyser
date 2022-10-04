# Import the required libraries
import tkinter as tk
from tkinter import font
#from adv_browser import Browser
from adv_browser import Browser
from price_predictor import price_predictor

# Create an instance of tkinter frame or window
win = tk.Tk()

# Set the size of the window
win.geometry("880x680")
win.resizable(0, 0)
win.title("Cars Adv Scroller")
        
menubar = tk.Menu(win)
win.config(menu=menubar)
file_menu = tk.Menu(menubar)        
menubar.add_cascade(label = "Help", menu = file_menu)
file_menu.add_command(label='About',command = help)

# Create two frames in the window
greet = tk.Frame(win)
order = tk.Frame(win)
browser = Browser(win)
predictor = price_predictor(win)
buttons = tk.Frame(win)


# Define a function for switching the frames
def change_to_browser():
    predictor.main_frame.destroy()
    browser.__init__(win)
    browser.main_frame.grid(row=1, column=0)

def change_to_predictor():
    browser.main_frame.destroy()
    predictor.__init__(win)
    predictor.main_frame.grid(row=1, column=0)
    
# Create fonts for making difference in the frame
font1 = font.Font(family='Georgia', size='22', weight='bold')
font2 = font.Font(family='Aerial', size='12')

# Add a button to switch between two frames
btn1 = tk.Button(buttons, text="Open adverts browser", font=font2, command=change_to_browser)
btn1.grid(row=0, column=0,ipadx=141)
btn2 = tk.Button(buttons, text="Open price predictor", font=font2, command=change_to_predictor)
btn2.grid(row=0, column=1,ipadx=138)

buttons.grid(row=0, column=0)
change_to_browser()
win.mainloop()