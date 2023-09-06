import pygame
import os
import sys
from button import Button

pygame.init()
pygame.font.init()
pygame.mixer.init()
import pygame.display
pygame.display.init()

pygame.display.set_caption("Chess")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


info = pygame.display.Info()
height_width_line=str(info).split('\n')[7]
width_line=height_width_line.split(",")[0]
WIDTH=int(width_line.split(" = ")[1])
height_line=height_width_line.split(",")[1]
HEIGHT=int(height_line.split(" = ")[1])-100

GRID_SIZE=(min(WIDTH,HEIGHT)//8)*8

CELL_SIZE=GRID_SIZE//8

#bounds definition
RESOLUTIONS = [(1280, 768), (1600, 900), (1920, 1080)]
#picked_resolution = input("Pick the current resolution, 0 for 1280x768, 1 for 1600x900, 2 for 1920x1080\n")
BG = pygame.transform.scale(
    pygame.image.load("assets/Background.png"),(GRID_SIZE,GRID_SIZE))
WIN = pygame.display.set_mode(size=(GRID_SIZE,GRID_SIZE))

WHITE=(255,255,255)
GREEN=(118,150,86)
FPS=60

#START PIECES CREATION
#BLACK PIECES
BLACK_KING_IMG = pygame.image.load(
    os.path.join('piecesPNGs','black_king.png'))
BLACK_KING = pygame.transform.scale(
    BLACK_KING_IMG,(CELL_SIZE,CELL_SIZE))

BLACK_QUEEN_IMG=pygame.image.load(
    os.path.join('piecesPNGs','black_queen.png'))
BLACK_QUEEN=pygame.transform.scale(
    BLACK_QUEEN_IMG,(CELL_SIZE,CELL_SIZE))

BLACK_ROOK_IMG=pygame.image.load(
    os.path.join('piecesPNGs','black_rook.png'))
BLACK_ROOK=[pygame.transform.scale(
    BLACK_ROOK_IMG,(CELL_SIZE,CELL_SIZE))]*2

BLACK_BISHOP_IMG=pygame.image.load(
    os.path.join('piecesPNGs','black_bishop.png'))
BLACK_BISHOPS=[pygame.transform.scale(
    BLACK_BISHOP_IMG,(CELL_SIZE,CELL_SIZE))]*2

BLACK_KNIGHT_IMG=pygame.image.load(
    os.path.join('piecesPNGs','black_knight.png'))
BLACK_KNIGHTS=[pygame.transform.scale(
    BLACK_KNIGHT_IMG,(CELL_SIZE,CELL_SIZE))]*2

BLACK_PAWN_IMG=pygame.image.load(
    os.path.join('piecesPNGs','black_pawn.png'))
BLACK_PAWNS=[pygame.transform.scale(
    BLACK_PAWN_IMG,(CELL_SIZE,CELL_SIZE))]*8


WHITE_KING_IMG = pygame.image.load(
    os.path.join('piecesPNGs','white_king.png'))
WHITE_KING = pygame.transform.scale(
    WHITE_KING_IMG,(CELL_SIZE,CELL_SIZE))

WHITE_QUEEN_IMG=pygame.image.load(
    os.path.join('piecesPNGs','white_queen.png'))
WHITE_QUEEN=pygame.transform.scale(
    WHITE_QUEEN_IMG,(CELL_SIZE,CELL_SIZE))

WHITE_ROOK_IMG=pygame.image.load(
    os.path.join('piecesPNGs','white_rook.png'))
WHITE_ROOK=[pygame.transform.scale(
    WHITE_ROOK_IMG,(CELL_SIZE,CELL_SIZE))]*2

WHITE_BISHOP_IMG=pygame.image.load(
    os.path.join('piecesPNGs','white_bishop.png'))
WHITE_BISHOPS=[pygame.transform.scale(
    WHITE_BISHOP_IMG,(CELL_SIZE,CELL_SIZE))]*2

WHITE_KNIGHT_IMG=pygame.image.load(
    os.path.join('piecesPNGs','white_knight.png'))
WHITE_KNIGHTS=[pygame.transform.scale(
    WHITE_KNIGHT_IMG,(CELL_SIZE,CELL_SIZE))]*2

WHITE_PAWN_IMG=pygame.image.load(
    os.path.join('piecesPNGs','white_pawn.png'))
WHITE_PAWNS=[pygame.transform.scale(
    WHITE_PAWN_IMG,(CELL_SIZE,CELL_SIZE))]*8

#WHITE PIECES

#END PIECES CREATION

def draw_window_white(starting_position):
    #fill the background with a different color and update it
    #WIN.fill(WHITE)
    if starting_position:
        board=pygame.Surface((CELL_SIZE*8,CELL_SIZE*8))
        board.fill(WHITE)
        for x in range(0, 8, 2):
            for y in range(1, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for x in range(1, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))        
        WIN.blit(board,board.get_rect())
        
        #black pieces draw
        WIN.blit(BLACK_KING,(CELL_SIZE*4,0))
        WIN.blit(BLACK_QUEEN,(CELL_SIZE*3,0))
        WIN.blit(BLACK_BISHOPS[0],(CELL_SIZE*2,0))
        WIN.blit(BLACK_BISHOPS[1],(CELL_SIZE*5,0))
        WIN.blit(BLACK_KNIGHTS[0],(CELL_SIZE,0))
        WIN.blit(BLACK_KNIGHTS[1],(CELL_SIZE*6,0))
        WIN.blit(BLACK_ROOK[0],(0,0))
        WIN.blit(BLACK_ROOK[1],(CELL_SIZE*7,0))
        for i in range(len(BLACK_PAWNS)):
            WIN.blit(BLACK_PAWNS[i],(CELL_SIZE*i,CELL_SIZE))
            
        #white pieces draw
        WIN.blit(WHITE_KING,(CELL_SIZE*4,CELL_SIZE*7))
        WIN.blit(WHITE_QUEEN,(CELL_SIZE*3,CELL_SIZE*7))
        WIN.blit(WHITE_BISHOPS[0],(CELL_SIZE*2,CELL_SIZE*7))
        WIN.blit(WHITE_BISHOPS[1],(CELL_SIZE*5,CELL_SIZE*7))
        WIN.blit(WHITE_KNIGHTS[0],(CELL_SIZE,CELL_SIZE*7))
        WIN.blit(WHITE_KNIGHTS[1],(CELL_SIZE*6,CELL_SIZE*7))
        WIN.blit(WHITE_ROOK[0],(0,CELL_SIZE*7))
        WIN.blit(WHITE_ROOK[1],(CELL_SIZE*7,CELL_SIZE*7))
        for i in range(len(WHITE_PAWNS)):
            WIN.blit(WHITE_PAWNS[i],(CELL_SIZE*i,CELL_SIZE*6))
    
def draw_window_black(starting_position):
    #fill the background with a different color and update it
    #WIN.fill(WHITE)
    if starting_position:
        board=pygame.Surface((CELL_SIZE*8,CELL_SIZE*8))
        board.fill(WHITE)
        for x in range(0, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for x in range(1, 8, 2):
            for y in range(1, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))        
        WIN.blit(board,board.get_rect())
        
        #black pieces draw
        WIN.blit(BLACK_KING,(CELL_SIZE*4,CELL_SIZE*7))
        WIN.blit(BLACK_QUEEN,(CELL_SIZE*3,CELL_SIZE*7))
        WIN.blit(BLACK_BISHOPS[0],(CELL_SIZE*2,CELL_SIZE*7))
        WIN.blit(BLACK_BISHOPS[1],(CELL_SIZE*5,CELL_SIZE*7))
        WIN.blit(BLACK_KNIGHTS[0],(CELL_SIZE,CELL_SIZE*7))
        WIN.blit(BLACK_KNIGHTS[1],(CELL_SIZE*6,CELL_SIZE*7))
        WIN.blit(BLACK_ROOK[0],(0,CELL_SIZE*7))
        WIN.blit(BLACK_ROOK[1],(CELL_SIZE*7,CELL_SIZE*7))
        for i in range(len(BLACK_PAWNS)):
            WIN.blit(BLACK_PAWNS[i],(CELL_SIZE*i,CELL_SIZE*6))
            
        #white pieces draw
        WIN.blit(WHITE_KING,(CELL_SIZE*4,0))
        WIN.blit(WHITE_QUEEN,(CELL_SIZE*3,0))
        WIN.blit(WHITE_BISHOPS[0],(CELL_SIZE*2,0))
        WIN.blit(WHITE_BISHOPS[1],(CELL_SIZE*5,0))
        WIN.blit(WHITE_KNIGHTS[0],(CELL_SIZE,0))
        WIN.blit(WHITE_KNIGHTS[1],(CELL_SIZE*6,0))
        WIN.blit(WHITE_ROOK[0],(0,0))
        WIN.blit(WHITE_ROOK[1],(CELL_SIZE*7,0))
        for i in range(len(WHITE_PAWNS)):
            WIN.blit(WHITE_PAWNS[i],(CELL_SIZE*i,CELL_SIZE))

#variables
def main_white():
    running = True
    clock = pygame.time.Clock()
    #Need to add a menu to choose the color
    
    
    #drawing chessboard first time
    draw_window_white(starting_position=True)
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
        
            pygame.display.update()
        draw_window_white(starting_position=False)
        
    pygame.quit()
    
def main_black():
    running = True
    clock = pygame.time.Clock()
    #Need to add a menu to choose the color
    
    
    #drawing chessboard first time
    draw_window_black(starting_position=True)
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
        
            pygame.display.update()
        draw_window_black(starting_position=False)
        
    pygame.quit()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        WIN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(GRID_SIZE//2, 100))

        PLAY_WHITE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(GRID_SIZE//2, 250), 
                            text_input="PLAY_WHITE", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        PLAY_BLACK_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(GRID_SIZE//2, 400), 
                            text_input="PLAY_BLACK", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(GRID_SIZE//2, 550), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_WHITE_BUTTON, PLAY_BLACK_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_WHITE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_white()
                if PLAY_BLACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_black()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    