import pyglet
import time
from pyglet.gl import *  # pořád mi to nešlo až s hvězdičkou
from pyglet.window import key
from random import randrange
from pathlib import Path


class Game_state:
    def __init__(self):
        self.direction = direction
        self.enjoy = enjoy
        self.alive = alive
        self.status = status
    
snake = Game_state
snake.direction = (1, 0)
snake.enjoy = False
snake.alive = True
snake.status = 'game'  #  nebo 'gameover'


souradnice = [(0, 0), (1, 0), (2, 0)]
souradnice_ovoce = [(1,1)]
tile_size = 64  # x * x pixels
rozmer_hriste_x = 16
rozmer_hriste_y = 9

pocet_tahu = 6  # po krerych se prida ovoce
aktualni_pocet_tahu = pocet_tahu
speed = 1.  # počáteční rychlost hada 1
#set_speed = speed


obrazek = pyglet.image.load('green.png')
had = pyglet.sprite.Sprite(obrazek)
obrazek = pyglet.image.load('apple.png')
apple = pyglet.sprite.Sprite(obrazek)
apple_2 = pyglet.image.load('apple.png')


''' načtení souboru s obrázy části hada '''
TILES_DIRECTORY = Path('snake-tiles')
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)


def snake_article_calculation(a, b):
    if a == 'tail' or a == 'head': return a
    x1, y1 = a
    x2, y2 = b
    if x1 == x2 - 1: return 'left'
    elif x1 == x2 + 1: return 'right'
    elif y1 == y2 - 1: return 'bottom'
    elif y1 == y2 + 1: return 'top'
    
    # x pro kam při pohybu mimo hřiště
    elif x1 + rozmer_hriste_x - 1 == x2: return 'right'
    # x odkud při pohybu mimo hřiště
    elif x1 == x2 + rozmer_hriste_x - 1: return 'left'
    
    # y pro kam při pohybu mimo hřiště
    elif y1 + rozmer_hriste_y - 1 == y2: return 'top'
    # y odkud při pohybu mimo hřiště
    elif y1 == y2 + rozmer_hriste_y - 1: return 'bottom'

    return 'error'


def draw_snake():
    window.clear()
    score = len(souradnice)
    label_score = pyglet.text.Label(f'Score: {score}             rychlost: {round(101 - speed * 100)}', font_name = 'Terminus', font_size=30, x = window.width//8, y = window.height - 50)
    label_score.draw()
    
    # line under score
    glColor3f(1.0, 1.0, 1.0);  # nastaveni barvy pro kresleni
    glBegin(GL_LINES);         # nyni zacneme vykreslovat body
    glVertex2i( 0, window.height - 60);
    glVertex2i(window.width,  window.height - 60);
    glEnd();
    
    # draws snake
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    for a, b, c in zip(['tail'] + souradnice, souradnice, souradnice[1:] + ['head']):
        x, y = b
        wherefrom = snake_article_calculation(a, b)
        where_to = snake_article_calculation(c, b)
        if where_to == 'head' and not snake.alive:
            where_to = 'dead'
        if where_to == 'head' and snake.enjoy:
            where_to = 'tongue'
            snake.enjoy = False
        snake_tiles[wherefrom + '-' + where_to].blit(x * tile_size, y * tile_size, width = tile_size, height = tile_size)
        
    # draw apples
    for x, y in souradnice_ovoce:
        apple_2.blit(x * tile_size, y * tile_size, width = tile_size, height = tile_size)
        #apple.draw()


''' původní jednoduché vykreslení '''
def draw_01():
    window.clear()
    for x, y in souradnice:
        had.x = x * tile_size
        had.y = y * tile_size
        had.draw()
    for x, y in souradnice_ovoce:
        apple.x = x * tile_size
        apple.y = y * tile_size
        apple.draw()



def vysledky():
    pass

def draw_game_over():
    label_game_over = pyglet.text.Label('game over', font_name = 'Terminus', font_size = 20, x = 2, y = 5)
    label_game_over.draw()
    pyglet.clock.unschedule(movement)

#window.push_handlers(on_text = text)






def draw():
    if snake.status == "game":
        draw_snake()
    else:
        # elifsnake.status == "gameover":
        draw_game_over()


'''
def draw_game_over():
        #label_score = pyglet.text.Label('game over', font_name = 'Terminus', font_size = 20, x = 2, y = 5)
        #label_score.draw()
        startTime = time.time()
        while (time.time() - startTime) <= 3:  # pauza 3 sekundy
            pass

def draw():
    #maximize()
    #pyglet.set_location( 20 , 10 )
    if snake.status == "game":
        draw_snake()
       # draw_01()
    else:
        # elif snake.status == "gameover":
        draw_game_over()
'''

def add_fruit():
    if (rozmer_hriste_x * rozmer_hriste_y) - (len(souradnice) - len(souradnice_ovoce)) > 1:  # je misto pro ovoce ?
        i = 0
        while True:
            i += 1
            if i > 200:  # ať to tady dlouho netrvá - plynulost hry při hledání posledích míst
                #print('                    Nestihl najít ovoce, pokusů při hledání místa pro ovoce:', i)
                break            
            n, m = (randrange(0, rozmer_hriste_x), randrange(0, rozmer_hriste_y))
            if not (n, m) in souradnice and not (n, m) in souradnice_ovoce:
                souradnice_ovoce.append((n, m))
                #print('pokusů ovoce:', i)
                break


def movement(t):
    global speed, aktualni_pocet_tahu
    if not snake.alive:
        snake.status = "gameover"
        return    
    x, y = souradnice[-1]
    x2, y2 = snake.direction
    new_coordinates = (x + x2, y + y2)
    
    # je had mimo hřiště ? , tak vyleze naproti
    if new_coordinates[1] == - 1:
        new_coordinates = new_coordinates[0] , rozmer_hriste_y - 1
    elif new_coordinates[1] == rozmer_hriste_y:
        new_coordinates = new_coordinates[0] , 0
    elif new_coordinates[0] == - 1:
        new_coordinates = rozmer_hriste_x - 1, new_coordinates[1]
    elif new_coordinates[0] == rozmer_hriste_x:
        new_coordinates = 0, new_coordinates[1]
    souradnice.append(new_coordinates)  # had se posunuje, přidání nové souřadnice - hlava
    
    # co kdyby se kousl ?
    if souradnice[-1] in souradnice[:-2]:
        print(' Had se kousl a je ponim.')
        snake.alive = False
        return
    # a co jablko ?
    if souradnice[-1] in souradnice_ovoce:  # Snědl jablko ?
        snake.enjoy = True  # vyplázene jazyk
        speed *= 0.96  # zvýší rychlost hada po potravě
        print('speed', speed)
        pyglet.clock.unschedule(movement)  # ukončí smyčku událostí
        pyglet.clock.schedule_interval(movement, speed)  # přidá novou smyčku a zvýší rychlost hada
        souradnice.insert(0, souradnice[0])  # had vyroste - ocas
        souradnice_ovoce.pop(souradnice_ovoce.index(souradnice[-1]))  # vyjme snězené jablko ze seznamu
    souradnice.pop(0)  # had se posunuje, takže odstranime poslední souřadnici
    # přidání ovoce po pocet_tahu    
    if aktualni_pocet_tahu % pocet_tahu == 0:
        add_fruit()
    aktualni_pocet_tahu += 1


def key_press(symbol, modifiers):
    if symbol == key.UP:
        if snake.direction != (0, -1):
            snake.direction = (0, 1)
    if symbol == key.DOWN:
        if snake.direction != (0, 1):
            snake.direction = (0, -1)
    if symbol == key.LEFT:
        if snake.direction != (1, 0):
            snake.direction = (-1, 0)
    if symbol == key.RIGHT:
        if snake.direction != (-1, 0):
            snake.direction = (1, 0)


window = pyglet.window.Window(width = rozmer_hriste_x * tile_size, height = rozmer_hriste_y * tile_size + 60, caption = 'Snake 2D')
label_snake = pyglet.text.Label(' Snake, neboli Had', font_name = 'Terminus', font_size=50, x = window.width//5, y=window.height//2.5)

window.push_handlers(
    on_draw = draw,  # na vykresleni okna pouzij funkci vykresli
    on_key_press = key_press,  # po stisknuti klavesy zavolej stisk_klavesy
    )

pyglet.clock.schedule_interval(movement, speed)

pyglet.app.run()
