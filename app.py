class Proceso():
    def __init__(self, rafaga, entrada, nombre):
        self.entrada = entrada
        self.rafaga = rafaga
        self.nombre = nombre
        self.wait = 0

    def __str__(self):
        return f"'{self.nombre}'-'{self.rafaga}'-'{self.entrada}' "


def srtf(*procesos):
    map_ordered_by_entry = {}
    total_time = 0

    for proceso in procesos:
        
        total_time += proceso.rafaga
        if proceso.entrada in map_ordered_by_entry:
            map_ordered_by_entry[proceso.entrada].append(proceso)
        else:
            map_ordered_by_entry[proceso.entrada] = [proceso]
        print(map_ordered_by_entry)

    wait_list = []
    process = []

    for i in range(0, total_time):
        print(i)
        print(process)
        for proceso in wait_list:
            proceso.wait = proceso.wait + 1

        if i in map_ordered_by_entry:
            shortest = map_ordered_by_entry[i][0]

            for proceso in map_ordered_by_entry[i][1:]:
                print("lol")
                if shortest.rafaga > proceso.rafaga:
                    shortest = proceso
                else:
                    wait_list.append(proceso)

            if i == 0:
                process.append(shortest)
            elif process[i-1].rafaga == 0:
                process.append(shortest)
            elif shortest.rafaga < process[i-1].rafaga:
                process.append(shortest)
                wait_list.append(process[i])
            else:
                wait_list.append(shortest)
                process.append(process[i-1])
                process[i].rafaga = process[i].rafaga - 1
        else:
            aux = process[i-1]
            aux.rafaga = aux.rafaga - 1
            process.append(aux)

        if wait_list:
            shortest = wait_list[0]

            for proceso in wait_list[1:]:

                if shortest.rafaga > proceso.rafaga:
                    shortest = proceso
                elif shortest.rafaga == proceso.rafaga:
                    shortest = proceso if proceso.entrada < shortest.entrada else shortest

            if process[i-1].rafaga == 0:
                process.append(shortest)

            if shortest.rafaga < process[i-1].rafaga:
                process.append(shortest)
                wait_list.append(process[i])

            else:
                process.append(process[i-1])
                process[i].rafaga = process[i].rafaga - 1

    return process


p1 = Proceso(4, 0, "p1")
p2 = Proceso(3, 3, "p2")
p3 = Proceso(1, 2, "p3")

gantt = srtf(p1, p2, p3)

for ob in gantt:
    print(f"Proceso: '{ob.nombre}' ; rafaga: ''{ob.rafaga}''")
