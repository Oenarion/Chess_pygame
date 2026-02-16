from enum import Enum
import pygame

class GameState(Enum):
    ONGOING = 0
    CHECKMATE_WHITE_WINS = 1
    CHECKMATE_BLACK_WINS = 2
    DRAW_STALEMATE = 3
    DRAW_INSUFFICIENT = 4
    DRAW_FIFTY_MOVE = 5
    DRAW_THREEFOLD = 6
    PROMOTION = 7
    
class GameController:
    def __init__(self, game_grid, spritesheet, scale):
        self.game_grid = game_grid
        self.legal_moves = None
        self.spritesheet = spritesheet
        self.piece_selected = None
        self.piece_selected_position = None
        self.is_white_turn = True
        self.pending_promotion = None
        self.scale = scale
        self._build_promo_cache()

    def handle_click(self, row, col):
        """
        Args:
            row (int): row of the grid
            col (int): col of the grid

        Returns:
            INT, Returns the state of the game -> check class GameState
        """
        print(f"mouse clicked on: ({row},{col})")
        b_row, b_col = self.game_grid.board_to_screen(row, col)
        print(f"mouse clicked on: ({b_row},{b_col})")
        if self.pending_promotion:
            print(self.pending_promotion)
            is_promoted = self.handle_promotion_click(b_row, b_col)
            if is_promoted:
                return GameState.ONGOING
            return GameState.PROMOTION
            
        if self.legal_moves:
            if (b_row, b_col) in self.legal_moves:
                self.game_grid.move_piece(
                    self.piece_selected,
                    self.piece_selected_position,
                    (b_row, b_col)
                )
                # save promotion state and return it
                if self.game_grid.pawn_promotion:
                    self.pending_promotion = self.game_grid.pawn_promotion
                    return GameState.PROMOTION
                
                self.is_white_turn = not self.is_white_turn
                self.clear_selection()
                # check gamestate
                return self.post_move_evaluation()
            
            elif self.game_grid.is_empty(b_row, b_col):
                self.clear_selection()
                return GameState.ONGOING
            else:
                piece = self.game_grid.grid[b_row][b_col]
                if piece != 0 and self.is_white_turn == piece.is_white:
                    self.select_piece(b_row, b_col)
                    return GameState.ONGOING
        else:
            piece = self.game_grid.grid[b_row][b_col]
            if piece != 0 and self.is_white_turn == piece.is_white:
                self.select_piece(b_row, b_col)
            return GameState.ONGOING
        
    def _build_promo_cache(self):
        # save the sprites for promotion
        self.promo_sprites = self.game_grid.generate_promotion_pieces(self.spritesheet, self.scale)
        
    def draw_promotion_choices(self, screen):
        if not self.pending_promotion:
            return 
        
        pr, pc, is_white = self.pending_promotion
        # print(f"pawn position: ({pr, pc})")
        r, c = self.game_grid.board_to_screen(pr, pc)
        # print(f"pawn position after board to screen: ({r, c})")
        color = (211, 211, 211)
        order = ["Q", "R", "B", "K"]
        direction = -1 if c > 4 else 1

        for i, key in enumerate(order):
            dir = (i+1) * direction
            # print(f"board coordinates -> row: {r}  col: {c+dir}")
            # print(f"screen coordinates -> ({self.game_grid.border + r * self.game_grid.tile_size}, {c+dir * self.game_grid.tile_size})")
            rect = pygame.Rect((c+dir) * self.game_grid.tile_size, self.game_grid.border + r * self.game_grid.tile_size,
                self.game_grid.tile_size, self.game_grid.tile_size)
            pygame.draw.rect(screen, color, rect)
            piece = self.promo_sprites[is_white][key]
            piece.draw(screen, self.game_grid.tile_size, self.game_grid.border, (r, c+dir))

    def handle_promotion_click(self, b_row, b_col):
        if not self.pending_promotion:
            return False

        pr, pc, is_white = self.pending_promotion
        # same logic as draw
        direction = -1 if pc > 4 else 1
        order = ["Q", "R", "B", "K"]  

        # ignore if pawn is clicked
        if (b_row, b_col) == (pr, pc):
            return False

        # check if one of the 4 squares is clicked
        chosen_key = None
        for i, key in enumerate(order):
            dir = (i + 1) * direction
            if (b_row, b_col) == (pr, pc + dir):
                chosen_key = key
                break

        # clicked somewhere else, ignore
        if chosen_key is None:
            return False

        self.game_grid.promote_pawn((pr, pc), chosen_key, is_white, self.spritesheet, self.scale)

        # not promotion anymore
        self.pending_promotion = None
        self.legal_moves = None
        self.piece_selected = None
        self.piece_selected_position = None
        self.is_white_turn = not self.is_white_turn
        return True
        

    def clear_selection(self):
        self.legal_moves = None
        self.piece_selected = None
        self.piece_selected_position = None

    def select_piece(self, row, col):
        self.piece_selected = self.game_grid.grid[row][col]
        self.piece_selected_position = [row, col]
        self.legal_moves = self.piece_selected.get_legal_moves(
            (row, col), self.game_grid
        )

    def post_move_evaluation(self):
        """
        Checks the state of the game.
        """
        side_to_move = self.is_white_turn
        
        # checkmate
        king_pos = self.game_grid.get_king_square(self.is_white_turn)
        in_check = self.game_grid.checkmate(king_pos, self.is_white_turn)
        
        any_legal = self.game_grid.any_legal_move(side_to_move)
        if not any_legal:
            # who is moving loses
            if in_check:
                return GameState.CHECKMATE_BLACK_WINS if side_to_move else GameState.CHECKMATE_WHITE_WINS
            # stalemate
            else:
                return GameState.DRAW_STALEMATE
            
        # insufficient draw
        if self.game_grid.check_insufficient_material():
            return GameState.DRAW_INSUFFICIENT
        
        # 50 full moves without eating
        print(f"current turn: {self.game_grid.turn}")
        print(f"last time eaten: {self.game_grid.last_eaten}")
        if self.game_grid.turn - self.game_grid.last_eaten >= 100:
            return GameState.DRAW_FIFTY_MOVE

        # threefold
        count = self.game_grid.record_position(side_to_move)
        if count >= 3:
            return GameState.DRAW_THREEFOLD
        
        return GameState.ONGOING

def sliding_moves(piece, position, grid, directions):
    moves = []
    row, col = position

    for dr, dc in directions:
        r, c = row + dr, col + dc

        while 0 <= r < 8 and 0 <= c < 8:
            if grid.is_empty(r, c):
                moves.append((r, c))

            elif grid.is_enemy(r, c, piece.is_white):
                moves.append((r, c))
                break

            else:
                break

            r += dr
            c += dc

    return moves


