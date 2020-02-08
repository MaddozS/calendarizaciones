class SRTF():
    processes = []
    map_ordered_by_entry = {}
    total_time = 0
    count_processes = 0
    wait_list = []
    actual_process = None

    def __init__(self, *procesos):
        self.processes = procesos

        for proceso in self.processes:
            self.total_time += proceso.rafaga
            self.count_processes += 1
            proceso.wait = 0
            print(proceso.wait, " ", proceso.nombre)

            if proceso.entrada in self.map_ordered_by_entry:
                if proceso not in self.map_ordered_by_entry[proceso.entrada]:
                    self.map_ordered_by_entry[proceso.entrada].append(proceso)
            else:
                self.map_ordered_by_entry[proceso.entrada] = [proceso]
        print(self.map_ordered_by_entry)

    def srtf(self):
        gantt = {}
        for i in range(0, self.total_time):

            if i in self.map_ordered_by_entry:
                # Si se ingresan nuevos procesos, se añaden a la lista de espera
                self.wait_list += self.map_ordered_by_entry[i]
                # Siempre será el primero, se hace una comparación de cual de los
                # procesos tiene menor tiempo de rafaga restante
                shortest = self.wait_list[0]

                # El tiempo de ráfaga restante se calcula con la siguiente formula
                # tiempo restante = ráfaga - (momento del algoritmo - tiempo de entrada del proceso + tiempo de espera total del proceso)

                for proceso in self.wait_list[1:]:
                    if shortest.remaining_time(i) > proceso.remaining_time(i):
                        shortest = proceso

                if i == 0:
                    self.remove_from_wait_list(shortest)
                    self.actual_process = shortest
                    gantt[i] = {}
                    gantt[i]["Proceso"] = self.actual_process.nombre
                    # gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

                elif self.actual_process.remaining_time(i) == 0:
                    self.remove_from_wait_list(shortest)

                    self.actual_process = shortest
                    gantt[i] = {}
                    gantt[i]["Proceso"] = self.actual_process.nombre
                    # gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

                elif shortest.remaining_time(i) < self.actual_process.remaining_time(i):
                    self.remove_from_wait_list(shortest)
                    self.wait_list.append(self.actual_process)
                    self.actual_process = shortest
                    gantt[i] = {}
                    gantt[i]["Proceso"] = self.actual_process.nombre
                    # gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

                else:
                    if shortest not in self.wait_list:
                        self.wait_list.append(shortest)
                    gantt[i] = {}
                    gantt[i]["Proceso"] = self.actual_process.nombre
                    gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

            elif self.actual_process.remaining_time(i) != 0:

                # gantt[i]["Proceso"] = self.actual_process.nombre
                # gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)
                pass
            else:
                shortest = self.wait_list[0]

                for proceso in self.wait_list[1:]:
                    if shortest.remaining_time(i) > proceso.remaining_time(i):
                        shortest = proceso
                    elif shortest.remaining_time(i) == proceso.remaining_time(i):
                        if shortest.entrada > proceso.entrada:
                            shortest = proceso
                gantt[i] = {}
                gantt[i]["Proceso"] = shortest.nombre
                # gantt[i]["Ráfaga restante"] = shortest.remaining_time(i)

                self.wait_list.remove(shortest)
                self.actual_process = shortest

            for proceso in self.wait_list:
                print("On wait ",proceso.wait, " ", proceso.nombre)
                proceso.wait += 1

            for proceso in self.processes:
                print(proceso.wait, " ", proceso.nombre)
        return gantt

    def total_wait_time(self):
        total = 0
        for proceso in self.processes:
            total += proceso.wait
        return total

    def remove_from_wait_list(self, process):
        if process in self.wait_list:
            self.wait_list.remove(process)
