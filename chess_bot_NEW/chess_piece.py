import pygame
import utils

class Grid():
    def __init__(self, rows, cols, tile_size, border, player_is_white=True):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.border = border
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        # map with piece, from (row, col), to (row, col), special move like "double_step" for pawns
        self.last_move = None
        # we flip rendering if player is white, not the game logic
        self.flip = not player_is_white
        
    def get_cell(self, row, col):
        return self.grid[row][col]
    
    def populate_grid(self, black_pieces, white_pieces):
        self.grid[0] = [
        black_pieces["rook"][0],
        black_pieces["knight"][0],
        black_pieces["bishop"][0],
        black_pieces["queen"],
        black_pieces["king"],
        black_pieces["bishop"][1],
        black_pieces["knight"][1],
        black_pieces["rook"][1],
        ]

        for i in range(8):
            self.grid[1][i] = black_pieces["pawn"][i]

        # white back rank
        self.grid[7] = [
        white_pieces["rook"][0],
        white_pieces["knight"][0],
        white_pieces["bishop"][0],
        white_pieces["queen"],
        white_pieces["king"],
        white_pieces["bishop"][1],
        white_pieces["knight"][1],
        white_pieces["rook"][1],
        ]

        for i in range(8):
            self.grid[6][i] = white_pieces["pawn"][i]
        
    def board_to_screen(self, row, col):
        """Convert board coords -> screen coords depending on flip."""
        if self.flip:
            row = 7 - row
            col = 7 - col
        return row, col
        
    def get_all_pieces(self, color):
        """
        Get all pieces of a certain color.
        """
        pieces = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] != 0 and self.grid[row][col].is_white == color:
                    pieces.append([self.grid[row][col], [row, col]])
        
        return pieces
        
    def draw(self, screen, color, legal_moves, selected_square = None):
        self.draw_chessboard(screen, color)
        if selected_square:
            r, c = selected_square
            rect = pygame.Rect(
                c * self.tile_size,
                self.border + r * self.tile_size,
                self.tile_size,
                self.tile_size,
            )
            pygame.draw.rect(screen, (210, 20, 20), rect)
            
        if legal_moves:
            self.draw_legal_moves(screen, legal_moves)
        self.draw_pieces(screen)    
    
    def draw_chessboard(self, screen, colors):
        # DRAW TILES
        for row in range(8):
            for col in range(8):
                r, c = self.board_to_screen(row, col)
                color = colors[(row + col) % 2]


                rect = pygame.Rect(
                c * self.tile_size,
                self.border + r * self.tile_size,
                self.tile_size,
                self.tile_size,
                )
                pygame.draw.rect(screen, color, rect)  
                
    def draw_legal_moves(self, screen, legal_moves):
        for row, col in legal_moves:
            r, c = self.board_to_screen(row, col)

            pygame.draw.circle(screen, (255, 200, 33),
            (c * self.tile_size + self.tile_size // 2,self.border + r * self.tile_size + self.tile_size // 2,),
            self.tile_size // 2 - 7)
            
    def draw_pieces(self, screen):
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece != 0:
                    r, c = self.board_to_screen(i, j)
                    piece.draw(screen, self.tile_size, self.border, (r, c))
        
    def is_empty(self, row, col):
        # empty space
        return self.grid[row][col] == 0

    def is_enemy(self, row, col, is_white):
        if self.is_empty(row, col):
            return False
        # if is_white is not == to current is_white we have an enemy
        return self.grid[row][col].is_white != is_white
    
    def move_piece(self, piece, from_pos, to_pos):
        s_row, s_col = from_pos
        e_row, e_col = to_pos
        
        # get special capture // en passant
        if isinstance(piece, Pawn):
            if s_col != e_col and self.is_empty(e_row, e_col):
                self.grid[s_row][e_col] = 0
        
        # check castle
        if isinstance(piece, King) and abs(e_col - s_col) == 2:
            # short
            if e_col == 6:
                rook = self.grid[s_row][7]
                self.grid[s_row][5] = rook
                self.grid[s_row][7] = 0
                rook.castle = False
            # long
            elif e_col == 2:
                rook = self.grid[s_row][0]
                self.grid[s_row][3] = rook
                self.grid[s_row][0] = 0
                rook.castle = False

                
        self.grid[e_row][e_col] = piece
        self.grid[s_row][s_col] = 0
        
        if isinstance(piece, Pawn):
            piece.first_move = False
            
        if isinstance(piece, Rook):
            piece.castle = False
            
        if isinstance(piece, King):
            piece.castle = False
            
        self.last_move = {
            "piece": piece,
            "from": from_pos,
            "to": to_pos,
            "double_step": isinstance(piece, Pawn) and abs(from_pos[0] - to_pos[0]) == 2
        }
                
    def can_en_passant(self, pos, direction):
        if not self.last_move:
            return [-1, -1]
        
        lm = self.last_move
        
        if not lm["double_step"]:
            return [-1,-1]
        
        # same row
        if (lm["to"][0] - pos[0]) == 0:
            # check if they are adjacent
            # enemy pawn on the left
            if abs(pos[1] - lm["to"][1]) == 1:
                return [pos[0]+direction,lm["to"][1]] 
                
        return [-1, -1]
    
    def is_square_attacked(self, square, pieces):
        for piece, pos in pieces:
            moves = piece.get_attack_squares(pos, self)
            
            if square in moves:
                return True
        return False

    def can_short_castle(self, king_pos, enemy_color):
        row, col = king_pos
        enemy_pieces = self.get_all_pieces(enemy_color)

        king = self.grid[row][col]
        rook = self.grid[row][7]

        # check all the condition that don't let castle happen
        if (not isinstance(king, King)) or (not isinstance(rook, Rook)):
            return False, [-1, -1]

        if not king.castle or not rook.castle:
            return False, [-1, -1]

        if (not self.is_empty(row, 5)) or (not self.is_empty(row, 6)):
            return False, [-1, -1]

        # king is in check or other square are attacked
        if self.is_square_attacked([row, 4], enemy_pieces):
            return False, [-1, -1]
        if self.is_square_attacked([row, 5], enemy_pieces) or self.is_square_attacked([row, 6], enemy_pieces):
            return False, [-1, -1]

        return True, [row, 6]
            
    def can_long_castle(self, king_pos, enemy_color):
        row, col = king_pos
        enemy_pieces = self.get_all_pieces(enemy_color)

        king = self.grid[row][col]
        rook = self.grid[row][0]

        if (not isinstance(king, King)) or (not isinstance(rook, Rook)):
            return False, [-1, -1]

        if not king.castle or not rook.castle:
            return False, [-1, -1]

        # squares between rook and king: 1,2,3 must be empty
        if (not self.is_empty(row, 1)) or (not self.is_empty(row, 2)) or (not self.is_empty(row, 3)):
            return False, [-1, -1]

        if self.is_square_attacked([row, 4], enemy_pieces):
            return False, [-1, -1]
        if self.is_square_attacked([row, 3], enemy_pieces) or self.is_square_attacked([row, 2], enemy_pieces):
            return False, [-1, -1]

        return True, [row, 2]


class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_sprite(self, x, y, w, h, s):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, w, h))
        if s != 1:
            sprite = pygame.transform.scale(
                sprite, (w * s, h * s)
            )
        #print(sprite.get_size())
        return sprite

class ChessPiece:
    def __init__(self, name, sprite):
        self.name = name
        self.sprite = sprite
        
        
    def draw(self, screen, tile_size, border, position):
        row, col = position
        x = col * tile_size
        y = row * tile_size + border
        screen.blit(self.sprite, (x, y))

class Pawn(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 0, 32, 32, scale)
        # special condition for first move
        self.first_move = True
        # this will be up only for one turn
        self.en_passant = False
        # to check if the piece is whether white or black
        self.is_white = is_white
        super().__init__("pawn", sprite)
        
    def get_attack_squares(self, position, grid: Grid):
        row, col = position
        direction = -1 if self.is_white else 1
        attacks = []
        for dc in (-1, 1):
            r, c = row + direction, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                attacks.append([r, c])
        return attacks 
        
    def get_legal_moves(self, position, grid: Grid):
        row, col = position
        direction = -1 if self.is_white else 1
        moves = []
        # check first square
        if 0 <= row+direction < 8 and grid.is_empty(row+direction, col):
            moves.append([row+direction, col])  
            # check second square if pawn never moved
            if self.first_move:
                if grid.is_empty(row+(direction*2), col) and row+(direction*2) >= 0:
                    moves.append([row+(direction*2), col])
        if col + 1 < 8 and grid.is_enemy(row + direction, col + 1, self.is_white):
            moves.append([row + direction, col + 1])
        if col - 1 >= 0 and grid.is_enemy(row + direction, col - 1, self.is_white):
            moves.append([row + direction, col - 1])
        
        en_passant = grid.can_en_passant(position, direction)
        if en_passant != (-1, -1):
            moves.append(en_passant)

        return moves
            
        
class Rook(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 32, 32, 32, scale)
        self.is_white = is_white
        super().__init__("rook", sprite)
        self.castle = True       
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_legal_moves(position, grid)
        
    def get_legal_moves(self, position, grid: Grid):
        directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
        ]
        return utils.sliding_moves(self, position, grid, directions)
        
class Bishop(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 64, 32, 32, scale)
        self.is_white = is_white
        super().__init__("bishop", sprite)
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_legal_moves(position, grid)
        
    def get_legal_moves(self, position, grid: Grid):
        directions = [
        (-1, -1),
        (1, -1),
        (-1, 1),
        (1, 1)
        ]
        return utils.sliding_moves(self, position, grid, directions)
    
class Knight(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 96, 32, 32, scale)
        self.is_white = is_white
        super().__init__("knight", sprite)
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_legal_moves(position, grid)
        
    def get_knight_moves(self, position, grid: Grid, directions):
        row, col = position
        dr, dc = directions
        r = row + dr
        c = col + dc
        
        if 0 <= r < 8 and 0 <= c < 8 and (grid.is_empty(r,c) or grid.is_enemy(r,c, self.is_white)):
            return [r,c]
                
    def get_legal_moves(self, position, grid: Grid):
        moves = []
        all_directions = [
            (-1, -2), (-1, 2), (1, -2), (1, 2),
            (-2, -1), (-2, 1), (2, -1), (2, 1)
        ]
        # possible cases: (-1,-2), (-1,2), (1,-2), (1,2), (-2,-1), (-2,1), (2,-1), (2,1)
        for directions in all_directions:
            curr_move = self.get_knight_moves(position, grid, directions)
            if curr_move:
                moves.append(curr_move)
        return moves
            
class Queen(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 128, 32, 32, scale)
        self.is_white = is_white
        super().__init__("queen", sprite)
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_legal_moves(position, grid)
        
    def get_legal_moves(self, position, grid: Grid):
        
        directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (1, -1), (-1, 1), (1, 1)
        ]
        return utils.sliding_moves(self, position, grid, directions)
    
class King(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 160, 32, 32, scale)
        self.is_white = is_white
        super().__init__("king", sprite)
        self.castle = True
        
    def get_attack_squares(self, position, grid: Grid):
        moves = []
        all_directions = [
            (-1, 0), (-1, -1), (0, -1), (1, -1),
            (1, 0), (1, 1), (0, 1), (-1, 1)
        ]
        for directions in all_directions:
            curr_move = self.get_king_moves(position, grid, directions)
            if curr_move:
                moves.append(curr_move)
        
        return moves
    
    def get_king_moves(self, position, grid:Grid, directions):
        row, col = position
        dr, dc = directions
        r = row + dr
        c = col + dc
        
        if 0 <= r < 8 and 0 <= c < 8 and (grid.is_empty(r,c) or grid.is_enemy(r,c, self.is_white)):
            return [r,c]
        
        
    def get_legal_moves(self, position, grid: Grid):
        moves = []
        all_directions = [
            (-1, 0), (-1, -1), (0, -1), (1, -1),
            (1, 0), (1, 1), (0, 1), (-1, 1)
        ]
        for directions in all_directions:
            curr_move = self.get_king_moves(position, grid, directions)
            if curr_move:
                moves.append(curr_move)
        if self.castle:
            ok, move = grid.can_long_castle(position, not self.is_white)
            if ok:
                moves.append(move)
            ok, move = grid.can_short_castle(position, not self.is_white)
            if ok:
                moves.append(move)
        
        return moves