#!/usr/bin/env python3
################################################################################
#
#   CSSE1001/7030 - Assignment 3
#
################################################################################

# VERSION 1.0.2

################################################################################
#
# The following is support code. DO NOT CHANGE.

from a3_support import *

# End of support code
################################################################################
# Write your code below
################################################################################

# Write your classes here (including import statements, etc.)

import random
from PIL import Image, ImageTk
import pygame

# Enemy Constants
ENEMY_WEAKNESS = {
    'fire': 'water',
    'water': 'ice',
    'poison': 'psychic',
    'psychic': 'poison',
    'ice': 'fire',
}

ENEMY_STRENGTH = {
    'fire': 'ice',
    'water': 'fire',
    'poison': 'poison',
    'psychic': 'psychic',
    'ice': 'water'
}

# Add new types to tiles
# Colours for each tile
TILE_COLOURS['health'] = 'pink'
TILE_COLOURS['shield'] = 'magenta'
TILE_COLOURS['power'] = 'orange'

# Ratio of probabilities that a tile of this type will be generated.
TILE_PROBABILITIES['health'] = 5
TILE_PROBABILITIES['shield'] = 5
TILE_PROBABILITIES['power'] = 5

# Sprites
SPRITE_SIZE = (80, 80)
SPRITE_SIZE_LG = (96, 96)

TILE_IMAGES = {
    'red': Image.open('imgs/tile_fire.png').resize(SPRITE_SIZE),
    'green': Image.open('imgs/tile_poison.png').resize(SPRITE_SIZE),
    'blue': Image.open('imgs/tile_water.png').resize(SPRITE_SIZE),
    'gold': Image.open('imgs/tile_gold.png').resize(SPRITE_SIZE),
    'purple': Image.open('imgs/tile_psychic.png').resize(SPRITE_SIZE),
    'light sky blue': Image.open('imgs/tile_ice.png').resize(SPRITE_SIZE),
    'pink': Image.open('imgs/tile_health.png').resize(SPRITE_SIZE),
    'magenta': Image.open('imgs/tile_shield.png').resize(SPRITE_SIZE),
    'orange': Image.open('imgs/tile_power.png').resize(SPRITE_SIZE)
}

TILE_IMAGES_LG = {
    'red': Image.open('imgs/tile_fire_sel.png').resize(SPRITE_SIZE_LG),
    'green': Image.open('imgs/tile_poison_sel.png').resize(SPRITE_SIZE_LG),
    'blue': Image.open('imgs/tile_water_sel.png').resize(SPRITE_SIZE_LG),
    'gold': Image.open('imgs/tile_gold_sel.png').resize(SPRITE_SIZE_LG),
    'purple': Image.open('imgs/tile_psychic_sel.png').resize(SPRITE_SIZE_LG),
    'light sky blue': Image.open('imgs/tile_ice_sel.png').resize(SPRITE_SIZE_LG),
    'pink': Image.open('imgs/tile_health_sel.png').resize(SPRITE_SIZE_LG),
    'magenta': Image.open('imgs/tile_shield_sel.png').resize(SPRITE_SIZE_LG),
    'orange': Image.open('imgs/tile_power_sel.png').resize(SPRITE_SIZE_LG)
}

# Player and Enemy Images
PORTRAIT_SIZE = (150, 150)

PORTRAIT_IMGS = {
    'player': Image.open('imgs/player_port.png').resize(PORTRAIT_SIZE),
    'enemy': Image.open('imgs/enemy_port.png').resize(PORTRAIT_SIZE)
}

# Sound Effects

SOUNDS = {
    'coin': 'sound/coin.wav',
    'fire': 'sound/fire.wav',
    'ice': 'sound/ice.wav',
    'poison': 'sound/poison.wav',
    'psychic': 'sound/psychic.wav',
    'water': 'sound/water.wav',
    'bgmusic': 'sound/bgmusic.wav',
    'gameover': 'sound/gameover.wav',
    'victory': 'sound/victory.wav',
    'health': 'sound/health.wav',
    'power': 'sound/power.wav',
    'shield': 'sound/shield.wav'
}


################################################################################
# Task 1
################################################################################

class SimplePlayer(object):
    """Represents the Player and tracks player status."""

    def __init__(self):
        """Initialise player score and swap count for tracking.

        Constructor(SimplePlayer)
        """
        self._score = 0
        self._swap_count = 0

    def add_score(self, score):
        """Adds a score to player score.

        SimplePlayer.add_score(int) -> int
        """
        self._score += score
        return self.get_score()

    def get_score(self):
        """Return player score.

        SimplePlayer.get_score() -> int
        """
        return self._score

    def reset_score(self):
        """Reset player score to 0.

        SimplePlayer.reset_score() -> None
        """
        self._score = 0

    def record_swap(self):
        """Records player swap.

        SimplePlayer.record_swap() -> int
        """
        self._swap_count += 1
        return self.get_swaps()

    def get_swaps(self):
        """Returns player swap count.

        SimplePlayer.get_swaps() -> int
        """
        return self._swap_count

    def reset_swaps(self):
        """Reset player swap count to 0.

        SimplePlayer.reset_swaps() -> None
        """
        self._swap_count = 0


class SimpleStatusBar(tk.Frame):
    """Status bar tracks player score and number of swaps"""

    def __init__(self, master):
        """
        Constructor(SimpleStatusBar, tk.Frame)
        """
        super().__init__(master)

        self._score_lbl = tk.Label(self, text=SCORE_FORMAT.format(0))
        self._swaps_lbl = tk.Label(self, text=SWAPS_FORMAT.format(0, 's'))
        self._swaps_lbl.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self._score_lbl.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def update_swaps(self, swaps):
        """Updates player swaps on status bar.

        SimpleStatusBar.update_swaps(int) -> None
        """
        if swaps == 1:
            self._swaps_lbl.config(text=SWAPS_FORMAT.format(swaps, ''))
        else:
            self._swaps_lbl.config(text=SWAPS_FORMAT.format(swaps, 's'))

    def update_score(self, score):
        """Updates player score on status bar.

        SimpleStatusBar.update_score(int) -> None
        """
        self._score_lbl.config(text=SCORE_FORMAT.format(score))


class SimpleTileApp(object):

    def __init__(self, master):
        """
        Constructor(SimpleTileApp, tk.Frame)
        """
        self._master = master
        self._master.title("Simple Tile Game")

        self._game = SimpleGame()
        self._player = SimplePlayer()

        # Listeners
        self._game.on('swap', self._handle_swap)
        self._game.on('score', self._handle_score)

        # View
        self._grid_view = TileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        # Status Bar
        self._status_bar = SimpleStatusBar(self._master)
        self._status_bar.pack(side=tk.TOP, expand=True, fill=tk.X)
        self._reset_button = tk.Button(self._master, text="Reset Status",
                                       command=self.reset_status)
        self._reset_button.pack(side=tk.TOP, expand=True)

        # Main Menu
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)
        # File Menu
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        # File Menu Items
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Exit", command=self.exit_game)

    def _handle_swap(self, from_pos, to_pos):
        """Run when a swap on the grid happens.

        SimpleTileApp._handle_swap(tuple, tuple) -> None
        """
        # print("SimplePlayer made a swap from {} to {}!".format(from_pos, to_pos))
        self._player.record_swap()
        self._status_bar.update_swaps(self._player.get_swaps())

    def _handle_score(self, score):
        """Run when a score update happens.

        SimpleTileApp._handle_score(int) -> None
        """
        # print("SimplePlayer scored {}!".format(score))
        self._player.add_score(score)
        self._status_bar.update_score(self._player.get_score())

    def reset_status(self):
        """Resets the player and status bar.

        SimpleTileApp.reset_status() -> None
        """
        if self._grid_view.is_resolving():
            tk.messagebox.showerror("Error", "Cannot reset status when grid " +
                                    "is resolving.")
        else:
            self._player.reset_score()
            self._player.reset_swaps()
            self._status_bar.update_score(self._player.get_score())
            self._status_bar.update_swaps(self._player.get_swaps())

    def new_game(self):
        """Starts new game resetting both the grid and player statuses.
        If grid is currently resolving, will prevent and display error message.

        SimpleTileApp.new_game() -> None
        """
        if self._grid_view.is_resolving():
            tk.messagebox.showerror("Error", "Cannot start new game when grid "
                                             + "is resolving.")
        else:
            self._game.reset()
            self._grid_view.draw()
            self.reset_status()

    def exit_game(self):
        """Exits game.

        SimpleTileApp.exit_game() -> None
        """
        self._master.destroy()


################################################################################
# Task 2
################################################################################

class Character(object):
    """Basic player/enemy functionality superclass"""

    def __init__(self, max_health):
        """Tracks:
        - Character max and current health

        Constructor(Character, int)
        Precondition: max_health > 0
        """
        self._max_hp = max_health
        self._current_hp = max_health

    def get_max_health(self):
        """Returns maximum player health.

        Character.get_max_health() -> int
        """
        return self._max_hp

    def get_health(self):
        """Returns current health.

        Character.get_health() -> int
        """
        return self._current_hp

    def lose_health(self, amount):
        """Decreases player health by amount. Health cannot go below zero.

        Character.lose_health(int) -> None
        """
        if self.get_health() < amount:
            self._current_hp -= (amount - (amount - self.get_health()))
        else:
            self._current_hp -= amount

    def gain_health(self, amount):
        """Increase player health by amount. Health cannot go above max.

        Character.gain_health(int) -> None
        """
        self._current_hp += amount
        if self.get_health() > self.get_max_health():
            self._current_hp = self.get_max_health()

    def reset_health(self):
        """Reset player health to maximum.

        Character.reset_health() -> None
        """
        self._current_hp = self._max_hp


class Enemy(Character):
    """Represents enemy, inherits from Character superclass"""

    def __init__(self, type, max_health, attack):
        """Tracks:
        - Health
        - Enemy Type
        - Enemy Attack range

        Constructor(Enemy, str, int, tuple)
        Precondition: max_health > 0
        Precondition: each attack value in tuple > 0 && value 1 < value 2

        """
        super().__init__(max_health)
        self._type = type
        self._attack = attack

    def get_type(self):
        """Returns enemy type.

        Enemy.get_type() -> str
        """
        return self._type

    def attack(self):
        """Returns enemy attack strength. Chosen as random int from
        enemy attack range.

        Enemy.attack() -> int
        """
        min, max = self._attack
        return random.randint(min, max)


class Player(Character):
    """Represents human player, inherits from Character superclass"""

    def __init__(self, max_health, swaps_per_turn, base_attack):
        """Tracks:
        - Max swaps and current swap count for player
        - Player base attack

        Constructor(Player, int, int, int)
        Precondition: swaps_per_turn > 0
        Precondition: max_health > 0
        Precondition: base_attack > 0

        """
        super().__init__(max_health)
        self._swap_max = swaps_per_turn
        self._swap_count = swaps_per_turn
        self._base_attack = base_attack

    def record_swap(self):
        """Decreases swap count by one. Swap count remains >= 0

        Player.record_swaps() -> int
        """
        if self._swap_count > 0:
            self._swap_count -= 1
        return self._swap_count

    def get_swaps(self):
        """Returns player current swap count.

        Player.get_swaps() -> int
        """
        return self._swap_count

    def reset_swaps(self):
        """Resets player swaps to maximum.

        Player.reset_swaps() -> None
        """
        self._swap_count = self._swap_max

    def get_base_attack(self):
        """Returns player base attack modifier.

        Player.get_base_attack() -> int
        """
        return self._base_attack

    def attack(self, runs, defender_type):
        """Takes a list of Run instances and a defender type.
        Calculates damage and then returns list of pairs in form (tile, damage)

        Player.attack(Runs(object), str) -> list(str, int)
        """
        attacks = []
        chain = len(runs)
        print("Chain of attacks: {}".format(chain))
        for run in runs:
            damage = 0
            damage_type = list(run.items())[0][1].get_type()
            print('Attacking with {}'.format(damage_type))

            # Calculate Base Damage
            damage += (len(run) * run.get_max_dimension()
                       * self.get_base_attack())
            print('Base damage: {}'.format(damage))

            # Add Chain bonus
            if chain > 1:
                damage *= (1.0 + (chain / 4))
            print('After chain bonus: {}'.format(damage))

            # Check enemy weaknesses and strengths against damage type
            if defender_type in ENEMY_PROBABILITIES:
                if damage_type == ENEMY_WEAKNESS[defender_type]:
                    damage *= 1.5
                    print("It's super effective!")
                elif damage_type == ENEMY_STRENGTH[defender_type]:
                    damage *= 0.5
                    print("It's not very effective...")
            # print('After weak/str: {}'.format(damage))
            print("Damage dealt to enemy: {}".format(int(damage)))
            # Add to attacks list
            attacks.append((damage_type, int(damage)))
        return attacks


class VersusStatusBar(tk.Frame):
    """Displays game, player, and enemy status."""

    def __init__(self, master):
        """
        Constructor(VersusStatusBar, tk.Frame)
        """
        super().__init__(master)

        # Level Counter
        self._level_lbl = tk.Label(self, text=LEVEL_FORMAT.format(1),
                                   font="Arial 12 bold")
        self._level_lbl.pack(side=tk.TOP, expand=True, fill=tk.X)

        # Health Bars
        self._stats_cvs = tk.Canvas(self, width=GRID_WIDTH, height=20)
        self._stats_cvs.pack(side=tk.TOP, expand=True, fill=tk.X)

        self._player_hp_outline = self._stats_cvs.create_rectangle(10, 5, 100,
                                                                   15, fill="")
        self._player_hp_bar = self._stats_cvs.create_rectangle(10, 5, 110, 15,
                                                               fill="green")

        self._enemy_hp_outline = self._stats_cvs.create_rectangle(440, 5, 540,
                                                                  15, fill="")
        self._enemy_hp_bar = self._stats_cvs.create_rectangle(440, 5, 540, 15,
                                                              fill="red")

        # Player and Enemy Stats
        self._stats_frame = tk.Frame(self)

        self._player_hp = tk.Label(self._stats_frame,
                                   text=HEALTH_FORMAT.format(0),
                                   font="Verdana 8 bold")
        self._player_swaps = tk.Label(self._stats_frame,
                                      text=SWAPS_LEFT_FORMAT.format(0, 's'),
                                      font="Verdana 8 bold")
        self._enemy_hp = tk.Label(self._stats_frame,
                                  text=HEALTH_FORMAT.format(0),
                                  font="Verdana 8 bold")

        self._player_hp.pack(side=tk.LEFT, anchor=tk.W, padx=10)
        self._player_swaps.pack(side=tk.LEFT, expand=True, fill=tk.X,
                                anchor=tk.CENTER)
        self._enemy_hp.pack(side=tk.RIGHT, anchor=tk.E, padx=10)

        self._stats_frame.pack(side=tk.TOP, expand=True, fill=tk.X)

    def update_swaps(self, swaps):
        """Update swaps remaining for Player.

        VersusStatusBar.update_swaps(int) -> None
        """
        if swaps == 1:
            self._player_swaps.config(text=SWAPS_LEFT_FORMAT.format(swaps, ''))
        else:
            self._player_swaps.config(text=SWAPS_LEFT_FORMAT.format(swaps, 's'))

    def update_player_health(self, health, max_health):
        """Updates player health.

        VersusStatusBar.update_player_health(int, int) -> None
        """
        hp_percentage = (health / max_health)
        self._player_hp.config(text=HEALTH_FORMAT.format(health))
        self._stats_cvs.coords(self._player_hp_bar, 10, 5,
                               (10 + 100 * hp_percentage), 15)

    def update_enemy_health(self, health, max_health):
        """Updates enemy health.

        VersusStatusBar.update_enemy_health(int, int) -> None
        """
        hp_percentage = (health / max_health)
        self._enemy_hp.config(text=HEALTH_FORMAT.format(health))
        self._stats_cvs.coords(self._enemy_hp_bar, 440, 5,
                               (440 + (100 * hp_percentage)), 15)

    def update_level(self, level):
        """Updates the level counter in status bar.

        VersusStatusBar.update_level(int) -> None
        """
        self._level_lbl.config(text=LEVEL_FORMAT.format(level))


class ImageTileGridView(TileGridView):
    """Displays images on tile grid."""

    def __init__(self, master, grid, *args, width=GRID_WIDTH,
                 height=GRID_HEIGHT,
                 cell_width=GRID_CELL_WIDTH, cell_height=GRID_CELL_HEIGHT,
                 **kwargs):
        """
        Constructor(ImageTileGridView, TileGrid(EventEmitter), list(str, int),
                    args, int, int, int, int, kwargs)
        """

        # Setup Images
        self._tkImages = dict()
        self._tkImagesLG = dict()
        for colour, img in TILE_IMAGES.items():
            self._tkImages[colour] = ImageTk.PhotoImage(img)
        for colour, img in TILE_IMAGES_LG.items():
            self._tkImagesLG[colour] = ImageTk.PhotoImage(img)

        # Call super
        super().__init__(master, grid, width=GRID_WIDTH,
                         height=GRID_HEIGHT, bg='black')

    def draw_tile_sprite(self, xy_pos, tile, selected):
        """Draws the sprite for the given tile at given (x, y) position.

        ImageTileGridView.draw_tile_sprite(tuple, Tile, bool) -> None
        """
        colour = tile.get_colour()
        x, y = xy_pos
        if selected:
            return self.create_image(x, y, image=self._tkImagesLG[colour])
        else:
            return self.create_image(x, y, image=self._tkImages[colour])


class SinglePlayerTileApp(SimpleTileApp):
    """Top-level GUI for task 2"""

    def __init__(self, master):
        """
        Constructor(SinglePlayerTileApp, SimpleTileApp)
        """
        super().__init__(master)
        self._master = master
        self._master.title("Tile Game v2 - Level {}".format(1))

        self._player1 = None
        self._enemy = None

        # Game State
        self._current_level = 1
        self._game_end = True

        # Listeners
        self._game.on('swap', self._handle_swaps)
        self._game.on('runs', self._handle_runs)
        self._game.on('swap_resolution', self._handle_swap_res)

        # View
        self._grid_view.destroy()
        self._grid_view = ImageTileGridView(
            master, self._game.get_grid(),
            width=GRID_WIDTH, height=GRID_HEIGHT, bg='black')
        self._grid_view.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        # Status Bar
        self._status_bar.pack_forget()
        self._reset_button.pack_forget()
        self._versus_bar = VersusStatusBar(self._master)
        self._versus_bar.pack(side=tk.TOP, expand=True, fill=tk.X)

        # Player & Enemy Graphics
        self._player_img = ImageTk.PhotoImage(PORTRAIT_IMGS['player'])
        self._enemy_img = ImageTk.PhotoImage(PORTRAIT_IMGS['enemy'])

        self._portrait_frame = tk.Frame(self._master)
        self._portrait_cv = tk.Canvas(self._master, width=GRID_WIDTH,
                                      height=PORTRAIT_SIZE[1])
        self._portrait_cv.pack(side=tk.TOP, expand=True, fill=tk.X)

        self._portrait_cv.create_image(PORTRAIT_SIZE[0] / 2 + 10,
                                       PORTRAIT_SIZE[1] / 2,
                                       image=self._player_img)
        self._portrait_cv.create_image(GRID_WIDTH - (PORTRAIT_SIZE[0] / 2 + 10),
                                       PORTRAIT_SIZE[1] / 2,
                                       image=self._enemy_img)

        self._portrait_frame.pack(side=tk.TOP, expand=True, fill=tk.X)

        # Setup
        self.new_game()

    def _handle_swaps(self, from_pos, to_pos):
        """Functionality when swaps on the grid occurs.

        SinglePlayerTileApp._handle_swap(tuple, tuple) -> None
        """
        print("\nSwap handled at {} to {}".format(from_pos, to_pos))
        self._player1.record_swap()
        print("Swaps left: {}".format(self._player1.get_swaps()))
        self._versus_bar.update_swaps(self._player1.get_swaps())

    def _handle_runs(self, runs):
        """Functionality when a run is resolves. Takes a list of runs.

        Player attack resolved.

        SinglePlayerTileApp._handle_run(list) -> None
        """
        attacks = self._player1.attack(runs, self._enemy.get_type())
        for attack in attacks:
            self._enemy.lose_health(attack[1])
            self._versus_bar.update_enemy_health(self._enemy.get_health(),
                                                 self._enemy.get_max_health())

    def _handle_swap_res(self, from_pos, to_pos):
        """Functionality when all runs resolved, resolving final swap.

        Player and Enemy resolves attack.

        SinglePlayerTileApp._handle_swap_res(tuple, tuple) -> None
        """
        print("Swap resolved!")

        # Check enemy state
        if self._enemy.get_health() <= 0:
            print("{} Enemy is defeated!".format(self._enemy.get_type()))
            tk.messagebox.showinfo("Victory!",
                                   "You have won Level {}!"
                                   .format(self.get_level()))
            self._current_level += 1
            return self.start_level(self.get_level())

        # Resolve enemy attack if player swaps finished
        if self._player1.get_swaps() <= 0:
            enemy_damage = self._enemy.attack()
            print("You took {} damage from enemy attack!".format(enemy_damage))
            self._player1.lose_health(enemy_damage)
            self._versus_bar.update_player_health(self._player1.get_health(),
                                                  self._player1.get_max_health())
            self._player1.reset_swaps()
            self._versus_bar.update_swaps(self._player1.get_swaps())

        # Check player state
        if self._player1.get_health() <= 0:
            print("Game over! You have been defeated!")
            if tk.messagebox.askyesno("Game over!",
                                      "You have been defeated!\n"
                                      + "Do you want to start a new game?"):
                self._game_end = True
                return self.new_game()
            else:
                return self.exit_game()

    def new_game(self):
        """Starts new game at level 1.

        SinglePlayerTileApp.new_game() -> None
        """
        if not self._game_end:
            if not tk.messagebox.askyesno("New Game", "Are you sure you want "
                                          + "to start a new game?"):
                return

        # Reset grid level
        self._current_level = 1
        self.start_level(self.get_level())
        self._game_end = False

    def get_level(self):
        """Returns current active level.

        SinglePlayerTileApp.get_level() -> int
        """
        return self._current_level

    def start_level(self, level):
        """Setups a new level, and randomly generates an enemy based on level.

        Higher levels are more difficult.

        SinglePlayerTileApp.start_level() -> None
        """
        # Setup Player
        self._player1 = Player(PLAYER_BASE_HEALTH, SWAPS_PER_TURN,
                               PLAYER_BASE_ATTACK)

        # Setup Enemy
        enemy_prob = WeightedTable(list(ENEMY_PROBABILITIES.items()))
        enemy_hp, enemy_attack = generate_enemy_stats(level)
        enemy_type = enemy_prob.choose()
        self._enemy = Enemy(enemy_type, enemy_hp, enemy_attack)

        # Status
        self._versus_bar.update_enemy_health(self._enemy.get_health(),
                                             self._enemy.get_max_health())
        self._versus_bar.update_player_health(self._player1.get_health(),
                                              self._player1.get_max_health())
        self._versus_bar.update_swaps(self._player1.get_swaps())
        self._versus_bar.update_level(self.get_level())

        # Reload grid
        self._game.reset()
        self._grid_view.draw()
        self._master.title("Tile Game v2 - Level {}".format(self.get_level()))


################################################################################
# Task 3
################################################################################

class ExtendedTileApp(SinglePlayerTileApp):
    """Top level GUI for task 3"""

    def __init__(self, master):
        """
        Inherits game from SinglePlayerTileApp.

        Constructor(ExtendedTileApp, SinglePlayerTileApp)
        """
        # Init super
        super().__init__(master)

        # Setup Sound System with PyGame
        # pygame.mixer.init()
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self._sounds = dict()
        for key, value in SOUNDS.items():
            self._sounds[key] = pygame.mixer.Sound(value)

        self._sounds['bgmusic'].set_volume(0.2)
        self._sounds['bgmusic'].play(-1)
        self._bgOn = True

        # Main Menu
        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)
        # File Menu
        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        # File Menu Items
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Exit", command=self.exit_game)
        # Toggle music
        menubar.add_command(label="Toggle Music", command=self.toggle_bg)

    def exit_game(self):
        """Exits game.

        SimpleTileApp.exit_game() -> None
        """
        self._master.destroy()
        pygame.quit()

    def toggle_bg(self):
        """Toggles background music with PyGame.

        ExtendedTileApp.toggle_bg() -> None
        """
        if self._bgOn:
            self._sounds['bgmusic'].stop()
        else:
            self._sounds['bgmusic'].play(-1)
        self._bgOn = not self._bgOn

    def _handle_runs(self, runs):
        """Functionality when a run is resolves. Takes a list of runs.

        Player attack resolved.

        ExtendedTileApp._handle_run(list) -> None
        """
        # Attacks
        attacks = self._player1.attack(runs, self._enemy.get_type())
        for typ, dmg in attacks:
            self._sounds[typ].play()
            if typ == 'health':
                # Update player health if health potion used
                self._player1.toggle_health_pot()
                self._versus_bar.update_player_health(self._player1.get_health(),
                                                self._player1.get_max_health())
            self._enemy.lose_health(dmg)
            self._versus_bar.update_enemy_health(self._enemy.get_health(),
                                                 self._enemy.get_max_health())

    def _handle_swap_res(self, from_pos, to_pos):
        """Functionality when all runs resolved, resolving final swap.

        Player and Enemy resolves attack.

        ExtendedTileApp._handle_swap_res(tuple, tuple) -> None
        """
        print("Swap resolved!")

        # Check enemy state
        if self._enemy.get_health() <= 0:
            self._sounds['victory'].play()
            print("{} Enemy is defeated!".format(self._enemy.get_type()))
            tk.messagebox.showinfo("Victory!",
                                   "You have won Level {}!"
                                   .format(self.get_level()))
            self._current_level += 1
            return self.start_level(self.get_level())

        # Resolve enemy attack if player swaps finished
        if self._player1.get_swaps() <= 0:
            # Remove power ups
            if self._player1.get_power_status():
                self._player1.toggle_power_up()

            # Enemy attacks
            if self._player1.get_shield_status():
                enemy_damage = self._enemy.attack() * 0.5
                print("Your shield halves incoming damage!")
                self._player1.toggle_shield()
            else:
                enemy_damage = self._enemy.attack()

            self._sounds[self._enemy.get_type()].play()
            print("You took {} damage from enemy attack!".format(enemy_damage))
            self._player1.lose_health(enemy_damage)

            self._versus_bar.update_player_health(self._player1.get_health(),
                                                  self._player1.get_max_health())
            self._player1.reset_swaps()
            self._versus_bar.update_swaps(self._player1.get_swaps())

        # Check player state
        if self._player1.get_health() <= 0:
            self._sounds['gameover'].play()
            print("Game over! You have been defeated!")
            if tk.messagebox.askyesno("Game over!",
                                      "You have been defeated!\n"
                                      + "Do you want to start a new game?"):
                self._game_end = True
                return self.new_game()
            else:
                return self.exit_game()

    def start_level(self, level):
        """Setups a new level, and randomly generates an enemy based on level.

        Higher levels are more difficult.

        ExtendedTileApp.start_level() -> None
        """
        # Setup Player
        self._player1 = ExtPlayer(PLAYER_BASE_HEALTH, SWAPS_PER_TURN,
                                  PLAYER_BASE_ATTACK)

        # Setup Enemy
        enemy_prob = WeightedTable(list(ENEMY_PROBABILITIES.items()))
        enemy_hp, enemy_attack = generate_enemy_stats(level)
        enemy_type = enemy_prob.choose()
        self._enemy = Enemy(enemy_type, enemy_hp, enemy_attack)

        # Status
        self._versus_bar.update_enemy_health(self._enemy.get_health(),
                                             self._enemy.get_max_health())
        self._versus_bar.update_player_health(self._player1.get_health(),
                                              self._player1.get_max_health())
        self._versus_bar.update_swaps(self._player1.get_swaps())
        self._versus_bar.update_level(self.get_level())

        # Reload grid
        self._game.reset()
        self._grid_view.draw()
        self._master.title(
            "Tile Game v2 - Level {}".format(self.get_level()))


class ExtPlayer(Player):
    """Represents human player, inherits from Character superclass"""

    def __init__(self, max_health, swaps_per_turn, base_attack):
        """Tracks:
        - Max swaps and current swap count for player
        - Player base attack

        Constructor(Player, int, int, int)
        Precondition: swaps_per_turn > 0
        Precondition: max_health > 0
        Precondition: base_attack > 0

        """
        super().__init__(max_health, swaps_per_turn, base_attack)
        self._power = False
        self._shield = False
        self._health_pot = False
        print('using extended player')

    def attack(self, runs, defender_type):
        """Takes a list of Run instances and a defender type.
        Calculates damage and then returns list of pairs in form (tile, damage)

        Player.attack(Runs(object), str) -> list(str, int)
        """
        attacks = []
        chain = len(runs)
        print("Chain of attacks: {}".format(chain))
        for run in runs:
            damage = 0
            damage_type = list(run.items())[0][1].get_type()
            # Check Power Up - Power Up does no damage
            if damage_type == 'power':
                if not self.get_power_status():
                    self.toggle_power_up()
                    print("Attacks boosted by 50% from Power Potion!")
                    attacks.append((damage_type, int(damage)))
                continue

            if damage_type == 'health':
                health = (self.get_max_health() / 2) * random.uniform(0.8, 1.2)
                self.gain_health(health)
                self.toggle_health_pot()
                print("Restored {} health!".format(health))
                attacks.append((damage_type, int(damage)))
                continue

            if damage_type == 'shield':
                if not self.get_shield_status():
                    self.toggle_shield()
                    print("Shield up!")
                attacks.append((damage_type, int(damage)))
                continue

            # Calculate Attacks when no item used
            if self.get_power_status():
                base_attack = self.get_base_attack() * 1.5
            else:
                base_attack = self.get_base_attack()
            print('Attacking with {}'.format(damage_type))

            # Calculate Base Damage
            damage += (len(run) * run.get_max_dimension()
                       * base_attack)
            print('Base damage: {}'.format(damage))

            # Add Chain bonus
            if chain > 1:
                damage *= (1.0 + (chain / 4))
            print('After chain bonus: {}'.format(damage))

            # Check enemy weaknesses and strengths against damage type
            if defender_type in ENEMY_PROBABILITIES:
                if damage_type == ENEMY_WEAKNESS[defender_type]:
                    damage *= 1.5
                    print("It's super effective!")
                elif damage_type == ENEMY_STRENGTH[defender_type]:
                    damage *= 0.5
                    print("It's not very effective...")
            # print('After weak/str: {}'.format(damage))
            print("Damage dealt to enemy: {}".format(int(damage)))
            # Add to attacks list
            attacks.append((damage_type, int(damage)))
        return attacks

    def toggle_power_up(self):
        """Toggles player power up status.

        ExtPlayer.toggle_power_up() -> None
        """
        self._power = not self._power

    def toggle_shield(self):
        """Toggles player shield status.

        ExtPlayer.toggle_shield() -> None
        """
        self._shield = not self._shield

    def toggle_health_pot(self):
        """Toggle health potion use.

        ExtPlayer.toggle_health_pot() -> None
        """
        self._health_pot = not self._health_pot

    def get_power_status(self):
        """Returns player power up status.

        ExtPlayer.get_power_status() -> bool
        """
        return self._power

    def get_shield_status(self):
        """Returns player shield status.

        ExtPlayer.get_shield_status() -> bool
        """
        return self._shield

    def get_health_status(self):
        """Returns player health potion usage status.

        ExtPlayer.get_health_status() -> bool
        """
        return self._health_pot


def task1():
    # Add task 1 GUI code here
    root = tk.Tk()
    app = SimpleTileApp(root)
    root.mainloop()

def task2():
    # Add task 2 GUI code here
    root = tk.Tk()
    app = SinglePlayerTileApp(root)
    root.mainloop()

def task3():
    # Add task 3 GUI code here

    root = tk.Tk()
    app = ExtendedTileApp(root)
    root.mainloop()

def main():
    # Choose relevant task to run
    # task1()
    # task2()
    task3()

if __name__ == '__main__':
    main()
