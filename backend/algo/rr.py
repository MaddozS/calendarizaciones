class RR:
    processes = []
    total_time = 0
    transcurred_time = 0
    count_processes = 0
    actual_process = None
    quantum = 0

    def __init__(self, quantum, *procesos):
        self.processes = list(procesos)
        self.quantum = quantum

        for proceso in procesos:
            self.total_time += proceso.rafaga
            self.count_processes += 1



    def rr(self):
        gantt = {}
        while self.transcurred_time != self.total_time:
            for x in self.processes:
                print(x.nombre)

            for proceso in self.processes:
                print(proceso.nombre, " ", proceso.rafaga)
                proceso.wait = self.transcurred_time - proceso.summon
                if proceso.rafaga > self.quantum:
                    proceso.rafaga -= self.quantum
                    self.transcurred_time += self.quantum
                    proceso.summon = self.transcurred_time
                else:
                    self.transcurred_time += proceso.rafaga
                    proceso.summon = self.transcurred_time
                    proceso.rafaga -= proceso.rafaga

                    self.processes.remove(proceso)

                gantt[self.transcurred_time] = {}
                gantt[self.transcurred_time]["Proceso"] = proceso.nombre
                gantt[self.transcurred_time]["Ráfaga restante"] = proceso.rafaga

        return gantt





