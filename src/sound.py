import os
import pygame


class SoundManager:
    def __init__(self):
        # Initialize sound system
        pygame.mixer.quit()  # First close any running sound system
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.set_num_channels(8)  # Set more channels

        # Initialize sound properties
        self.eat_sound = None
        self.crash_sound = None
        self.background_music = None
        self.background_channel = pygame.mixer.Channel(0)

        # Load sounds
        self.load_sounds()

    def load_sound(self, file_path):
        """Load a sound file and return the Sound object."""
        if not os.path.exists(file_path):
            print(f"Sound file not found: {file_path}")
            return None
        try:
            sound = pygame.mixer.Sound(file_path)
            print(f"Successfully loaded sound: {file_path}")
            return sound
        except Exception as sound_load_error:
            print(f"Failed to load sound file {file_path}: {str(sound_load_error)}")
            return None

    def load_sounds(self):
        """Load all game sounds."""
        self.eat_sound = self.load_sound("sounds/eat.wav")
        self.crash_sound = self.load_sound("sounds/crash.wav")
        self.background_music = self.load_sound("sounds/background.mp3")

        # Set volumes
        if self.eat_sound:
            self.eat_sound.set_volume(0.4)
        if self.crash_sound:
            self.crash_sound.set_volume(0.3)
        if self.background_music:
            self.background_music.set_volume(0.8)
            self.background_channel.set_volume(0.8)

    def play_background_music(self):
        """Start playing background music on loop."""
        if self.background_music:
            try:
                self.background_channel.play(self.background_music, loops=-1)
                print("Background music started playing")
            except Exception as e:
                print(f"Failed to play background music: {str(e)}")

    def play_eat_sound(self):
        """Play the eating sound effect."""
        if self.eat_sound:
            self.eat_sound.play()

    def play_crash_sound(self):
        """Play the crash sound effect."""
        if self.crash_sound:
            self.crash_sound.play()
