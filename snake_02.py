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
        self.coordinates = coordinates
        self.coordinates_fruit = coordinates_fruit
        self.tile_size = tile_size
        self.field_size_x = field_size_x
        self.field_size_y = field_size_y
        self.number_of_moves_for_add_apple = number_of_moves_for_add_apple
        self.current_numbers_of_moves = current_numbers_of_moves
        self.speed = speed

snake = Game_state
snake.direction = (1, 0)
snake.enjoy = False
snake.alive = True
snake.status = 'game'  #  or 'gameover'
snake.coordinates = [(0, 0), (1, 0), (2, 0)]
snake.coordinates_fruit = [(1,1)]
snake.tile_size = 64  # x * x pixelu - članek hada, jablko
snake.field_size_x = 16
snake.field_size_y = 9
snake.number_of_moves_for_add_apple = 8  # po krerych se prida ovoce
snake.current_numbers_of_moves = 0
snake.speed = 0.8

snake_2 = Game_state  #




#souradnice = [(0, 0), (1, 0), (2, 0)]
#souradnice_ovoce = [(1,1)]
#tile_size = 64  # x * x pixels
#rozmer_hriste_x = 16
#rozmer_hriste_y = 9
#pocet_tahu = 6  # po krerych se prida ovoce
#aktualni_pocet_tahu = current_numbers_of_moves
#speed = 1.  # počáteční rychlost hada 1



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
    elif x1 + snake.field_size_x - 1 == x2: return 'right'
    # x odkud při pohybu mimo hřiště
    elif x1 == x2 + snake.field_size_x - 1: return 'left'
    
    # y pro kam při pohybu mimo hřiště
    elif y1 + snake.field_size_y - 1 == y2: return 'top'
    # y odkud při pohybu mimo hřiště
    elif y1 == y2 + snake.field_size_y - 1: return 'bottom'
    return 'error'


def draw_snake():
    window.clear()
    window.set_location(2, 34)
    score = len(snake.coordinates)
    label_score = pyglet.text.Label(f'Score: {score}             rychlost: {round(101 - snake.speed * 100)}', font_name = 'Terminus', font_size=30, x = window.width//8, y = window.height - 50)
    label_score.draw()
    
    # line under score
    glColor3f(1.0, 1.0, 1.0);  # nastaveni barvy pro kresleni
    glBegin(GL_LINES);         # nyni zacneme vykreslovat body
    glVertex2i( 0, window.height - 60);
    glVertex2i(window.width,  window.height - 60);
    glEnd();
    
    # draw snake
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    for a, b, c in zip(['tail'] + snake.coordinates, snake.coordinates, snake.coordinates[1:] + ['head']):
        x, y = b
        wherefrom = snake_article_calculation(a, b)
        where_to = snake_article_calculation(c, b)
        if where_to == 'head' and not snake.alive:
            where_to = 'dead'
        if where_to == 'head' and snake.enjoy:
            where_to = 'tongue'
            snake.enjoy = False
        snake_tiles[wherefrom + '-' + where_to].blit(x * snake.tile_size, y * snake.tile_size, width = snake.tile_size, height = snake.tile_size)
        
    # draw apples
    for x, y in snake.coordinates_fruit:
        apple_2.blit(x * snake.tile_size, y * snake.tile_size, width = snake.tile_size, height = snake.tile_size)
        #apple.draw()


''' původní jednoduché vykreslení '''
def draw_01():
    window.clear()
    for x, y in snake.coordinates:
        had.x = x * snake.tile_size
        had.y = y * snake.tile_size
        had.draw()
    for x, y in snake.coordinates_fruit:
        apple.x = x * snake.tile_size
        apple.y = y * snake.tile_size
        apple.draw()



def best_score():
    pass

def draw_game_over():
    label_game_over = pyglet.text.Label('game over', font_name = 'Terminus', font_size = 20, x = 2, y = 5)
    label_game_over.draw()
    pyglet.clock.unschedule(movement)


def draw():
    if snake.status == "game":
        draw_snake()
    else:
        # elifsnake.status == "gameover":
        draw_game_over()


def add_fruit():
    if (snake.field_size_x * snake.field_size_y) - (len(snake.coordinates) - len(snake.coordinates_fruit)) > 1:  # je misto pro ovoce ?
        i = 0
        while True:
            i += 1
            if i > 200:  # ať to tady dlouho netrvá - plynulost hry při hledání posledích míst
                #print('                    Nestihl najít ovoce, pokusů při hledání místa pro ovoce:', i)
                break            
            n, m = (randrange(0, snake.field_size_x), randrange(0, snake.field_size_y))
            if not (n, m) in snake.coordinates and not (n, m) in snake.coordinates_fruit:
                snake.coordinates_fruit.append((n, m))
                #print('pokusů ovoce:', i)
                break


def movement(t):    
    if not snake.alive:
        snake.status = "gameover"
        return    
    x, y = snake.coordinates[-1]
    x2, y2 = snake.direction
    new_coordinates = (x + x2, y + y2)
    
    # je had mimo hřiště ? , tak vyleze naproti
    if new_coordinates[1] == - 1:
        new_coordinates = new_coordinates[0] , snake.field_size_y - 1
    elif new_coordinates[1] == snake.field_size_y:
        new_coordinates = new_coordinates[0] , 0
    elif new_coordinates[0] == - 1:
        new_coordinates = snake.field_size_x - 1, new_coordinates[1]
    elif new_coordinates[0] == snake.field_size_x:
        new_coordinates = 0, new_coordinates[1]
    snake.coordinates.append(new_coordinates)  # had se posunuje, přidání nové souřadnice - hlava
    
    # co kdyby se kousl ?
    if snake.coordinates[-1] in snake.coordinates[:-2]:
        print(' Had se kousl a je ponim.')
        snake.alive = False
        return
    # a co jablko ?
    if snake.coordinates[-1] in snake.coordinates_fruit:  # Snědl jablko ?
        snake.enjoy = True  # vyplázene jazyk
        snake.speed *= 0.96  # zvýší rychlost hada po potravě
        print('snake.speed', snake.speed)
        pyglet.clock.unschedule(movement)  # ukončí smyčku událostí
        pyglet.clock.schedule_interval(movement, snake.speed)  # přidá novou smyčku a zvýší rychlost hada
        snake.coordinates.insert(0, snake.coordinates[0])  # had vyroste - ocas
        snake.coordinates_fruit.pop(snake.coordinates_fruit.index(snake.coordinates[-1]))  # vyjme snězené jablko ze seznamu
    snake.coordinates.pop(0)  # had se posunuje, takže odstranime poslední souřadnici
    # přidání ovoce po počtu_tahu
    if snake.current_numbers_of_moves % snake.number_of_moves_for_add_apple == 0:
        add_fruit()
    snake.current_numbers_of_moves += 1


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


window = pyglet.window.Window(width = snake.field_size_x * snake.tile_size, height = snake.field_size_y * snake.tile_size + 60, caption = 'Snake 2D')
label_snake = pyglet.text.Label(' Snake, neboli Had', font_name = 'Terminus', font_size=50, x = window.width//5, y=window.height//2.5)

window.push_handlers(
    on_draw = draw,  # na vykresleni okna pouzij funkci vykresli
    on_key_press = key_press,  # po stisknuti klavesy zavolej stisk_klavesy
    )

pyglet.clock.schedule_interval(movement, snake.speed)

pyglet.app.run()
