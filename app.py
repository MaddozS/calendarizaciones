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


def total_wait_time(*procesos):
    total = 0
    for proceso in procesos:
        total += proceso.wait
    return total


def srtf(*procesos):
    gantt = {}
    map_ordered_by_entry = {}
    total_time = 0

    for proceso in procesos:
        total_time += proceso.rafaga
        if proceso.entrada in map_ordered_by_entry:
            map_ordered_by_entry[proceso.entrada].append(proceso)
        else:
            map_ordered_by_entry[proceso.entrada] = [proceso]

    wait_list = []
    actual_process = None

    print(map_ordered_by_entry)
    for i in range(0, total_time):
        gantt[i] = {
            "Proceso": None,
            "Ráfaga restante": None,
        }

        for proceso in wait_list:
            proceso.wait += 1

        if i in map_ordered_by_entry:

            # Si se ingresan nuevos procesos, se añaden a la lista de espera
            aux_list = wait_list + map_ordered_by_entry[i]
            # Siempre será el primero, se hace una comparación de cual de los
            # procesos tiene menor tiempo de rafaga restante
            shortest = aux_list[0]

            # El tiempo de ráfaga restante se calcula con la siguiente formula
            # tiempo restante = ráfaga - (momento del algoritmo - tiempo de entrada del proceso + tiempo de espera total del proceso)

            for proceso in aux_list[1:]:
                if shortest.remaining_time(i) > proceso.remaining_time(i):
                    shortest = proceso
                else:
                    wait_list.append(proceso)

            if i == 0 or actual_process.remaining_time(i) == 0:
                actual_process = shortest

                gantt[i]["Proceso"] = actual_process.nombre
                gantt[i]["Ráfaga restante"] = actual_process.remaining_time(i)

            elif shortest.remaining_time(i) < actual_process.remaining_time(i):
                wait_list.append(actual_process)
                actual_process = shortest

                gantt[i]["Proceso"] = actual_process.nombre
                gantt[i]["Ráfaga restante"] = actual_process.remaining_time(i)

            else:
                wait_list.append(shortest)

                gantt[i]["Proceso"] = actual_process.nombre
                gantt[i]["Ráfaga restante"] = actual_process.remaining_time(i)

        elif actual_process.remaining_time(i) != 0:
            gantt[i]["Proceso"] = actual_process.nombre
            gantt[i]["Ráfaga restante"] = actual_process.remaining_time(i)

        else:
            shortest = wait_list[0]

            for proceso in wait_list[1:]:
                if shortest.remaining_time(i) >= proceso.remaining_time(i):
                    if shortest.entrada > proceso.entrada:
                        shortest = proceso

            gantt[i]["Proceso"] = shortest.nombre
            gantt[i]["Ráfaga restante"] = shortest.remaining_time(i)

            wait_list.remove(shortest)
            actual_process = shortest

    return gantt


p1 = Proceso(7, 0, "p1")
p2 = Proceso(4, 2, "p2")
p3 = Proceso(1, 4, "p3")
p4 = Proceso(4, 5, "P4")

procesos = [p1, p2, p3, p4]
gantt = srtf(*procesos)
total_waiting_time = total_wait_time(*procesos)

# print("Resultado:\n", json.dumps(gantt, indent=1, sort_keys=True))
i=0
for instant in gantt:
    process = gantt[instant]
    print(f"{i}: {process}")
    i+=1

print("Tiempo de espera individuales: ")
for proceso in procesos:
    print(f"Proceso: {proceso.nombre} - Espero: {proceso.wait}")

print("Total de tiempo en espera: ", total_waiting_time)
print("Tiempo de espera promedio: ", total_waiting_time/len(procesos))
