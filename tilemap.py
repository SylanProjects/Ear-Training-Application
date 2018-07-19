# Ear Training App
# Developed by Sylwester Stremlau
# 2018
# University of West London

import pygame as pg
import pytmx
from settings import *
from pytmx.util_pygame import load_pygame

class TiledMap:
    def __init__(self, filename):
        # Linux:
        tm = load_pygame(filename, pixelalpha=True)
        # Windows: ?
        #tm = pytmx.load_pygame(filename, pixelalpha=True)

        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        tm = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile=tm(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
