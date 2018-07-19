import pygame as pg
from settings import *
from sprites import *
from main import *




def start_screen():
    game = Game()
    game.level_choice = "start_screen.tmx"
    game.new()
    waiting = True
    game.new_game()
    while waiting:
        game.events()
        game.update()
        game.draw()
        if game.button.butname == 'start':

            waiting = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.running = False

    #self.level_screen()
