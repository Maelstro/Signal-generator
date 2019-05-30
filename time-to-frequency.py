#Generates FFT from file

import numpy as np
import scipy as s
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        # Define frame
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky='nsew')
        menu = tk.Menu(frame)
        menu.add_command(label="Open file", command=self.calculate)
        menu.add_command(label="Help", command=lambda: self.help_popup)
        self.config(menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.callback)

    def callback(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            tk.sys.exit()

    def calculate(self):
        filename = tk.filedialog.askopenfilename(initialdir="/home/maelstro", title="Select file", filetypes=(("Text files","*.txt"), ("All files", "*.*")))
        signal = np.loadtxt(filename)
        fsHz = len(signal)
        transformed = np.fft.fft(signal, fsHz)/fsHz
        magTransformed = abs(transformed)
        faxis = np.linspace(-fsHz/2, fsHz/2, fsHz)
        plt.plot(faxis, np.fft.fftshift(magTransformed))
        plt.grid()
        plt.show()

if __name__ == '__main__':
    app = Window()
    app.title("FFT generator")
    app.geometry("1024x768")
    app.mainloop()