import pygame
import noise
import random

# Set the resolution and size of the world
WIDTH, HEIGHT = 800, 600  # Pixel dimensions
TILE_SIZE = 40  # Size of each tile on screen (in pixels)
TERRAIN_WIDTH, TERRAIN_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

# Define terrain types
TERRAIN_TYPES = ['Soil', 'Rock', 'Radiation', 'Water']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural World Generation")

# Generate Perlin Noise based terrain
def generate_terrain():
    terrain_grid = []
    scale = 5.0  # Controls the granularity of the noise
    seed = random.randint(0, 100)  # Generate a random seed
    for y in range(TERRAIN_HEIGHT):
        row = []
        for x in range(TERRAIN_WIDTH):
            noise_value = noise.pnoise2(x / scale, y / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=seed)
            if noise_value < -0.033:
                terrain_type = 'Soil'
            elif noise_value < 0.033:
                terrain_type = 'Rock'
            elif noise_value < 0.067:
                terrain_type = 'Radiation'
            else:
                terrain_type = 'Water'
            row.append(terrain_type)
        terrain_grid.append(row)
    return terrain_grid

# Draw the terrain on the screen
def draw_terrain(terrain_grid):
    colors = {
        'Soil': (207, 124, 51),
        'Rock': (128, 128, 128),
        'Radiation': (0, 255, 0),
        'Water': (179, 245, 249)
    }
    for y in range(TERRAIN_HEIGHT):
        for x in range(TERRAIN_WIDTH):
            terrain_type = terrain_grid[y][x]
            color = colors[terrain_type]
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Define the Player class
class Player:
    def __init__(self, x, y, color=(255, 255, 255), size=TILE_SIZE // 2):
        self.x = x  # Grid position
        self.y = y
        self.color = color  # Player's color
        self.size = size  # Player's size (visual representation)
        self.speed = 1  # How many tiles the player moves per keypress

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2),
            self.size // 2
        )

    def move(self, dx, dy, terrain_width, terrain_height):
        # Move the player while staying within bounds
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < terrain_width and 0 <= new_y < terrain_height:
            self.x = new_x
            self.y = new_y

# Main game loop
def main():
    terrain_grid = generate_terrain()
    player = Player(TERRAIN_WIDTH // 2, TERRAIN_HEIGHT // 2)  # Start player in the center of the map
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1, 0, TERRAIN_WIDTH, TERRAIN_HEIGHT)
                elif event.key == pygame.K_RIGHT:
                    player.move(1, 0, TERRAIN_WIDTH, TERRAIN_HEIGHT)
                elif event.key == pygame.K_UP:
                    player.move(0, -1, TERRAIN_WIDTH, TERRAIN_HEIGHT)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 1, TERRAIN_WIDTH, TERRAIN_HEIGHT)

        screen.fill((0, 0, 0))
        draw_terrain(terrain_grid)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()