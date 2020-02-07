class Proceso():
    entrada = 0
    rafaga = 0
    nombre = 0
    wait = 0
    summon=0
    def __init__(self, entrada, rafaga, nombre):
        self.entrada = entrada
        self.rafaga = rafaga
        self.nombre = nombre
        self.wait = 0

    def __str__(self):
        return f"'{self.nombre}'-'{self.rafaga}'-'{self.entrada}'- '{self.wait}'"

    def remaining_time(self, tiempo_del_cpu):
        return self.rafaga - (tiempo_del_cpu - self.entrada - self.wait)

