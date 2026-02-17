import random

class Bot:
    def choose_move(self, grid, color_is_white):
        return NotImplementedError
    
    
class RandomBot(Bot):
    def choose_move(self, grid, color_is_white):
        moves = grid.iter_legal_moves(color_is_white)
        if not moves:
            return None
        # moves is a tuple (piece, piece_moves)
        selected_piece, piece_moves = random.choice(moves)
        random_move = random.choice(piece_moves)
        return (selected_piece, random_move)