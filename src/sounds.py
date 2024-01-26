# -*- coding: utf-8 -*-

import lzma

import pyglet.media

from src.constants import (SoundEffects,
                           SOUND_EFFECTS_PATHS,
                           THR_PELLETS_SIREN_SOUNDS)



class Sounds:
    
    def __init__(self):
        self._effects = {}
        for key, path in SOUND_EFFECTS_PATHS.items():
            file = lzma.open(path, 'r') if path.lower().endswith('.xz') else None
            self._effects[key] = pyglet.media.load(path, file, streaming = False)

        self._player_single = pyglet.media.Player()
        self._player_loop   = pyglet.media.Player()
        self._player_loop.loop = True

        self._munch_counter = 0
        self._current_player_loop_sound = None

    
    def stop(self, only_sirens = False):
        self._current_player_loop_sound = None

        players_to_stop = [self._player_loop]

        if not only_sirens:
            players_to_stop.append(self._player_single)

        for player in self._player_single, self._player_loop:
            player.pause()

            # Clear queued sources.
            source = not None
            while source is not None:
                source = player.next_source()


    def _play_once(self, key):
        if key is SoundEffects.EXTRA_LIFE:
            self._effects[key].play()
            return
        
        self._player_single.queue(self._effects[key])
        self._player_single.play()


    def _play_repeat(self, key):
        # Check if already playing.
        if key == self._current_player_loop_sound:
            return

        self.stop(only_sirens = True)
        self._player_loop.queue(self._effects[key])
        self._player_loop.play()
        self._current_player_loop_sound = key


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


    def queue_correct_siren(self, n_pellets, fright_on, any_ghost_retreating):
        expected_siren = None

        if any_ghost_retreating:
            expected_siren = SoundEffects.GHOST_RETREATING
        elif fright_on:
            expected_siren = SoundEffects.FRIGHT_ON
        else:
            for siren_source, threshold in THR_PELLETS_SIREN_SOUNDS:
                if n_pellets <= threshold:
                    expected_siren = siren_source
                    break

        self._play_repeat(expected_siren)