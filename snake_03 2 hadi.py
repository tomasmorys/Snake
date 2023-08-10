import pyglet
import time
from pyglet import gl
from pyglet.gl import *  # pořád mi to nešlo až s hvězdičkou
from pyglet.window import key
from random import randrange
from pathlib import Path


class Snake():
    def __init__(self):
        self.direction = (1,0)
        self.enjoy = False
        self.alive = True        
        self.coordinates = (0, 0)
        self.speed = 1
        self.snake_tiles = {}

    def move_snake_number(self):
        x, y = self.coordinates[-1]
        x2, y2 = self.direction
        new_coordinates = (x + x2, y + y2)
        # je had mimo hřiště ? , tak vyleze naproti
        if new_coordinates[1] == - 1:
            new_coordinates = new_coordinates[0] , game.area_size_y - 1
        elif new_coordinates[1] == game.area_size_y:
            new_coordinates = new_coordinates[0] , 0
        elif new_coordinates[0] == - 1:
            new_coordinates = game.area_size_x - 1, new_coordinates[1]
        elif new_coordinates[0] == game.area_size_x:
            new_coordinates = 0, new_coordinates[1]
        self.coordinates.append(new_coordinates)  # had se posunuje, přidání nové souřadnice - hlava    
        # co kdyby se kousl ?
        if self.coordinates[-1] in self.coordinates[:-2]:
            print(' Had se kousl a je ponim.')
            self.alive = False
            return
        if self.coordinates[-1] in game.coordinates_number.keys():            
            if game.result ==  game.coordinates_number[self.coordinates[-1]]:  # je na správném čísle ?
                print('správně', game.result, game.coordinates_number[self.coordinates[-1]])
                self.enjoy = True  # vyplázene jazyk
                self.speed *= 0.98  # zvýší rychlost hada po potravě
                self.coordinates.insert(0, self.coordinates[0])  # had vyroste - ocas
                del game.coordinates_number[self.coordinates[-1]]  # vyjme číslo ze slovníku
                game.new_number()
            else:
                print('špatné číslo !!!')
                pass
        self.coordinates.pop(0)  # had se posunuje, takže odstranime poslední souřadnici

        
    def move_snake(self):
        if not self.alive:
            print('uř je ponim')
            return
        x, y = self.coordinates[-1]
        x2, y2 = self.direction
        new_coordinates = (x + x2, y + y2)
    
        # je had mimo hřiště ? , tak vyleze naproti
        if new_coordinates[1] == - 1:
            new_coordinates = new_coordinates[0] , game.area_size_y - 1
        elif new_coordinates[1] == game.area_size_y:
            new_coordinates = new_coordinates[0] , 0
        elif new_coordinates[0] == - 1:
            new_coordinates = game.area_size_x - 1, new_coordinates[1]
        elif new_coordinates[0] == game.area_size_x:
            new_coordinates = 0, new_coordinates[1]
            
        # co kdyby se kousl ?
        if self.coordinates[-1] in self.coordinates[:-2]:
            print(' Had se kousl a je ponim.')
            self.alive = False
            return
        self.coordinates.append(new_coordinates)  # had se posunuje, přidání nové souřadnice - hlava
        # a co jablko ?
        if self.coordinates[-1] in game.coordinates_fruit:  # Snědl jablko ?
            self.enjoy = True  # vyplázene jazyk
            self.speed *= 0.9  # zvýší rychlost hada po potravě
            print('snake.speed', snake.speed, ' 2: ', snake2.speed)
#            pyglet.clock.unschedule(movement)  # ukončí smyčku událostí
#            pyglet.clock.schedule_interval(movement, snake.speed)  # přidá novou smyčku a zvýší rychlost hada
            self.coordinates.insert(0, self.coordinates[0])  # had vyroste - ocas
            game.coordinates_fruit.pop(game.coordinates_fruit.index(self.coordinates[-1]))  # vyjme snězené jablko ze seznamu
        self.coordinates.pop(0)  # had se posunuje, takže odstranime poslední souřadnici


    def draw_snake_number(self):
        # vypis zadání
        v = game.label_task
        label_task = pyglet.text.Label(f'  {v}', font_name = 'Terminus', font_size = 24, x = 20, y = window.height - 40)
        label_task.draw()
        # line under score
        gl.glColor3f(1.0, 1.0, 1.0);  # nastaveni barvy pro kresleni
        gl.glBegin(GL_LINES);         # nyni zacneme vykreslovat body
        gl.glVertex2i( 0, window.height - 60);
        gl.glVertex2i(window.width,  window.height - 60);
        gl.glEnd();
        # draw snake
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        for a, b, c in zip(['tail'] + self.coordinates, self.coordinates, self.coordinates[1:] + ['head']):
            x, y = b
            move_from = snake_article_calculation(a, b)
            move_to = snake_article_calculation(c, b)
            if move_to == 'head' and not self.alive:
                move_to = 'dead'
            if move_to == 'head' and self.enjoy:
                move_to = 'tongue'
                self.enjoy = False
            self.snake_tiles[move_from + '-' + move_to].blit(x * game.tile_size, y * game.tile_size, width = game.tile_size, height = game.tile_size)
        # vypiš čísla
        for key, value in game.coordinates_number.items():
            x, y = key
            label_number = pyglet.text.Label(f'{value}', font_name = 'Terminus', font_size = 40, x = x * game.tile_size, y = 10 + y * game.tile_size)
            label_number.draw()


    def draw_snake(self):
        # line under score
        gl.glColor3f(1.0, 1.0, 1.0);  # nastaveni barvy pro kresleni
        gl.glBegin(GL_LINES);         # nyni zacneme vykreslovat body
        gl.glVertex2i( 0, window.height - 60);
        gl.glVertex2i(window.width,  window.height - 60);
        gl.glEnd();
        # draw snake
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        for a, b, c in zip(['tail'] + self.coordinates, self.coordinates, self.coordinates[1:] + ['head']):
            x, y = b
            move_from = snake_article_calculation(a, b)
            move_to = snake_article_calculation(c, b)
            if move_to == 'head' and not self.alive:
                move_to = 'dead'
            if move_to == 'head' and self.enjoy:
                move_to = 'tongue'
                self.enjoy = False
            self.snake_tiles[move_from + '-' + move_to].blit(x * game.tile_size, y * game.tile_size, width = game.tile_size, height = game.tile_size)
        # draw fruit
        for x, y in game.coordinates_fruit:
            apple_2.blit(x * game.tile_size, y * game.tile_size, width = game.tile_size, height = game.tile_size)


class Game_state(Snake):
    def initialize(self):
        self.tile_size = 64  # x * x pixelu - članek hada, jablko
        self.area_size_x = 16  # velikost hřiště
        self.area_size_y = 9
        self.number_of_moves_for_add_apple = 8  # po krerych se prida ovoce
        self.number_of_moves_for_add_number = 5
        self.current_numbers_of_moves = 0  # celkový počet tahů
        self.state = 'main_screen'  # game_snake, game_snake_2, game_number, game_over, main_screen
        self.coordinates_fruit = [(1, 1)]
        self.coordinates_number = {(0, 0): 19, (15, 0): 18, (0, 8): 10}
        self.result = 19
        self.label_task = '10 + 9'
        # smazat self.snake_1 = True
        self.time = time.time()
        


    def new_number(self):
        game.result = randrange(2, 21)
        n1 = game.result - randrange(1, game.result)
        n2 = game.result - n1
        self.label_task = str(n1)+  ' + ' + str(n2)
        print('result:', game.result, ' : ', str(n1)+  ' + ' + str(n2))

        # přidání čísel k výběru
        game.coordinates_number.clear()
        n = 5
        for i in range(n):
            x = randrange(0, game.area_size_x)
            y = randrange(0, game.area_size_y)
            game.coordinates_number[x, y] = randrange(2, game.result + 1)
            if i == n - 1:
                game.coordinates_number[x, y] = game.result
        print(game.coordinates_number)
        print(' - - - - - - - - - - - ')
        #label_task = pyglet.text.Label(self.label_task, font_name = 'Terminus', font_size = 24, x = 20, y = window.height - 40)
        #label_task.draw()


        
    def add_fruit(self):
# zde je použito snake.coordinates na misto self.coordinates - co s tím ???        
        if (self.area_size_x * self.area_size_y) - (len(snake.coordinates) + len(snake2.coordinates) + len(self.coordinates_fruit)) > 5:  # je misto pro ovoce ?
            i = 0            
            while True:
                i += 1
                if i > 100:  # ať to tady dlouho netrvá - plynulost hry při hledání posledích míst
                    print('                    Nestihl najít ovoce, pokusů při hledání místa pro ovoce:', i)
                    break            
                n, m = (randrange(0, game.area_size_x), randrange(0, game.area_size_y))
# zde je použito snake.coordinates na misto self.coordinates - co s tím ???
                if (n, m) not in snake.coordinates and (n, m) not in snake2.coordinates and (n, m) not in self.coordinates_fruit:
                    self.coordinates_fruit.append((n, m))
                    break


    def draw_game_over(self):
        label_game_over = pyglet.text.Label('game over', font_name = 'Terminus', font_size = 20, x = 2, y = 5)
        label_game_over.draw()
        # ? pyglet.clock.unschedule(movement)


game = Game_state()
game.initialize()

snake = Snake()
snake.direction = (1, 0)
snake.enjoy = False
snake.alive = True
snake.coordinates = [(0, 0), (1, 0), (2, 0)]
snake.speed = 1
TILES_DIRECTORY = Path('snake-tiles')  # načtení souboru s obrázy části hada
for path in TILES_DIRECTORY.glob('*.png'):
    snake.snake_tiles[path.stem] = pyglet.image.load(path)

snake2 = Snake()
snake2.direction = (1, 0)
snake2.enjoy = False
snake2.alive = True
snake2.coordinates = [(0, 3), (1, 3), (2, 3)]
snake2.speed = 1
TILES_DIRECTORY = Path('snake-tiles-2')  # načtení souboru s obrázy části druhého hada
for path in TILES_DIRECTORY.glob('*.png'):
    snake2.snake_tiles[path.stem] = pyglet.image.load(path)

obrazek = pyglet.image.load('green.png')
had = pyglet.sprite.Sprite(obrazek)
obrazek = pyglet.image.load('apple.png')
apple = pyglet.sprite.Sprite(obrazek)
apple_2 = pyglet.image.load('apple.png')


def snake_article_calculation(a, b):
    if a == 'tail' or a == 'head': return a
    x, y = a
    x2, y2 = b
    if x == x2 - 1: return 'left'
    elif x == x2 + 1: return 'right'
    elif y == y2 - 1: return 'bottom'
    elif y == y2 + 1: return 'top'
    
    # x pro kam při pohybu mimo hřiště
    elif x + game.area_size_x - 1 == x2: return 'right'
    # x odkud při pohybu mimo hřiště
    elif x == x2 + game.area_size_x - 1: return 'left'
    
    # y pro kam při pohybu mimo hřiště
    elif y + game.area_size_y - 1 == y2: return 'top'
    # y odkud při pohybu mimo hřiště
    elif y == y2 + game.area_size_y - 1: return 'bottom'
    return 'error'


def best_score():
    pass


def draw():  # game_snake, game_snake_2, game_number, game_over, main_screen
#    window.set_location(2, 34)
    if game.state == 'main_screen':
        window.clear()
        label_snake.draw()        
        label_score = pyglet.text.Label(f' J - hra had', font_name = 'Terminus', font_size = 20, x = 20, y = window.height - 40)
        label_score.draw()
        label_score = pyglet.text.Label(f' D - hra pro dva hráče', font_name = 'Terminus', font_size = 20, x = 20, y = window.height - 80)
        label_score.draw()
        label_score = pyglet.text.Label(f' N - hra s čísly', font_name = 'Terminus', font_size = 20, x = 20, y = window.height - 120)
        label_score.draw()
    if game.state == 'game_snake':
        window.clear()
        label_snake.draw()
        # smazat game.snake_1 = True
        snake.draw_snake()
        at = time.time() - game.time
        score = round(300 * (len(snake.coordinates) - 3) / at)
        label_score = pyglet.text.Label(f'Score hada:  {score}', font_name = 'Terminus', font_size = 24, x = 20, y = window.height - 40)
        label_score.draw()
    elif game.state == 'game_snake_2':
        window.clear()
        label_snake.draw()
        # prvni had        
        # smazat game.snake_1 = True
        snake.draw_snake()
        at = time.time() - game.time
        score = round(300 * (len(snake.coordinates) - 3) / at)
        label_score = pyglet.text.Label(f'Score had1: {score}', font_name = 'Terminus', font_size = 24, x = 20, y = window.height - 40)
        label_score.draw()
#        label_score = pyglet.text.Label(f'Score had1:  {len(snake.coordinates)}    rychlost: {round(101 - snake.speed * 100)}', font_name = 'Terminus', font_size = 24, x = 20, y = window.height - 40)
#        label_score.draw()
        # druhy had
        # smazat game.snake_1 = False
        snake2.draw_snake()
#        label_score = pyglet.text.Label(f'Score had2:  {len(snake2.coordinates)}    rychlost: {round(101 - snake2.speed * 100)}', font_name = 'Terminus', font_size = 24, x = 570, y = window.height - 40)
#        label_score.draw()
    elif game.state == 'game_number':
        window.clear()
        #label_snake.draw()
        snake.draw_snake_number()
    elif game.state == 'game_over':
        game.draw_game_over()

def movement_snake_number(t):
    if not snake.alive:
        game.state = 'game_over'
        pyglet.clock.unschedule(movement_snake_number)
        return
    snake.move_snake_number()
    pyglet.clock.schedule_once(movement_snake_number, snake.speed)


def movement_snake(t):
    if not snake.alive:
        game.state = 'game_over'
        pyglet.clock.unschedule(movement_snake)  ###############
        return
    pyglet.clock.schedule_once(movement_snake, snake.speed)
    snake.move_snake()
    # přidání ovoce po počtu_tahu
    if game.current_numbers_of_moves % game.number_of_moves_for_add_apple == 0:
        game.add_fruit()
    game.current_numbers_of_moves += 1


def movement_snake_1(t):
    if not snake.alive or not snake2.alive:
        game.state = 'game_over'
        return
    snake.move_snake()
    pyglet.clock.schedule_once(movement_snake_1, snake.speed)
    if snake.coordinates[-1] in snake2.coordinates:
        print('První Had kousl do druhého a je ponich.')
        snake.alive = False
    # přidání ovoce po počtu_tahu
    if game.current_numbers_of_moves % game.number_of_moves_for_add_apple == 0:
        game.add_fruit()
    game.current_numbers_of_moves += 1


def movement_snake_2(t):
    if not snake.alive or not snake2.alive:
        game.state = 'game_over'
        return
    snake2.move_snake()
    pyglet.clock.schedule_once(movement_snake_2, snake2.speed)
    if snake2.coordinates[-1] in snake.coordinates:
        print('Druhý Had kousl do prvního a je ponich.')
        snake2.alive = False
    # přidání ovoce po počtu_tahu
    if game.current_numbers_of_moves % game.number_of_moves_for_add_apple == 0:
        game.add_fruit()
    game.current_numbers_of_moves += 1


def movement(t):
    if game.state == 'main_screen':
        pass
    if game.state == 'game_snake':
        pyglet.clock.unschedule(movement)
        movement_snake(0.5)
    if game.state == 'game_snake_2':
        pyglet.clock.unschedule(movement)
        movement_snake_1(0.5)
        movement_snake_2(0.5)
    if game.state == 'game_number':
        pyglet.clock.unschedule(movement)
        movement_snake_number(0.5)


def key_press(symbol, modifiers):
    if game.state == 'game_over':
        return
    if symbol == key.J and game.state == 'main_screen':
        game.state = 'game_snake'
    if symbol == key.D and game.state == 'main_screen':
        game.state = 'game_snake_2'
    if symbol == key.N and game.state == 'main_screen':
        game.state = 'game_number'

    if symbol == key.UP:
        if snake.direction != (0, -1):
            snake.direction = (0, 1)
    elif symbol == key.DOWN:
        if snake.direction != (0, 1):
            snake.direction = (0, -1)
    elif symbol == key.LEFT:
        if snake.direction != (1, 0):
            snake.direction = (-1, 0)
    elif symbol == key.RIGHT:
        if snake.direction != (-1, 0):
            snake.direction = (1, 0)
    # ovladani pro druheho hada - w, s, a, d - nahoru, dolu, vlevo, vpravo
    if symbol == key.W:
        if snake2.direction != (0, -1):
            snake2.direction = (0, 1)
    elif symbol == key.S:
        if snake2.direction != (0, 1):
            snake2.direction = (0, -1)
    elif symbol == key.A:
        if snake2.direction != (1, 0):
            snake2.direction = (-1, 0)
    elif symbol == key.D:
        if snake2.direction != (-1, 0):
            snake2.direction = (1, 0)


window = pyglet.window.Window(width = game.area_size_x * game.tile_size, height = game.area_size_y * game.tile_size + 60, caption = 'Snake 2D')
label_snake = pyglet.text.Label(' Snake, neboli Had', font_name = 'Terminus', font_size = 50, x = window.width / 5, y = window.height / 2.5)

window.push_handlers(
    on_draw = draw,  # na vykresleni okna pouzij funkci vykresli
    on_key_press = key_press,  # po stisknuti klavesy zavolej stisk_klavesy
    )

pyglet.clock.schedule_interval(movement, 0.5)


pyglet.app.run()
