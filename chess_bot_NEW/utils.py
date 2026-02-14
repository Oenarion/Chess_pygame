class GameController:
    def __init__(self, game_grid):
        self.game_grid = game_grid
        self.legal_moves = None
        self.piece_selected = None
        self.piece_selected_position = None
        self.is_white_turn = True

    def handle_click(self, row, col):
        """
        Args:
            row (int): row of the grid
            col (int): col of the grid

        Returns:
            Boolean, checks if the game ends as well.
        """
        b_row, b_col = self.game_grid.board_to_screen(row, col)
        if self.legal_moves:
            if (b_row, b_col) in self.legal_moves:
                self.game_grid.move_piece(
                    self.piece_selected,
                    self.piece_selected_position,
                    (b_row, b_col)
                )
                self.is_white_turn = not self.is_white_turn
                self.clear_selection()
                return self.check_checkmate()
            elif self.game_grid.is_empty(b_row, b_col):
                self.clear_selection()
                return False
            else:
                piece = self.game_grid.grid[b_row][b_col]
                if piece != 0 and self.is_white_turn == piece.is_white:
                    self.select_piece(b_row, b_col)
                return False
        else:
            piece = self.game_grid.grid[b_row][b_col]
            if piece != 0 and self.is_white_turn == piece.is_white:
                self.select_piece(b_row, b_col)
            return False
                

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
        
    def check_checkmate(self):
        king_pos = self.game_grid.get_king_square(self.is_white_turn)
        return self.game_grid.checkmate(king_pos, self.is_white_turn)


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
