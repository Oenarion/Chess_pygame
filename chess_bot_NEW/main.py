import pygame
import os
import chess_piece as p
from utils import GameController, GameState, OpeningReader
import bot
import ui


WHITE=(255,255,255)
GREEN=(118,150,86)
BOARD_W = 512
PANEL_W = 260
WIDTH = BOARD_W + PANEL_W
HEIGHT = 592
BORDER = 40
TILE_SIZE = (HEIGHT - 2 * BORDER) // 8
SCALE = 2
START_SECONDS = 5 * 60  # per-side clock
CWD = "\\".join(os.path.abspath(__file__).split("\\")[:-1])

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
    
    openings_file = CWD+"\\openings.txt"
    opening_reader = OpeningReader(openings_file)
    
    controller = GameController(game_grid, PIECE_SPRITESHEET, SCALE, opening_reader)
    ai_bots = [bot.RandomBot(),
               bot.MiniMaxBot(depth=3, game_controller=controller, opening_reader=opening_reader),
               bot.TTMiniMaxBot(depth=3, game_controller=controller)]
    # using minimax for now
    ai_bot = ai_bots[1]
    grid_colors = [WHITE, GREEN]

    # --- UI setup ---
    fonts = {
        "title": pygame.font.SysFont("segoeui", 20, bold=True),
        "body": pygame.font.SysFont("segoeui", 18, bold=True),
        "mono": pygame.font.SysFont("consolas", 17),
        "clock": pygame.font.SysFont("consolas", 20, bold=True),
        "result": pygame.font.SysFont("segoeui", 24, bold=True),
    }
    panel = ui.SidePanel(BOARD_W, 0, PANEL_W, HEIGHT, fonts)
    white_clock = ui.Clock(START_SECONDS)
    black_clock = ui.Clock(START_SECONDS)
    # clock boxes sit in the two black strips, on the right edge of the board
    clock_w, clock_h = 92, 28
    clock_x = BOARD_W - clock_w - 8
    top_clock_rect = pygame.Rect(clock_x, (BORDER - clock_h) // 2, clock_w, clock_h)
    bottom_clock_rect = pygame.Rect(clock_x, HEIGHT - BORDER + (BORDER - clock_h) // 2, clock_w, clock_h)
    board_rect = pygame.Rect(0, BORDER, BOARD_W, BOARD_W)
    # bottom strip belongs to the side sitting at the bottom of the board
    bottom_is_white = not game_grid.flip

    running = True
    game_over = False
    gamestate = GameState.ONGOING
    clock = pygame.time.Clock()
    
    while running:
        dt = clock.tick(60) / 1000
        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        panel.update_hover(mouse_pos)
        promotion_gamestate = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()

                # ---- side panel (resign / draw) ----
                action = panel.handle_click((x, y))
                if action and not game_over:
                    if action == "resign":
                        gamestate = (GameState.RESIGN_BLACK_WINS if player_color
                                     else GameState.RESIGN_WHITE_WINS)
                    elif action == "draw":
                        gamestate = GameState.DRAW_AGREEMENT
                    continue

                # do not check board input if an animation is running
                if game_grid.anim is not None:
                    continue

                # ---- board click (only inside the board area) ----
                if x < BOARD_W and BORDER < y < HEIGHT - BORDER:
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

        # ---- clocks ----
        if not game_over and gamestate != GameState.PROMOTION:
            white_clock.tick(dt, controller.is_white_turn)
            black_clock.tick(dt, not controller.is_white_turn)
            if white_clock.is_flagged():
                gamestate = GameState.TIMEOUT_BLACK_WINS
                game_over = True
            elif black_clock.is_flagged():
                gamestate = GameState.TIMEOUT_WHITE_WINS
                game_over = True

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

        # ---- clocks in the top/bottom black strips ----
        bottom_clock = white_clock if bottom_is_white else black_clock
        top_clock = black_clock if bottom_is_white else white_clock
        bottom_active = controller.is_white_turn == bottom_is_white
        top_clock.draw(screen, fonts["clock"], top_clock_rect, not bottom_active and not game_over)
        bottom_clock.draw(screen, fonts["clock"], bottom_clock_rect, bottom_active and not game_over)

        # ---- side panel ----
        panel.draw(screen, controller.moves)

        # ---- game over banner ----
        if game_over:
            ui.draw_game_over(screen, fonts["result"], board_rect, gamestate)

        pygame.display.flip()

    pygame.quit()

    
    
if __name__ == "__main__":
    main()