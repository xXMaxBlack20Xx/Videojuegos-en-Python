import pgzrun
import math

#Estas constantes definen el tamaño de la ventana del juego.
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
#Establece el color de fuente en negro.
FONT_COLOR = (0, 0, 0)
#Establece el numero de huevos que se necesitan para ganas el juego.
EGG_TARGET = 20
#Establece la posicion del heroe al iniciar el juego.
HERO_START = (200, 300)
#Esta es la distancia en pixeles en la que un dragon puede atacar al heroe.
ATTACK_DISTANCE = 200
#Esta es la cantidad de segundos que los dragones permanecen despiertos.
DRAGON_WAKE_TIME = 2
#Establece la cantidad de segundos que los huevos estaran ocultos.
EDD_HIDE_TIME = 2
#Este es el numero de pixeles que se mueve el heroe por cada tecla oprimida.
MOVE_DISTANCE = 5

#Esta variable rastrea el numero de vidas restantes.
lives = 3 
#Rastrea el numeros de huevos recolectados.
eggs_collected = 0
#Esta variable rastrea si el juego ha terminado.
game_over = False
#Esta variable rastrea si el jugador ha ganado.
game_complete = False
reset_required = False

easy_lair = {
    #Estas son las coordenadas del dragon en esta guarida.
    "dragon": Actor("dragon-asleep", pos=(600, 100)),
    #esto establece las coordenadas de un huevo.
    "eggs": Actor("one-egg", pos=(400,100)),
    #Esto establece la cantidad de huevos para la guarida.
    "egg_count": 1,
    #Esto comprueba si el huevo esta actualmente escondido.
    "egg_hidden": False,
    #Esto rastrea cuantos segundos ha estado oculto el huevo.
    "egg_hide_counter": 0,
    #Esto rastrea el ciclo de sueño del dragon.
    "sleep_length": 10,
    "sleep_counter": 0,
    "wake_counter": 0
}

medium_lair = {
    #Estas son las coordenadas del dragon en esta guarida.
    "dragon": Actor("dragon-asleep", pos=(600, 300)),
    #esto establece las coordenadas de los huevos.
    "eggs": Actor("two-eggs", pos=(400,300)),
    #Esto establece la cantidad de huevos para la guarida.
    "egg_count": 2,
    #Esto comprueba si los huevos estan actualmente escondidos.
    "egg_hidden": False,
    #Esto rastrea cuantos segundos han estados ocultos los huevos.
    "egg_hide_counter": 0,
    #Esto rastrea el ciclo de sueño del dragon.
    "sleep_length": 7,
    "sleep_counter": 0,
    "wake_counter": 0
}

hard_lair = {
    #Estas son las coordenadas del dragon en esta guarida.
    "dragon": Actor("dragon-asleep", pos=(600, 500)),
    #esto establece las coordenadas de los huevos.
    "eggs": Actor("three-eggs", pos=(400,500)),
    #Esto establece la cantidad de huevos para la guarida.
    "egg_count": 3,
    #Esto comprueba si los huevos estan actualmente escondidos.
    "egg_hidden": False,
    #Esto rastrea cuantos segundos han estados ocultos los huevos.
    "egg_hide_counter": 0,
    #Esto rastrea el ciclo de sueño del dragon.
    "sleep_length": 4,
    "sleep_counter": 0,
    "wake_counter": 0
}

#Esta lista contiene todas las guaridas.
lairs = [easy_lair, medium_lair, hard_lair]

#Esto establece la posicion inicial del actor heroe.
hero = Actor("hero", pos=HERO_START)

def draw():
    global lairs, eggs_collected, lives, game_complete
    screen.clear()
    #Esto agrega un fondo al juego.
    screen.blit("dungeon", (0, 0)) 
    
    if game_over:
        screen.draw.text("YOU WON!", fontsize=60, center=CENTER, color=FONT_COLOR)
    else:
        hero.draw()
        draw_lairs(lairs)
        draw_counters(eggs_collected, lives)

def draw_lairs(lairs_to_draw):
    pass

def draw_counters(eggs_collected, lives):
    pass

pgzrun.go()

