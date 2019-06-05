#Generates FFT from file

import numpy as np
import scipy as sc
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
        menu.add_command(label="Help", command=self.help_popup)
        self.config(menu=menu)
        self.protocol("WM_DELETE_WINDOW", self.callback)
        # Define figure
        frame.canvasFig = plt.figure(1)
        fig = matplotlib.figure.Figure(dpi=100)
        fig_subplot = fig.add_subplot(111)
        self.line1, = fig_subplot.plot(0, 0, 'r-')
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=frame)
        self.plot_widget = self.canvas.get_tk_widget()
        tk.Grid.columnconfigure(frame, 1, weight=1)
        tk.Grid.rowconfigure(frame, 0, weight=1)
        self.plot_widget.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.update()


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
        faxis = np.linspace(0, fsHz/2, fsHz/2)
        finalFFT = np.fft.fftshift(magTransformed)
        plt.plot(faxis, finalFFT[int(fsHz/2):int(fsHz)])
        self.refresh_fig(faxis, finalFFT[int(fsHz/2):int(fsHz)])

    def refresh_fig(self, x, y):
        self.line1.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min() - 1, y.max() + 1)
        ax.grid(self)
        self.canvas.draw()

    def help_popup(self):
        tk.messagebox.showinfo("Help", "Window in creation...")

if __name__ == '__main__':
    app = Window()
    app.title("FFT generator")
    app.geometry("1024x768")
    app.mainloop()