# resources used:
# https://www.geeksforgeeks.org/python-gui-tkinter/
# https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
# code from seth

# helpful for plotting:
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/update-a-graph-in-real-time
# https://learn.sparkfun.com/tutorials/graph-sensor-data-with-python-and-matplotlib/speeding-up-the-plot-animation


# Used for creating the GUI (buttons, scrollbars, etc)(This doesn't let you plot things)
import tkinter as tk
from functools import partial

# TODO: remove if not used
# Used to plot things
import matplotlib
matplotlib.use("TkAgg")     # backend of matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# from Seth for the BLE communication
from wearable_api import BLE

global notifications, ble
ble = BLE()
# hold over from Seth's code (can be used to find the number of notifications per second)
# TODO: remove this later if it isn't used
notifications = 0
sleep_time = 5

FONT = ("Verdana", 14)

class FMG_gui(tk.Tk):

    # Sets the structure to contain 'frames' for each page of the GUI
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self,default="clienticon.ico")
        tk.Tk.wm_title(self,"Force Myography")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {};

        for F in (StartPage, Julia, Bren, Matt):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=FONT)
        label.pack(pady=10, padx=10)

        # create button which is used to connect to wearable using BLE
        btnConn = tk.Button(self, text='Connect to Wearable Device', command=partial(connect_ble, ble))
        btnConn.pack()

        # create button which is used to disconnect from wearable
        btnDisConn = tk.Button(self, text='Disconnect from Wearable Device', command=partial(disconnect_ble, ble))
        btnDisConn.pack()

        # Create buttons to show other pages in GUI
        btnJulia = tk.Button(self, text="Visit Julia's Value Added", command=partial(controller.show_frame, Julia))
        btnJulia.pack()
        btnBren = tk.Button(self, text="Visit Brendan's Value Added", command=partial(controller.show_frame, Bren))
        btnBren.pack()
        btnMatt = tk.Button(self, text="Visit Matthew's Value Added", command=partial(controller.show_frame, Matt))
        btnMatt.pack()


class Julia(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Calibration and Classification for FMG signals", font=FONT)
        label.pack(pady=10, padx=10)

        btnBack = tk.Button(self, text="Back to Start Page", command=partial(controller.show_frame, StartPage))
        btnBack.pack()


class Bren(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Training Game", font=FONT)
        label.pack(pady=10, padx=10)

        btnBack = tk.Button(self, text="Back to Start Page", command=partial(controller.show_frame, StartPage))
        btnBack.pack()

class Matt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BLE Mouse", font=FONT)
        label.pack(pady=10, padx=10)

        btnBack = tk.Button(self, text="Back to Start Page", command=partial(controller.show_frame, StartPage))
        btnBack.pack()

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""

    print( BLE.format_notification_data(data) )
    notifications += 1


def connect_ble(ble):

    print('The function to connect to BLE has been called upon')

    address = "00:A0:50:81:22:E0"       # this address is constant (therefore hardcoded)
    connected = ble.connect(address)    # connect to wearable device

    if not connected:
        print("Failed to connect to the wearable device")
    # Start Force and IMU notifications
    ble.enable_notifications(BLE.DATA_CHARACTERISTIC_UUID, notification_handler)


def disconnect_ble(ble):
    # Stop receiving the notifications
    ble.disable_notifications(BLE.DATA_CHARACTERISTIC_UUID)

    # At the end of this file the wearable will automatically disconnect (after the timeout period) or we can call ble.disconnect()
    ble.disconnect()

    print(f'Successfully disconnected from wearable device')


# fig = Figure(figsize = (5,5), dpi=100)
# sub = fig.add_subplot(111)                  # 1-by-1, and chart # 1
# canvas = FigureCanvasTkAgg(fig, master=wndw)

app = FMG_gui()
app.mainloop()

