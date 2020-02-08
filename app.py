import tkinter as tk
from backend.proceso import Proceso
from backend.algo.srtf import SRTF
import copy


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)

        self.frames = {}

        for F in (MainWindow, SRTFWindow):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainWindow)
        self.container.pack()

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
    promedio = 0
    result = {}

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0)

        self.create_table_task()
        self.create_wait_table()
        self.create_gantt()

    def add_process_window(self):
        AddProcessWindowSRTF(tk.Toplevel(self), self.count_proceso)

    def create_table_task(self):
        # Table of the processes added
        self.process_table = tk.Frame(self.frame, borderwidth=2, relief="solid")
        self.process_table.grid(row=0, column=0, sticky="nswe", padx=(20, 10))

        self.name_process_head = tk.Label(self.process_table, text="Procesos", justify='center', background="#FEFCE5")
        self.name_process_head.grid(row=0, column=0, sticky="wsn")

        self.add_process_button_head = tk.Button(self.process_table, text=" agregar ", command=self.add_process_window)
        self.add_process_button_head.grid(row=0, column=1, sticky="ens")

        self.process_table_body = tk.Frame(self.process_table)
        self.process_table_body.grid(row=1, column=0, sticky="we", columnspan=4)

    def update_process_list_table(self):
        i = 0
        for p in self.procesos_list:
            name_process = tk.Label(self.process_table_body, text="Nombre: " + p.nombre, justify='center', name=f"np{i+1}")
            name_process.grid(row=i, column=0, sticky="we", padx=(10, 5))

            entry_process = tk.Label(self.process_table_body, text="Entro: " + str(p.entrada), justify='center', name=f"ep{i+1}")
            entry_process.grid(row=i, column=1, sticky="we", padx=5)

            burst_process = tk.Label(self.process_table_body, text="Ráfaga: " + str(p.rafaga), justify='center', name=f"bp{i+1}")
            burst_process.grid(row=i, column=2, sticky="we", padx=5)

            remove_process_button = tk.Button(self.process_table_body, text=" eliminar ", command=lambda: self.remove_process(p.nombre), name=f"rp{i+1}", foreground="white", background="red")
            remove_process_button.grid(row=i, column=3, sticky="we", padx=(5, 10))
            i += 1

    def create_wait_table(self):
        self.wait_table = tk.Frame(self.frame, borderwidth=2, relief="solid")
        self.wait_table.grid(row=0, column=1, sticky="nwes", padx=(20,10))

        self.wburst_process_head = tk.Label(self.wait_table, text="Tiempo de espera por proceso", justify='center', background="white")
        self.wburst_process_head.grid(row=0, column=0, sticky="wens", columnspan=2)

        self.wprocess_table_body = tk.Frame(self.wait_table)
        self.wprocess_table_body.grid(row=1, column=0, sticky="wens", columnspan=2)

        self.w_media = tk.Label(self.wait_table, text="Tiempo promedio de espera: ", justify='center', background="white")
        self.w_media.grid(row=2, column=0, sticky="nswe")

        self.w_media = tk.Label(self.wait_table, text=self.promedio, justify='center', background="white")
        self.w_media.grid(row=2, column=1, sticky="wnse")

    def update_process_wait_table(self):
        i = 0
        for p in self.procesos_list:
            name_process = tk.Label(self.wprocess_table_body, text="Nombre: " + p.nombre, justify='center', name=f"np{i+1}")
            name_process.grid(row=i, column=0, sticky="we", padx=(10, 5))

            wait_process = tk.Label(self.wprocess_table_body, text="Espero: " + str(p.wait), justify='center', name=f"ep{i+1}")
            wait_process.grid(row=i, column=1, sticky="we", padx=(5,10))
            i += 1

        self.w_media["text"] = self.promedio

    def remove_process(self, process):
        for w in self.process_table_body.winfo_children():
            w.destroy()

        for w in self.wprocess_table_body.winfo_children():
            w.destroy()

        self.count_proceso -= 1
        
        for x in self.procesos_list:
            if process == x.nombre:
                print("found")
                self.procesos_list.remove(x)
                break

        self.update_gantt()
        self.update_process_list_table()
        self.update_process_wait_table()

    def update_gantt(self):
        aux = self.procesos_list
        algo = SRTF(*aux)
        self.result = algo.srtf()

        print(self.result)
        self.promedio = algo.total_wait_time() / algo.count_processes
        self.total_time = algo.total_time

        self.create_gantt()

    def create_gantt(self):
        self.c_frame = tk.Frame(self.frame, borderwidth=2, relief="solid")
        self.c_frame.grid(row=1, column=0, sticky="nwes", columnspan=2, pady=40)

        if self.result:
            self.delete_gantt()

            i = 0
            for x in self.result:
                print("xd", x)
                text = "|" + "    " + str(self.result[x]['Proceso']) + "    "
                p = tk.Label(self.c_frame, text=text, justify='center', name=f"p{i+1}")
                p.grid(row=0, column=i, sticky="wens")

                n = tk.Label(self.c_frame, text=str(x), justify='center', name=f"pnum{i+1}")
                n.grid(row=1, column=i, sticky="wns")
                i += 1
                print("f")

            p2 = tk.Label(self.c_frame, text="|", justify='center', name=f"pend")
            p2.grid(row=0, column=i, sticky="wens")

            n = tk.Label(self.c_frame, text=self.total_time, justify='center', name=f"pnumend")
            n.grid(row=1, column=i, sticky="wns")

    def delete_gantt(self):
        for w in self.c_frame.winfo_children():
            w.destroy()

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
        try:
            burst = self.input1.get()
            entry = self.input2.get()
            self.parent.master.count_proceso += 1

            name = f"p{self.parent.master.count_proceso}"
            process = Proceso(int(entry), int(burst), name)

            self.parent.master.procesos_list.append(process)
            self.close_windows()
        except:
            self.parent.master.count_proceso -= 1

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
