"""Simple original sound effects generated with Python and Pygame."""

import math
from array import array

import pygame


class SoundEffects:
    def __init__(self):
        self.enabled = False

        try:
            pygame.mixer.quit()
            pygame.mixer.init(
                frequency=22050,
                size=-16,
                channels=1,
                buffer=512,
            )
            self.sample_rate = 22050

            self.coin_sound = self._make_tone(
                start_frequency=900,
                end_frequency=1300,
                duration=0.12,
                volume=0.35,
            )
            self.stomp_sound = self._make_tone(
                start_frequency=260,
                end_frequency=90,
                duration=0.16,
                volume=0.45,
            )
            self.enabled = True
        except pygame.error:
            # The game can still run if the computer has no audio device.
            self.enabled = False

    def _make_tone(self, start_frequency, end_frequency, duration, volume):
        sample_count = int(self.sample_rate * duration)
        samples = array("h")

        for index in range(sample_count):
            progress = index / sample_count
            frequency = start_frequency + (
                end_frequency - start_frequency
            ) * progress
            envelope = (1 - progress) ** 2
            wave_value = math.sin(
                2 * math.pi * frequency * index / self.sample_rate
            )
            samples.append(int(32767 * volume * envelope * wave_value))

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play_coin(self):
        if self.enabled:
            self.coin_sound.play()

    def play_stomp(self):
        if self.enabled:
            self.stomp_sound.play()