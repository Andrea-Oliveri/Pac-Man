# -*- coding: utf-8 -*-

import pyglet.media

from src.constants import (SoundEffects,
                           SOUND_EFFECTS_PATHS)



class Sounds:
    
    def __init__(self):
        self._effects = {k: pyglet.media.StaticSource(pyglet.media.load(v)) for k, v in SOUND_EFFECTS_PATHS.items()}
        
        self._player_single = pyglet.media.Player()
        self._player_loop   = pyglet.media.Player()
        self._player_loop.loop = True

        self._player_extra_life = pyglet.media.Player()

        self._munch_counter = 0

    
    def stop_all(self):
        for player in self._player_single, self._player_loop, self._player_extra_life:
            player.next_source()


    def _play_once(self, key):
        player = self._player_extra_life if key == SoundEffects.EXTRA_LIFE else self._player_single

        player.queue(self._effects[key])
        player.play()


    def _play_repeat(self, key):
        self._player_loop.queue(self._effects[key])
        self._player_loop.play()


    def notify_pellet_eaten(self):
        key = SoundEffects.MUNCH_2 if self._munch_counter % 2 else SoundEffects.MUNCH_1
        self._munch_counter += 1

        self._play_once(key)


    def notify_fruit_eaten(self):
        self._play_once(SoundEffects.EAT_FRUIT)


    def notify_ghost_eaten(self):
        self._play_once(SoundEffects.EAT_GHOST)

    
    def notify_extra_life(self):
        self._play_once(SoundEffects.EXTRA_LIFE)


    def notify_life_lost(self):
        self._play_once(SoundEffects.LIFE_LOST)


    def notify_first_welcome(self):
        self._play_once(SoundEffects.GAME_START_MUSIC)

    
    def notify_intermission(self):
        self._play_repeat(SoundEffects.INTERMISSION_MUSIC)
