import pygame
import math
import chess_piece as p
from utils import GameController, GameState
import bot

WHITE=(255,255,255)
GREEN=(118,150,86)
WIDTH = 512
HEIGHT = 592
BORDER = 40
TILE_SIZE = (HEIGHT - 2 * BORDER) // 8
SCALE = 2

def create_pieces(spritesheet):            
    black_pieces = {}
    b_pawns = [p.Pawn(spritesheet, scale=SCALE, is_white=0) for _ in range(8)]
    b_rooks = [p.Rook(spritesheet, scale=SCALE, is_white=0) for _ in range(2)]
    b_knights = [p.Knight(spritesheet, scale=SCALE, is_white=0) for _ in range(2)]
    b_bishops = [p.Bishop(spritesheet, scale=SCALE, is_white=0) for _ in range(2)]
    b_queen = p.Queen(spritesheet, scale=SCALE, is_white=0)
    b_king = p.King(spritesheet, scale=SCALE, is_white=0)
    black_pieces["pawn"] = b_pawns
    black_pieces["rook"] = b_rooks
    black_pieces["knight"] = b_knights
    black_pieces["bishop"] = b_bishops
    black_pieces["queen"] = b_queen
    black_pieces["king"] = b_king
    
    white_pieces = {}
    w_rooks = [p.Rook(spritesheet, scale=SCALE, is_white=1) for _ in range(2)]
    w_pawns = [p.Pawn(spritesheet, scale=SCALE, is_white=1) for _ in range(8)]
    w_knights = [p.Knight(spritesheet, scale=SCALE, is_white=1) for _ in range(2)]
    w_bishops = [p.Bishop(spritesheet, scale=SCALE, is_white=1) for _ in range(2)]
    w_queen = p.Queen(spritesheet, scale=SCALE, is_white=1)
    w_king = p.King(spritesheet, scale=SCALE, is_white=1)
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

    player_color = True 
    
    game_grid = p.Grid(8, 8, TILE_SIZE, BORDER, player_color)
    game_grid.populate_grid(black_pieces, white_pieces)
    # records the first position of the board
    game_grid.record_position(True)

    controller = GameController(game_grid, PIECE_SPRITESHEET, SCALE)   
    ai_bots = [bot.RandomBot(), bot.MiniMaxBot(depth=3, game_controller=controller)]
    # using minimax for now
    ai_bot = ai_bots[1]
    grid_colors = [WHITE, GREEN]
    running = True
    game_over = False
    gamestate = GameState.ONGOING
    clock = pygame.time.Clock()
    
    while running:
        dt = clock.tick(60) / 1000
        screen.fill((0, 0, 0))
        promotion_gamestate = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                # do not check mouse input if animation is running
                if game_grid.anim is not None:
                    continue
                x, y = pygame.mouse.get_pos()

                # check if the piece is in bounds
                if BORDER < y < HEIGHT - BORDER:
                    row = int((y - BORDER) // TILE_SIZE)
                    col = int(x // TILE_SIZE)

                    # player turn
                    if not game_over and controller.is_white_turn == player_color:
                        # handles all the moving piece part
                        gamestate = controller.handle_click(row, col) 
                        if gamestate != GameState.ONGOING:
                            print(f"current gamestate: {gamestate}")
                        if gamestate == GameState.PROMOTION:
                            promotion_gamestate = True
                        print(f"PROMOTION GAMESTATE: {promotion_gamestate}")

        # GAME OVER        
        if gamestate != GameState.ONGOING and gamestate != GameState.PROMOTION:
            game_over = True
            print(f"GAME OVER: {gamestate}")
            
        # BOT TURN
        # check always if it's already game over
        if not game_over and controller.is_white_turn != player_color:
            if game_grid.anim is None:
                controller.bot_move(ai_bot, controller.is_white_turn)
                clock.tick() 

        if controller.pending_promotion and controller.is_white_turn == player_color:
            in_promotion = controller.pending_promotion
        else:
            in_promotion = None
        game_grid.update_animation(dt)
        game_grid.draw(screen, grid_colors, controller.legal_moves, in_promotion, controller.piece_selected_position)
        controller.draw_promotion_choices(screen)
        
        pygame.display.flip()

    pygame.quit()

    
    
if __name__ == "__main__":
    main()