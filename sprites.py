# Ear Training App
# Developed by Sylwester Stremlau
# 2018
# University of West London

import pygame as pg
from settings import *




class PianoKey(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, note):
        self.groups = game.pianokeys
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        # notes will be saved into variable "notename"
        self.notename = '?'
        self.note = note
        self.x = x
        self.y = y
        self.count = 0
    #    self.octave = octave
        self.current_note = '?'
        self.status = ''
        self.playing = False
        self.confirmed_note = 0


class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, butname):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.butname = butname
        self.x = x
        self.y = y
        self.current_button = 0
        self.last_update = 0
        self.last_played = 0


        # Update button 1
    def update_1(self):
        if self.game.mouse_press == 0:
            now = pg.time.get_ticks()
            if now - self.last_played > 300:
                self.last_played = now
                #self.game.note_sound.play()
                self.game.notes[int(str(NOTE_NUMBERS.index(str(self.game.note_1))))].play()

        # Update button 2 to play the note after 300ms
    def update_2(self):
        if self.game.mouse_press == 0:

            now = pg.time.get_ticks()
            if now - self.last_played > 300:
                self.last_played = now
                # Find the position of the note by using the array "NOTE_NUMBERS"
                self.game.notes[int(str(NOTE_NUMBERS.index(str(self.game.note_2))))].play()






class Mouse(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Mouse sprite is used to allow for collision between mouse and other sprites
        # and to be able to use pg.sprite.Collide instead of mousecollide
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mouse_image
        # mouse image is only 1x1 pixels
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        mouse = pg.mouse.get_pos()
        # make the sprite follow the mouse
        self.rect.x = mouse[0]
        self.rect.y = mouse[1]
