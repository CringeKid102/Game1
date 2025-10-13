import pygame
import sys
import os
import time
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Game with Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
    
# Load assets
