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
    def __init__(self, depth, game_controller):
        self.depth= depth
        self.game_controller = game_controller
           
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