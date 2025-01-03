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
        'Water': (201, 248, 246)
    }
    for y in range(TERRAIN_HEIGHT):
        for x in range(TERRAIN_WIDTH):
            terrain_type = terrain_grid[y][x]
            color = colors[terrain_type]
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Main game loop
def main():
    terrain_grid = generate_terrain()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_terrain(terrain_grid)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
