import json
import algo.srtf as srtf
import algo.rr as rr
from proceso import Proceso
from flask import Flask

p1 = Proceso(0, 7, "p1")
p2 = Proceso(2, 4, "p2")
p3 = Proceso(4, 1, "p3")
p4 = Proceso(5, 4, "p4")
procesos = [p1, p2, p3, p4]

gantt = srtf.SRTF(*procesos)

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

# Flask constructor takes the name of  
# current module (__name__) as argument. 
app = Flask(__name__) 
@app.route('/get_results') 
def results(): 
    return result

@app.route('/')
  
# main driver function 
if __name__ == '__main__': 
    app.run() 

