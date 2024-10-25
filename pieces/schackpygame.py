import pygame
import os
print(os.getcwd())

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (50, 100, 50)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Board")

# Load images for chess pieces (placeholders, adjust paths as needed)
piece_images = {
    'bR': pygame.image.load('C:/Dokument/Python/Mschack/schack/black_rook.png'),
    'bN': pygame.image.load('C:/Dokument/Python/Mschack/schack/black_knight.png'),
    'bB': pygame.image.load('C:/Dokument/Python/Mschack/schack/black_bishop.png'),
    'bQ': pygame.image.load('C:/Dokument/Python/Mschack/schack/black_queen.png'),
    'bK': pygame.image.load('C:/Dokument/Python/Mschack/schack/black_king.png'),
    'bP': pygame.image.load('C:/Dokument/Python/Mschack/schack/black_pawn.png'),
    'wR': pygame.image.load('C:/Dokument/Python/Mschack/schack/white_rook.png'),
    'wN': pygame.image.load('C:/Dokument/Python/Mschack/schack/white_knight.png'),
    'wB': pygame.image.load('C:/Dokument/Python/Mschack/schack/white_bishop.png'),
    'wQ': pygame.image.load('C:/Dokument/Python/Mschack/schack/white_queen.png'),
    'wK': pygame.image.load('C:/Dokument/Python/Mschack/schack/white_king.png'),
    'wP': pygame.image.load('C:/Dokument/Python/Mschack/schack/white_pawn.png'),
}

# Resize the pieces to fit the squares
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))

# Initial chessboard setup (2D list representation)
chess_board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Function to draw the chess board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the pieces on the board
def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = chess_board[row][col]
            if piece:
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board()  # Draw the board every frame
    draw_pieces()  # Draw the chess pieces
    pygame.display.update()  # Update the display

pygame.quit()