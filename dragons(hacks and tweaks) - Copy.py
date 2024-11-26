import pgzrun
import math
import random

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
ATTACK_DISTANCE = 230
#Esta es la cantidad de segundos que los dragones permanecen despiertos.
DRAGON_WAKE_TIME = 2
#Establece la cantidad de segundos que los huevos estaran ocultos.
EGG_HIDE_TIME = 2
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
    "sleep_length": 0,
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
    "sleep_length": 0,
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
    "sleep_length": 0,
    "sleep_counter": 0,
    "wake_counter": 0
}

#Esta lista contiene todas las guaridas.
lairs = [easy_lair, medium_lair, hard_lair]

#Esto establece la posicion inicial del actor heroe.
hero = Actor("niña", pos=HERO_START)

def draw():
    global lairs, eggs_collected, lives, game_complete
    screen.clear()
    #Esto agrega un fondo al juego.
    screen.blit("dungeon", (0, 0)) 
    
    if game_over:
        screen.draw.text("GAME OVER!", fontsize=60, center=CENTER, color=FONT_COLOR)
    elif game_complete:
        screen.draw.text("YOU WON!", fontsize=60, center=CENTER, color=FONT_COLOR)
    else:
        hero.draw()
        draw_lairs(lairs)
        draw_counters(eggs_collected, lives)

def draw_lairs(lairs_to_draw):
    #Esto itera por cada guarida.
    for lair in lairs_to_draw:
        #Esto dibuja un actor dragon para cada guarida.
        lair["dragon"].draw()
        if lair["egg_hidden"] is False:
            #Esto pinta los huevos de cada guarida si no estan ocultos actualmente.
            lair["eggs"].draw()

def draw_counters(eggs_collected, lives):
    #Esto dibuja un icono para representar el numero de huevos recolectados.
    screen.blit("egg-count", (0, HEIGHT - 30))
    screen.draw.text(str(eggs_collected),
                     fontsize=40,
                     pos=(30, HEIGHT - 30),
                     color=FONT_COLOR)
    #Esto dibuja un icono para representar la cantidad de vidas que le quedan al jugador.
    screen.blit("life-count", (60, HEIGHT - 30))
    screen.draw.text(str(lives),
                     fontsize=40,
                     pos=(90, HEIGHT - 30),
                     color=FONT_COLOR)
    
def update():
    if keyboard.right:
        hero.x += MOVE_DISTANCE
        if hero.x > WIDTH:
            hero.x = WIDTH
    elif keyboard.left:
        hero.x -= MOVE_DISTANCE
        if hero.x < 0:
            hero.x = 0
    elif keyboard.down:
        hero.y += MOVE_DISTANCE
        if hero.y > HEIGHT:
            hero.y = HEIGHT
    elif keyboard.up:
        hero.y -= MOVE_DISTANCE
        if hero.y < 0:
            hero.y = 0
    # if keyboard.d:
    #     hero2.x += MOVE_DISTANCE
    #     if hero2.x > WIDTH:
    #         hero2.x = WIDTH
    # elif keyboard.a:
    #     hero2.x -= MOVE_DISTANCE
    #     if hero2.x < 0:
    #         hero2.x = 0
    # elif keyboard.s:
    #     hero2.y += MOVE_DISTANCE
    #     if hero2.y > HEIGHT:
    #         hero2.y = HEIGHT
    # elif keyboard.w:
    #     hero2.y -= MOVE_DISTANCE
    #     if hero2.y < 0:
    #         hero2.y = 0
    check_for_collisions()
    
def update_lairs():
    global lairs, hero, lives
    #Esto recorre las tres guaridas.
    for lair in lairs:
        #Este bloque animará al dragón.
        if lair["dragon"].image == "dragon-asleep":
            #Esto es llamado si el dragón está dormido.
            update_sleeping_dragon(lair)
        elif lair["dragon"].image == "dragon-awake":
            #Esto es llamado si el dragón está despierto.
            update_waking_dragon(lair)
        #Esto animara los blanquillos.
        update_egg(lair)
        
#Esta función programa una llamada a otra función en intervalos regulares.
clock.schedule_interval(update_lairs, 1) #El número de segundos entre cada llamada a la función se puede cambiar actualizando este número.
    
def update_sleeping_dragon(lair):
    #Esto comprueba si sleep_counter es mayor o igual a sleep_length.
    if lair["sleep_counter"] >= lair["sleep_length"]:
        if random.choice([True, False]):
            lair["dragon"].image = "dragon-awake"
            #Esto reincia el sleep_counter del dragon a cero.
            lair["sleep_counter"] = 0
    else:
        #Esto incrementa el sleep_counter en 1.
        lair["sleep_counter"] += 1

def update_waking_dragon(lair):
    #Esto comprueba si el dragon ha estado despierto el tiempo suficiente.
    if lair["wake_counter"] >= DRAGON_WAKE_TIME:
        #Esto actualiza la imagen del dragon.
        lair["dragon"].image = "dragon-asleep"
        #Esto restablece el wake_counter del dragon a cero.
        lair["wake_counter"] = 0
    else:
        #Esto suma uno a wake_counter.
        lair["wake_counter"] += 1

#Esta funcion comprueba si algún huevo debe permanecer oculto o no.
def update_egg(lair):
    if lair["egg_hidden"] is True:
        #Este bloque se ejecuta si algún huevo ha estado oculto el tiempo suficiente.
        if lair["egg_hide_counter"] >= EGG_HIDE_TIME:
            lair["egg_hidden"] = False
            lair["egg_hide_counter"] = 0
        else:
            #Esto suma uno al egg_hide_counter.
            lair["egg_hide_counter"] += 1

def check_for_collisions():
    global lairs, eggs_collected, lives, reset_required, game_complete
    for lair in lairs:
        if lair["egg_hidden"] is False:
            #Está función es llamada si los huevos no estan ocultos.
            check_for_egg_collision(lair)
        #Esto asegura que el jugador no pierda una vida cuando el héroe regresa a la posición inicial.
        if lair["dragon"].image == "dragon-awake" and reset_required is False:
            #Está función es llamada si el dragón está despierto y la posición del héroe no se restablece.
            check_for_dragon_collision(lair)
    
def check_for_dragon_collision(lair):
    #Esto calcula las distancias horizontales y verticales entre el dragón y el héroe.
    x_distance = hero.x - lair["dragon"].x
    y_distance = hero.y - lair["dragon"].y
    #Esto encuentra la distancia entre el dragón y el héroe en una linea recta.
    distance = math.hypot(x_distance, y_distance)
    if distance < ATTACK_DISTANCE:
        #Esta función se llama si la distancia entre el héroe y el dragón es menor que ATTACK_DISTANCE.
        handle_dragon_collision()
        
def handle_dragon_collision():
    global reset_required
    reset_required = True
    #Está función se llama cuando se completa la animación.
    animate(hero, pos=HERO_START, on_finished=subtract_life)
    
def check_for_egg_collision(lair):
    global eggs_collected, game_complete
    if hero.colliderect(lair["eggs"]):
        lair["egg_hidden"] = True
        #Esto suma la cantidad de huevos de la guarida actual al recuento de huevos del jugador.
        eggs_collected += lair["egg_count"]
        #Esto compueba si el número de huevos recolectados es mayor o igual que EGG_TARGET
        if eggs_collected >= EGG_TARGET:
            game_complete = True
    
def subtract_life():
    global lives, reset_required, game_over
    lives -= 1
    if lives == 0:
        game_over = True
    #Esta variable se establece en False, ya que el héroe se encuentra en la posición inicial.
    reset_required = False
    
pgzrun.go()

