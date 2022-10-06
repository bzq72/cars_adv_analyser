import tkinter as tk
from tkinter import font
from adv_browser import Browser
from price_predictor import Price_Predictor

# Create an instance of tkinter frame or window
win = tk.Tk()

"""Setting main gui window"""
win.geometry("880x680")
win.resizable(0, 0)
win.title("Cars Adv Analyser")
menubar = tk.Menu(win)
win.config(menu=menubar)
file_menu = tk.Menu(menubar)        
menubar.add_cascade(label = "Help", menu = file_menu)
file_menu.add_command(label='About',command = help)


"""Creating objects for side windows"""
browser = Browser(win)
predictor = Price_Predictor(win)

def change_to_browser():
    """switching to brower window"""
    predictor.main_frame.destroy()
    browser.__init__(win)
    browser.main_frame.grid(row=1, column=0)

def change_to_predictor():
    """switching to price predict window"""
    browser.main_frame.destroy()
    predictor.__init__(win)
    predictor.main_frame.grid(row=1, column=0)

"""Creating buttons"""
font1 = font.Font(family='Aerial', size='12')
buttons = tk.Frame(win)
btn1 = tk.Button(buttons, text="Open adverts browser", font=font1, command=change_to_browser)
btn1.grid(row=0, column=0,ipadx=141)
btn2 = tk.Button(buttons, text="Open price predictor", font=font1, command=change_to_predictor)
btn2.grid(row=0, column=1,ipadx=138)
buttons.grid(row=0, column=0)

change_to_browser()
win.mainloop()