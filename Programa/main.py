
import pygame, sys, os, random
from pygame.locals import *

frutas = [(9,5),(2,11),(8,18),(17,4),(13,19)] # ubicacion de las frutas
listMoves = [] # lista que contiene todos los movimientos que realizo la serpiente para comer todas las frutas (recorrido realizado)
listaManzanas = ["esfera.png", "esfera2.png", "esfera4.png", "esfera3.png", "esfera5.png"]
graff = {}
posHead = (0, 0)
lastOfUs = (17, 4)
flag = False
movs = 1
thyme = 0.0
proff = [(2, 11), (8, 18), (13, 19), (17, 4), (9, 5)]
rutasListas = 0
pantallazo = pygame.image.load("pantalla_de_game_over.png")
imgHead = [4,4,4,4,4,4,4,4,4,4,4,6,6,4,4,4,4,4,4,4,6,6,6,6,6,6,4,6,6,6,6,6,1,5,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,6,6,6,6,6,6,6,6]

# - - - - - - - - - - - - - - - - - - -
#           PARTE GRAFICA
# - - - - - - - - - - - - - - - - - - -

# Funcion principal que llama la parte visual del juego utilizando la lista de movimientos que se genero en la parte logica
def juego_prin():
    global movs, lista_Moves, rutasListas, flag
    pygame.init()  # se inicializa el pygame
    ventana = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)  # se crea una ventana nueva
    pygame.display.set_caption("Juego")
    fondo = pygame.image.load("fondo.png")  # se carga un fondo y se le aplica a la ventana
    reloj1 = pygame.time.Clock()
    datos_juego = pygame.image.load("score.jpg")
    cabezaiz = pygame.image.load("left.png")
    cabezader = pygame.image.load("right.png")
    cabezaup = pygame.image.load("up.png")
    cabezadown = pygame.image.load("down.png")

    pygame.mixer.music.load('cancion.mp3') # cancion de pantalla de juego
    pygame.mixer.music.play()

    LARGO = 35
    ALTO = 28  # se declaran algunas variables necesarias para el correcto funcionamiento del juego.
    MARGEN = 13
    matriz_logica = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    clock = pygame.time.Clock()
    timer = 0  # Decrease this to count down.
    dt = 0  # Delta time (time since last tick).
    def crear_matriz():
        global proff
        for x in range(18):
            for y in range(20):
                matriz_logica[x].append(3)  # llenar matriz con numeros aleatorios
        matriz_logica[0][0] = 1
        for i in proff:
            matriz_logica[i[0]][i[1]] = 2

    crear_matriz()

    def timer1(time):
        thyme = pygame.font.SysFont("Pokemon R/S Regular", 50)
        letras = thyme.render(str(round(time, 2)), True, (0, 0, 0))  # función que permite ver la puntación en pantalla
        ventana.blit(letras, [1099, 130])

    def movimientos():
        global movs
        cant_rest = pygame.font.SysFont("Pokemon R/S Regular",50)  # función que permite ver los movimientos restantes en pantalla
        movimiento = cant_rest.render(str(movs), True, (0, 0, 0))
        ventana.blit(movimiento, [1265, 130])

    def conseguirSig():
        global listMoves, rutasListas
        for i in listMoves:
            if i != []:
                tup = i
                del i
                return tup
            else:
                rutasListas += 1

    def cambiar(t1, t2):
        global movs, posHead, flag, imgHead
        #print(flag)
        if flag == True:
            matriz_logica[posHead[0]][posHead[1]] = 3
            matriz_logica[listMoves[0][0]][listMoves[0][1]] = 1
            del listMoves[0]
            ventana.blit(cabezadown, [(MARGEN + LARGO) * 4 + MARGEN, (MARGEN + ALTO) * 17 + MARGEN, LARGO, ALTO])
            pygame.display.update()
            global thyme
            thyme = timer
            pygame.mixer.stop()
            game_over(ventana, thyme, movs, pantallazo, reloj1)
            return
        n1, n2 = t1
        n3, n4 = t2
        if matriz_logica[n3][n4] == 2:
            matriz_logica[n3][n4] = 3
        n5 = matriz_logica[n3][n4]
        matriz_logica[n3][n4] = imgHead[0]
        matriz_logica[n1][n2] = n5
        del listMoves[0]
        del imgHead[0]
        movs += 1
        posHead = t2

    while True:
        i = 0
        ventana.blit(fondo, (0, 0))
        ventana.blit(datos_juego, (1060, 0))

        for fila in range(18):
            for columna in range(20):
                if matriz_logica[fila][columna] == 1:
                    ventana.blit(cabezaiz,[(MARGEN + LARGO) * columna + MARGEN, (MARGEN + ALTO) * fila + MARGEN, LARGO, ALTO])
                elif matriz_logica[fila][columna] == 2:
                    manzana = pygame.image.load(listaManzanas[i])
                    i = i + 1
                    ventana.blit(manzana,[(MARGEN + LARGO) * columna + MARGEN, (MARGEN + ALTO) * fila + MARGEN, LARGO, ALTO])
                elif matriz_logica[fila][columna] == 4:
                    ventana.blit(cabezader,[(MARGEN + LARGO) * columna + MARGEN, (MARGEN + ALTO) * fila + MARGEN, LARGO, ALTO])
                elif matriz_logica[fila][columna] == 5:
                    ventana.blit(cabezaup,[(MARGEN + LARGO) * columna + MARGEN, (MARGEN + ALTO) * fila + MARGEN, LARGO, ALTO])
                elif matriz_logica[fila][columna] == 6:
                    ventana.blit(cabezadown,[(MARGEN + LARGO) * columna + MARGEN, (MARGEN + ALTO) * fila + MARGEN, LARGO, ALTO])
        reloj1.tick(5)  # comandos para refrescar la pantalla
        timer += dt
        timer1(timer)
        dt = clock.tick(30) / 1000
        rutasListas = 0
        nextPos = conseguirSig()
        movimientos()
        print("Siguiente paso: " + str(nextPos))
        if nextPos == lastOfUs:
            flag = True
            cambiar(posHead, lastOfUs)
            pygame.display.update()
            global thyme
            thyme = timer
            pygame.display.update()
            game_over(ventana, thyme, movs, pantallazo, reloj1)
        cambiar(posHead, listMoves[0])
        pygame.display.update()

# función que acaba el juego, poniendo en pantalla el clasico "gameover" y dando una opcion de volver a juegar
#Funcion encargada de finalizar la ejecucion del juego
# ventana: la ventana donde se muestra el juego
# thyme: tiempo que tardo en comer todas las frutas a cierta velocidad dada
# moves: cantidad de movimientos en la que logro comer todos los objetivos
# pantallazo: imagen que pone opacado o el fondo inactivo para mostrar las letras de fin de juego
# reloj1: objeto que se encarga de llevar el tiempo, en esta funcion se detiene porque ya termino el juego
def game_over(ventana, thyme, moves, pantallazo, reloj1):
    texto = "Fin de Juego"
    texto2 = "Faltan 2 esferas del dragón, continuará..."
    looser = pygame.font.SysFont("Comic Sans MS",80)  # se carga e imprime en pantalla el mensaje de "fin de juego"
    texto2a = pygame.font.SysFont("Comic Sans MS",40)
    badluck = looser.render(texto, True, (255, 255, 255))
    texto2b = texto2a.render(texto2, True, (255, 255, 255))
    ventana.blit(pantallazo, (0, 0))
    ventana.blit(badluck, (320, 250))
    ventana.blit(texto2b, (140,360))
    #pygame.mixer.music.play()
    pygame.display.update()
    pygame.time.delay(4400)
    while True:
        # ciclo sin fin que refresca la pantalla y espera a que el jugador accione un evento de los programados.
        ventana.blit(pantallazo, (0, 0))
        ventana.blit(badluck, (320, 250))
        pygame.display.update()
        pygame.time.delay(5000)
        reloj1.tick(20)
        pygame.display.update()
        pygame.mixer.stop()
        print("\n# movimientos: "+str(moves) + "\nTiempo: " + str(thyme))
        pygame.quit()
        sys.exit()


# - - - - - - - - - - - - - - - - - - -
#           PARTE GRAFICA
# - - - - - - - - - - - - - - - - - - -

# Funcion encargada de la creacion/extraccion de los vecinos cercanos a la cabeza de la serpiente ubicada en la posicion (x,y)
# vecinos: lista en donde se almacenaran los vecinos de la posicion (x,y) recibidas por parametro
# x: fila en la que se encuentra la cabeza de la serpiente
# y: columna en la que se encuentra la cabeza de la serpiente
def sacarVecinos(vecinos,x,y):# recibe una lista que se va a cargar con los vecinos cercanos a la cabeza que va a estar en la pos (x,y)
    if (x != 0 and x != 17):
        if (y != 0 and y != 19):
            vecinos.append((x + 1, y))  # vecino de abajo
            vecinos.append((x - 1, y))  # vecino de arriba
            vecinos.append((x, y + 1))  # vecino de der
            vecinos.append((x, y - 1))  # vecino de izq
        elif (y == 0):
            vecinos.append((x-1, y)) # vecino de arriba
            vecinos.append((x+1, y)) # vecino de abajo
            vecinos.append((x, y+1)) # vecino de der
        else: #y == 19
            vecinos.append((x-1, y))  # vecino de arriba
            vecinos.append((x+1, y))  # vecino de abajo
            vecinos.append((x, y-1))  # vecino de izq
    elif (x == 0):
        if (y != 0 and y != 19):
            vecinos.append((x+1, y)) # vecino de abajo
            vecinos.append((x, y-1)) # vecino de izq
            vecinos.append((x, y+1)) # vecino de der
        elif (y == 0):
            vecinos.append((x+1,y)) # vecino de abajo
            vecinos.append((x,y+1)) # vecino de der
        else: # y == 19
            vecinos.append((x,y-1)) # vecino de izq
            vecinos.append((x+1, y)) # vecino de abajo
    else: #x == 17
        if (y != 0 and y != 19):
            vecinos.append((x-1, y)) # vecino de arriba
            vecinos.append((x, y-1)) # vecino de izq
            vecinos.append((x, y+1)) # vecino de der
        elif (y == 0):
            vecinos.append((x-1, y)) # vecino de arriba
            vecinos.append((x, y+1)) # vecino de der
        else: # y == 19
            vecinos.append((x-1, y)) # vecino de arriba
            vecinos.append((x, y-1)) # vecino de izq

# Funcion encargada del recorrido en profundidad de los vecinos
# x: posicion de fila actual de la cabeza
# y: posicion de columna actual de la cabeza
# vecinos: lista donde se almacenaran los vecinos cercanos a la posicion de la cabeza
# frutas: lista con las frutas restantes por comer
def profundidad(x,y, frutas):
    vecinos = [] # aqui se almacenan los vecinos cercanos a la posicion (x,y) esta lista es creada en cada llamada recursiva porque almacena los vecinos de la posicion actual de la cabeza de la serpiente
    sacarVecinos(vecinos,x,y)

    frutas = sacarDistanciasObjetivo(x,y,frutas) # devuelve las frutas ordenadas

    vecinos = sacarDistanciasObjetivo(frutas[0][0],frutas[0][1],vecinos) # me devuelve los vecinos ordenados de manera que el mas optimo esta en la pos 0

    if (x == frutas[0][0] and y == frutas[0][1]): # si me encuentro en la posicion de la fruta
        del frutas[0] # elimino la fruta de la pos 0 de la lista
    listMoves.append((x,y))
    if (len(frutas) == 0):
        return
    if (vecinos[0] in listMoves):
        del vecinos[0]

    vecinos = sacarDistanciasObjetivo(frutas[0][0], frutas[0][1], vecinos) # ordeno vecinos

    vecinoSig = vecinos[0]
    del vecinos[0]

    profundidad(vecinoSig[0],vecinoSig[1],frutas)  # llamo a profundidad con la nueva posicion de la cabeza


# Funcion que limpia una lista eliminando los elementos que contiene
# lista: lista vaciar (no dejar elementos dentro)
def clean(lista):
    for i in range(len(lista)):
        del lista[0]


# Funcion que calcula la cantidad de movimientos hacia un objetivo
# x: posicion x de origen (cabeza snake)
# y: posicion y de origen (cabeza snake)
# vecinos: lista con los vecinos del origen
def sacarDistanciasObjetivo(x,y,vecinos):
    listaOrdenada = [] #almacena --> (distancia a objetivo, pos x de vecino, pos y de vecino)
    listaFinal = []
    for vecino in vecinos:
        peso = 0
        if (vecino[0] >= x):
            peso = vecino[0] - x
        else:
            peso = x - vecino[0]
        if (vecino[1] >= y):
            peso += vecino[1] - y
        else:
            peso += y - vecino[1]
        listaOrdenada.append((peso,vecino[0],vecino[1])) # almaceno el vecino junto a la distancia del objetivo
    listaOrdenada.sort() # ordena las frutas por distancia mas corta
    for elemento in listaOrdenada:
        listaFinal.append((elemento[1],elemento[2]))
    clean(listaOrdenada) # libero la memoria de esa lista
    return listaFinal


# Funcion principal desde donde se ejecuta el programa
def main():
    profundidad(0,0,frutas) # la culebra inicia en la posicion (0,0)
    del listMoves[0] # la primer posicion no cuenta porque la culebra solo aparece ahi, no se tiene que mover para estar en la posicion (0,0) el primer movimiento es hacia un vecino
    #print(listMoves)

    print("Cantidad de movimientos: " + str(len(listMoves)))
    juego_prin()

main()
