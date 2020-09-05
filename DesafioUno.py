import numpy as np
import os
import heapq as h


class Container():
    def __init__(self, state):
        """
            Inicialización del estado.
                El estado recibirá una matriz numpy 
                de NxM, nuestras pruebas fueron realizadas con matrices
                de 5x5.

        """
        self.state = np.array(state, copy=True)
        self.x, self.y = self.state.shape


        self.max = np.amax(self.state)
        self.min = np.amin(self.state)

    ## Lower Than: Esta funcion sera utilizada para el
    ## heap, asi identificara cual es el estado mejor evaluado
    def __lt__(self, other):
        
        return self.evaluate() > other.evaluate()

    ## Lo mismo que Lower Than, pero sera para Lower equal.
    def __le__(self, other):
        return self.evaluate() >= other.evaluate()


    ## Este metodo devuelve un objeto Container con un estado identico
    ## Al del que lo crea.
    def getCopy(self):
        return Container(self.state)


    ## Este metodo obtiene el top
    ## De la columna i
    def getTop(self, i):
        for pos in range(self.y - 1, -1, -1):
            if self.state[i][pos] > 0:
                return self.state[i][pos]
        return 0

    ## Identifica si la columna i esta bien ordenada
    def isSorted(self, i):
        lastNum = 999999
        for num in np.array(self.state[i]):
            if num == 0:
                break
            if num > lastNum:
                return False
            lastNum = num
        return True

    ## Verificara si el stack se encuentra vacio
    def isStackEmpty(self, i):
        return self.state[i][0] == 0

    ## Verificara si el stack se encuentra lleno
    def isStackFull(self, i):
        return self.state[i][self.y - 1] != 0

    ## Metodo utilizado para realizar acciones.
    ## src = stack de fuente (desde donde se sacara el container)
    ## dest = stack de destino (en donde se dejara)
    def moveStack(self, src, dest):
        value = 0

        #---> Primero, verificamos que la accion se pueda realizar.
        if self.isStackFull(dest) or self.isStackEmpty(src):
            return False

        #---> Segundo, conseguimos y eliminamos el valor en top.
        for pos in range(self.y - 1, -1, -1):
            if self.state[src][pos] > 0:
                value = self.state[src][pos]
                self.state[src][pos] = 0
                break

        #---> Dejamos el valor
        for pos in range(self.y):
            if self.state[dest][pos] == 0:
                self.state[dest][pos] = value
                break
        return True


    ## Este metodo vera si es posible realizar una accion,
    ## sera utilizada en la generacion de acciones posibles.
    def canMove(self, src, dest):
        #---> Primero, verificamos que la accion se pueda realizar.
        if src != dest and (self.isStackFull(dest) or self.isStackEmpty(src)):
            return False
        return True

    ## Metodo que muestra el estado actual.
    def render(self):
        rend = np.rot90(self.state, k=1)
        print(rend)

    ## Cuenta la cantidad de stacks en una columna
    def countStackBlocks(self, i):
        count = 0
        for num in self.state[i]:
            if num != 0:
                count = count + 1
            else:
                break
        return count

    def getAllSorts(self):
        sorted = np.zeros(self.x, dtype=np.bool)
        for i in range(self.x):
            sorted[i] = self.isSorted(i)
        return sorted

    ## Comprueba si es un estado final.
    def isDone(self):
        for sort in self.getAllSorts():
            if not sort:
                return False
        return True


    ## Obtendra todas las posibles acciones desde un estado
    def getActions(self):
        actions = []
        for i in range(self.x):
            for j in range(self.x):
                if self.canMove(i, j):
                    actions.append([i, j])
        return actions

    ## Heuristica 1:
    ## Cuenta la cantidad de bloques bien ordenados
    def countSortedBlocks(self):
        count = 0

        for i in range(self.x):
            lastNum = 999999
            for num in np.array(self.state[i]):
                if num == 0 or num > lastNum:
                    break

                lastNum = num
                count += 1

        return count

    ## Heuristica 2:
    ## Este metodo calculara la diferencia de los top y top-1 de
    ## todas las columnas bien ordenadas.
    def getTopDiff(self, i):
        stack = np.array(self.state[i])

        if stack[0] == 0:
            return 0

        for i in range(len(stack)):
            if i == len(stack)-1 or stack[i+1] == 0:
                if stack[i] == 0:
                    return 0
                elif i == 0:
                    return (1/((self.max - stack[0])+1))
                else:
                    return (1/((stack[i-1]- stack[i] )+1))

    ## Este metodo calculara la evaluacion del estado
    ## sumando la heuristica 1 + heuristica 2.
    def evaluate(self):
        difference = 0 
        for i in range(self.x):
            if self.isSorted(i):
                difference += self.getTopDiff(i)

        return difference + self.countSortedBlocks() 


## Metodo de Busqueda

#Esta funcion buscara si la matriz se encuentra en la lista de visitados
def isVisited(list, state):
    return False in [False in (s == state) for s in list]


## Greedy Search
def best_first(initial_state: Container):
    count = 0
    heap = []
    visited = []
    h.heappush(heap, initial_state)
    while len(heap) > 0:
        current_state = h.heappop(heap)

        heap = []

        if isVisited(visited, current_state.state):
            continue

        visited.append(np.array(current_state.state, copy=True))
        actions = current_state.getActions()

        for action in actions:
            trans_state = current_state.getCopy()
            trans_state.moveStack(action[0], action[1])
            #trans_state.render()

            if not isVisited(visited, np.array(trans_state.state, copy=True)):
                count += 1
                h.heappush(heap, trans_state)
                if trans_state.isDone():
                    print("Pasos totales: ", count)
                    return trans_state


cont = Container(
    np.array(
        [
        [19, 2, 0, 0, 0], 
        [16, 15, 0, 0, 0], 
        [16, 14, 4, 7, 19],
        [10, 13, 0, 0, 0], 
        [18, 13, 13, 7, 0]
        ]
        )
)

cont2 = Container(
    np.array([[19, 2, 0, 0, 0], [16, 15, 0, 0, 0], [16, 14, 4, 7, 0],
              [10, 19, 13, 0, 0], [18, 13, 13, 7, 0]]))

cont3 = Container(
    np.array([[2, 19, 0, 0, 0], [16, 15, 0, 0, 0], [16, 14, 4, 7, 0],
              [10, 13, 19, 0, 0], [18, 13, 13, 7, 0]]))

cont4 = Container(
    np.array([[2, 19, 0, 0, 0], [15, 16, 0, 0, 0], [14, 16, 4, 7, 19],
              [10, 13, 0, 0, 0], [18, 13, 13, 7, 0]]))


res = best_first(cont)
res.render()

res = best_first(cont2)
res.render()

res = best_first(cont3)
res.render()

res = best_first(cont4)
res.render()

