import pygame
import grid
import chess_piece as p

WHITE=(255,255,255)
GREEN=(118,150,86)
WIDTH = 672
HEIGHT = 672
BORDER = 80
TILE_SIZE = (WIDTH - 2 * BORDER) // 8



def draw_chessboard(screen, black_pieces, white_pieces):
    colors = [WHITE, GREEN]  # light and dark squares

    # DRAW TILES
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            rect = pygame.Rect(col * TILE_SIZE, BORDER + row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            
    # DRAW PIECES
    for piece in black_pieces.values():
            if isinstance(piece, list):
                for pce in piece:
                    pce.draw(screen, TILE_SIZE, BORDER)
            else:
                piece.draw(screen, TILE_SIZE, BORDER)
    
    for piece in white_pieces.values():
        if isinstance(piece, list):
            for pce in piece:
                pce.draw(screen, TILE_SIZE, BORDER)
        else:
            piece.draw(screen, TILE_SIZE, BORDER)

def create_pieces(spritesheet):            
    black_pieces = {}
    b_pawns = [p.Pawn(spritesheet, (1, col), scale=2, is_white=0) for col in range(8)]
    b_rooks = [p.Rook(spritesheet, (0, col*7), scale=2, is_white=0) for col in range(2)]
    b_knights = [p.Knight(spritesheet, (0, col*5+1), scale=2, is_white=0) for col in range(2)]
    b_bishops = [p.Bishop(spritesheet, (0, col*3+2), scale=2, is_white=0) for col in range(2)]
    b_queen = p.Queen(spritesheet, (0, 3), scale=2, is_white=0)
    b_king = p.King(spritesheet, (0, 4), scale=2, is_white=0)
    black_pieces["pawns"] = b_pawns
    black_pieces["rooks"] = b_rooks
    black_pieces["knights"] = b_knights
    black_pieces["bishops"] = b_bishops
    black_pieces["queen"] = b_queen
    black_pieces["king"] = b_king
    
    white_pieces = {}
    w_rooks = [p.Rook(spritesheet, (7, col*7), scale=2, is_white=1) for col in range(2)]
    w_pawns = [p.Pawn(spritesheet, (6, col), scale=2, is_white=1) for col in range(8)]
    w_knights = [p.Knight(spritesheet, (7, col*5+1), scale=2, is_white=1) for col in range(2)]
    w_bishops = [p.Bishop(spritesheet, (7, col*3+2), scale=2, is_white=1) for col in range(2)]
    w_queen = p.Queen(spritesheet, (7, 3), scale=2, is_white=1)
    w_king = p.King(spritesheet, (7, 4), scale=2, is_white=1)
    white_pieces["pawns"] = w_pawns
    white_pieces["rooks"] = w_rooks
    white_pieces["knights"] = w_knights
    white_pieces["bishops"] = w_bishops
    white_pieces["queen"] = w_queen
    white_pieces["king"] = w_king
    
    return black_pieces, white_pieces
    
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Bot")
    PIECE_SPRITESHEET = p.SpriteSheet("chess_bot_NEW/pngs/chess_pieces.png")
    black_pieces, white_pieces = create_pieces(PIECE_SPRITESHEET)
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_chessboard(screen, black_pieces, white_pieces)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()

    pygame.quit()
    
    
if __name__ == "__main__":
    main()