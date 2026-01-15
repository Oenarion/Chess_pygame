import pygame

possible_moves = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),   
    'right': (0, 1),
}

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
    def __init__(self, name, sprite, position):
        self.name = name
        self.sprite = sprite
        self.position = position  # (row, col)
        
    def draw(self, screen, tile_size, border):
        row, col = self.position
        x = col * tile_size
        y = row * tile_size + border
        screen.blit(self.sprite, (x, y))

class Pawn(ChessPiece):
    def __init__(self, spritesheet, position, scale, is_white=0):
        sprite = spritesheet.get_sprite(0+32*is_white, 0, 32, 32, scale)
        super().__init__("pawn", sprite, position)
        
class Rook(ChessPiece):
    def __init__(self, spritesheet, position, scale, is_white=0):
        sprite = spritesheet.get_sprite(0+32*is_white, 32, 32, 32, scale)
        super().__init__("rook", sprite, position)
        
class Bishop(ChessPiece):
    def __init__(self, spritesheet, position, scale, is_white=0):
        sprite = spritesheet.get_sprite(0+32*is_white, 64, 32, 32, scale)
        super().__init__("bishop", sprite, position)
        
class Knight(ChessPiece):
    def __init__(self, spritesheet, position, scale, is_white=0):
        sprite = spritesheet.get_sprite(0+32*is_white, 96, 32, 32, scale)
        super().__init__("knight", sprite, position)
        
class Queen(ChessPiece):
    def __init__(self, spritesheet, position, scale, is_white=0):
        sprite = spritesheet.get_sprite(0+32*is_white, 128, 32, 32, scale)
        super().__init__("queen", sprite, position)
        
class King(ChessPiece):
    def __init__(self, spritesheet, position, scale, is_white=0):
        sprite = spritesheet.get_sprite(0+32*is_white, 160, 32, 32, scale)
        super().__init__("king", sprite, position)