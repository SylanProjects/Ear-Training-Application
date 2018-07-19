# Ear Training App
# Developed by Sylwester Stremlau
# 2018
# University of West London

import pygame as pg
from sprites import *


class DefaultSettings:
    def __init__(self, game):
        self.game = game

class Level:
    def __init__(self, game):
        self.game = game
        #self.game.level_choice = 'test_level.tmx'
        self.octave = 5
        self.menu = Menu(self)
        self.finished_levels = []
        #self.game.menu_screen = 'level'
        self.level_name = 's1_level_'
        self.level_score = 100
        #self.game.level_choice = 'test_level.tmx'




    def generic_level(self, stage, level, note_1, note_2, score, level_name):
        self.game.click_sound.play()
        self.level_name = level_name
        self.stage_no = stage
        self.level_no = level
        self.game.level_choice = "test_level.tmx"
        self.game.note_1 = note_1
        self.game.note_2 = note_2
        self.level_score = score
        #self.game.menu_screen = 'stage_1'

    def random_level(self, note_1, note_2):
        self.game.click_sound.play()
        self.level_name = "random"
        self.game.level_choice = "random.tmx"
        self.game.note_1 = note_1
        self.game.note_2 = note_2
        self.level_score = 100
        self.game.menu_screen = 'random'


    def update(self):
        self.game.click_sound.play()
        self.game.reset_game()


class Menu:
    def __init__(self, game):
        self.game = game
        self.level_choice = 'start_screen.tmx'


    def start_screen(self):
        self.level = Level(self)
        self.game.level_choice = "start_screen.tmx"
        self.game.new()
        self.game.menu_screen = 'start'
        self.game.shift = False
        waiting = True
        #self.game.new_game()
        while waiting:
            self.game.events()
            self.game.update()
            self.game.draw()

            if self.game.unlocked_levels[2] == False:
                self.game.input()
            if self.game.button.butname == 'reset_save':
                self.game.reset_save()

            if self.game.button.butname == 'start':
                self.game.click_sound.play()


                waiting = False
                self.game.playing = False

                self.generic_screen("stage_choice")

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.quit()



    def generic_screen(self, name):
        self.game.click_sound.play()
        self.game.menu_screen = (name)
        self.game.level_choice = (name+".tmx")
        #self.game.new()
        self.game.pianokey.notename = 0
        self.game.button.current_button = 0
        self.game.new()
        self.game.wait_for_key()

        self.game.pianokey.playing = True
