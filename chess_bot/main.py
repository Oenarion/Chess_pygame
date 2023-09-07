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
    return pygame.font.Font("chess_bot/assets/font.ttf", size)


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
    pygame.image.load("chess_bot/assets/Background.png"),(GRID_SIZE,GRID_SIZE))
WIN = pygame.display.set_mode(size=(GRID_SIZE,GRID_SIZE))

WHITE=(255,255,255)
GREEN=(118,150,86)
FPS=60

#START PIECES IMG CREATION
#BLACK PIECES
BLACK_KING_IMG = pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_king.png'))
black_king = pygame.transform.scale(
    BLACK_KING_IMG,(CELL_SIZE,CELL_SIZE))

BLACK_QUEEN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_queen.png'))
black_queen=pygame.transform.scale(
    BLACK_QUEEN_IMG,(CELL_SIZE,CELL_SIZE))

BLACK_ROOK_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_rook.png'))
black_rook=pygame.transform.scale(
    BLACK_ROOK_IMG,(CELL_SIZE,CELL_SIZE))

BLACK_BISHOP_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_bishop.png'))
black_bishop=pygame.transform.scale(
    BLACK_BISHOP_IMG,(CELL_SIZE,CELL_SIZE))

BLACK_KNIGHT_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_knight.png'))
black_knight=pygame.transform.scale(
    BLACK_KNIGHT_IMG,(CELL_SIZE,CELL_SIZE))

BLACK_PAWN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_pawn.png'))
black_pawn=pygame.transform.scale(
    BLACK_PAWN_IMG,(CELL_SIZE,CELL_SIZE))

#WHITE PIECES
WHITE_KING_IMG = pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_king.png'))
white_king = pygame.transform.scale(
    WHITE_KING_IMG,(CELL_SIZE,CELL_SIZE))

WHITE_QUEEN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_queen.png'))
white_queen=pygame.transform.scale(
    WHITE_QUEEN_IMG,(CELL_SIZE,CELL_SIZE))

WHITE_ROOK_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_rook.png'))
white_rook=pygame.transform.scale(
    WHITE_ROOK_IMG,(CELL_SIZE,CELL_SIZE))

WHITE_BISHOP_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_bishop.png'))
white_bishop=pygame.transform.scale(
    WHITE_BISHOP_IMG,(CELL_SIZE,CELL_SIZE))

WHITE_KNIGHT_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_knight.png'))
white_knight=pygame.transform.scale(
    WHITE_KNIGHT_IMG,(CELL_SIZE,CELL_SIZE))

WHITE_PAWN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_pawn.png'))
white_pawn=pygame.transform.scale(
    WHITE_PAWN_IMG,(CELL_SIZE,CELL_SIZE))
#END

#This section is used to create two chessboards, one will be used to replace spots with no more pieces with the right color
#the other to know in which position each piece is
startingGreen=[False,False,False,False,False,False,False,False]
startingPieces=['','','','','','','','']
isGreen=[]
pieces_position=[]
for i in range(8):
    isGreen.append(startingGreen*1)
    pieces_position.append(startingPieces*1)




def draw_window_white(starting_position,black_pieces,white_pieces):
    #fill the background with a different color and update it
    #WIN.fill(WHITE)
    if starting_position:
        board=pygame.Surface((CELL_SIZE*8,CELL_SIZE*8))
        board.fill(WHITE)
        for x in range(0, 8, 2):
            for y in range(1, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                isGreen[x][y]=True
        for x in range(1, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                isGreen[x][y]=True        
        WIN.blit(board,board.get_rect())
        
        #black pieces draw
        WIN.blit(black_king,(black_pieces["black_king"].x,black_pieces["black_king"].y))
        WIN.blit(black_queen,(black_pieces["black_queen"].x,black_pieces["black_queen"].y))
        WIN.blit(black_bishop,(black_pieces["black_bishop_0"].x,black_pieces["black_bishop_0"].y))
        WIN.blit(black_bishop,(black_pieces["black_bishop_1"].x,black_pieces["black_bishop_1"].y)) 
        WIN.blit(black_knight,(black_pieces["black_knight_0"].x,black_pieces["black_knight_0"].y))
        WIN.blit(black_knight,(black_pieces["black_knight_1"].x,black_pieces["black_knight_1"].y))
        WIN.blit(black_rook,(black_pieces["black_rook_0"].x,black_pieces["black_rook_0"].y))
        WIN.blit(black_rook,(black_pieces["black_rook_1"].x,black_pieces["black_rook_1"].y))
        for i in range(8):
            WIN.blit(black_pawn,(black_pieces[f"black_pawn_{i}"].x,black_pieces[f"black_pawn_{i}"].y))
            
        pieces_position[0][0]='black_rook_0'
        pieces_position[0][1]='black_knight_0'
        pieces_position[0][2]='black_bishop_0'
        pieces_position[0][3]='black_queen'
        pieces_position[0][4]='black_king'
        pieces_position[0][7]='black_rook_1'
        pieces_position[0][6]='black_knight_1'
        pieces_position[0][5]='black_bishop_1'
        for i in range(8):
            pieces_position[1][i]=f'black_pawn_{i}'
            
        #white pieces draw
        WIN.blit(white_king,(white_pieces["white_king"].x,white_pieces["white_king"].y))
        WIN.blit(white_queen,(white_pieces["white_queen"].x,white_pieces["white_queen"].y))
        WIN.blit(white_bishop,(white_pieces["white_bishop_0"].x,white_pieces["white_bishop_0"].y))
        WIN.blit(white_bishop,(white_pieces["white_bishop_1"].x,white_pieces["white_bishop_1"].y))
        WIN.blit(white_knight,(white_pieces["white_knight_0"].x,white_pieces["white_knight_0"].y))
        WIN.blit(white_knight,(white_pieces["white_knight_1"].x,white_pieces["white_knight_1"].y))
        WIN.blit(white_rook,(white_pieces["white_rook_0"].x,white_pieces["white_rook_0"].y))
        WIN.blit(white_rook,(white_pieces["white_rook_1"].x,white_pieces["white_rook_1"].y))
        for i in range(8):
            WIN.blit(white_pawn,(white_pieces[f"white_pawn_{i}"].x,white_pieces[f"white_pawn_{i}"].y))
            
        pieces_position[7][0]='white_rook_0'
        pieces_position[7][1]='white_knight_0'
        pieces_position[7][2]='white_bishop_0'
        pieces_position[7][3]='white_queen'
        pieces_position[7][4]='white_king'
        pieces_position[7][7]='white_rook_1'
        pieces_position[7][6]='white_knight_1'
        pieces_position[7][5]='white_bishop_1'
        for i in range(8):
            pieces_position[6][i]=f'white_pawn_{i}'
            
        print(pieces_position)
            
def white_pieces_creation(black_pieces,white_pieces):
    
    black_king_piece=pygame.Rect(CELL_SIZE*4,0,CELL_SIZE,CELL_SIZE)
    black_pieces["black_king"]=black_king_piece
    black_queen_piece=pygame.Rect(CELL_SIZE*3,0,CELL_SIZE,CELL_SIZE)
    black_pieces["black_queen"]=black_queen_piece
    black_bishop_pieces=[]
    black_bishop_pieces.append(pygame.Rect(CELL_SIZE*2,0,CELL_SIZE,CELL_SIZE))
    black_bishop_pieces.append(pygame.Rect(CELL_SIZE*5,0,CELL_SIZE,CELL_SIZE))
    black_pieces["black_bishop_0"]=black_bishop_pieces[0]
    black_pieces["black_bishop_1"]=black_bishop_pieces[1]
    black_knight_pieces=[]
    black_knight_pieces.append(pygame.Rect(CELL_SIZE,0,CELL_SIZE,CELL_SIZE))
    black_knight_pieces.append(pygame.Rect(CELL_SIZE*6,0,CELL_SIZE,CELL_SIZE))
    black_pieces["black_knight_0"]=black_knight_pieces[0]
    black_pieces["black_knight_1"]=black_knight_pieces[1]
    black_rook_pieces=[]
    black_rook_pieces.append(pygame.Rect(0,0,CELL_SIZE,CELL_SIZE))
    black_rook_pieces.append(pygame.Rect(CELL_SIZE*7,0,CELL_SIZE,CELL_SIZE))
    black_pieces["black_rook_0"]=black_rook_pieces[0]
    black_pieces["black_rook_1"]=black_rook_pieces[1]
    black_pawn_pieces=[]
    for i in range(8):
        black_pawn_pieces.append(pygame.Rect(CELL_SIZE*i,CELL_SIZE,CELL_SIZE,CELL_SIZE))
        black_pieces[f"black_pawn_{i}"]=black_pawn_pieces[-1]
    
    white_king_piece=pygame.Rect(CELL_SIZE*4,CELL_SIZE*7,CELL_SIZE,CELL_SIZE)
    white_pieces["white_king"]=white_king_piece
    white_queen_piece=pygame.Rect(CELL_SIZE*3,CELL_SIZE*7,CELL_SIZE,CELL_SIZE)
    white_pieces["white_queen"]=white_queen_piece
    white_bishop_pieces=[]
    white_bishop_pieces.append(pygame.Rect(CELL_SIZE*2,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
    white_bishop_pieces.append(pygame.Rect(CELL_SIZE*5,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
    white_pieces["white_bishop_0"]=white_bishop_pieces[0]
    white_pieces["white_bishop_1"]=white_bishop_pieces[1]
    white_knight_pieces=[]
    white_knight_pieces.append(pygame.Rect(CELL_SIZE,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
    white_knight_pieces.append(pygame.Rect(CELL_SIZE*6,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
    white_pieces["white_knight_0"]=white_knight_pieces[0]
    white_pieces["white_knight_1"]=white_knight_pieces[1]
    white_rook_pieces=[]
    white_rook_pieces.append(pygame.Rect(0,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
    white_rook_pieces.append(pygame.Rect(CELL_SIZE*7,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
    white_pieces["white_rook_0"]=white_rook_pieces[0]
    white_pieces["white_rook_1"]=white_rook_pieces[1]
    white_pawn_pieces=[]
    for i in range(8):
        white_pawn_pieces.append(pygame.Rect(CELL_SIZE*i,CELL_SIZE*6,CELL_SIZE,CELL_SIZE))
        white_pieces[f"white_pawn_{i}"]=white_pawn_pieces[i]
    
    
def draw_window_black(starting_position):
    #fill the background with a different color and update it
    #WIN.fill(WHITE)
    if starting_position:
        board=pygame.Surface((CELL_SIZE*8,CELL_SIZE*8))
        board.fill(WHITE)
        for x in range(0, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                #print(x,y,isGreen)
                isGreen[x][y]=True
            #print(isGreen)
        for x in range(1, 8, 2):
            for y in range(1, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))  
                isGreen[x][y]=True      
        #print(isGreen)
        WIN.blit(board,board.get_rect())
        
        #black pieces draw
        WIN.blit(black_king,(CELL_SIZE*4,CELL_SIZE*7))
        black_king_piece=pygame.Rect(CELL_SIZE*4,CELL_SIZE*7,CELL_SIZE,CELL_SIZE)
        WIN.blit(black_queen,(CELL_SIZE*3,CELL_SIZE*7))
        black_queen_piece=pygame.Rect(CELL_SIZE*3,CELL_SIZE*7,CELL_SIZE,CELL_SIZE)
        
        WIN.blit(black_bishop,(CELL_SIZE*2,CELL_SIZE*7))
        WIN.blit(black_bishop,(CELL_SIZE*5,CELL_SIZE*7))
        black_bishops_pieces=[]
        black_bishops_pieces.append(pygame.Rect(CELL_SIZE*2,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
        black_bishops_pieces.append(pygame.Rect(CELL_SIZE*5,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
        
        WIN.blit(black_knight,(CELL_SIZE,CELL_SIZE*7))
        WIN.blit(black_knight,(CELL_SIZE*6,CELL_SIZE*7))
        black_knights_pieces=[]
        black_knights_pieces.append(pygame.Rect(CELL_SIZE,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
        black_knights_pieces.append(pygame.Rect(CELL_SIZE*6,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
        
        WIN.blit(black_rook,(0,CELL_SIZE*7))
        WIN.blit(black_rook,(CELL_SIZE*7,CELL_SIZE*7))
        black_rook_pieces=[]
        black_rook_pieces.append(pygame.Rect(0,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
        black_rook_pieces.append(pygame.Rect(CELL_SIZE*7,CELL_SIZE*7,CELL_SIZE,CELL_SIZE))
        
        black_pawns_pieces=[]
        for i in range(8):
            WIN.blit(black_pawn,(CELL_SIZE*i,CELL_SIZE*6))
            black_pawns_pieces.append(pygame.Rect(CELL_SIZE*i,CELL_SIZE,CELL_SIZE,CELL_SIZE))
            
        #white pieces draw
        WIN.blit(white_king,(CELL_SIZE*4,0))
        white_king_piece=pygame.Rect(CELL_SIZE*4,0,CELL_SIZE,CELL_SIZE)
        
        WIN.blit(white_queen,(CELL_SIZE*3,0))
        white_queen_piece=pygame.Rect(CELL_SIZE*3,0,CELL_SIZE,CELL_SIZE)
        
        WIN.blit(white_bishop,(CELL_SIZE*2,0))
        WIN.blit(white_bishop,(CELL_SIZE*5,0))
        white_bishop_pieces=[]
        white_bishop_pieces.append(pygame.Rect(CELL_SIZE*2,0,CELL_SIZE,CELL_SIZE))
        white_bishop_pieces.append(pygame.Rect(CELL_SIZE*5,0,CELL_SIZE,CELL_SIZE))
        
        WIN.blit(white_knight,(CELL_SIZE,0))
        WIN.blit(white_knight,(CELL_SIZE*6,0))
        white_knight_pieces=[]
        white_knight_pieces.append(pygame.Rect(CELL_SIZE,0,CELL_SIZE,CELL_SIZE))
        white_knight_pieces.append(pygame.Rect(CELL_SIZE*6,0,CELL_SIZE,CELL_SIZE))
        
        WIN.blit(white_rook,(0,0))
        WIN.blit(white_rook,(CELL_SIZE*7,0))
        white_rook_pieces=[]
        white_rook_pieces.append(pygame.Rect(0,0,CELL_SIZE,CELL_SIZE))
        white_rook_pieces.append(pygame.Rect(CELL_SIZE*7,0,CELL_SIZE,CELL_SIZE))
        
        white_pawn_pieces=[]
        for i in range(8):
            WIN.blit(white_pawn,(CELL_SIZE*i,CELL_SIZE))
            white_pawn_pieces.append(pygame.Rect(CELL_SIZE*i,CELL_SIZE,CELL_SIZE,CELL_SIZE))

#variables
def main_white():
    running = True
    clock = pygame.time.Clock()
    
    #pieces creation
    black_pieces={}
    white_pieces={}
    white_pieces_creation(black_pieces,white_pieces)
    #drawing chessboard first time
    draw_window_white(True,black_pieces,white_pieces)
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
        
            pygame.display.update()
        #draw_window_white(starting_position=False)
        
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

#TO ADD
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

        PLAY_WHITE_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=(GRID_SIZE//2, 250), 
                            text_input="PLAY_WHITE", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        PLAY_BLACK_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=(GRID_SIZE//2, 400), 
                            text_input="PLAY_BLACK", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Quit Rect.png"), pos=(GRID_SIZE//2, 550), 
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
    