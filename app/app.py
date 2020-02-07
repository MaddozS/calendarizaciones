import tkinter as tk

class Demo1:
    def __init__(self, master):
        self.master = master
        # self.master.geometry("500x500")

        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.frame, text="Simulador de calendarización de procesos", justify='center')
        self.label.grid(row=0, column=0, sticky="we", columnspan=2, pady=40, padx = 20)

        self.label2 = tk.Label(self.frame, text="Numero de procesos", justify='center')
        self.label2.grid(row=1, column=0, sticky="we", columnspan=2, padx = 20)

        self.input1 = tk.Entry(self.frame)
        self.input1.grid(row=2, column=0, sticky="we", columnspan=2, padx = 20)

        self.label3 = tk.Label(self.frame, text="Quantum (solo para RR)", justify='center')
        self.label3.grid(row=3, column=0, sticky="we", columnspan=2, padx=20)

        self.input2 = tk.Entry(self.frame)
        self.input2.grid(row=4, column=0, sticky="we", columnspan=2, padx=20, pady = (0,40))
        
        self.button1 = tk.Button(self.frame, text = 'SRTF', command = self.new_window, background='blue')
        self.button1.grid(row=5, column=0)

        self.button2 = tk.Button(self.frame, text = 'Round Robin', command = self.new_window, background='blue')
        self.button2.grid(row=5, column=1)

        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

def main(): 
    root = tk.Tk()
    app = Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()