import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
GRID_SIZE = 40
FPS = 30
FONT_SIZE = 36

# Directions (x, y offsets)
DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}

# Game Variables
player_pos = [1, 1]
player_orientation = 0  # Initial orientation in degrees (0 = facing up)
hydrogen = 100
points = 0
hydrogen_collected = 0
unlock_threshold = 2
unlocked_walls = 0
TARGET_POINTS = 5000
hydrogen_stations = 0

# Maze Grid (0: path, 1: wall, 2: fuel station)
maze_template = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Initialize the Pygame display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HydroDrive 5000 Challenge")

# Paths to Images
car_image_path = "truck.jpg"
station_image_path = "hydrogen.png"
grass_texture_path = "grass.jpg"

# Load and Resize Images
car_image = pygame.image.load(car_image_path)
car_image = pygame.transform.scale(car_image, (GRID_SIZE, GRID_SIZE))

station_image = pygame.image.load(station_image_path)
station_image = pygame.transform.scale(station_image, (GRID_SIZE, GRID_SIZE))

grass_texture = pygame.image.load(grass_texture_path)
grass_texture = pygame.transform.scale(grass_texture, (GRID_SIZE, GRID_SIZE))

# Font
font = pygame.font.SysFont(None, FONT_SIZE)

# Notices
notices = []
notice_duration = 90  # Frames (~3 seconds)

# Particles
particles = []

# Sounds
move_sound = pygame.mixer.Sound("carmove.wav")
collect_sound = pygame.mixer.Sound("Collectsound.mp3")
unlock_sound = pygame.mixer.Sound("Unlock.wav")
low_hydrogen_sound = pygame.mixer.Sound("low battery.wav")

# Background music
pygame.mixer.music.load("backgroundmusic.mp3")
pygame.mixer.music.set_volume(0.5)

# Difficulty level
hydrogen_consumption_rate = 1.0

# Add notice
def add_notice(message):
    notices.append({"message": message, "timer": notice_duration})

# Randomize fuel stations
def randomize_placements():
    empty_cells = [(row_idx, col_idx) for row_idx, row in enumerate(maze_template)
                   for col_idx, cell in enumerate(row) if cell == 0]
    random.shuffle(empty_cells)
    for _ in range(10):  # Place 10 fuel stations
        if empty_cells:
            x, y = empty_cells.pop()
            maze_template[x][y] = 2

# Unlock one random wall if conditions are met
def unlock_one_wall():
    global hydrogen_collected, unlocked_walls
    if hydrogen_collected >= unlock_threshold:
        wall_cells = [(row_idx, col_idx) for row_idx, row in enumerate(maze_template)
                      for col_idx, cell in enumerate(row) if cell == 1]
        if wall_cells:
            x, y = random.choice(wall_cells)
            maze_template[x][y] = 0
            hydrogen_collected = 0
            unlocked_walls += 1
            add_notice(f"New routes created  at ({x}, {y})!")
            unlock_sound.play()

# Build a refueling station
def build_station():
    global points, hydrogen_stations
    if points >= 100:
        points -= 100
        hydrogen_stations += 1
        empty_cells = [(row_idx, col_idx) for row_idx, row in enumerate(maze_template)
                       for col_idx, cell in enumerate(row) if cell == 0]
        if empty_cells:
            x, y = random.choice(empty_cells)
            maze_template[x][y] = 2
            add_notice(f"Station built at ({x}, {y})!")

# Draw functions
def draw_maze():
    for row_idx, row in enumerate(maze_template):
        for col_idx, cell in enumerate(row):
            rect = pygame.Rect(col_idx * GRID_SIZE, row_idx * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if cell == 1:
                pygame.draw.rect(screen, (255, 255, 255), rect)
            elif cell == 0:
                screen.blit(grass_texture, rect.topleft)
            elif cell == 2:
                screen.blit(station_image, rect.topleft)

def draw_player():
    rect = pygame.Rect(player_pos[1] * GRID_SIZE, player_pos[0] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    screen.blit(car_image, rect.topleft)

def draw_notices():
    notice_y = len(maze_template) * GRID_SIZE + 10
    for notice in notices:
        alpha = int((notice["timer"] / notice_duration) * 255)
        notice_surface = font.render(notice["message"], True, (255, 0, 0))
        notice_surface.set_alpha(alpha)
        screen.blit(notice_surface, (10, notice_y))
        notice_y += 30

def draw_hud():
    hydrogen_bar_width = 300
    hydrogen_bar_height = 20
    filled_width = (hydrogen / 100) * hydrogen_bar_width

    # Draw the hydrogen bar
    pygame.draw.rect(screen, (255, 0, 0), (10, SCREEN_HEIGHT - 70, hydrogen_bar_width, hydrogen_bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (10, SCREEN_HEIGHT - 70, filled_width, hydrogen_bar_height))

    # Render hydrogen bar label
    hydrogen_text = font.render(f"Hydrogen: {int(hydrogen)}%", True, (255, 255, 255))
    screen.blit(hydrogen_text, (10, SCREEN_HEIGHT - 95))  # Position above the hydrogen bar

    # Render points and stations with adjusted spacing
    points_text = font.render(f"Points: {points}/{TARGET_POINTS}", True, (255, 255, 255))
    stations_text = font.render(f"Stations: {hydrogen_stations}", True, (255, 255, 255))

    # Adjust Y-coordinates to create more spacing
    screen.blit(points_text, (10, SCREEN_HEIGHT - 120))  # Move points higher
    screen.blit(stations_text, (10, SCREEN_HEIGHT - 40))  # Keep stations at the same position


# Particles
def add_particle(x, y):
    for _ in range(10):
        particles.append({
            "x": x + random.randint(-5, 5),
            "y": y + random.randint(-5, 5),
            "dx": random.uniform(-1, 1),
            "dy": random.uniform(-1, 1),
            "timer": 50
        })

def update_particles():
    for particle in particles:
        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]
        particle["timer"] -= 1
    particles[:] = [p for p in particles if p["timer"] > 0]

# Update notices by reducing their timer and removing expired ones
def update_notices():
    for notice in notices:
        notice["timer"] -= 1
    # Remove notices with timers <= 0
    notices[:] = [notice for notice in notices if notice["timer"] > 0]


def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, (255, 255, 0), (int(particle["x"]), int(particle["y"])), 3)

# Difficulty menu
def difficulty_menu():
    screen.fill((0, 0, 0))
    easy_button = pygame.Rect(300, 200, 400, 50)
    medium_button = pygame.Rect(300, 300, 400, 50)
    hard_button = pygame.Rect(300, 400, 400, 50)

    pygame.draw.rect(screen, (0, 255, 0), easy_button)
    pygame.draw.rect(screen, (255, 255, 0), medium_button)
    pygame.draw.rect(screen, (255, 0, 0), hard_button)

    easy_text = font.render("Easy", True, (0, 0, 0))
    medium_text = font.render("Medium", True, (0, 0, 0))
    hard_text = font.render("Hard", True, (0, 0, 0))

    screen.blit(easy_text, (400, 210))
    screen.blit(medium_text, (380, 310))
    screen.blit(hard_text, (400, 410))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    return 0.5
                elif medium_button.collidepoint(event.pos):
                    return 1.0
                elif hard_button.collidepoint(event.pos):
                    return 1.5

# Movement logic
def move_player(dx, dy):
    global hydrogen, points, hydrogen_collected, player_orientation
    new_x = player_pos[1] + dy
    new_y = player_pos[0] + dx
    if hydrogen <= 0:
        return
    if 0 <= new_x < len(maze_template[0]) and 0 <= new_y < len(maze_template):
        if maze_template[new_y][new_x] != 1:
            player_pos[1] = new_x
            player_pos[0] = new_y
            move_sound.play()

            # Update orientation based on direction
            if dx == -1 and dy == 0:  # Moving up
                player_orientation = 0
            elif dx == 1 and dy == 0:  # Moving down
                player_orientation = 180
            elif dx == 0 and dy == -1:  # Moving left
                player_orientation = 90
            elif dx == 0 and dy == 1:  # Moving right
                player_orientation = -90

            # Check for hydrogen cell collection
            if maze_template[new_y][new_x] == 2:
                hydrogen = min(100, hydrogen + 20)
                points += 500
                hydrogen_collected += 1
                maze_template[new_y][new_x] = 0
                collect_sound.play()
                add_notice("Hydrogen cell collected!")
                add_particle(player_pos[1] * GRID_SIZE + GRID_SIZE // 2,
                             player_pos[0] * GRID_SIZE + GRID_SIZE // 2)
            hydrogen -= hydrogen_consumption_rate
    if hydrogen <= 20:
        low_hydrogen_sound.play()


# Start screen
def start_screen():
    pygame.mixer.music.play(-1)
    screen.fill((0, 0, 0))
    title_font = pygame.font.SysFont(None, 64)
    title = title_font.render("Welcome to the HydroDrive Coders Game!", True, (255, 255, 255))
    instructions = [
        "Use arrow keys to move your car.",
        "Collect hydrogen cells (blue) to refuel.",
        "Build stations (press 'B') using 100 points.",
        "Unlock new paths automatically by collecting 2 hydrogen cells.",
        "Your goal: Earn 5000 points before running out of hydrogen.",
    ]
    start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50)

    # Draw Title and Instructions
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    for i, line in enumerate(instructions):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (50, 200 + i * 40))

    # Draw Start Button
    pygame.draw.rect(screen, (0, 200, 0), start_button)
    start_text = font.render("Start", True, (0, 0, 0))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 110))

    pygame.display.update()

    # Wait for the player to click Start
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

# Main game loop
def game_loop():
    global hydrogen, points, hydrogen_consumption_rate
    hydrogen_consumption_rate = difficulty_menu()
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_maze()
        draw_player()
        draw_particles()
        draw_notices()
        draw_hud()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(-1, 0)
                elif event.key == pygame.K_DOWN:
                    move_player(1, 0)
                elif event.key == pygame.K_LEFT:
                    move_player(0, -1)
                elif event.key == pygame.K_RIGHT:
                    move_player(0, 1)
                elif event.key == pygame.K_b:
                    build_station()
        unlock_one_wall()
        update_particles()
        update_notices()  # Fixed function call
        if points >= TARGET_POINTS:
            win_text = font.render("Mission Complete!", True, (255, 255, 255))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False
        elif hydrogen <= 0:
            lose_text = font.render("Game Over!", True, (255, 255, 255))
            screen.blit(lose_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            running = False
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
    pygame.quit()


# Run the game
randomize_placements()
start_screen()
game_loop()
