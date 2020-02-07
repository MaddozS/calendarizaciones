import tkinter as tk

class Demo1:
    def __init__(self, master):
        self.master = master
        # self.master.geometry("500x500")

        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.frame, text="Simulador de calendarización de procesos", justify='center')
        self.label.grid(row=0, column=0, sticky="we", columnspan=2, pady=40, padx = 20)
        
        self.button1 = tk.Button(self.frame, text = 'SRTF', command = self.add_process, background='#F3EBA3')
        self.button1.grid(row=1, column=0, pady = (0,40))

        self.button2 = tk.Button(self.frame, text = 'Round Robin', command = self.add_process, background='#F3EBA3')
        self.button2.grid(row=1, column=1, pady = (0,40))

        self.frame.pack()

    def add_process(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = AddProcessWindow(self.newWindow)

class SRTFWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.label2 = tk.Label(self.frame, text="Ráfaga", justify='center')
        self.label2.grid(row=0, column=0, sticky="we")

        self.input2 = tk.Entry(self.frame)
        self.input2.grid(row=0, column=1, sticky="we")

        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

class AddProcessWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.label2 = tk.Label(self.frame, text="Ráfaga", justify='center')
        self.label2.grid(row=0, column=0, sticky="we")

        self.input2 = tk.Entry(self.frame)
        self.input2.grid(row=0, column=1, sticky="we")

        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

def main(): 
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()