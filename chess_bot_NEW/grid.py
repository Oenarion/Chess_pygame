import pygame

class Grid():
    def __init__(self, rows, cols, tile_size, border):
        self.rows = rows
        self.cols = cols
        self.tile_size = tile_size
        self.border = border
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        
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
        
    def draw(self, screen, color):
        self.draw_chessboard(screen, color)
        self.draw_pieces(screen)    
    
    def draw_chessboard(self, screen, colors):
        # DRAW TILES
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                rect = pygame.Rect(col * self.tile_size, self.border + row * self.tile_size, 
                                   self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)    
                
    def draw_pieces(self, screen):
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] != 0:
                    self.grid[i][j].draw(screen, self.tile_size, self.border, (i, j))
        