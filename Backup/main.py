
import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from sprites import *
vec = pg.math.Vector2




class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.level_folder = path.join(game_folder, "levels")
        self.mouse_image = pg.image.load(path.join(img_folder, 'mouse.png')).convert_alpha()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.pianokeys = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.levels = TiledMap(path.join(self.level_folder, "test_level.tmx"))
        self.levels_img = self.levels.make_map()
        self.levels_rect = self.levels_img.get_rect()


        for tile_object in self.levels.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)


            if tile_object.name == 'key0':
                self.pianokey = PianoKey(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.name == 'key1':
                self.pianokey1 = PianoKey(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'key2':
                self.pianokey2 = PianoKey(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.name == 'key3':
                self.pianokey3 = PianoKey(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'f#1':
                self.pianokey4 = PianoKey(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'key5':
                self.pianokey5 = PianoKey(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)



    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()




        self.check_note()




    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        # self.screen.fill(BGCOLOR)

        self.draw_text("TEST", self.font_name, 40, YELLOW, WIDTH - 150, 20, align="nw")
        self.screen.blit(self.levels_img, self.levels_rect)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image)
        self.draw_text("Coins:{}".format(str(self.pianokey.notename)), self.font_name, 40, YELLOW, WIDTH - 150, 20, align="nw")
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def check_note(self):
        mouse = pg.mouse.get_pos()


        if self.pianokey.rect.collidepoint(mouse):
            self.pianokey.notename = 'C'
        elif self.pianokey1.rect.collidepoint(mouse):
            self.pianokey.notename = 'C#'
        elif self.pianokey2.rect.collidepoint(mouse):
            self.pianokey.notename = 'D'
        elif self.pianokey3.rect.collidepoint(mouse):
            self.pianokey.notename = "D#"
        elif self.pianokey4.rect.collidepoint(mouse):
            self.pianokey.notename = "asd"
        elif self.pianokey4.rect.collidepoint(mouse):
            self.pianokey.notename = "key5"
        elif self.pianokey5.rect.collidepoint(mouse):
            self.pianokey.notename = "b1"

        else:
            self.pianokey.notename = 'none'





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

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen
