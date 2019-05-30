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
        global samp
        samp_label = tk.Label(parameter_frame, text="Number of samples")
        samp_label.grid(row=0, column=0, sticky='w')
        samp = tk.Entry(parameter_frame)
        samp.grid(row=0, column=1, sticky='e')
        # Signal selector
        if value == "Sine wave":
            global amp, freq
            amp_label = tk.Label(parameter_frame, text="Amplitude")
            amp_label.grid(row=1, column=0, sticky='w')
            amp = tk.Entry(parameter_frame)
            amp.grid(row=1, column=1, sticky='e')
            freq_label = tk.Label(parameter_frame, text='Frequency')
            freq_label.grid(row=2, column=0, sticky='w')
            freq = tk.Entry(parameter_frame)
            freq.grid(row=2, column=1, sticky='e')
            button = tk.Button(parameter_frame, text='Generate & write to file', command=lambda: self.getParameter("Sine"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "White noise":
            global mean, std
            mean_label = tk.Label(parameter_frame, text="Mean")
            mean_label.grid(row=1, column=0, sticky='w')
            mean = tk.Entry(parameter_frame)
            mean.grid(row=1, column=1, sticky='e')
            std_label = tk.Label(parameter_frame, text='Standard Deviation')
            std_label.grid(row=2, column=0, sticky='w')
            std = tk.Entry(parameter_frame)
            std.grid(row=2, column=1, sticky='e')
            button = tk.Button(parameter_frame, text='Generate & write to file', command=lambda: self.getParameter("White Noise"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "Constant":
            global constant
            const_label = tk.Label(parameter_frame, text="Constant value")
            const_label.grid(row=1, column=0, sticky='w')
            constant = tk.Entry(parameter_frame)
            constant.grid(row=1, column=1, sticky='e')
            button = tk.Button(parameter_frame, text='Generate & write to file', command=lambda: self.getParameter("Constant"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "Square wave":
            amp_label = tk.Label(parameter_frame, text="Amplitude")
            amp_label.grid(row=1, column=0, sticky='w')
            amp = tk.Entry(parameter_frame)
            amp.grid(row=1, column=1, sticky='e')
            freq_label = tk.Label(parameter_frame, text='Frequency')
            freq_label.grid(row=2, column=0, sticky='w')
            freq = tk.Entry(parameter_frame)
            freq.grid(row=2, column=1, sticky='e')
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.getParameter("Square"))
            button.grid(row=3, columnspan=2)
            self.update()
        elif value == "Sine with white noise":
            amp_label = tk.Label(parameter_frame, text="Amplitude")
            amp_label.grid(row=1, column=0, sticky='w')
            amp = tk.Entry(parameter_frame)
            amp.grid(row=1, column=1, sticky='e')
            freq_label = tk.Label(parameter_frame, text='Frequency')
            freq_label.grid(row=2, column=0, sticky='w')
            freq = tk.Entry(parameter_frame)
            freq.grid(row=2, column=1, sticky='e')
            mean_label = tk.Label(parameter_frame, text="Mean")
            mean_label.grid(row=3, column=0, sticky='w')
            mean = tk.Entry(parameter_frame)
            mean.grid(row=3, column=1, sticky='e')
            std_label = tk.Label(parameter_frame, text='Standard Deviation')
            std_label.grid(row=4, column=0, sticky='w')
            std = tk.Entry(parameter_frame)
            std.grid(row=4, column=1, sticky='e')
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.getParameter("Sine with noise"))
            button.grid(row=5, columnspan=2)
            self.update()
        elif value == "Mixed signal":
            global amp2, freq2
            amp_label = tk.Label(parameter_frame, text="Amplitude of first sine")
            amp_label.grid(row=1, column=0, sticky='w')
            amp = tk.Entry(parameter_frame)
            amp.grid(row=1, column=1, sticky='e')
            freq_label = tk.Label(parameter_frame, text='Frequency of first sine')
            freq_label.grid(row=2, column=0, sticky='w')
            freq = tk.Entry(parameter_frame)
            freq.grid(row=2, column=1, sticky='e')
            amp2_label = tk.Label(parameter_frame, text="Amplitude of second sine")
            amp2_label.grid(row=3, column=0, sticky='w')
            amp2 = tk.Entry(parameter_frame)
            amp2.grid(row=3, column=1, sticky='e')
            freq2_label = tk.Label(parameter_frame, text='Frequency of second sine')
            freq2_label.grid(row=4, column=0, sticky='w')
            freq2 = tk.Entry(parameter_frame)
            freq2.grid(row=4, column=1, sticky='e')
            mean_label = tk.Label(parameter_frame, text="Mean")
            mean_label.grid(row=5, column=0, sticky='w')
            mean = tk.Entry(parameter_frame)
            mean.grid(row=5, column=1, sticky='e')
            std_label = tk.Label(parameter_frame, text='Standard Deviation')
            std_label.grid(row=6, column=0, sticky='w')
            std = tk.Entry(parameter_frame)
            std.grid(row=6, column=1, sticky='e')
            const_label = tk.Label(parameter_frame, text="Constant value")
            const_label.grid(row=7, column=0, sticky='w')
            constant = tk.Entry(parameter_frame)
            constant.grid(row=7, column=1, sticky='e')
            button = tk.Button(parameter_frame, text='Generate & write to file',
                               command=lambda: self.getParameter("Mixed"))
            button.grid(row=8, columnspan=2)
            self.update()

    def refreshFig(self, x, y):
        self.line1.set_data(x, y)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(y.min()-1, y.max()+1)
        ax.grid(self)
        self.canvas.draw()

    def callback(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            sys.exit()

    def getParameter(self, funct):
        if funct == "Sine":
            A = float(amp.get())
            f = float(freq.get())
            samples = int(samp.get())
            rng = np.arange(samples)
            y = A * np.sin(2 * np.pi * f * (rng / samples))
            plt.plot(y)
            self.refreshFig(rng, y)
        elif funct == "White Noise":
            M = float(mean.get())
            sigma = float(std.get())
            samples = int(samp.get())
            y = np.random.normal(M, sigma, size=samples)
            smp = np.arange(samples)
            plt.plot(y)
            self.refreshFig(smp, y)
        elif funct == "Constant":
            val = float(constant.get())
            samples = int(samp.get())
            smp = np.arange(samples)
            y = val*np.heaviside(smp, 1)
            plt.plot(y)
            self.refreshFig(smp, y)
        elif funct == "Square":
            A = float(amp.get())
            f = float(freq.get())
            samples = int(samp.get())
            rng = np.linspace(0, 1, samples, endpoint=False)
            y = A * signal.square(2 * np.pi * f * rng)
            plt.plot(rng, y)
            self.refreshFig(rng, y)
        elif funct == "Sine with noise":
            A = float(amp.get())
            f = float(freq.get())
            samples = int(samp.get())
            rng = np.arange(samples)
            M = float(mean.get())
            sigma = float(std.get())
            y = A * np.sin(2 * np.pi * f * (rng / samples)) + np.random.normal(M, sigma, size=samples)
            plt.plot(y)
            self.refreshFig(rng, y)
        elif funct == "Mixed":
            A1 = float(amp.get())
            f1 = float(freq.get())
            A2 = float(amp2.get())
            f2 = float(freq2.get())
            val = float(constant.get())
            samples = int(samp.get())
            rng = np.arange(samples)
            M = float(mean.get())
            sigma = float(std.get())
            y = A1 * np.sin(2 * np.pi * f1 * (rng / samples)) + A2 * np.sin(2 * np.pi * f2 * (rng / samples)) \
                + np.random.normal(M, sigma, size=samples) + val
            plt.plot(y)
            self.refreshFig(rng, y)
        i = 0
        while os.path.exists("/home/maelstro/signals/generated_signal_%s.txt" % i):
            i += 1
        # Swap 'maelstro' with your  name if required
        file_name = ("/home/maelstro/signals/generated_signal_%s.txt" % i)
        np.savetxt(file_name, y, newline='\n')

if __name__ == "__main__":
    # Graphical main loop
    app = SigGen()
    app.title("Signal generator")
    app.geometry("1024x768")
    app.mainloop()
