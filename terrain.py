import pygame
import noise
import numpy as np

# Define grid dimensions
GRID_WIDTH = 40
GRID_HEIGHT = 20
CELL_SIZE = 36

menu_width = 100

# Initialize Pygame
pygame.init()

# Create a window
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + menu_width
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#font
font = pygame.font.Font(None, 36)

# Generate Perlin noise
noise_grid = np.zeros((GRID_WIDTH, GRID_HEIGHT))
for x in range(GRID_WIDTH):
    for y in range(GRID_HEIGHT):
        noise_grid[x][y] = noise.snoise2(x / 10, y / 10, octaves=6)

# Map noise values to images
image_mapping = {
    (0.0, 0.2): pygame.image.load("textures/TEX_TREE.png"),
    (0.2, 0.4): pygame.image.load("textures/HILL_TEX.png"),
    (0.4, 0.6): pygame.image.load("textures/TEX_MOUNTAIN.png"),
}

# Fallback image for unmapped noise values
fallback_image = pygame.image.load("textures/EMPTY_TEX.png")

# Initialize troop selection
selected_troop = None

# Store troop positions
troop_positions = {}

# Define troop selection menu items
menu_items = {
    "tank": pygame.image.load("textures/tank_modified.png"),
    "troop": pygame.image.load("textures/troop_tex.png"),
    "tank3": pygame.image.load("textures/tank_modified.png"),
    # Add more troop types and their corresponding images here
}

# Calculate the menu height based on the number of items
menu_item_height = WINDOW_HEIGHT // len(menu_items)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if the click is within the troop selection menu
                if 0 <= event.pos[1] < WINDOW_HEIGHT and WINDOW_WIDTH-menu_width < event.pos[0] < WINDOW_WIDTH :
                    # Determine the selected troop based on the click position
                    selected_troop = list(menu_items.keys())[event.pos[1] // menu_item_height]
                    print(selected_troop)
                # If not in the menu, handle troop placement
                else:
                    if selected_troop:
                        # Get the grid coordinates where the user clicked
                        x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE

                        # Place the selected troop on the grid
                        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                            troop_positions[(x, y)] = selected_troop


    ## Draw selection menu
    pygame.draw.rect(screen, (255,0,0), (WINDOW_WIDTH-menu_width, 0, menu_width, WINDOW_HEIGHT))
    for i,(k,v) in enumerate(menu_items.items()):
        text_surface = font.render(k, True, (0, 0, 0))
        if k == selected_troop:
            pass
        pygame.draw.rect(screen, (0,0,0), (WINDOW_WIDTH-menu_width, i*WINDOW_HEIGHT//len(menu_items), menu_width, (i+1)*WINDOW_HEIGHT//len(menu_items)),10)
        screen.blit(text_surface, (WINDOW_WIDTH-menu_width+10, 10+(i)*WINDOW_HEIGHT//len(menu_items)))


    # Draw the grid and insert images based on noise values
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cell_color = (0, 0, 0)  # Default cell color (black)

            for (min_val, max_val), image in image_mapping.items():
                if min_val <= noise_grid[x][y] < max_val:
                    screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))
                    break
                
                
            else:
                # Use the fallback image for unmapped noise values
                screen.blit(fallback_image, (x * CELL_SIZE, y * CELL_SIZE))

    # Draw troops on the grid
    for (x, y), troop_type in troop_positions.items():
        screen.blit(menu_items[troop_type], (x * CELL_SIZE, y * CELL_SIZE))




    pygame.display.flip()

# Quit Pygame
pygame.quit()
