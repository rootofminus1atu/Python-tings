import pygame

pygame.init()
pygame.mixer.init()
firstSound = pygame.mixer.music('/home/pi/laserharp-sounds/samples/ambi_dark.wav')
secondSound = pygame.mixer.music('/home/pi/laserharp-sounds/samples/ambi_choir.wav')
firstSound.play()
secondSound.play()