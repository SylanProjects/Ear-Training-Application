# Ear Training App
# Developed by Sylwester Stremlau
# 2018
# University of West London

HELP_1 = "Find the note on the right using the reference note on the left for help!"
HELP_2 = "Listen to the notes by pressing on each button, select the note on the piano"
HELP_3 = "and press Confirm to check if you guessed right."
HELP_4 = "You can listen to the notes as many times as you want. You also have as many tries as you want but remember that"
HELP_5 = "with each wrong try, the score reward decreases. "


# Define colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (66, 223, 244)
NAVY = (161, 177, 206)
GREY_2 = (168, 160, 159)

# Screen settings
            # SCORE, USERNAME, DID USER TYPE THE NAME, LEVELS
NEW_SAVE = [0, 0, False, 's1_level_1', 's2_level_1', ]

WIDTH = 1280
HEIGHT = 720
TILESIZE = 64

TITLE = "Ear Training Game"
FONT_NAME = "Arial"
FPS = 60
BGCOLOR = BLUE

# Difficulty settings
VERY_EASY = 2
EASY = 3
NORMAL = 5
HARD = 8
VERY_HARD = 11

# Difficulty store multiplier

VERY_EASY_MULT = 0.3
EASY_MULT = 0.5
NORMAL_MULT = 0.7
HARD_MULT = 1
VERY_HARD_MULT = 1.2
L_F_SIZE = 22
B_F_SIZE = 22

# There's probably a better way to do it
ALPHABET = {97:"a", 98: "b", 99:"c", 100:"d", 101:"e", 102:"f", 103:"g", 104:"h",
            105:"i", 106:"j", 107:"k", 108:"l", 109:"m", 110:"n", 111:"o", 112:"p", 113:"q",
            114:"r", 115:"s", 116:"t", 117:"u", 118:"v", 119:"w", 120:"x", 121:"y", 122:"z",
            32:" ", 48:"0", 49:"1", 50:"2", 51:"3", 52:"4", 53:"5", 54:"6", 55:"7",
            56:"8", 57:"9"}

# notes

NOTE_NUMBERS = ['A#4', 'A#5','A#6', 'A4', 'A5', 'A6', 'B4', 'B5', 'B6',
                'C#4', 'C#5','C#6', 'C4', 'C5', 'C6', 'C7', 'D#4', 'D#5','D#6', 'D4', 'D5', 'D6',
                  'E4', 'E5', 'E6', 'F#4', 'F#5','F#6', 'F4', 'F5', 'F6',
                  'G#4', 'G#5','G#6', 'G4', 'G5', 'G6',]

NOTE_NUMBERS_SORTED = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
                        'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5',
                        'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6']

BUTTONS = ['start', 'play_button_1', 'play_button_2', 'confirm', 'stage_1', 'stage_2', 'stage_3', 'stage_4']
LEVEL_BUTTONS = ['s1_level_1', 's1_level_2', 's1_level_3', 's1_level_4']
SAVE_FILE = 'save.txt'
