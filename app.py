import tkinter as tk
from backend.proceso import Proceso
from backend.algo.srtf import SRTF
import copy


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainWindow, SRTFWindow):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainWindow)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class MainWindow(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.parent.geometry("500x500")
        self.frame = tk.Frame(self)

        self.label = tk.Label(self.frame, text="Simulador de calendarización de procesos", justify='center')
        self.label.grid(row=0, column=0, sticky="we", pady=40, padx=20, columnspan=2)

        self.button1 = tk.Button(self.frame, text='SRTF', command=lambda: controller.show_frame(SRTFWindow))
        self.button1.grid(row=1, column=0, pady=(0, 40), sticky="we")

        self.button2 = tk.Button(self.frame, text='Round Robin')
        self.button2.grid(row=1, column=1, pady=(0, 40), sticky="we")

        self.frame.pack()

    def srtf_window(self):
        self.newWindow = tk.Toplevel(self.parent)
        self.app = SRTFWindow(self.newWindow, 0, [])


class SRTFWindow(tk.Frame):
    procesos_list = []
    count_proceso = 0

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(self, background="black")

        self.create_table_task()
        self.create_wait_table()

        self.frame.pack()

    def add_process_window(self):
        AddProcessWindowSRTF(tk.Toplevel(self), self.count_proceso)

    def create_table_task(self):
        # Table of the processes added
        self.process_table = tk.Frame(self.frame)
        self.process_table.grid(row=0, column=0, sticky="nwe", padx=(15, 30), pady=(10, 40))

        self.name_process_head = tk.Label(self.process_table, text="Proceso", justify='center', background="white")
        self.name_process_head.grid(row=0, column=0, sticky="we")

        self.entry_process_head = tk.Label(self.process_table, text="Tiempo de entrada", justify='center', background="white")
        self.entry_process_head.grid(row=0, column=1, sticky="we")

        self.burst_process_head = tk.Label(self.process_table, text="Ráfaga", justify='center', background="white")
        self.burst_process_head.grid(row=0, column=2, sticky="we")

        self.add_process_button_head = tk.Button(self.process_table, text="+", command=self.add_process_window)
        self.add_process_button_head.grid(row=0, column=3, sticky="we")

        self.process_table_body = tk.Frame(self.process_table, background="red")
        self.process_table_body.grid(row=1, column=0, sticky="we", columnspan=4)

    def update_process_list_table(self):
        i = 0
        for p in self.procesos_list:
            name_process = tk.Label(self.process_table_body, text=p.nombre, justify='center', name=f"np{i+1}")
            name_process.grid(row=i, column=0, sticky="we")

            entry_process = tk.Label(self.process_table_body, text=p.entrada, justify='center', name=f"ep{i+1}")
            entry_process.grid(row=i, column=1, sticky="we")

            burst_process = tk.Label(self.process_table_body, text=p.rafaga, justify='center', name=f"bp{i+1}")
            burst_process.grid(row=i, column=2, sticky="we")

            remove_process_button = tk.Button(self.process_table_body, text="-", command=lambda: self.remove_process(p), name=f"rp{i+1}")
            remove_process_button.grid(row=i, column=3, sticky="we")
            i += 1

    def create_wait_table(self):
        self.wait_table = tk.Frame(self.frame)
        self.wait_table.grid(row=0, column=1, sticky="nwe", padx=(30, 15), pady=(10, 40))

        self.wait_process_head = tk.Label(self.wait_table, text="Proceso", justify='center', background="white")
        self.wait_process_head.grid(row=0, column=0, sticky="we")

        self.wburst_process_head = tk.Label(self.wait_table, text="Tiempo de espera", justify='center', background="white")
        self.wburst_process_head.grid(row=0, column=1, sticky="we")

        self.wprocess_table_body = tk.Frame(self.wait_table, background="red")
        self.wprocess_table_body.grid(row=1, column=0, sticky="we", columnspan=2)

    def update_process_wait_table(self):
        i = 0
        for p in self.procesos_list:
            name_process = tk.Label(self.wprocess_table_body, text=p.nombre, justify='center', name=f"wnp{i+1}")
            name_process.grid(row=i, column=0, sticky="we")

            burst_process = tk.Label(self.wprocess_table_body, text=p.wait, justify='center', name=f"wwp{i+1}")
            burst_process.grid(row=i, column=1, sticky="we")
            i += 1

    def remove_process(self, process):
        for w in self.process_table_body.winfo_children():
            w.destroy()

        for w in self.wprocess_table_body.winfo_children():
            w.destroy()

        self.count_proceso -= 1

        self.procesos_list.remove(process)
        self.update_process_list_table()
        self.update_process_wait_table()

    def update_gantt(self):
        aux = self.procesos_list
        for p in aux:
            print("ayuda dios ", p)
        algo = SRTF(*aux)
        result = algo.srtf()
        print(result)


class AddProcessWindowSRTF():

    def __init__(self, parent, count_p):
        self.parent = parent
        self.count_p = count_p

        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)

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

        self.count = tk.Label(self.frame, text=f"{self.parent.master.count_proceso}", justify='right')
        self.count.grid(row=3, column=0, columnspan=2)

    def add_process_(self):
        burst = self.input1.get()
        entry = self.input2.get()
        self.parent.master.count_proceso += 1

        name = f"p{self.parent.master.count_proceso}"
        process = Proceso(int(entry), int(burst), name)

        self.parent.master.procesos_list.append(process)
        self.close_windows()

    def close_windows(self):
        self.parent.master.update_gantt()
        self.parent.master.update_process_list_table()
        self.parent.master.update_process_wait_table()
        self.parent.destroy()


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
