#! /usr/bin/env python

"""
# Notactión

## Mapa

En mapa original:

* 0: libre
* 1: ocupado (muro/obstáculo)

Vía código incorporamos:

* 2: visitado
* 3: start
* 4: goal

## Nodo

Nós
* -2: parentId del nodo start
* -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

# Específico de implementación Python

* Índices empiezan en 0
* charMap
"""

# # Initial values are hard-coded (A nivel mapa)

#FILE_NAME = "/usr/local/share/master-ipr/map1/map1.csv" # Linux-style absolute path
#FILE_NAME = "C:\\Users\\USER_NAME\\Downloads\\master-ipr\\map1\\map1.csv" # Windows-style absolute path, note the `\\` and edit `USER_NAME`
#FILE_NAME = "../../../../map1/map1.csv" # Linux-style relative path
FILE_NAME = "..\\..\\..\\..\\map5\\map5.csv" # Windows-style relative path, note the `\\`
START_X = 2
START_Y = 2
END_X = 3
END_Y = 18

#Los valores de inicio y final se solicitan por consola

print("¿Valor X del nodo de incio?")
START_X = int(input())
print("¿Valor Y del nodo de incio?")
START_Y = int(input())
print("¿Valor X del nodo de final?")
END_X= int(input())
print("¿Valor Y del nodo de final?")
END_Y = int(input())

import matplotlib.pyplot as plt  #Librerías para el gráfico del mapa
import numpy as np

# # Mapa

# ## Creamos estructura de datos para mapa

charMap = []

# ## Creamos función para volcar estructura de datos para mapa

def dumpMap():
    for line in charMap:
        print(line)

# ## De fichero, llenar estructura de datos de fichero (`to parse`/`parsing``) para mapa

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

# ## A nivel mapa, integramos la info que teníamos de start & end

charMap[START_X][START_Y] = '3' # 3: start
charMap[END_X][END_Y] = '4' # 4: goal


#Creación de gráfico para charMap utilizando numpy y matplotlib

map_array = np.array(charMap, dtype=int)
cmap = plt.cm.get_cmap("coolwarm", 5) 
bounds = [0, 1, 2, 3, 4, 5] 
norm = plt.Normalize(bounds[0], bounds[-1])
fig, ax = plt.subplots()
plt.ion()


#Función para visualizar el gráfico del mapa

def visualize_map(map_array):
    ax.clear() 
    img = ax.imshow(map_array, cmap=cmap, norm=norm)
    plt.draw()  
    plt.pause(0.01) # Tiempo de visualización entre pasos del algoritmo



# Definir la clase Node. Se añade a la clase original la función de costo (g), función heurística (h) y función de evaluación (f)

class Node:
    def __init__(self, x, y, myId, parentId, g, h):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
        self.g = g  
        self.h = h  
        self.f = g + h  

    def dump(self):
        print("---------- x " + str(self.x) +
              " | y " + str(self.y) +
              " | id " + str(self.myId) +
              " | parentId " + str(self.parentId) +
              " | g " + str(self.g) +
              " | h " + str(self.h) +
              " | f " + str(self.f))



# Función para determinar heurística de un nodo (distancia Manhattan)

def heuristic(node):
    return abs(node.x - END_X) + abs(node.y - END_Y)



# Crear el primer nodo
init = Node(START_X, START_Y, 0, -2, 0, 0)

#Definición de listas que se van a utilizar: Lista de nodos "abierta" y "cerrada", y una lista "nodes" auxiliar para la búsqueda del camino óptimo después de encontrar la meta.

open=[]
closed=[]
nodes=[]
nodes.append(init)
open.append(init)
done=False
goalParentId = -1


# Bucle principal del algoritmo A*

while not done and len(open) > 0:

    current_node = min(open, key=lambda node: node.f)  #El nodo actual será el de la lista abierta con menor valor de f
    open.remove(current_node)                           
    closed.append(current_node)
    nodes.append(Node(current_node.x,current_node.y,len(nodes),current_node.myId,0,0)) 

    if charMap[current_node.x][current_node.y] == '4':      #Comprobamos si es la meta
        done = True
        goalParentId=current_node.myId
        print("GOAAAAL")

    charMap[current_node.x][current_node.y] = '2'            #Si no lo es lo marcamos como visitado


    successors = []                                          #Evaluamos sus posibles sucesores en las 4 direcciones

    for i, j in [(0, -1), (-1, 0),(1, 0), (0, 1)]:

        x, y = current_node.x + i, current_node.y + j

        if charMap[x][y] == '0' or charMap[x][y] == '4':
        
            g = current_node.g + 1
            h = heuristic(Node(x, y, 0, 0, 0, 0))
            f = g + h
            
            in_closed = any(node.x == x and node.y == y for node in closed)
            if in_closed:
                continue
            
            in_open = any(node.x == x and node.y == y for node in open)
            if not in_open or f < current_node.f:
                successors.append(Node(x, y, len(closed), current_node.myId, g, h))

    open.extend(successors)

    map_array = np.array(charMap, dtype=int)                #Actualizamos el gráfico
    visualize_map(map_array)
 


#Encontrar el camino óptimo cuando se ha llegado a meta

ok = False
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            charMap[node.x][node.y] = '5'
            goalParentId = node.parentId
            if( goalParentId == -2):
                ok = True

map_array = np.array(charMap, dtype=int)
visualize_map(map_array)

plt.ioff()
plt.show()