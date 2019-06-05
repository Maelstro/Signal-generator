# Import libraries + set graphical interface of matplotlib
import numpy as np
import tkinter as tk
from tkinter import *
from scipy import signal

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import os


# Graphical interface
class SigGen(tk.Tk):
    params = []
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        # Define frame
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky='nsew')
        # Define listbox
        lb = tk.Listbox(frame)
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        lb.grid(row=0, column=0, sticky="nsew")
        # Define plotting space
        frame.canvasFig = plt.figure(1)
        fig = matplotlib.figure.Figure(dpi=100)
        fig_subplot = fig.add_subplot(111)
        self.line1, = fig_subplot.plot(0, 0, 'r-')
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=frame)
        self.plot_widget = self.canvas.get_tk_widget()
        tk.Grid.columnconfigure(frame, 1, weight=1)
        tk.Grid.rowconfigure(frame, 0, weight=1)
        self.plot_widget.grid(row=0, column=1, rowspan=2, sticky="nsew")
        for item in ["Sine wave", "White noise", "Constant", "Square wave", "Sine with white noise", "Mixed signal"]:
            lb.insert(tk.END, item)
        # Define widget for data insertion
        global parameter_frame
        parameter_frame = tk.Frame(frame)
        parameter_frame.grid(row=1, column=0, sticky='nsew')
        self.update()
        # Bind functions to buttons/window
        lb.bind("<Double-Button-1>", self.OnDouble)
        self.protocol("WM_DELETE_WINDOW", self.callback)

    def OnDouble(self, event):
        for wid in parameter_frame.winfo_children():
            wid.destroy()
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        self.params = []
        self.params.append(self.make_entry(parameter_frame, "Number of samples", 0, 0))
        # Signal selector
        if value == "Sine wave":
            self.params.append(self.make_entry(parameter_frame, "Amplitude", 1, 0))
            self.params.append(self.make_entry(parameter_frame, "Frequency", 2, 0))
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.get_parameter("Sine"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "White noise":
            self.params.append(self.make_entry(parameter_frame, "Mean", 1, 0))
            self.params.append(self.make_entry(parameter_frame, "Standard Deviation", 2, 0))
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.get_parameter("White Noise"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "Constant":
            global constant
            self.params.append(self.make_entry(parameter_frame, "Constant value", 1, 0))
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.get_parameter("Constant"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "Square wave":
            self.params.append(self.make_entry(parameter_frame, "Amplitude", 1, 0))
            self.params.append(self.make_entry(parameter_frame, "Frequency", 2, 0))
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.get_parameter("Square"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "Sine with white noise":
            self.params.append(self.make_entry(parameter_frame, "Amplitude", 1, 0))
            self.params.append(self.make_entry(parameter_frame, "Frequency", 2, 0))
            self.params.append(self.make_entry(parameter_frame, "Mean", 3, 0))
            self.params.append(self.make_entry(parameter_frame, "Standard Deviation", 4, 0))
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.get_parameter("Sine with noise"))
            button.grid(row=5, columnspan=2)
            self.update()
        elif value == "Mixed signal":
            global amp2, freq2
            self.params.append(self.make_entry(parameter_frame, "Amplitude of first sine", 1, 0))
            self.params.append(self.make_entry(parameter_frame, "Frequency of first sine", 2, 0))
            self.params.append(self.make_entry(parameter_frame, "Amplitude of second sine", 3, 0))
            self.params.append(self.make_entry(parameter_frame, "Frequency of second sine", 4, 0))
            self.params.append(self.make_entry(parameter_frame, "Mean", 5, 0))
            self.params.append(self.make_entry(parameter_frame, "Standard Deviation", 6, 0))
            self.params.append(self.make_entry(parameter_frame, "Constant value", 7, 0))
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.get_parameter("Mixed"))
            button.grid(row=8, columnspan=2)
            self.update()

    def refreshFig(self, x, y):
        self.line1.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min() - 1, y.max() + 1)
        ax.grid(self)
        self.canvas.draw()

    def callback(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            sys.exit()

    def get_parameter(self, funct):
        parameters = []
        for item in self.params:
            parameters.append(float(item.get()))
        samples = int(parameters[0])
        rng = np.arange(samples)
        if funct == "Sine":
            y = parameters[1] * np.sin(2 * np.pi * parameters[2] * (rng / parameters[0]))
            plt.plot(y)
            self.refreshFig(rng, y)
        elif funct == "White Noise":
            y = np.random.normal(parameters[1], parameters[2], size=int(parameters[0]))
            plt.plot(y)
            self.refreshFig(rng, y)
        elif funct == "Constant":
            val = float(parameters[1])
            y = val * np.heaviside(rng, 1)
            plt.plot(y)
            self.refreshFig(rng, y)
        elif funct == "Square":
            rng = np.linspace(0, 1, samples, endpoint=False)
            y = parameters[1] * signal.square(2 * np.pi * parameters[2] * rng)
            plt.plot(rng, y)
            self.refreshFig(rng, y)
        elif funct == "Sine with noise":
            y = parameters[1] * np.sin(2 * np.pi * parameters[2] * (rng / parameters[0]))\
                + np.random.normal(parameters[3], parameters[4], size=samples) + 0.5
            plt.plot(y)
            self.refreshFig(rng, y)
        elif funct == "Mixed":
            step = rng/parameters[0]
            y = parameters[1] * np.sin(2 * np.pi * parameters[2] * step) \
                + parameters[3] * np.sin(2 * np.pi * parameters[4] * step) \
                + np.random.normal(parameters[5], parameters[6], size=samples) + parameters[7]
            plt.plot(y)
            self.refreshFig(rng, y)
        i = 0
        if sys.platform == "linux":
            while os.path.exists("/home/maelstro/signals/generated_signal_%s.txt" % i):
                i += 1
            # Swap 'maelstro' with your  name if required
            file_name = ("/home/maelstro/signals/generated_signal_%s.txt" % i)
            np.savetxt(file_name, y, newline='\n')
        elif sys.platform == "win32":
            while os.path.exists("C:\signals\generated_signal_%s.txt" % i):
                i += 1
            file_name = ("C:\signals\generated_signal_%s.txt" % i)
            np.savetxt(file_name, y, newline='\n')

    # Entry constructor
    def make_entry(self, parent, text, row, column):
        par_label = tk.Label(parent, text=text)
        par_label.grid(row=row, column=column, sticky='w')
        parameter = tk.Entry(parent)
        parameter.grid(row=row, column=column+1, sticky='e')
        return parameter

if __name__ == "__main__":
    # Graphical main loop
    app = SigGen()
    app.title("Signal generator")
    app.geometry("1024x768")
    app.mainloop()
