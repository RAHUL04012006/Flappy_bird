import pygame
import sys
import random

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Game constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
PIPE_GAP = 120
PIPE_WIDTH = 52
BIRD_WIDTH = 34
BIRD_HEIGHT = 24

# Physics constants
GRAVITY = 0.25
JUMP_FORCE = -5.0  # Slightly stronger than original
MAX_FALL_SPEED = 8

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Game variables
bird_movement = 0
game_active = False  
score = 0
high_score = 0
base_speed = 2
current_speed = base_speed
passed_pipes = set()  # To track which pipes we've passed
pipe_counter = 0  # Unique counter for each pipe pair

# Load images
bg_surface = pygame.image.load('flappy_background.jpg').convert()
bg_surface = pygame.transform.scale(bg_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))

bird_surface = pygame.image.load('bird1.png').convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (BIRD_WIDTH, BIRD_HEIGHT))
bird_rect = bird_surface.get_rect(center=(100, WINDOW_HEIGHT // 2))

pipe_surface = pygame.image.load('pipe.png').convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (PIPE_WIDTH, WINDOW_HEIGHT))
pipe_list = []

# Load sound effects
flap_sound = pygame.mixer.Sound('flap.mp3')
hit_sound = pygame.mixer.Sound('hit.mp3')
point_sound = pygame.mixer.Sound('point.mp3')

# Game events
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

PIPE_HEIGHTS = [200, 250, 300, 350, 400]

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= WINDOW_HEIGHT:
            window.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            window.blit(flip_pipe, pipe)

def create_pipe():
    global pipe_counter
    random_pipe_pos = random.choice(PIPE_HEIGHTS)
    bottom_pipe = pipe_surface.get_rect(midtop=(WINDOW_WIDTH + PIPE_WIDTH, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(WINDOW_WIDTH + PIPE_WIDTH, random_pipe_pos - PIPE_GAP))
    pipe_counter += 1
    return (bottom_pipe, top_pipe, pipe_counter)  # Return pipe pair with unique ID

def move_pipes(pipes):
    global current_speed, score
    current_speed = base_speed + (score * 0.002)
    
    new_pipes = []
    for pipe in pipes:
        bottom_pipe, top_pipe, pipe_id = pipe
        bottom_pipe.centerx -= current_speed
        top_pipe.centerx -= current_speed
        
        # Score when bird passes the right edge of the pipe
        if 100 < bottom_pipe.right < 105 and pipe_id not in passed_pipes:
            score += 1
            passed_pipes.add(pipe_id)
            point_sound.play()
        
        if bottom_pipe.right > -PIPE_WIDTH:
            new_pipes.append((bottom_pipe, top_pipe, pipe_id))
    
    return new_pipes

def check_collision(pipes):
    global game_active
    # Check if bird hits ground or ceiling
    if bird_rect.top <= -50 or bird_rect.bottom >= WINDOW_HEIGHT:
        hit_sound.play()
        game_active = False
        return False

    # Check pipe collisions
    for pipe in pipes:
        bottom_pipe, top_pipe, _ = pipe
        if bird_rect.colliderect(bottom_pipe) or bird_rect.colliderect(top_pipe):
            hit_sound.play()
            game_active = False
            return False
    return True

def rotate_bird(bird):
    rotation = -bird_movement * 6
    rotation = max(-90, min(45, rotation))
    return pygame.transform.rotozoom(bird, rotation, 1)

def display_score():
    font = pygame.font.SysFont('Arial', 30, bold=True)
    score_surface = font.render(str(int(score)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
    window.blit(score_surface, score_rect)

def reset_game():
    global bird_movement, pipe_list, score, current_speed, game_active, passed_pipes, pipe_counter
    pipe_list.clear()
    passed_pipes.clear()
    pipe_counter = 0
    bird_rect.center = (100, WINDOW_HEIGHT // 2)
    bird_movement = 0
    score = 0
    current_speed = base_speed
    game_active = True

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement += JUMP_FORCE
                    flap_sound.play()
                else:
                    reset_game()
        if event.type == SPAWNPIPE and game_active:
            pipe_list.append(create_pipe())

    window.blit(bg_surface, (0, 0))

    if game_active:
        # Bird physics
        bird_movement += GRAVITY
        bird_movement = min(bird_movement, MAX_FALL_SPEED)
        bird_rect.centery += bird_movement
        
        rotated_bird = rotate_bird(bird_surface)
        window.blit(rotated_bird, bird_rect)
        
        # Pipes
        pipe_list = move_pipes(pipe_list)
        for pipe in pipe_list:
            bottom_pipe, top_pipe, _ = pipe
            draw_pipes([bottom_pipe, top_pipe])
        game_active = check_collision(pipe_list)

        display_score()
    else:
        # Game over screen
        font = pygame.font.SysFont('Arial', 30, bold=True)
        game_over_surface = font.render('Game Over', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        window.blit(game_over_surface, game_over_rect)
        
        score_surface = font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        window.blit(score_surface, score_rect)
        
        high_score = max(score, high_score)
        high_score_surface = font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        window.blit(high_score_surface, high_score_rect)
        
        restart_font = pygame.font.SysFont('Arial', 20)
        restart_surface = restart_font.render('Press SPACE to restart', True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        window.blit(restart_surface, restart_rect)

    pygame.display.update()
    clock.tick(60)