# Ear Training App
# Developed by Sylwester Stremlau
# 2018
# University of West London


import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *
from levels import *
import os, glob
import pickle
import random


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()

        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        #self.font_name = pg.font.match_font(FONT_NAME)

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.game_folder = game_folder
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        font_folder = path.join(game_folder, 'fonts')
        self.font_name = path.join(font_folder, 'zekton.ttf')
        self.test_font = path.join(font_folder, 'font_1.ttf')
        self.level_folder = path.join(game_folder, "levels")
        self.mouse_image = pg.image.load(path.join(img_folder, 'mouse.png')).convert_alpha()
        self.note_sound = pg.mixer.Sound(path.join(snd_folder, 'C4.wav'))
        self.note_sound_2 = pg.mixer.Sound(path.join(snd_folder, 'D5.wav'))

        self.notes = []
        # Import piano sounds
        # TODO add to a proper folder
        for filename in glob.glob(path.join(snd_folder, '*.wav')):
            snd = pg.mixer.Sound(path.join(snd_folder, filename))
            self.notes.append(snd)
        self.click_sound = pg.mixer.Sound(path.join(music_folder, 'click.wav'))
        self.right_sound = pg.mixer.Sound(path.join(music_folder, 'right.wav'))
        self.wrong_sound = pg.mixer.Sound(path.join(music_folder, 'wrong.wav'))
        pg.mixer.music.load(path.join(music_folder, 'menu.wav'))
        self.test_image = pg.image.load(path.join(img_folder, 'test.png'))
        self.lock_image = pg.image.load(path.join(img_folder, 'lock.png'))
        self.grey_lock = pg.image.load(path.join(img_folder, 'grey_lock.png'))
        # Read information from save file
        # I/O for persistent data
        try:
            with open(path.join(game_folder, SAVE_FILE), 'rb') as f:
                # Read the file and put the list into unlocked_levels
                # The first value is the score
                self.unlocked_levels = pickle.load(f)
                self.score = self.unlocked_levels[0]

        except:
            # Create a new file
            with open(path.join(game_folder, SAVE_FILE), 'w') as f:
                self.unlocked_levels = NEW_SAVE
                self.score = 0


    def new_game(self):
        self.default_settings()
        self.playing = False
        playing = self.playing
        self.wait_timer = 0
        self.level_error = False
        self.inpt = ""

        #self.shift = False


    def default_settings(self):
        self.level = Level(self)
        self.level_choice = 'start_screen.tmx'
        self.menu_screen = 'none'
        self.note_1 = 'D4'
        self.note_2 = 'C6'
        self.mouse_press = 0
        self.locked_levels = []
        self.help = False
        self.ran_intro = False
        self.ran_win = False
        self.ran_counter = 0
        self.user_count = 5
        self.difficulty = 11
        self.difficulty_mult = 0.5
        self.difficulty_name = 'none'







    def new(self):
        menu = Menu(self)
        self.all_sprites = pg.sprite.Group()
        self.pianokeys = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        level = Level(self)
        self.levels = TiledMap(path.join(self.level_folder, self.level_choice))
        self.levels_img = self.levels.make_map()
        self.levels_rect = self.levels_img.get_rect()
        self.pianokey = PianoKey(self, 50, 50,50,50, '0')
        self.pianokey.notename = 0
        self.current_note = 0
        self.level_won = False


        for tile_object in self.levels.tmxdata.objects:

            if tile_object.name == 'mouse':
                self.mouse = Mouse(self, tile_object.x, tile_object.y)

            if tile_object.name in NOTE_NUMBERS:
                PianoKey(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)

            if tile_object.name == 'button':
                self.button = Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)

            if tile_object.name in BUTTONS or LEVEL_BUTTONS:
                Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)



    def run(self):
        self.pianokey.playing = True
        while self.pianokey.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            #pg.mixer.music.play(loops=-1)
            pg.mixer.music.play(0)
            self.events()
            self.update()
            self.draw()

        #levels.start_screen()

    def quit(self):
        pg.quit()
        sys.exit()




    def update(self):

        self.all_sprites.update()
        now = pg.time.get_ticks()

        self.check_note()



        if self.pianokey.playing == True:

            if self.help:
                waiting = True
                while waiting:
                    self.events()
                    self.level_won = True
                    self.draw()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            sys.exit()


                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_SPACE:
                                waiting = False
                                self.help = False



            # Compare notes and octaves
            # ANSWER

            if str(self.note_2) == str(self.pianokey.confirmed_note):
                self.pianokey.status = 'Right!'

                self.right_sound.play()
                self.win_message = ""
                if self.level.level_score <0:
                    self.level.level_score = 1
                # Convert stage number and level to a string
                if self.menu_screen != 'random':
                    next_level = "s"+ str(self.level.stage_no) + "_level_" + str(int(self.level.level_no) + 1)

                    if next_level in self.unlocked_levels:
                        pass
                    else:
                        self.score += self.level.level_score
                        self.unlocked_levels[0] = self.score
                        # Add the next level to the unlocked levels list
                        self.win_message = "Next level unlocked!"
                        self.unlocked_levels.append(next_level)

                        with open(path.join(self.game_folder, SAVE_FILE), 'wb') as f:
                            pickle.dump(self.unlocked_levels, f)

                            #f.write(str(highscore))

                waiting = True

                if self.menu_screen == 'random':


                    self.points += self.level.level_score * self.difficulty_mult
                    if self.points < 0:
                        self.points = 1

                while waiting:
                    self.events()
                    self.level_won = True
                    self.draw()
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            sys.exit()


                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_SPACE:
                                if self.menu_screen == 'random':
                                    #self.score += self.level.level_score

                                    #self.points += self.level.level_score

                                    self.ran_counter += 1
                                    if self.ran_counter == self.user_count:
                                        self.score += self.points
                                        self.unlocked_levels[0] = self.score


                                        with open(path.join(self.game_folder, SAVE_FILE), 'wb') as f:
                                            pickle.dump(self.unlocked_levels, f)
                                        self.ran_win = True

                                    if self.ran_counter != self.user_count:
                                        self.generate_random_note()
                                        self.level.update()
                                waiting = False


                self.wait_timer = now
                self.playing = False
                self.menu = Menu(self)
                #self.menu.level_screen()
                if self.menu_screen != 'random':
                    self.menu.generic_screen("stage_" + str(self.level.stage_no))
                else:
                    self.menu.generic_screen('stage_choice')
            elif str(self.note_2) != str(self.pianokey.confirmed_note):
                self.pianokey.status = 'Wrong!'
                self.unlocked_levels[3] += 1





            # Has to be kept at the end to avoid looping while holding the mouse button down
            # and to make sure the score works right
        self.mouse_press = 0
        if pg.mouse.get_pressed()[0]==1:
            self.mouse_press = 1




    def input(self):

        waiting = True
        while waiting:
            for event in pg.event.get():

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LSHIFT:
                        self.shift = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LSHIFT:
                        self.shift = True

                    if event.key in ALPHABET:
                        event_number = event.key
                        # 97 to 122
                        pressed_letter = ALPHABET[event_number]
                        if self.shift:
                            pressed_letter = pressed_letter.upper()

                        self.inpt = self.inpt[:len(self.inpt)-1]
                        self.inpt += pressed_letter + "_"

                    if event.key == pg.K_BACKSPACE:
                        self.inpt = self.inpt[:len(self.inpt)-2] + "_"


                    if event.key == pg.K_RETURN:
                        self.inpt = self.inpt[:len(self.inpt)-1]
                        self.unlocked_levels[1] = self.inpt
                        #self.inpt += "_"
                        self.unlocked_levels[2] = True
                        with open(path.join(self.game_folder, SAVE_FILE), 'wb') as f:
                            pickle.dump(self.unlocked_levels, f)
                    waiting = False
                if event.type == pg.QUIT:
                    self.quit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):






        self.screen.blit(self.levels_img, self.levels_rect)
        self.all_sprites.draw(self.screen)
        self.menu = Menu(self)
        font_size = 60

        # Highlight the selected note

        for tile_object in self.levels.tmxdata.objects:

            if tile_object.name == self.button.butname and tile_object.name not in NOTE_NUMBERS:
                self.draw_box(tile_object.width, tile_object.height, tile_object.x,  tile_object.y, 200, GREY_2)

            if tile_object.name == self.difficulty_name:
                self.draw_box(tile_object.width, tile_object.height, tile_object.x,  tile_object.y, 200, GREY_2)

            if tile_object.name == self.pianokey.notename and tile_object.y == 560:
                self.draw_box(10, 10, tile_object.x + (tile_object.width / 2), 370, 200, GREY_2)

            if tile_object.name == self.pianokey.notename and tile_object.height == 168 and '#' in tile_object.name:
                self.draw_box(10, 10, tile_object.x+ (tile_object.width / 2), 370, 200, GREY_2)

            if tile_object.name == self.note_1 and tile_object.y == 560:
                self.draw_box(10, 10, tile_object.x + (tile_object.width / 2), 370, 255, NAVY)

            if tile_object.name == self.note_1 and tile_object.height == 168 and '#' in tile_object.name:
                self.draw_box(10, 10, tile_object.x+ (tile_object.width / 2), 370, 255, NAVY)

        #self.draw_text(str(self.pianokey.notename), self.font_name, font_size, BLACK, WIDTH - 200, HEIGHT - 100, align="center")


        #self.draw_text(self.menu_screen, self.font_name, 50, BLACK, WIDTH / 2, 50, align="center")
        #self.draw_text("Menu:{}".format(str(self.menu_screen)), self.font_name, 20, BLACK, WIDTH -200, 40, align="nw")
        #self.draw_text(str(self.mouse_press), self.font_name, 30, BLACK, WIDTH - 100, 145, align="center")

        # STATS
        if self.unlocked_levels[1] != 0:
            self.draw_text(str(self.unlocked_levels[1]), self.font_name, 40, BLACK,  80, 30, align="w")
            self.draw_text("Score: {}".format(str(self.unlocked_levels[0])), self.font_name, 25, BLACK, 80, 60, align="w")
            #self.draw_text("Right answers: {}".format(str(self.button.butname)), self.font_name, 17, BLACK, 80, 90, align="w")
            #self.draw_text("Wrong answers: {}".format(str(self.unlocked_levels[4])), self.font_name, 17, BLACK, 80, 110, align="w")




        if self.menu_screen == 'stage_1' or self.menu_screen == 'stage_2':
            self.draw_text("Stage {}".format(self.menu_screen[6:]), self.test_font, font_size, BLACK, WIDTH / 2, 50, align="center")

        if self.menu_screen == 'random_lev_choice':
            self.draw_text("Random", self.font_name, font_size, BLACK, WIDTH / 2, 50, align="center")


        if self.pianokey.playing == True:
            #self.draw_text("Note:{}".format(str(self.pianokey.notename)), self.font_name, 20, BLACK, WIDTH - 1000, 20, align="nw")

            #self.draw_text("Notes:{}, {}".format(str(self.note_1), str(self.note_2)), self.font_name, 20, BLACK, WIDTH - 1000, 145, align="nw")
            #self.draw_text("Status:{}".format(str(self.pianokey.status)), self.font_name, 20, BLACK, WIDTH - 1000, 95, align="nw")
            #self.draw_text("Button:{}, {}".format(str(self.button.butname), str(self.note_2)), self.font_name, 20, BLACK, WIDTH - 1000, 120, align="nw")

            if self.menu_screen == 'random':
                self.draw_text("Level: {}".format(int(self.ran_counter+1)), self.font_name, 45, BLACK, WIDTH / 2, 50, align="center")
                self.draw_text("Current score: {}".format(int(self.points)), self.font_name, 30, BLACK, WIDTH / 2, 100, align="center")



        if self.pianokey.playing == False:
            pass
            #self.draw_text("Status:{}".format(str(self.button.butname)), self.font_name, 20, BLACK, WIDTH - 200 , 65, align="nw")
            #self.draw_text("Status:{}".format(str(self.unlocked_levels)), self.font_name, 20, BLACK, 100 , HEIGHT - 50, align="nw")

        if self.help:
            s = pg.Surface((WIDTH, HEIGHT))
            s.set_alpha(200)
            s.fill((BLACK))
            self.screen.blit(s, (0,0))
            self.draw_text("Help", self.font_name, 80, WHITE, WIDTH / 2 , HEIGHT / 2 - 250, align="center")

            self.draw_text(HELP_1, self.font_name, 20, WHITE, WIDTH / 2, HEIGHT / 2 - 200 + 50, align="center")
            c = 140
            self.draw_text(HELP_2, self.font_name, 20, WHITE, WIDTH / 2, HEIGHT / 2 - 200 + c, align="center")
            c += 50
            self.draw_text(HELP_3, self.font_name, 20, WHITE, WIDTH / 2, HEIGHT / 2 - 200 + c, align="center")
            c += 90
            self.draw_text(HELP_4, self.font_name, 20, WHITE, WIDTH / 2, HEIGHT / 2 - 200 + c, align="center")
            c += 50
            self.draw_text(HELP_5, self.font_name, 20, WHITE, WIDTH / 2, HEIGHT / 2 - 200 + c, align="center")

            c += 150
            self.draw_text("Press spacebar to continue...", self.font_name, 20, WHITE, WIDTH / 2, HEIGHT / 2 - 200 + c, align="center")




        #    self.draw_text(HELP, self.font_name, 40, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align="center")

        if self.ran_intro:
            s = pg.Surface((WIDTH, HEIGHT))
            s.set_alpha(200)
            s.fill((BLACK))
            self.screen.blit(s, (0,0))
            self.draw_text("TOTALLY", self.font_name, 40, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align="center")


        if self.level_won:
            #self.screen.fill(BLACK)
            s = pg.Surface((WIDTH, HEIGHT))
            s.set_alpha(200)
            s.fill((BLACK))
            self.screen.blit(s, (0,0))
            if self.ran_counter != self.user_count - 1:
                if self.menu_screen == 'random':
                    score = self.level.level_score * self.difficulty_mult
                else:
                    score = self.level.level_score
                self.draw_text("Score: {}".format(int(score)), self.font_name, 40, WHITE, WIDTH / 2, HEIGHT / 2 - 200, align="center")
                self.draw_text("Great!", self.font_name, 150, BLUE, WIDTH / 2, HEIGHT / 2, align="center")
                self.draw_text(str(self.win_message), self.font_name, 80, WHITE, WIDTH / 2, HEIGHT / 2 + 175, align="center")
                self.draw_text("Press spacebar to continue...", self.font_name, 30, WHITE, WIDTH / 2, HEIGHT / 2 + 300, align="center")

            if self.ran_counter == self.user_count - 1:
                self.draw_text("Total Score: {}".format(int(self.points)), self.font_name, 150, GREEN, WIDTH / 2, HEIGHT / 2, align="center")
                self.draw_text("Press spacebar to continue...", self.font_name, 30, WHITE, WIDTH / 2, HEIGHT / 2 + 300, align="center")


        for tile_object in self.levels.tmxdata.objects:

            #if tile_object.name == self.sprites.current_button:
            #    self.draw_box(tile_object.width, tile_object.height, tile_object.x, tile_object.y, 200, LIGHTGREY)


            if tile_object.name == 'start':
                self.draw_text("Start", self.test_font, 70, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")
                 #Checking if .index is working as intended
                #self.draw_text(str(int(str(NOTE_NUMBERS.index('A#5')))), self.font_name, 20, BLACK, tile_object.x + (tile_object.width/2) +200, tile_object.y +(tile_object.height/2)+200, align="center")

            if self.level_won == False and self.help == False:
                if tile_object.name == 'play_button_1':
                    #self.draw_box(tile_object.width * 0.8, tile_object.height * 0.8, tile_object.x + 13, tile_object.y + 10, 50, BLACK)
                    self.draw_text(str(self.note_1), self.font_name, 50, NAVY, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")

                if tile_object.name == 'play_button_2':
                    self.draw_text(str(self.pianokey.notename), self.font_name, 50, GREY_2, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")




                if tile_object.name == 'confirm':
                    self.draw_text("Confirm", self.font_name, 30, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")

            #if tile_object.name == 'score':
            #    self.draw_text(str(self.score), self.font_name, 30, BLACK, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")


            if tile_object.type == "octave_name":
                self.draw_text(str(tile_object.name), self.font_name, 30, BLACK, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")


            if tile_object.type == "button":

                # Reset button
                if self.help == False and self.level_won == False:
                    self.draw_text(str(tile_object.butname), self.font_name, 15, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")



            # random choice button

            if tile_object.type == "button_large":

            #    if self.help == False and self.level_won == False:
                self.draw_text(str(tile_object.butname), self.font_name, 30, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")

            # random difficulty level button
            if tile_object.type == "button_medium":
                self.draw_text(str(tile_object.butname), self.font_name, 20, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")


            if tile_object.name == 'level_number':
                self.draw_text(str(self.user_count), self.font_name, 30, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")


            if tile_object.name == 'back':
                if self.level_won == False and self.help == False:
                    self.draw_text("Back", self.font_name, B_F_SIZE, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")


            if tile_object.name == 'username':
                if self.unlocked_levels[2] == False:
                        username = str(self.inpt)
                        message1 = "Type in username:"
                else:
                    username = self.unlocked_levels[1]
                    message1 = "User:"
                self.draw_text(message1, self.font_name, 30, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2-20), align="center")
                self.draw_text(username, self.font_name, 30, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2+20), align="center")




            if tile_object.type == "level":# in LEVEL_BUTTONS:
                self.draw_text("Level "+ str(tile_object.level), self.font_name, L_F_SIZE, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")

                if str(tile_object.name) in self.unlocked_levels:
                    pass
                else:

                    self.draw_box(tile_object.width, tile_object.height, tile_object.x, tile_object.y, 200, LIGHTGREY)
                    self.screen.blit(self.lock_image, (tile_object.x+23, tile_object.y+5))

            if tile_object.type == 'stage':
                    self.draw_text(str(tile_object.stage_name), self.font_name, 35, WHITE, tile_object.x + (tile_object.width/2), tile_object.y +(tile_object.height/2), align="center")


        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()


    def draw_box(self, width, height, x, y, trans, color):
        col_0 = color[0]
        col_1 = color[1]
        col_2 = color[2]

        box_surface_fill = pg.Surface((width, height), pg.SRCALPHA)
        box_surface_fill.fill((col_0, col_1, col_2, trans))
        self.screen.blit(box_surface_fill, (x, y))




    def reset_game(self):
        waiting = False
        self.new()
        self.run()

    def generate_random_note(self):
        number = []
        for i in range(len(NOTE_NUMBERS_SORTED)):
            number.append(1+len(number))

        rand_num1 = random.choice((number))

        if rand_num1 >= len(NOTE_NUMBERS_SORTED):
            rand_num1 = len(NOTE_NUMBERS_SORTED) - 1

        note_1 = NOTE_NUMBERS_SORTED[rand_num1]

        number = []
        for i in range(self.difficulty):
            number.append(1+len(number))

        ran = random.choice((number))
        ran = random.choice((ran, -ran))


        rand_num2 = rand_num1 + ran

        if rand_num2 < 0:
            rand_num2 = 0

        if rand_num2 >= len(NOTE_NUMBERS_SORTED):
            rand_num2 = len(NOTE_NUMBERS_SORTED) - 1

        note_2 = NOTE_NUMBERS_SORTED[rand_num2]


        self.level.random_level(note_1, note_2)

    def wait_for_key(self):

        waiting = True
        #self.new_game()
        while waiting:
            self.clock.tick(FPS)
            self.events()
            #self.update()
            #self.draw()

            self.level_error = False

            if self.button.butname in self.unlocked_levels:
                for tile_object in self.levels.tmxdata.objects:

                    if tile_object.name == self.button.butname:
                        self.level.generic_level(tile_object.stage, tile_object.level, tile_object.note_1, tile_object.note_2, int(tile_object.score), tile_object.name)
                        self.level.update()
                        self.button.butname = 'button'


                        # Random Stage
            if self.button.butname == "stage_4":
                self.points = 0
                self.ran_counter = 0
                self.user_count = 5
                menu.generic_screen("random_lev_choice")
                self.button.butname = 'button'

                #self.ran_intro = True
            if self.button.butname == "confirm2":
#
                self.generate_random_note()
                self.level.update()
                self.button.butname = 'button'

            if self.button.butname == "stage_1":
                #self.new()
                self.button.butname = 'button'
                menu.generic_screen("stage_1")
                self.button.butname = 'button'

            if self.button.butname == "stage_2":
                #self.new()
                self.button.butname = 'button'
                menu.generic_screen("stage_2")
                self.button.butname = 'button'

            if self.button.butname == 'back':
                if self.menu_screen == "stage_1" or "stage_2" or "random":
                    self.button.butname = 'button'
                    menu.generic_screen("stage_choice")
                    self.button.butname = 'button'

            if self.button.butname == 'reset_save':
                self.unlocked_levels = [0, 0, False, 0, 0,'s1_level_1', 's2_level_1', ]# NEW_SAVE
                self.inpt = "_"
                self.button.butname = 'button'
                self.button.butname = 'button'
                self.menu.start_screen()
                #self.reset_save()

            self.update()
            self.draw()


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

    def reset_save(self):
        self.unlocked_levels = [0, 0, False, 0, 0,'s1_level_1', 's2_level_1', ]
        self.inpt = "_"
        self.menu.start_screen()

    def check_note(self):
        mouse = pg.mouse.get_pos()


        hits = pg.sprite.spritecollide(self.mouse, self.pianokeys, False)
        # Collide mouse sprite with pianokeys
        for hit in hits:
            if pg.mouse.get_pressed()[0]==1 and self.mouse_press == 0:
                # If left mouse button is pressed :
                self.button.butname = 'button'
                self.pianokey.notename = str(hit.note)
                self.button.butname = 'button'
                #self.pianokey.octave = str(hit.octave)

        hits = pg.sprite.spritecollide(self.mouse, self.buttons, False)
        if self.button.butname == 'back':
            if self.menu_screen != "random":
                self.button.butname = 'button'
                menu.generic_screen("stage_"+str(self.level.stage_no))
                self.playing = False
            else:
                self.button.butname = 'button'
                menu.generic_screen("stage_choice")
                self.playing = False

        if self.button.butname == 'help':
            self.click_sound.play()
            self.help = True
            waiting = True
            while waiting:
                self.draw()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()


                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            self.click_sound.play()
                            waiting = False
                            self.help = False
                            self.button.butname = ""



        for hit in hits:
            if pg.mouse.get_pressed()[0]==1:

                self.button.butname = str(hit.butname)

                if self.button.butname == 'play_button_1':
                    self.button.update_1()
                    self.button.butname = 'button'

                if self.button.butname == 'play_button_2':
                    self.button.update_2()
                    self.button.butname = 'button'

                if self.button.butname == 'add' and self.mouse_press == 0:
                    self.user_count += 1
                    self.button.butname = 'button'

                if self.button.butname == 'subtract' and self.mouse_press == 0:
                    self.user_count -= 1
                    if self.user_count < 1:
                        self.user_count = 1
                    self.button.butname = 'button'


                #self.difficulty = Difficulty(self)
                # DIFFICULTY CHOICES

                if self.button.butname == 'very_easy':
                    self.difficulty = VERY_EASY
                    self.difficulty_mult = VERY_EASY_MULT
                    self.difficulty_name = self.button.butname
                    self.button.butname = 'button'
                if self.button.butname == 'easy':
                    self.difficulty = EASY
                    self.difficulty_mult = EASY_MULT
                    self.difficulty_name = self.button.butname
                    self.button.butname = 'button'
                if self.button.butname == 'normal':
                    self.difficulty = NORMAL
                    self.difficulty_mult = NORMAL_MULT
                    self.difficulty_name = self.button.butname
                    self.button.butname = 'button'
                if self.button.butname == 'hard':
                    self.difficulty = HARD
                    self.difficulty_mult = HARD_MULT
                    self.difficulty_name = self.button.butname
                    self.button.butname = 'button'
                if self.button.butname == 'very_hard':
                    self.difficulty = VERY_HARD
                    self.difficulty_mult = VERY_HARD_MULT
                    self.difficulty_name = self.button.butname
                    self.button.butname = 'button'




                if self.button.butname == 'confirm':

                    self.pianokey.confirmed_note = self.pianokey.notename

                    if self.pianokey.confirmed_note != self.note_2 and self.mouse_press == 0:

                        self.level.level_score = self.level.level_score - 5
                        self.wrong_sound.play()
                    self.button.butname = 'button'




    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)

        self.screen.blit(text_surface, text_rect)


playing = False


g = Game()
g.new_game()
menu = Menu(g)
level = menu.start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen
pg.sys.exit()
