import pygame
import math
import chess_piece as p
from utils import GameController

WHITE=(255,255,255)
GREEN=(118,150,86)
WIDTH = 512
HEIGHT = 592
BORDER = 40
TILE_SIZE = (HEIGHT - 2 * BORDER) // 8

def create_pieces(spritesheet):            
    black_pieces = {}
    b_pawns = [p.Pawn(spritesheet, scale=2, is_white=0) for _ in range(8)]
    b_rooks = [p.Rook(spritesheet, scale=2, is_white=0) for _ in range(2)]
    b_knights = [p.Knight(spritesheet, scale=2, is_white=0) for _ in range(2)]
    b_bishops = [p.Bishop(spritesheet, scale=2, is_white=0) for _ in range(2)]
    b_queen = p.Queen(spritesheet, scale=2, is_white=0)
    b_king = p.King(spritesheet, scale=2, is_white=0)
    black_pieces["pawn"] = b_pawns
    black_pieces["rook"] = b_rooks
    black_pieces["knight"] = b_knights
    black_pieces["bishop"] = b_bishops
    black_pieces["queen"] = b_queen
    black_pieces["king"] = b_king
    
    white_pieces = {}
    w_rooks = [p.Rook(spritesheet, scale=2, is_white=1) for _ in range(2)]
    w_pawns = [p.Pawn(spritesheet, scale=2, is_white=1) for _ in range(8)]
    w_knights = [p.Knight(spritesheet, scale=2, is_white=1) for _ in range(2)]
    w_bishops = [p.Bishop(spritesheet, scale=2, is_white=1) for _ in range(2)]
    w_queen = p.Queen(spritesheet, scale=2, is_white=1)
    w_king = p.King(spritesheet, scale=2, is_white=1)
    white_pieces["pawn"] = w_pawns
    white_pieces["rook"] = w_rooks
    white_pieces["knight"] = w_knights
    white_pieces["bishop"] = w_bishops
    white_pieces["queen"] = w_queen
    white_pieces["king"] = w_king
    
    return black_pieces, white_pieces
    
    
def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Bot")

    PIECE_SPRITESHEET = p.SpriteSheet("chess_bot_NEW/pngs/chess_pieces.png")

    black_pieces, white_pieces = create_pieces(PIECE_SPRITESHEET)

    game_grid = p.Grid(8, 8, TILE_SIZE, BORDER)
    game_grid.populate_grid(black_pieces, white_pieces, True)

    controller = GameController(game_grid)   

    grid_colors = [WHITE, GREEN]
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                # check if the piece is in bounds
                if BORDER < y < HEIGHT - BORDER:
                    row = int((y - BORDER) // TILE_SIZE)
                    col = int(x // TILE_SIZE)

                    # handles all the moving piece part
                    controller.handle_click(row, col) 

        game_grid.draw(screen, grid_colors, controller.legal_moves)

        pygame.display.flip()

    pygame.quit()

    
    
if __name__ == "__main__":
    main()