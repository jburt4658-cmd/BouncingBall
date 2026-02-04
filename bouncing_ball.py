import pygame
import math
import sys
import json

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
WIDTH, HEIGHT = 576, 1024
INFO_WIDTH, INFO_HEIGHT = 300, 200
FPS = 90
BACKGROUND_COLOR = (20, 20, 30)
CIRCLE_COLOR = (100, 200, 255)
BALL_COLOR = (255, 100, 100)

# Physics constants
GRAVITY = 0.3  # Reduced gravity for slower bouncing
BOUNCE_DAMPING = 1.02  # Energy loss on bounce (higher = more bouncy)
SHRINK_FACTOR = 0.995   # Circle shrinks to 99% of size each bounce (less shrinking)

# Circle properties
circle_center = (WIDTH // 2, HEIGHT // 2)
circle_radius = 350
initial_radius = circle_radius

# Ball properties
ball_radius = 20  # Increased from 15 to 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2 - 200  # Start near top
ball_vx = 4  # Horizontal velocity (reduced for slower bouncing)
ball_vy = 0  # Vertical velocity
ball_color = BALL_COLOR
border_color = (128, 128, 128)  # Grey border

# Camera properties
camera_x = 0
camera_y = 0

# Trail properties
trail = []
# No max_trail_length - trail lasts forever!

# Track bounces
bounce_count = 0
hue = 0  # For rainbow color cycling

# Shared data file for info window
DATA_FILE = "/tmp/ball_info.json"

# Function to convert HSV to RGB for smooth rainbow colors
def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB. h is 0-360, s and v are 0-1"""
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

# Function to create beep sound
def make_beep(frequency=440, duration=0.08):
    """Generate a beep sound at given frequency"""
    try:
        import numpy as np
        
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        
        # Generate sine wave
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(2 * math.pi * frequency * t)
        
        # Apply envelope to prevent clicks (exponential decay)
        envelope = np.exp(-t * 15)
        wave = wave * envelope
        
        # Convert to 16-bit integer
        wave = np.int16(wave * 32767)
        
        # Make stereo
        stereo_wave = np.column_stack((wave, wave))
        
        # Create sound
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    except ImportError:
        print("NumPy not found. Install with: pip install numpy")
        return None

# Setup main display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Shrinking Circle")
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Apply gravity
    ball_vy += GRAVITY
    
    # Update position
    ball_x += ball_vx
    ball_y += ball_vy
    
    # Update camera to follow ball smoothly, but center when circle is small
    if circle_radius < 40:
        # Center the camera on the circle center when radius is small
        camera_x = circle_center[0] - WIDTH // 2
        camera_y = circle_center[1] - HEIGHT // 2
    else:
        # Follow the ball
        camera_x = ball_x - WIDTH // 2
        camera_y = ball_y - HEIGHT // 2
    
    # Update rainbow color smoothly
    hue = (hue + 2) % 360  # Cycle through hues
    ball_color = hsv_to_rgb(hue, 1.0, 1.0)  # Full saturation and brightness
    
    # Add current position to trail (trail lasts forever)
    trail.append((int(ball_x), int(ball_y), ball_color))
    
    # Check collision with circle boundary
    dx = ball_x - circle_center[0]
    dy = ball_y - circle_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    
    # If ball hits the circle edge
    if distance + ball_radius >= circle_radius:
        # Normalize the distance vector
        if distance > 0:
            nx = dx / distance
            ny = dy / distance
        else:
            nx, ny = 1, 0
        
        # Position ball at circle boundary
        ball_x = circle_center[0] + nx * (circle_radius - ball_radius)
        ball_y = circle_center[1] + ny * (circle_radius - ball_radius)
        
        # Calculate velocity dot normal
        dot_product = ball_vx * nx + ball_vy * ny
        
        # Reflect velocity
        ball_vx = ball_vx - 2 * dot_product * nx
        ball_vy = ball_vy - 2 * dot_product * ny
        
        # Apply damping
        ball_vx *= BOUNCE_DAMPING
        ball_vy *= BOUNCE_DAMPING
        
        # Shrink the circle
        circle_radius *= SHRINK_FACTOR
        bounce_count += 1
        
        # Play beep sound with pitch that increases as circle shrinks
        # Map radius to frequency: larger circle = lower pitch, smaller = higher
        # As circle goes from 350 -> 0, frequency goes from 300 -> 800 Hz
        radius_ratio = circle_radius / initial_radius
        frequency = int(800 - (radius_ratio * 500))  # Starts at ~300Hz, goes up to 800Hz
        frequency = max(250, min(1200, frequency))  # Clamp between 250-1200 Hz
        
        beep = make_beep(frequency, 0.08)
        if beep:
            beep.play()
        
        # Prevent circle from getting too small
        if circle_radius < ball_radius + 5:
            circle_radius = ball_radius + 5
    
    # Clear screen
    screen.fill(BACKGROUND_COLOR)
    
    # Calculate positions relative to camera
    circle_screen_x = circle_center[0] - camera_x
    circle_screen_y = circle_center[1] - camera_y
    ball_screen_x = ball_x - camera_x
    ball_screen_y = ball_y - camera_y
    
    # Draw circle
    pygame.draw.circle(screen, CIRCLE_COLOR, (int(circle_screen_x), int(circle_screen_y)), int(circle_radius), 3)
    
    # Draw watermark text above the circle
    watermark_font = pygame.font.Font(None, 32)
    watermark_text = watermark_font.render("@mbrt07xd", True, (255, 255, 255))
    text_rect = watermark_text.get_rect(center=(int(circle_screen_x), int(circle_screen_y - circle_radius - 30)))
    screen.blit(watermark_text, text_rect)
    
    # Filter trail to only show positions inside the circle
    visible_trail = []
    for tx, ty, tcolor in trail:
        dx = tx - circle_center[0]
        dy = ty - circle_center[1]
        distance = math.sqrt(dx**2 + dy**2)
        # Keep trail point if it's inside the circle
        if distance <= circle_radius:
            visible_trail.append((tx, ty, tcolor))
    
    # Draw trail with fading effect
    for i, (tx, ty, tcolor) in enumerate(visible_trail):
        # Calculate alpha based on position in trail (older = more transparent)
        alpha = int(255 * (i / len(visible_trail)) ** 2) if len(visible_trail) > 0 else 255
        trail_radius = int(ball_radius * 0.7)  # Trail circles are smaller
        
        # Apply camera offset to trail position
        trail_screen_x = tx - camera_x
        trail_screen_y = ty - camera_y
        
        # Create surface for alpha blending
        trail_surface = pygame.Surface((trail_radius * 2, trail_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, (*tcolor, alpha), (trail_radius, trail_radius), trail_radius)
        screen.blit(trail_surface, (trail_screen_x - trail_radius, trail_screen_y - trail_radius))
    
    # Draw ball with grey border (always centered on screen since camera follows it)
    pygame.draw.circle(screen, ball_color, (int(ball_screen_x), int(ball_screen_y)), ball_radius)
    pygame.draw.circle(screen, border_color, (int(ball_screen_x), int(ball_screen_y)), ball_radius, 2)
    
    # Update display
    pygame.display.flip()
    clock.tick(FPS)
    
    # Write data to shared file for info window
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({'bounces': bounce_count, 'radius': circle_radius}, f)
    except:
        pass

pygame.quit()
sys.exit()
