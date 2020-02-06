import json


class Proceso():
    entrada = 0
    rafaga = 0
    nombre = 0
    wait = 0

    def __init__(self, rafaga, entrada, nombre):
        self.entrada = entrada
        self.rafaga = rafaga
        self.nombre = nombre
        self.wait = 0

    def __str__(self):
        return f"'{self.nombre}'-'{self.rafaga}'-'{self.entrada}' "

    def remaining_time(self, tiempo_del_cpu):
        return self.rafaga - (tiempo_del_cpu - self.entrada - self.wait)

class SRTF():
    processes = []
    map_ordered_by_entry = {}
    total_time = 0
    count_processes = 0
    wait_list = []
    actual_process = None

    def __init__(self, *procesos):
        self.processes = procesos

        for proceso in procesos:
            self.total_time += proceso.rafaga
            self.count_processes += 1

            if proceso.entrada in self.map_ordered_by_entry:
                self.map_ordered_by_entry[proceso.entrada].append(proceso)
            else:
                self.map_ordered_by_entry[proceso.entrada] = [proceso]
            

    def srtf(self):
        gantt = {}
        print(self.map_ordered_by_entry)
        for i in range(0, self.total_time):
            gantt[i] = {}

            if i in self.map_ordered_by_entry:

                # Si se ingresan nuevos procesos, se añaden a la lista de espera
                aux_list = self.wait_list + self.map_ordered_by_entry[i]
                # Siempre será el primero, se hace una comparación de cual de los
                # procesos tiene menor tiempo de rafaga restante
                shortest = aux_list[0]

                # El tiempo de ráfaga restante se calcula con la siguiente formula
                # tiempo restante = ráfaga - (momento del algoritmo - tiempo de entrada del proceso + tiempo de espera total del proceso)

                for proceso in aux_list[1:]:
                    if shortest.remaining_time(i) > proceso.remaining_time(i):
                        shortest = proceso
            
                if i == 0 or self.actual_process.remaining_time(i) == 0:
                    self.actual_process = shortest
                    

                    gantt[i]["Proceso"] = self.actual_process.nombre
                    gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

                elif shortest.remaining_time(i) < self.actual_process.remaining_time(i):
                        
                    self.wait_list.append(self.actual_process)
                    self.actual_process = shortest

                    gantt[i]["Proceso"] = self.actual_process.nombre
                    gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

                else:
                    wait_list.append(shortest)

                    gantt[i]["Proceso"] = self.actual_process.nombre
                    gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

            elif self.actual_process.remaining_time(i) != 0:

                gantt[i]["Proceso"] = self.actual_process.nombre
                gantt[i]["Ráfaga restante"] = self.actual_process.remaining_time(i)

            else:
                shortest = self.wait_list[0]

                for proceso in self.wait_list[1:]:
                    if shortest.remaining_time(i) > proceso.remaining_time(i):
                            shortest = proceso
                    elif shortest.remaining_time(i) == proceso.remaining_time(i):
                        if shortest.entrada > proceso.entrada:
                            shortest = proceso
                
                gantt[i]["Proceso"] = shortest.nombre
                gantt[i]["Ráfaga restante"] = shortest.remaining_time(i)

                self.wait_list.remove(shortest)
                self.actual_process = shortest

            for proceso in self.wait_list:
                proceso.wait += 1

        return gantt

    def total_wait_time(self):
        total = 0
        for proceso in self.processes:
            total += proceso.wait
        return total

p1 = Proceso(7, 0, "p1")
p2 = Proceso(4, 2, "p2")
p3 = Proceso(1, 4, "p3")
p4 = Proceso(4, 5, "P4")

procesos = [p1, p2, p3, p4]
gantt = SRTF(*procesos)

# print("Resultado:\n", json.dumps(gantt, indent=1, sort_keys=True))
i=0

result = gantt.srtf()
for instant in result:
    process = result[instant]
    print(f"{i}: {process}")
    i+=1

print("Tiempo de espera individuales: ")
for proceso in procesos:
    print(f"Proceso: {proceso.nombre} - Espero: {proceso.wait}")
print("Total de tiempo en espera: ", gantt.total_wait_time())
print("Tiempo de espera promedio: ", gantt.total_wait_time()/gantt.count_processes)
