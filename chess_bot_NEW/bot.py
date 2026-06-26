import random
from gamestate import GameState

MATE_SCORE = 10**6

class Bot:
    def choose_move(self, grid, color_is_white):
        return NotImplementedError
    
    
class RandomBot(Bot):
    def choose_move(self, grid, color_is_white):
        moves = grid.iter_legal_moves(color_is_white)
        if not moves:
            return None
        # moves is a tuple (piece, piece_moves)
        selected_piece, _, piece_moves = random.choice(moves)
        random_move = random.choice(piece_moves)
        return (selected_piece, random_move)
    
    
class MiniMaxBot(Bot):
    def __init__(self, depth, game_controller, opening_reader):
        self.depth= depth
        self.game_controller = game_controller
        self.opening_reader = opening_reader
        self.follow_opening = True
        self.opening_followed = None
        
    def get_opening_move(self, grid, index, turn, color_is_white, opening):
        """
        Get a possible opening to follow and a consequentially a move to do as the bot.
        """
        self.opening_followed = opening
        # get white move
        print(f"OPENING CHOSEN: {self.opening_followed}")
        fullmove = self.opening_followed[turn][index]
        start_pos, end_pos = self.opening_reader.get_start_end_from_move(fullmove, color_is_white)
        s_row, s_col = self.game_controller.coord_grid.get_cell_from_square_name(start_pos)
        e_row, e_col = self.game_controller.coord_grid.get_cell_from_square_name(end_pos)
        piece = grid.grid[s_row][s_col]
        move = (e_row, e_col)
        return (piece, move)
    
    def check_opening(self, turn, color_is_white):
        """
        Checks if any opening is possible, if not minimax algorithm will start.
        """
        # full history of half-moves played so far (prefixes stripped)
        played_moves = [m.split(":")[1][1:] for m in self.game_controller.moves]
        possible_openings = self.opening_reader.get_possible_openings(played_moves)
        print(f"POSSIBLE OPENINGS: {possible_openings}")
        if not possible_openings:
            self.follow_opening = None
            self.opening_followed = None
            return None
        return possible_openings
                
    def choose_move(self, grid, color_is_white):
        if self.follow_opening:
            curr_turn = grid.turn // 2
            index = 0 if color_is_white else 1
            # choose the openings
            if not self.opening_followed:
                # choose a random opening
                if color_is_white:
                    opening = self.opening_reader.get_random_opening()
                    return self.get_opening_move(grid, index, curr_turn, color_is_white, opening)
                else:
                    print("GOT HERE?")
                    # if opening is present we proceed with normal opening
                    possible_openings = self.check_opening(curr_turn, color_is_white)
                    if possible_openings:
                        opening = random.choice(possible_openings)
                        return self.get_opening_move(grid, index, curr_turn, color_is_white, opening)
                    # else we just go back to minimax
                    return self.choose_move(grid, color_is_white)
            # next moves
            else:
                possible_openings = self.check_opening(curr_turn, color_is_white)
                if possible_openings:
                    opening = random.choice(possible_openings)
                    return self.get_opening_move(grid, index, curr_turn, color_is_white, opening)
                return self.choose_move(grid, color_is_white)
        else:
            best_move, _ = self.minimax(grid, depth = self.depth, 
                                                    alpha = -MATE_SCORE, 
                                                    beta = MATE_SCORE, 
                                                    maximizing_player=color_is_white, 
                                                    maximizing_color=color_is_white)
            if best_move is None:
                return (None, None)
            best_piece, _ , move = best_move
        return (best_piece, move)
        
    def minimax(self, grid, depth, alpha, beta, maximizing_player, maximizing_color):
        moves = grid.iter_legal_moves(maximizing_player)
        # reached maximum depth or gameover
        if depth == 0 or not moves:
            return None, self.evaluate(grid, maximizing_color)
        
        
        # MAXIMIZING PATH
        if maximizing_player == maximizing_color:
            best_move = None
            max_eval = -MATE_SCORE    
            for piece, start_pos, other_moves in moves:
                for move in self.order_moves(grid, other_moves):
                    undo = grid.move_piece(piece, start_pos, move, record_undo=True)
                    king_pos = grid.get_king_square(maximizing_player)
                    enemy = grid.get_all_pieces(not maximizing_player)
                    if grid.is_square_attacked(king_pos, enemy):
                        grid.undo_move(undo)
                        continue
                    # continue with the recursion, take only the max/min eval
                    _, current_eval = self.minimax(grid, depth - 1, alpha, beta, not maximizing_player, maximizing_color)
                    grid.undo_move(undo)
                    
                    # save best move
                    if current_eval > max_eval:
                        max_eval = current_eval
                        best_move = (piece, start_pos, move)
                    # prune if possible useless paths
                    alpha = max(alpha, current_eval)
                    if beta <= alpha:
                        return best_move, max_eval
            return best_move, max_eval
        # MINIMIZING PATH
        else:
            best_move = None
            min_eval = MATE_SCORE
            for piece, start_pos, other_moves in moves:
                for move in self.order_moves(grid, other_moves):
                    undo = grid.move_piece(piece, start_pos, move, record_undo=True)
                    king_pos = grid.get_king_square(maximizing_player)
                    enemy = grid.get_all_pieces(not maximizing_player)
                    if grid.is_square_attacked(king_pos, enemy):
                        grid.undo_move(undo)
                        continue
                    # continue with the recursion, take only the max/min eval
                    _, current_eval = self.minimax(grid, depth - 1, alpha, beta, not maximizing_player, maximizing_color)
                    grid.undo_move(undo)
                    
                    # save best move
                    if current_eval < min_eval:
                        min_eval = current_eval
                        best_move = (piece, start_pos, move)
                    # prune if possible useless paths
                    beta = min(beta, current_eval)
                    if beta <= alpha:
                        return best_move, min_eval
            return best_move, min_eval
            
    def order_moves(self, grid, other_moves):
        def key(move):
            r, c = move
            return 0 if grid.grid[r][c] != 0 else 1
        return sorted(other_moves, key=key)

        
    def evaluate(self, grid, maximizing_color):
        black_score = grid.compute_current_score(False)
        white_score = grid.compute_current_score(True)
        # true is white
        if maximizing_color:
            return white_score - black_score
        # false is black
        else:
            return black_score - white_score
        
        
class TTMiniMaxBot(Bot):
    def __init__(self, depth, game_controller):
        self.depth= depth
        self.game_controller = game_controller
        self.tt = {}
           
    def choose_move(self, grid, color_is_white):
        best_move, _ = self.minimax(grid, depth = self.depth, 
                                                alpha = -MATE_SCORE, 
                                                beta = MATE_SCORE, 
                                                maximizing_player=color_is_white, 
                                                maximizing_color=color_is_white)
        if best_move is None:
            return (None, None)
        best_piece, _ , move = best_move
        return (best_piece, move)
        
    def minimax(self, grid, depth, alpha, beta, maximizing_player, maximizing_color):
        # === TT LOOKUP ===
        key = grid.position_signature(side_to_move_is_white=maximizing_player)
        tt_entry = self.tt.get(key)
        if tt_entry is not None and tt_entry["depth"] >= depth:
            flag = tt_entry["flag"]
            val = tt_entry["value"]
            best = tt_entry["best"]
            if flag == "EXACT":
                return best, val
            elif flag == "LOWER":
                alpha = max(alpha, val)
            elif flag == "UPPER":
                beta = min(beta, val)
            if alpha >= beta:
                return best, val

        # === MOVE GENERATION (fix: side to move!) ===
        moves = grid.iter_legal_moves(maximizing_player)

        # terminal
        if depth == 0 or not moves:
            val = self.evaluate(grid, maximizing_color)
            # salva come EXACT (valutazione terminale)
            self.tt[key] = {"depth": depth, "value": val, "flag": "EXACT", "best": None}
            return None, val

        alpha_orig = alpha
        beta_orig = beta

        # per ordering: se TT aveva best move, proviamo prima quella
        tt_best = tt_entry["best"] if tt_entry else None

        def ordered_moves():
            # moves è [(piece, start_pos, [moves...]), ...]
            # appiattisco in triple (piece, start, move)
            flat = []
            for piece, start_pos, other_moves in moves:
                om = list(other_moves)
                # se tt_best matcha questo pezzo/start, portala davanti
                if tt_best is not None:
                    tb_piece, tb_start, tb_move = tt_best
                    if piece is tb_piece and start_pos == tb_start and tb_move in om:
                        om.remove(tb_move)
                        om = [tb_move] + om
                for mv in self.order_moves(grid, om):
                    flat.append((piece, start_pos, mv))
            return flat

        best_move = None

        # MAX node: quando tocca al colore root
        if maximizing_player == maximizing_color:
            best_val = -MATE_SCORE
            for piece, start_pos, move in ordered_moves():
                undo = grid.move_piece(piece, start_pos, move, record_undo=True)

                king_pos = grid.get_king_square(maximizing_player)
                enemy = grid.get_all_pieces(not maximizing_player)
                if grid.is_square_attacked(king_pos, enemy):
                    grid.undo_move(undo)
                    continue

                _, val = self.minimax(grid, depth - 1, alpha, beta, not maximizing_player, maximizing_color)
                grid.undo_move(undo)

                if val > best_val:
                    best_val = val
                    best_move = (piece, start_pos, move)

                alpha = max(alpha, val)
                if alpha >= beta:
                    break

            # === TT STORE ===
            if best_val <= alpha_orig:
                flag = "UPPER"
            elif best_val >= beta_orig:
                flag = "LOWER"
            else:
                flag = "EXACT"
            self.tt[key] = {"depth": depth, "value": best_val, "flag": flag, "best": best_move}
            return best_move, best_val

        # MIN node: tocca all'avversario del colore root
        else:
            best_val = MATE_SCORE
            for piece, start_pos, move in ordered_moves():
                undo = grid.move_piece(piece, start_pos, move, record_undo=True)

                king_pos = grid.get_king_square(maximizing_player)
                enemy = grid.get_all_pieces(not maximizing_player)
                if grid.is_square_attacked(king_pos, enemy):
                    grid.undo_move(undo)
                    continue

                _, val = self.minimax(grid, depth - 1, alpha, beta, not maximizing_player, maximizing_color)
                grid.undo_move(undo)

                if val < best_val:
                    best_val = val
                    best_move = (piece, start_pos, move)

                beta = min(beta, val)
                if alpha >= beta:
                    break

            # === TT STORE ===
            if best_val <= alpha_orig:
                flag = "UPPER"
            elif best_val >= beta_orig:
                flag = "LOWER"
            else:
                flag = "EXACT"
            self.tt[key] = {"depth": depth, "value": best_val, "flag": flag, "best": best_move}
            return best_move, best_val
            
                
    def order_moves(self, grid, other_moves):
        def key(move):
            r, c = move
            return 0 if grid.grid[r][c] != 0 else 1
        return sorted(other_moves, key=key)
        
    def evaluate(self, grid, maximizing_color):
        black_score = grid.compute_current_score(False)
        white_score = grid.compute_current_score(True)
        # true is white
        if maximizing_color:
            return white_score - black_score
        # false is black
        else:
            return black_score - white_score
        
    