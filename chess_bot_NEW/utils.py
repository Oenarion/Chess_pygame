import pygame
from gamestate import GameState
    
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
        self.coord_grid = CoordinateGrid()
        self.moves = []

    def handle_click(self, row, col):
        """
        Args:
            row (int): row of the grid
            col (int): col of the grid

        Returns:
            INT, Returns the state of the game -> check class GameState
        """
        b_row, b_col = self.game_grid.board_to_screen(row, col)
        
        # promotion 
        if self.pending_promotion:
            print(self.pending_promotion)
            is_promoted = self.handle_promotion_click(b_row, b_col)
            # register move
            last_move = self.game_grid.last_move
            end_r, end_c = last_move["to"]
            piece = self.game_grid.grid[end_r][end_c].name[0].upper()
            # last turn changed so we need to pass the last turn in the parameters
            self.moves.append(self.coord_grid.register_move(last_move, not self.is_white_turn,
                                                            promotion=True, promoted_piece=piece))
            print(self.moves[-1])
            if is_promoted:
                return GameState.ONGOING
            return GameState.PROMOTION
             
        # moving or not moving the piece
        if self.legal_moves:
            if (b_row, b_col) in self.legal_moves:
                self.game_grid.move_piece(
                    self.piece_selected,
                    self.piece_selected_position,
                    (b_row, b_col)
                )
                last_move = self.game_grid.last_move
                
                # save promotion state and return it
                if self.game_grid.pawn_promotion:
                    self.pending_promotion = self.game_grid.pawn_promotion
                    return GameState.PROMOTION
                
                # REGISTER AND PRINT LAST MOVE
                self.moves.append(self.coord_grid.register_move(last_move, self.is_white_turn))
                print(self.moves[-1])
                
                # change player turn and clear everything
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
        order = ["Q", "R", "B", "N"]
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
        order = ["Q", "R", "B", "N"]  

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
        
    def bot_move(self, bot, bot_color):
        piece, move = bot.choose_move(self.game_grid, bot_color)
        promotion = False
        
        # if game over or stalemate
        if piece is None or move is None:
            return self.post_move_evaluation()
        
        piece_pos = self.game_grid.get_piece_pos(piece)
        self.game_grid.move_piece(piece, piece_pos, move)
        # add promotion check
        if self.game_grid.pawn_promotion:
            pr, pc, is_white = self.game_grid.pawn_promotion
            self.game_grid.promote_pawn((pr, pc), "Q", is_white, self.spritesheet, self.scale)
            self.game_grid.pawn_promotion = None
            promotion = True
        
        last_move = self.game_grid.last_move
        is_white = self.is_white_turn
        self.moves.append(self.coord_grid.register_move(last_move, is_white, promotion=promotion, promoted_piece="Q"))
        print(self.moves[-1])
        
        self.is_white_turn = not self.is_white_turn
        return self.post_move_evaluation()

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


class CoordinateGrid:
    def __init__(self):
        self.grid = self.create_grid()
        
    def create_grid(self):
        order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        grid = []
        for i in range(8):
            temp = []
            for j in range(8):
                temp.append(order[j]+str(i+1))
            grid.append(temp)
        
        final_grid = []
        for i in range(len(grid)-1, -1, -1):
            final_grid.append(grid[i])
            
        return final_grid

    def register_move(self, last_move, is_white, promotion=False, promoted_piece = None):
        """
        last_move: piece, from, to, has_eaten
        if not pawn we need to specify the piece move K,Q,R,B,N
        if capture x is specified after the piece, for example Qxe5, for pawns we also specify the starting file exf4
        lastly, I will append white move or black move on top just to know which side moved, in the final UI this
        won't be needed.
        
        SPECIAL CASES:
        Castles are viewed as O-O (short) or O-O-O (long)
        Promotion are viewed as either finalsquare=piece, or if captured just add what the promotion is.
        """
        piece = last_move["piece"]
        start_r, start_c = last_move["from"]
        end_r, end_c = last_move["to"]
        has_eaten = last_move["eaten"]
        castle = last_move["castle"]
        player_moving = "white" if is_white else "black"
        
        final_str = player_moving + ": "
        
        # castle special case
        if castle != None:
            if castle == "short":
                final_str += "O-O"
            else:
                final_str += "O-O-O"
            return final_str
        
        # special case promotion
        if promotion and not has_eaten:
            final_str += self.grid[end_r][end_c] + "=" + promoted_piece
            return final_str
        
        if piece.name != "pawn":
            final_str += piece.name[0].upper()
        else:
            if has_eaten:
                # takes the name of the starting file if we have a capture with a pawn
                final_str += self.grid[start_r][start_c][0]
                
        if has_eaten:
            final_str += "x"
            
        # write the final square position
        final_str += self.grid[end_r][end_c]
        
        # promotion with capture
        if promotion:
            final_str += promoted_piece.upper()
        
        return final_str