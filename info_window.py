import pygame
import sys
import json
import os

# Initialize Pygame
pygame.init()

# Constants
INFO_WIDTH, INFO_HEIGHT = 300, 200
BACKGROUND_COLOR = (20, 20, 30)

# Setup display
screen = pygame.display.set_mode((INFO_WIDTH, INFO_HEIGHT))
pygame.display.set_caption("Info - Bounces & Radius")
clock = pygame.time.Clock()

# Shared data file
DATA_FILE = "/tmp/ball_info.json"

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Read data from shared file
    bounce_count = 0
    circle_radius = 0
    
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                bounce_count = data.get('bounces', 0)
                circle_radius = data.get('radius', 0)
    except:
        pass
    
    # Clear screen
    screen.fill(BACKGROUND_COLOR)
    
    # Display bounce count and radius
    font = pygame.font.Font(None, 48)
    
    bounce_text = font.render(f"Bounces: {bounce_count}", True, (255, 255, 255))
    screen.blit(bounce_text, (20, 40))
    
    radius_text = font.render(f"Radius: {int(circle_radius)}", True, (255, 255, 255))
    screen.blit(radius_text, (20, 100))
    
    # Update display
    pygame.display.flip()
    clock.tick(30)  # Info window doesn't need high FPS

pygame.quit()
sys.exit()
