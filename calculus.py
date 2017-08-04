import os
import sys
import threading
import win32clipboard
from Tkinter import *
from ttk import *
from sympy import diff, integrate, symbols

letters = [chr(i) for i in range(ord("a"), ord("z") + 1)]

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

class App:
    def __init__(self):
        self.running = True
        self.symbols = symbols(" ".join(letters))
        self.fontSize = 9
        self.padding = 25
        self.root = Tk()
        self.root.title("Calculus")
        self.root.iconbitmap(resource_path(os.path.join("data", "icon.ico")))
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.mainFrame = Frame(self.root)
        self.mainFrame.pack(padx = self.padding, pady = self.padding, expand = True, anchor = CENTER)

        self.derivLabel = Label(self.mainFrame, text = "Derivative", font = (None, 12))
        self.derivLabel.grid(row = 0, column = 1)

        self.derivInputLabel = Label(self.mainFrame, text = "Equation:", font = (None, self.fontSize))
        self.derivInputLabel.grid(row = 1, column = 0, sticky = E)
        self.derivInput = Entry(self.mainFrame)
        self.derivInput.grid(row = 1, column = 1)

        self.derivVarOptionLabel = Label(self.mainFrame, text = "Variable:", font = (None, self.fontSize))
        self.derivVarOptionLabel.grid(row = 2, column = 0, sticky = E)
        self.derivVar = StringVar(self.mainFrame)
        self.derivVarOption = OptionMenu(self.mainFrame, self.derivVar, "", *letters)
        self.derivVar.set("x")
        self.derivVarOption.grid(row = 2, column = 1)

        self.derivTimesLabel = Label(self.mainFrame, text = "Times:", font = (None, self.fontSize))
        self.derivTimesLabel.grid(row = 3, column = 0, sticky = E)
        self.derivTimes = Entry(self.mainFrame)
        self.derivTimes.insert(0, "1")
        self.derivTimes.grid(row = 3, column = 1)

        self.integLabel = Label(self.mainFrame, text = "Integral", font = (None, 12))
        self.integLabel.grid(row = 4, column = 1, pady = (self.padding, 0))

        self.integInputLabel = Label(self.mainFrame, text = "Equation:", font = (None, self.fontSize))
        self.integInputLabel.grid(row = 5, column = 0, sticky = E)
        self.integInput = Entry(self.mainFrame)
        self.integInput.grid(row = 5, column = 1)

        self.integVarOptionLabel = Label(self.mainFrame, text = "Variable:", font = (None, self.fontSize))
        self.integVarOptionLabel.grid(row = 6, column = 0, sticky = E)
        self.integVar = StringVar(self.mainFrame)
        self.integVarOption = OptionMenu(self.mainFrame, self.integVar, "", *letters)
        self.integVar.set("x")
        self.integVarOption.grid(row = 6, column = 1)

        self.integUpperLabel = Label(self.mainFrame, text = "Upper:", font = (None, self.fontSize))
        self.integUpperLabel.grid(row = 7, column = 0, sticky = E)
        self.integUpper = Entry(self.mainFrame)
        self.integUpper.grid(row = 7, column = 1)
        self.integUpperInf = Button(self.mainFrame, text = u"\u221E", command = lambda: self.inf(1))
        self.integUpperInf.grid(row = 7, column = 2)

        self.integLowerLabel = Label(self.mainFrame, text = "Lower:", font = (None, self.fontSize))
        self.integLowerLabel.grid(row = 8, column = 0, sticky = E)
        self.integLower = Entry(self.mainFrame)
        self.integLower.grid(row = 8, column = 1)
        self.integLowerInf = Button(self.mainFrame, text = u"-\u221E", command = lambda: self.inf(0))
        self.integLowerInf.grid(row = 8, column = 2)

        self.derivative = Label(self.mainFrame, text = "", font = (None, 16))
        self.derivative.grid(row = 0, column = 3, rowspan = 4)

        self.integral = Label(self.mainFrame, text = "", font = (None, 16))
        self.integral.grid(row = 4, column = 3, rowspan = 5)

        self.mainFrame.columnconfigure(3, minsize = 500)
        self.mainFrame.columnconfigure(3, weight = 1)

        self.derivCopy = Button(self.mainFrame, text = "Copy", command = lambda: self.copy(self.derivative["text"]))
        self.derivCopy.grid(row = 0, column = 4, rowspan = 4)

        self.integCopy = Button(self.mainFrame, text = "Copy", command = lambda: self.copy(self.integral["text"]))
        self.integCopy.grid(row = 4, column = 4, rowspan = 5)
        
        self.mainthread = threading.Thread(target = self.main)
        self.mainthread.daemon = True
        self.mainthread.start()
        self.root.after(100, self.main)
        self.root.mainloop()

    def main(self):
        derivExp = ""
        integExp = ""
        bounds = ["", ""]
        derivExp = self.derivInput.get()
        if derivExp == "":
            self.derivative.configure(text = "")
        else:
            try:
                ans = diff(derivExp, self.derivVar.get(), self.derivTimes.get())
            except:
                self.derivative.configure(text = "Error")
            else:
                self.derivative.configure(text = ans.__str__())
        integExp = self.integInput.get()
        bounds = [self.integLower.get(), self.integUpper.get()]
        if not bounds[0]:
            bounds[0] = None
        elif bounds[0] == u"-\u221E":
            bounds[0] = "-oo"
        if not bounds[1]:
            bounds[1] = None
        elif bounds[1] == u"\u221E":
            bounds[1] = "oo"
        if integExp == "":
            self.integral.configure(text = "")
        else:
            try:
                ans = integrate(integExp, (self.integVar.get(), bounds[0], bounds[1]))
            except:
                self.integral.configure(text = "Error")
            else:
                if ans.__str__().startswith("Integral"):
                    self.integral.configure(text = "Impossible")
                elif ans.__str__().startswith("Piecewise"):
                    self.integral.configure(text = ans.args[1][0].__str__())
                elif ans.is_infinite:
                    if not ans.is_nonnegative:
                        self.integral.configure(text = u"-\u221E")
                    else:
                        self.integral.configure(text = u"\u221E")
                else:
                    self.integral.configure(text = ans.__str__())
        if self.running:
            self.root.after(100, self.main)

    def close(self):
        self.running = False
        self.root.destroy()
        sys.exit()

    def inf(self, bound):
        if bound == 1:
            self.integUpper.delete(0, END)
            self.integUpper.insert(0, u"\u221E")
        if bound == 0:
            self.integLower.delete(0, END)
            self.integLower.insert(0, u"-\u221E")

    def copy(self, text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()

if __name__ == "__main__":
    App()
