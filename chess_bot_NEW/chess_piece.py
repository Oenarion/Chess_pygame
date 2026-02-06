import pygame

possible_moves = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),   
    'right': (0, 1),
}

class Grid():
    def __init__(self, rows, cols, tile_size, border):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.border = border
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        # map with piece, from (row, col), to (row, col), special move like "double_step" for pawns
        self.last_move = None
        
    def get_cell(self, row, col):
        return self.grid[row][col]
    
    def populate_grid(self, black_pieces, white_pieces, is_player_white=True):
        self.grid[0][0] = black_pieces["rook"][0] if is_player_white else white_pieces["rook"][0]
        self.grid[0][1] = black_pieces["knight"][0] if is_player_white else white_pieces["knight"][0]
        self.grid[0][2] = black_pieces["bishop"][0] if is_player_white else white_pieces["bishop"][0]
        self.grid[0][3] = black_pieces["queen"] if is_player_white else white_pieces["king"]
        self.grid[0][4] = black_pieces["king"] if is_player_white else white_pieces["queen"]
        self.grid[0][5] = black_pieces["bishop"][1] if is_player_white else white_pieces["bishop"][1]
        self.grid[0][6] = black_pieces["knight"][1] if is_player_white else white_pieces["knight"][1]
        self.grid[0][7] = black_pieces["rook"][1] if is_player_white else white_pieces["rook"][1]
        for i in range(8):
            self.grid[1][i] = black_pieces["pawn"][i] if is_player_white else white_pieces["pawn"][i]
            
        self.grid[-1][0] = white_pieces["rook"][0] if is_player_white else black_pieces["rook"][0]
        self.grid[-1][1] = white_pieces["knight"][0] if is_player_white else black_pieces["knight"][0]
        self.grid[-1][2] = white_pieces["bishop"][0] if is_player_white else black_pieces["bishop"][0]
        self.grid[-1][3] = white_pieces["queen"] if is_player_white else black_pieces["king"]
        self.grid[-1][4] = white_pieces["king"] if is_player_white else black_pieces["queen"]
        self.grid[-1][5] = white_pieces["bishop"][1] if is_player_white else black_pieces["bishop"][1]
        self.grid[-1][6] = white_pieces["knight"][1] if is_player_white else black_pieces["knight"][1]
        self.grid[-1][7] = white_pieces["rook"][1] if is_player_white else black_pieces["rook"][1]
        for i in range(8):
            self.grid[-2][i] = white_pieces["pawn"][i] if is_player_white else black_pieces["pawn"][i]
        
    def draw(self, screen, color, legal_moves):
        self.draw_chessboard(screen, color)
        if legal_moves:
            self.draw_legal_moves(screen, legal_moves)
        self.draw_pieces(screen)    
    
    def draw_chessboard(self, screen, colors):
        # DRAW TILES
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                rect = pygame.Rect(col * self.tile_size, self.border + row * self.tile_size, 
                                   self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)    
                
    def draw_legal_moves(self, screen, legal_moves):
        for row, col in legal_moves:
            pygame.draw.circle(screen, (255, 200, 33), 
                               (col*self.tile_size + self.tile_size//2,self.border + row*self.tile_size + self.tile_size//2),
                               self.tile_size//2 - 5)
            
    def draw_pieces(self, screen):
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] != 0:
                    self.grid[i][j].draw(screen, self.tile_size, self.border, (i, j))
        
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
            
        self.grid[e_row][e_col] = piece
        self.grid[s_row][s_col] = 0
        
        if isinstance(piece, Pawn):
            piece.first_move = False
            
        self.last_move = {
            "piece": piece,
            "from": from_pos,
            "to": to_pos,
            "double_step": isinstance(piece, Pawn) and abs(from_pos[0] - to_pos[0]) == 2
        }
                
    def can_en_passant(self, pos, direction):
        if not self.last_move:
            return (-1, -1)
        
        lm = self.last_move
        
        if not lm["double_step"]:
            return (-1,-1)
        
        # same row
        if (lm["to"][0] - pos[0]) == 0:
            # check if they are adjacent
            # enemy pawn on the left
            if abs(pos[1] - lm["to"][1]) == 1:
                return (pos[0]+direction,lm["to"][1]) 
                
        return (-1, -1)


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
        
    def get_legal_moves(self, position, grid: Grid):
        row, col = position
        direction = -1 if self.is_white else 1
        moves = []
        # check first square
        if grid.is_empty(row+direction, col) and row+direction >= 0:
            moves.append([row+direction, col])  
        # check second square if pawn never moved
        if self.first_move:
            if grid.is_empty(row+(direction*2), col) and row+(direction*2) >= 0:
                moves.append([row+(direction*2), col])
        if grid.is_enemy(row + direction, col + 1, self.is_white):
            moves.append([row + direction, col + 1])
        if grid.is_enemy(row + direction, col - 1, self.is_white):
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
        
class Bishop(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 64, 32, 32, scale)
        self.is_white = is_white
        super().__init__("bishop", sprite)
        
class Knight(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 96, 32, 32, scale)
        self.is_white = is_white
        super().__init__("knight", sprite)
        
class Queen(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 128, 32, 32, scale)
        self.is_white = is_white
        super().__init__("queen", sprite)
        
class King(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 160, 32, 32, scale)
        self.is_white = is_white
        super().__init__("king", sprite)