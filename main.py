import pygame
import random
import math
import datetime 
from pygame import mixer

# Inicializar pygame
pygame.init()

#Crear la pantalla 
pantalla = pygame.display.set_mode((800, 600))

# Título e icono
pygame.display.set_caption("Un día en el campo")
icono = pygame.image.load("zanahoria_doble.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("bosque.png")

# Agregar musica

mixer.music.load('soundlings.mp3')
mixer.music.set_volume(0.012)
mixer.music.play(-1)

# Variables del jugador

img_jugador = pygame.image.load("conejo.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0


# Variables del enemigo

img_enemigo = pygame.image.load("jabali.png")
enemigo_x = random.randint(0, 736)
enemigo_y = random.randint(50, 200)
enemigo_x_cambio = 1
enemigo_y_cambio = 50


# Variables de la explosion
img_explosion = pygame.image.load("explosion.png")
explosion_x = 0
explosion_y = 0
enemigo_alcanzado = False
duracion_explosion = datetime.timedelta(seconds=1)

# Variables de la bala 

img_bala = pygame.image.load("zanahoria1.png")
bala_x = 0
bala_y = 500 
bala_x_cambio = 0
bala_y_cambio = 2
bala_visible = False

# Variables de mensajes

puntuacion = 0
global no_hay_mas_vidas
no_hay_mas_vidas = False

# por defecto pygame solo trae esta fuente
# fuente = pygame.font.Font('freesansbold.ttf', 32)
fuente = pygame.font.Font('AliceandtheWickedMonster.ttf', 45)
texto_x = 10
texto_y = 10

fuente_final = pygame.font.Font('AliceandtheWickedMonster.ttf', 100)
mi_fuente_final = fuente_final.render("THE END", True, (255, 255, 255))




# funcion puntuacion

def mostrar_puntuacion(x,y):
    texto = fuente.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))



# funcion jugador

def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# funcion enemigo

def enemigo(x, y):
    pantalla.blit(img_enemigo, (x+16, y+10))

def crear_explosion(x, y, img=img_explosion):
    global enemigo_alcanzado
    enemigo_alcanzado = True
    pantalla.blit(img_explosion, (x, y))



# funcion disparar bala

def disparar_bala(x, y):
    global bala_visible 
    bala_visible = True
    pantalla.blit(img_bala, (x, y))


# Distancia de la colision:
# D = srqt((x2 - x1)**2 + (y2 - y1)**2)

# Funcion detectar colisiones

def hay_colision(x_1, x_2, y_1, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2)+ math.pow(y_1 - y_2, 2))
    if distancia < 50:
        return True
    else:
        return False


def fin_de_explosion(tiempo_inicio, tiempo_actual):
    if tiempo_actual - tiempo_inicio >= duracion_explosion:
        return True
    return False

def partida_terminada():
    pantalla.blit(mi_fuente_final, (150, 200))




# Loop de juego
se_ejecuta = True

while se_ejecuta:

    # image de fondo 
    #pantalla.fill((205, 144, 228))
    pantalla.blit(fondo, (0,0))
    
    for evento in pygame.event.get():

        # evento cerrar 

        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # evento presionar teclas

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                #print("flecha izquierda presionada")
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                #print("flecha derecha presionada")
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                shooting_sound = mixer.Sound('flop.mp3')
                shooting_sound.set_volume(0.1)
                shooting_sound.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        


        # evento soltar flechas

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                #print("la tecla fue soltada")
                jugador_x_cambio = 0


    # modificar ubicacion jugador 
    jugador_x += jugador_x_cambio
    jugador(jugador_x, jugador_y)
    enemigo(enemigo_x, enemigo_y)
    mostrar_puntuacion(texto_x, texto_y)

    #disparar_bala(bala_x, bala_y)

    # mantener dentro de bordes al jugador 

    if jugador_x <= 0:
        jugador_x = 0
    
    if jugador_x >= 736:
        jugador_x = 736
    

    # modificar ubicacion enemigo 
    enemigo_x += enemigo_x_cambio
    enemigo(enemigo_x, enemigo_y)
    enemigo(enemigo_x, enemigo_y)


    # fin del juego

    if enemigo_y > 500:
        enemigo_x = -1000
        enemigo_y = -1000 
        enemigo(enemigo_x, enemigo_y)
        print("BAJÓ AL LÍMITE")
        if not enemigo_alcanzado:  # Solo termina si el enemigo no fue alcanzado
            no_hay_mas_vidas = True
        
        
    if no_hay_mas_vidas:
        partida_terminada()

        

    # mantener dentro de bordes al enemigo 

    if enemigo_x <= 0:
        enemigo_x_cambio = 1
        enemigo_y += enemigo_y_cambio

    
    if enemigo_x >= 736:
        enemigo_x_cambio = -1
        enemigo_y += enemigo_y_cambio

    # movimiento bala dentro de bordes
    if bala_y <= -32:
        bala_y = 600
        bala_visible = False

    # modificar ubicacion bala 

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    # colision

    if hay_colision(bala_x, enemigo_x, bala_y, enemigo_y):
        puntuacion += 1 
        global tiempo_alc
        tiempo_alcance = datetime.datetime.now()
        bala_y = 500
        bala_visible = False
        explosion_x = enemigo_x
        explosion_y = enemigo_y
        # Hacemos desaparecer al enemigo
        shooting_sound = mixer.Sound('boing.mp3')
        shooting_sound.set_volume(0.1)
        shooting_sound.play()
        enemigo_x = -1000
        enemigo_y = -1000
        # Mostramos explosion
        crear_explosion(explosion_x, explosion_y)


    if enemigo_alcanzado:

        tiempo_actual = datetime.datetime.now()
        crear_explosion(explosion_x, explosion_y)

        # Pasados unos segundos, desaparece la explosion y creamos un nuevo enemigo.

        if fin_de_explosion(tiempo_alcance, tiempo_actual):
            enemigo_alcanzado = False
            enemigo_x = random.randint(0, 736)
            enemigo_y = random.randint(50, 200)


    
    # actualizar
    pygame.display.update()





