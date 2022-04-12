"""from tkinter import *

top = Tk()
top.title('Stable mariage solver')
window_width = 300
window_height = 200

# get the screen dimension
screen_width = top.winfo_screenwidth()
screen_height = top.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
top.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

L1 = Label(top, text="HI")
L1.pack( side = LEFT)
E1 = Entry(top, bd =5)
E1.pack(side = RIGHT)
B=Button(top, text ="Hello",)
B.pack()
top.mainloop()"""

"""from tkinter import *


def return_pressed(event):
    print('Return key pressed.')


root = Tk()

btn = Button(root, text='Genarate instance')
btn.bind('<Button>', return_pressed)
E1 = Entry(root, bd =5)
E1.pack(side = RIGHT)
L1 = Label(root, text="male")
L1.pack( side = RIGHT)

btn.focus()
btn.pack(expand=True)

root.mainloop()"""
import tkinter as tk
from tkinter import ttk


class InputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)

        self.__create_widgets()

    def __create_widgets(self):
        # Find what
        ttk.Label(self, text='Generate instance:').grid(column=0, row=0, sticky=tk.W)
        keyword1 = ttk.Entry(self, width=5)
        keyword1.focus()
        keyword1.grid(column=1, row=0, sticky=tk.W)
        keyword2 = ttk.Entry(self, width=5)
        T1 = ttk. Label(self, text="Male").grid(column=2, row=0, sticky=tk.W)
        keyword2.focus()
        keyword2.grid(column=3, row=0, sticky=tk.W)
        T2 = ttk. Label(self, text="Female").grid(column=4, row=0, sticky=tk.W)


        # Match Case checkbox
        match_case = tk.StringVar()
        match_case_check = ttk.Checkbutton(
            self,
            text='Match case',
            variable=match_case,
            command=lambda: print(match_case.get()))
        match_case_check.grid(column=0, row=2, sticky=tk.W)

        # Wrap Around checkbox
        wrap_around = tk.StringVar()
        wrap_around_check = ttk.Checkbutton(
            self,
            variable=wrap_around,
            text='Wrap around',
            command=lambda: print(wrap_around.get()))
        wrap_around_check.grid(column=0, row=3, sticky=tk.W)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=5)


class ButtonFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        ttk.Button(self, text='Generate instance').grid(column=0, row=0)
        ttk.Button(self, text='Replace').grid(column=0, row=1)
        ttk.Button(self, text='Replace All').grid(column=0, row=2)
        ttk.Button(self, text='Cancel').grid(column=0, row=3)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=3)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Replace')
        self.geometry('600x200')
        self.resizable(0, 0)
        # windows only (remove the minimize/maximize button)
        #self.attributes('-toolwindow', True)

        # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # create the input frame
        input_frame = InputFrame(self)
        input_frame.grid(column=0, row=0)

        # create the button frame
        button_frame = ButtonFrame(self)
        button_frame.grid(column=1, row=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
