import tkinter
from tkinter import ttk

import numpy as np
import matplotlib as plt
import matplotlib.pyplot as pltpy
from sympy import poly
import ipywidgets

plt.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasAgg, FigureCanvasTkAgg, NavigationToolbar2Tk

# plt.backend_bases.NavigationToolbar2.toolitems = (
#     ('Home', 'Reset original view', 'home', 'home'),
#     ('Back', 'Back to  previous view', 'back', 'back'),
#     ('Forward', 'Forward to next view', 'forward', 'forward'),
#     (None, None, None, None),
#     ('Save', 'Save the figure', 'filesave', 'save_figure'),
# )
#


# window
window = tkinter.Tk()
window.title("Grapher")
window.geometry('600x600+100+100')

# Create a figure 
f = pltpy.figure(figsize = (5,5), dpi = 100)
plot = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f, master = window)


width = window.winfo_width()
lim = plot.get_xlim()
xAll = np.linspace(lim, width)
coeff = []



# graph function
def graph():
    # ipywidgets.interact(drawGraph, a = entryString.get(),zoom = (1, 10, 1))
    drawGraph(entryString.get())

def PolyCoefficients(x, coeffs):
    """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

    The coefficients must be in ascending order (``x**0`` to ``x**o``).
    """
    o = len(coeffs)
    # print(f'# This is a polynomial of order {o}.')
    y = 0
    for i in range(o):
        y += coeffs[i]*x**i
    return y

# draws a matplot graph of the given function
def zoom_factory(ax,base_scale = 2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        # set the range
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale

        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
        # set new limits
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])

        lim = plot.get_xlim()
        width = window.winfo_width()

        plotter(lim, width)


    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun

def pan_factory(ax):
    def onPress(event):
        global pressed
        pressed = True

    def onMotion(event):
        if pressed:
            lim = plot.get_xlim()
            width = window.winfo_width()
            plotter(lim, width)
            #return the function
        
    def onRelease(event):
        global pressed
        pressed = False

    fig = ax.get_figure() # get the figure of interest

    # attach the call back
    fig.canvas.mpl_connect('button_press_event',onPress)
    fig.canvas.mpl_connect('button_release_event',onRelease)
    fig.canvas.mpl_connect('motion_notify_event',onMotion)

pressed = False
def plotter(lim, width):
    global xAll
    xAll = np.linspace(lim[0] - 10, lim[1] + 10, width)

    plot.cla()
    plot.plot(xAll, PolyCoefficients(xAll, coeff))
    plot.grid()
    
    canvas.draw() # force re-draw the next time the GUI refreshes



def drawGraph(a):
    plot.cla()

    a = poly(a)
    global coeff
    coeff = a.all_coeffs()
    coeff = coeff[::-1]

    lim = plot.get_xlim()
    width = window.winfo_width()
    plotter(lim, width)

    ax = plot
    zoom_factory(ax, base_scale = 2)
    pan_factory(ax)

    canvas.draw()
    canvas.get_tk_widget().pack()

    # f.canvas.manager.toolbar.pan()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.pan()
    toolbar.update()

# title
title_font = ("Arial Bold", 50)
title = ttk.Label(window, text="Grapher", font=title_font)
title.pack()

# input field
input_frame = tkinter.Frame(window)
entryString = tkinter.StringVar()
entrypoint = tkinter.Entry(input_frame, width=50, textvariable = entryString)
button = tkinter.Button(input_frame, text="Graph", command = graph)
entrypoint.pack(side = tkinter.LEFT, padx=5) 
button.pack(side = tkinter.LEFT)
input_frame.pack()

# Output
output_font = ("Arial Bold", 20)
output_label = tkinter.Label(window, text="Graph", font=output_font)
output_frame = tkinter.Frame(window)
output_label.pack()
output_frame.pack()

def on_xlims_change(event_x):
    print("WIOWWO")
    drawGraph(entryString.get())

plot.callbacks.connect('xlim_changed', on_xlims_change)

# Run
window.mainloop()
