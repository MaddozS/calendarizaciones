import tkinter as tk
from backend.proceso import Proceso

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("")
        # self.master.geometry("500x500")

        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.frame, text="Simulador de calendarización de procesos", justify='center')
        self.label.grid(row=0, column=0, sticky="we", columnspan=2, pady=40, padx = 20)
        
        self.button1 = tk.Button(self.frame, text = 'SRTF', command = self.srtf_window)
        self.button1.grid(row=1, column=0, pady = (0,40))

        self.button2 = tk.Button(self.frame, text = 'Round Robin')
        self.button2.grid(row=1, column=1, pady = (0,40))

        self.frame.pack()

    def srtf_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = SRTFWindow(self.newWindow)

class SRTFWindow:
    procesos_list = []
    count_process = 0
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        # Table of the processes added
        self.process_table = tk.Frame(self.frame)
        self.process_table.grid(row=0, column=0, sticky="we", columnspan=10, padx=30)

        self.name_process = tk.Label(self.process_table, text="Proceso", justify='center', background = "white")
        self.name_process.grid(row=0, column=0, sticky="we")

        self.entry_process = tk.Label(self.process_table, text="Tiempo de entrada", justify='center', background = "white")
        self.entry_process.grid(row=0, column=1, sticky="we")

        self.burst_process = tk.Label(self.process_table, text="Ráfaga", justify='center', background = "white")
        self.burst_process.grid(row=0, column=2, sticky="we")

        self.add_process_button = tk.Button(self.process_table, text="+", command=self.add_process_window)
        self.add_process_button.grid(row=0, column=3,)

        self.frame.pack()

    def add_process_window(self):
        self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        self.app = AddProcessWindowSRTF(self.newWindow, self.count_process, self.procesos_list)

    def close_windows(self):
        self.master.destroy()

class AddProcessWindowSRTF:
    def __init__(self, master, count_proceso, procesos):
        self.count_proceso = count_proceso
        self.procesos = procesos
        self.master = master
        self.frame = tk.Frame(self.master)

        self.label1 = tk.Label(self.frame, text="Ráfaga", justify='right')
        self.label1.grid(row=0, column=0, sticky="we")

        self.input1 = tk.Entry(self.frame)
        self.input1.grid(row=0, column=1, sticky="we")

        self.label2 = tk.Label(self.frame, text="Tiempo de llegada", justify='right')
        self.label2.grid(row=1, column=0, sticky="we")

        self.input2 = tk.Entry(self.frame)
        self.input2.grid(row=1, column=1, sticky="we")

        self.add_process_button = tk.Button(self.frame, text="Añadir proceso", command=self.add_process_)
        self.add_process_button.grid(row=2, column=0, columnspan=2)

        self.count = tk.Label(self.frame, text=f"{self.count_proceso}", justify='right')
        self.count.grid(row=3, column=0, columnspan=2)

        self.frame.pack()

    def add_process_(self):
        burst = self.input1.get()
        entry = self.input2.get()
        self.count_proceso+=1
        name = f"p{self.count_proceso}"
        process = Proceso(entry, burst, name)

        self.procesos.append(process)
        self.close_windows()

    def close_windows(self):
        self.app = SRTFWindow(self.master)
        
        self.count_process = self.count_proceso
        self.procesos_list = self.procesos
        self.master.destroy()


def main(): 
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()