class Grid():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        
    def get_cell(self, row, col):
        return self.grid[row][col]
    
    