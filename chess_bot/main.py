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
    pygame.image.load("chess_bot/assets/Background.png"),(GRID_SIZE+100,GRID_SIZE))
WIN = pygame.display.set_mode(size=(GRID_SIZE+100,GRID_SIZE))


WHITE=(255,255,255)
GREEN=(118,150,86)
RED=(136,8,8)
YELLOW=(236,234,152)
GREY=(119,136,153)
FPS=60

#START PIECES IMG CREATION
#BLACK PIECES

#create a dictionary to store all the possible imgs to be able to use them way more easily
BLACK_PIECES_IMGS={}

BLACK_KING_IMG = pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_king.png'))
black_king = pygame.transform.scale(
    BLACK_KING_IMG,(CELL_SIZE,CELL_SIZE))
BLACK_PIECES_IMGS['black_king']=black_king


BLACK_QUEEN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_queen.png'))
black_queen=pygame.transform.scale(
    BLACK_QUEEN_IMG,(CELL_SIZE,CELL_SIZE))
BLACK_PIECES_IMGS['black_queen']=black_queen

BLACK_ROOK_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_rook.png'))
black_rook=pygame.transform.scale(
    BLACK_ROOK_IMG,(CELL_SIZE,CELL_SIZE))
BLACK_PIECES_IMGS['black_rook']=black_rook

BLACK_BISHOP_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_bishop.png'))
black_bishop=pygame.transform.scale(
    BLACK_BISHOP_IMG,(CELL_SIZE,CELL_SIZE))
BLACK_PIECES_IMGS['black_bishop']=black_bishop

BLACK_KNIGHT_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_knight.png'))
black_knight=pygame.transform.scale(
    BLACK_KNIGHT_IMG,(CELL_SIZE,CELL_SIZE))
BLACK_PIECES_IMGS['black_knight']=black_knight

BLACK_PAWN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','black_pawn.png'))
black_pawn=pygame.transform.scale(
    BLACK_PAWN_IMG,(CELL_SIZE,CELL_SIZE))
BLACK_PIECES_IMGS['black_pawn']=black_pawn


WHITE_PIECES_IMGS={}

#WHITE PIECES
WHITE_KING_IMG = pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_king.png'))
white_king = pygame.transform.scale(
    WHITE_KING_IMG,(CELL_SIZE,CELL_SIZE))
WHITE_PIECES_IMGS['white_king']=white_king

WHITE_QUEEN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_queen.png'))
white_queen=pygame.transform.scale(
    WHITE_QUEEN_IMG,(CELL_SIZE,CELL_SIZE))
WHITE_PIECES_IMGS['white_queen']=white_queen

WHITE_ROOK_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_rook.png'))
white_rook=pygame.transform.scale(
    WHITE_ROOK_IMG,(CELL_SIZE,CELL_SIZE))
WHITE_PIECES_IMGS['white_rook']=white_rook

WHITE_BISHOP_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_bishop.png'))
white_bishop=pygame.transform.scale(
    WHITE_BISHOP_IMG,(CELL_SIZE,CELL_SIZE))
WHITE_PIECES_IMGS['white_bishop']=white_bishop

WHITE_KNIGHT_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_knight.png'))
white_knight=pygame.transform.scale(
    WHITE_KNIGHT_IMG,(CELL_SIZE,CELL_SIZE))
WHITE_PIECES_IMGS['white_knight']=white_knight

WHITE_PAWN_IMG=pygame.image.load(
    os.path.join('chess_bot/piecesPNGs','white_pawn.png'))
white_pawn=pygame.transform.scale(
    WHITE_PAWN_IMG,(CELL_SIZE,CELL_SIZE))
WHITE_PIECES_IMGS['white_pawn']=white_pawn


board=pygame.display.set_mode((CELL_SIZE*8+100,CELL_SIZE*8))
#END

#This section is used to create two chessboards, one will be used to replace spots with no more pieces with the right color
#the other to know in which position each piece is
startingGreen=[False,False,False,False,False,False,False,False]
startingPieces=['','','','','','','','']
isGreen=[]
pieces_position=[]
isYellow=[]
for i in range(8):
    isGreen.append(startingGreen*1)
    isYellow.append(startingGreen*1)
    pieces_position.append(startingPieces*1)
    
#dictionary for all pieces
black_pieces={}
white_pieces={}

#variables for castle
blackKingMoved=False
blackRookMoved0=False
blackRookMoved1=False

whiteKingMoved=False
whiteRookMoved0=False
whiteRookMoved1=False

#variables for en-passant
#array with enpassant possible and position for it
WhiteEnPassantPossible=[False,-1,-1]
BlackEnPassantPossible=[False,-1,-1]

#variables for promotion
#3 is the starting number so that we don't have the same pieces called the same way
numberPromotedPiece=3
promotionCheck=False

#timer variables

#this variable is used when we surrend and want to start a fresh game without changing timer
#so that the timer restarts
lastSelectedNum=3

timers=[60,180,300,600,900,1800]
texts=['01:00','03:00','05:00','10:00','15:00','30:00']

white_counter=600
black_counter=600
white_text ='10:00'
black_text='10:00'
font = pygame.font.SysFont('Consolas', 30)

#to surrender the game
SURREND_RECT=pygame.transform.scale(
            pygame.image.load("chess_bot/assets/Quit Rect.png"),(90,50))

SURREND_WHITE_BUTTON = Button(image=SURREND_RECT, pos=(815, 640), 
                            text_input="Surrend", font=get_font(10), base_color="#d7fcd4", hovering_color=YELLOW)
SURREND_BLACK_BUTTON = Button(image=SURREND_RECT, pos=(815, 120), 
                            text_input="Surrend", font=get_font(10), base_color="#d7fcd4", hovering_color=YELLOW)


#sound effects
background_music=pygame.mixer.Sound('chess_bot/sound_effects/background_music.mp3')
button_sound=pygame.mixer.Sound("chess_bot/sound_effects/button_click.mp3")
capture_sound=pygame.mixer.Sound("chess_bot/sound_effects/capture.mp3")
move_sound=pygame.mixer.Sound("chess_bot/sound_effects/move-self.mp3")
winning_sound=pygame.mixer.Sound("chess_bot/sound_effects/winning_sound.mp3")


def draw_window_white(starting_position):
    #fill the background with a different color and update it
    #WIN.fill(WHITE)
    if starting_position:
        board.fill(WHITE)
        for x in range(0, 8, 2):
            for y in range(1, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                isGreen[x][y]=True
        for x in range(1, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(board, GREEN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                isGreen[x][y]=True        
                
        
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
        pieces_position[1][0]='black_knight_0'
        pieces_position[2][0]='black_bishop_0'
        pieces_position[3][0]='black_queen'
        pieces_position[4][0]='black_king'
        pieces_position[5][0]='black_bishop_1'
        pieces_position[6][0]='black_knight_1'
        pieces_position[7][0]='black_rook_1'

        for i in range(8):
            pieces_position[i][1]=f'black_pawn_{i}'
            
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
            
        pieces_position[0][7]='white_rook_0'
        pieces_position[1][7]='white_knight_0'
        pieces_position[2][7]='white_bishop_0'
        pieces_position[3][7]='white_queen'
        pieces_position[4][7]='white_king'
        pieces_position[5][7]='white_bishop_1'
        pieces_position[6][7]='white_knight_1'
        pieces_position[7][7]='white_rook_1'
        for i in range(8):
            pieces_position[i][6]=f'white_pawn_{i}'
            
        pygame.draw.rect(board,(0,0,0),(CELL_SIZE*8,0,10,CELL_SIZE*8))
        pygame.draw.rect(board,'#DE3163',(CELL_SIZE*8+10,0,90,CELL_SIZE*8))
        pygame.draw.rect(board,'#5D3FD3',(CELL_SIZE*8+10,CELL_SIZE,90,CELL_SIZE*6))
            
        print(pieces_position)
        print(isGreen)

#player is playing WHITE
def white_pieces_creation():
    #create a rectangle for every piece and place in a dictionary piece position
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

    
#using the dictionary we redraw each piece in it's current position
def draw_updatedPieces():
    for key in black_pieces:
        ignoreNums=key.split('_')
        newKey=ignoreNums[0]+'_'+ignoreNums[1]
        WIN.blit(BLACK_PIECES_IMGS[newKey],(black_pieces[key].x,black_pieces[key].y))

    for key in white_pieces:
        ignoreNums=key.split('_')
        newKey=ignoreNums[0]+'_'+ignoreNums[1]
        WIN.blit(WHITE_PIECES_IMGS[newKey],(white_pieces[key].x,white_pieces[key].y))


def draw_promotionPieces(color,pos):
    if color=='black':
        WIN.blit(black_queen,(pos[0]*CELL_SIZE,(pos[1]-1)*CELL_SIZE))
        WIN.blit(black_rook,(pos[0]*CELL_SIZE,(pos[1]-2)*CELL_SIZE))
        WIN.blit(black_bishop,(pos[0]*CELL_SIZE,(pos[1]-3)*CELL_SIZE))
        WIN.blit(black_knight,(pos[0]*CELL_SIZE,(pos[1]-4)*CELL_SIZE))
    else:
        WIN.blit(white_queen,(pos[0]*CELL_SIZE,(pos[1]+1)*CELL_SIZE))
        WIN.blit(white_rook,(pos[0]*CELL_SIZE,(pos[1]+2)*CELL_SIZE))
        WIN.blit(white_bishop,(pos[0]*CELL_SIZE,(pos[1]+3)*CELL_SIZE))
        WIN.blit(white_knight,(pos[0]*CELL_SIZE,(pos[1]+4)*CELL_SIZE))
#handles the deletion of multiple red squares, we have at most once 

def draw_piecesBeforePromotion(color,pos):
    #Have to temporaly delete elements in the way of promotion pieces, to be able to choose the correct one
    if color=='black':
        for key in black_pieces:
            ignoreNums=key.split('_')
            newKey=ignoreNums[0]+'_'+ignoreNums[1]
            if pos[0]==black_pieces[key].x//CELL_SIZE and ((pos[1]==black_pieces[key].y//CELL_SIZE)-1 or (pos[1]==black_pieces[key].y//CELL_SIZE)-2 or (pos[1]==black_pieces[key].y//CELL_SIZE)-3 or (pos[1]==black_pieces[key].y//CELL_SIZE)-4):
                continue
            else:    
                WIN.blit(BLACK_PIECES_IMGS[newKey],(black_pieces[key].x,black_pieces[key].y))

        for key in white_pieces:
            ignoreNums=key.split('_')
            newKey=ignoreNums[0]+'_'+ignoreNums[1]
            print(pos[0],pos[1],white_pieces[key].x,white_pieces[key].y)
            if pos[0]==white_pieces[key].x//CELL_SIZE and (pos[1]==(white_pieces[key].y//CELL_SIZE)-1 or pos[1]==(white_pieces[key].y//CELL_SIZE)-2 or (pos[1]==white_pieces[key].y//CELL_SIZE)-3 or (pos[1]==white_pieces[key].y//CELL_SIZE)-4):
                print("hello")
                continue
            else:    
                WIN.blit(WHITE_PIECES_IMGS[newKey],(white_pieces[key].x,white_pieces[key].y))
    else:
        for key in black_pieces:
            ignoreNums=key.split('_')
            newKey=ignoreNums[0]+'_'+ignoreNums[1]
            if pos[0]==black_pieces[key].x//CELL_SIZE and ((pos[1]==black_pieces[key].y//CELL_SIZE)+1 or (pos[1]==black_pieces[key].y//CELL_SIZE)+2 or (pos[1]==black_pieces[key].y//CELL_SIZE)+3 or (pos[1]==black_pieces[key].y//CELL_SIZE)+4):
                continue
            else:    
                WIN.blit(BLACK_PIECES_IMGS[newKey],(black_pieces[key].x,black_pieces[key].y))

        for key in white_pieces:
            ignoreNums=key.split('_')
            newKey=ignoreNums[0]+'_'+ignoreNums[1]
            if pos[0]==white_pieces[key].x//CELL_SIZE and ((pos[1]==white_pieces[key].y//CELL_SIZE)+1 or (pos[1]==white_pieces[key].y//CELL_SIZE)+2 or (pos[1]==white_pieces[key].y//CELL_SIZE)+3 or (pos[1]==white_pieces[key].y//CELL_SIZE)+4):
                continue
            else:    
                WIN.blit(WHITE_PIECES_IMGS[newKey],(white_pieces[key].x,white_pieces[key].y))

def redrawChessboard():
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

def deleteLastPossibleMoves():
    for i in range(8):
        for j in range(8):
            isYellow[i][j]=False

#once a yellow square is touched, we need to move the pieces
#update positions and remove eaten ones
def movePieces(piece,pos,currentTurn):
    global WhiteEnPassantPossible
    global BlackEnPassantPossible
    global whiteKingMoved
    global whiteRookMoved0
    global whiteRookMoved1
    global blackKingMoved
    global blackRookMoved0
    global blackRookMoved1
    global capture_sound,move_sound
    
    capture=False
    #if rook gets eaten we can't castle of course
    if "white_rook_0" not in white_pieces:
        whiteRookMoved0=True
    if "white_rook_1" not in white_pieces:
        whiteRookMoved1=True
    if "black_rook_0" not in black_pieces:
        blackRookMoved0=True
    if "black_rook_1" not in black_pieces:
        blackRookMoved1=True
            
    print(blackRookMoved0,blackRookMoved1,whiteRookMoved0,whiteRookMoved1)
    #print(white_pieces,black_pieces)
    #CHECK for en-passant as first thing
    
    if  BlackEnPassantPossible[0] and 'black_pawn' in piece and pos[0]==BlackEnPassantPossible[1] and pos[1]==BlackEnPassantPossible[-1]+1:
        current_piece=pieces_position[BlackEnPassantPossible[1]][pos[1]-1]
        print("black en passant",current_piece)
        white_pieces.pop(current_piece)
        pieces_position[BlackEnPassantPossible[1]][pos[1]-1]=''
        pieces_position[black_pieces[piece].x//CELL_SIZE][black_pieces[piece].y//CELL_SIZE]=''
        black_pieces[piece].x=pos[0]*CELL_SIZE
        black_pieces[piece].y=pos[1]*CELL_SIZE
        pieces_position[pos[0]][pos[1]]=piece
        capture_sound.play()

    elif WhiteEnPassantPossible[0] and 'white_pawn' in piece and pos[0]==WhiteEnPassantPossible[1] and pos[1]==WhiteEnPassantPossible[-1]-1:
        current_piece=pieces_position[WhiteEnPassantPossible[1]][pos[1]+1]
        print("white en passant", current_piece)
        black_pieces.pop(current_piece)
        pieces_position[WhiteEnPassantPossible[1]][pos[1]+1]=''
        pieces_position[white_pieces[piece].x//CELL_SIZE][white_pieces[piece].y//CELL_SIZE]=''
        white_pieces[piece].x=pos[0]*CELL_SIZE
        white_pieces[piece].y=pos[1]*CELL_SIZE
        pieces_position[pos[0]][pos[1]]=piece 
        capture_sound.play()
        
    WhiteEnPassantPossible=[False,-1,-1]
    BlackEnPassantPossible=[False,-1,-1]
    
    if currentTurn=='white':
        currentTurn='black'
    else:
        currentTurn='white'
    current_piece=pieces_position[pos[0]][pos[1]]
    
    if 'black_pawn' in piece and pos[1]==7:
        promotion('black',piece,pos)
        return currentTurn
    elif 'white_pawn' in piece and pos[1]==0:
        promotion('white',piece,pos)
        return currentTurn
    
    print(piece,current_piece)
    if 'black' in piece:
        if 'king' in piece and 'black_rook' in current_piece and not ((blackKingMoved and blackRookMoved0) or (blackKingMoved and blackRookMoved1)):
            #long castle
            if 'black_rook_0' in current_piece:
                pieces_position[black_pieces[piece].x//CELL_SIZE][black_pieces[piece].y//CELL_SIZE]=''
                #updating black pieces to draw figures
                black_pieces['black_rook_0'].x=3*CELL_SIZE
                black_pieces[piece].x=2*CELL_SIZE
                #updating grid to check for future movements
                pieces_position[0][0]=''
                pieces_position[4][0]=''
                pieces_position[2][0]=piece
                pieces_position[3][0]='black_rook_0'
                move_sound.play()
                
                #To ensure castle can't be used again
                blackRookMoved0=True
                blackRookMoved1=True
                blackKingMoved=True
            #short castle
            if 'black_rook_1' in current_piece:
                pieces_position[black_pieces[piece].x//CELL_SIZE][black_pieces[piece].y//CELL_SIZE]=''
                #updating black pieces to draw figures
                black_pieces['black_rook_1'].x=5*CELL_SIZE
                black_pieces[piece].x=6*CELL_SIZE
                #updating grid to check for future movements
                pieces_position[7][0]=''
                pieces_position[6][0]=piece
                pieces_position[5][0]='black_rook_1'
                move_sound.play()
                
                #To ensure castle can't be used again
                blackRookMoved0=True
                blackRookMoved1=True
                blackKingMoved=True
        #normalize new position as the starting of the square
        # print(pos[0],pos[1])
        # print((pos[0]//8*8),(pos[1]//8)*8)
        else:
            if piece=='black_king':
                blackKingMoved=True
            elif piece=='black_rook_0':
                blackRookMoved0=True
            elif piece=='black_rook_1':
                blackRookMoved1=True
            if 'black_pawn' in piece and black_pieces[piece].y//CELL_SIZE==1 and pos[1]==3:
                #store the x value to know which way we can en passant
                WhiteEnPassantPossible=[True,black_pieces[piece].x//CELL_SIZE,pos[1]]
                print(WhiteEnPassantPossible)
            #NEED TO REDRAW EACH PIECE IN NEW POSITION!!
            if 'white' in current_piece:
                white_pieces.pop(current_piece)
                capture_sound.play()
                capture=True
            if not capture:
                move_sound.play()
            pieces_position[black_pieces[piece].x//CELL_SIZE][black_pieces[piece].y//CELL_SIZE]=''
            black_pieces[piece].x=pos[0]*CELL_SIZE
            black_pieces[piece].y=pos[1]*CELL_SIZE
            pieces_position[pos[0]][pos[1]]=piece
        
        #draw_updatedPieces()
        #WIN.blit(BLACK_PIECES_IMGS[newKey],(black_pieces[piece].x,black_pieces[piece].y))
        
    else:
        if 'king' in piece and 'white_rook' in current_piece:
            #long castle
            if 'white_rook_0' in current_piece:
                pieces_position[white_pieces[piece].x//CELL_SIZE][white_pieces[piece].y//CELL_SIZE]=''
                #updating black pieces to draw figures
                white_pieces['white_rook_0'].x=3*CELL_SIZE
                white_pieces[piece].x=2*CELL_SIZE
                #updating grid to check for future movements
                pieces_position[0][7]=''
                pieces_position[4][7]=''
                pieces_position[2][7]=piece
                pieces_position[3][7]='white_rook_0'
                move_sound.play()
                
                #To ensure castle can't be used again
                whiteRookMoved0=True
                whiteRookMoved1=True
                whiteKingMoved=True
            #short castle
            if 'white_rook_1' in current_piece:
                pieces_position[white_pieces[piece].x//CELL_SIZE][white_pieces[piece].y//CELL_SIZE]=''
                #updating black pieces to draw figures
                white_pieces['white_rook_1'].x=5*CELL_SIZE
                white_pieces[piece].x=6*CELL_SIZE
                #updating grid to check for future movements
                pieces_position[7][7]=''
                pieces_position[6][7]=piece
                pieces_position[5][7]='white_rook_1'
                move_sound.play()
                
                #To ensure castle can't be used again
                whiteRookMoved0=True
                whiteRookMoved1=True
                whiteKingMoved=True
        else:
            #print(current_piece,pos,white_pieces[piece].x,white_pieces[piece].y)
            if piece=='white_king':
                whiteKingMoved=True
            elif piece=='white_rook_0':
                whiteRookMoved0=True
            elif piece=='white_rook_1':
                whiteRookMoved1=True
            if 'white_pawn' in piece and white_pieces[piece].y//CELL_SIZE==6 and pos[1]==4:
                #store the x value to know which way we can en passant, either left or right
                BlackEnPassantPossible=[True,white_pieces[piece].x//CELL_SIZE,pos[1]]
                print(BlackEnPassantPossible)
            if 'black' in current_piece:
                black_pieces.pop(current_piece)
                capture_sound.play()
                capture=True
            if not capture:
                move_sound.play()
            pieces_position[white_pieces[piece].x//CELL_SIZE][white_pieces[piece].y//CELL_SIZE]=''
            white_pieces[piece].x=pos[0]*CELL_SIZE
            white_pieces[piece].y=pos[1]*CELL_SIZE
            pieces_position[pos[0]][pos[1]]=piece
    
    #to redraw everything with modifications
    redrawChessboard()
    redrawTimer(font,white_text,black_text,SURREND_WHITE_BUTTON,SURREND_BLACK_BUTTON)
    draw_updatedPieces()
    print(pieces_position)
    return currentTurn
    
#Changes the color of the box to red if we want to move a piece
def changeBoxColor(current_squareX,current_squareY):
    print(current_squareX,current_squareY)
    #If we already have a RED square we have to remove it
    redrawChessboard()
    redrawTimer(font,white_text,black_text,SURREND_WHITE_BUTTON,SURREND_BLACK_BUTTON)
    #Add the RED square where mouse cursor is
    pygame.draw.rect(board, RED, (current_squareX*CELL_SIZE, current_squareY*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    #Redraw all pieces because they get removed every time we redraw the chessboard
    check_possible_moves(current_squareX,current_squareY)
    draw_updatedPieces()
    return pieces_position[current_squareX][current_squareY]

def check_possible_moves(current_x,current_y):
    currentPiece=pieces_position[current_x][current_y]
    print(currentPiece)
    if "black_pawn" in currentPiece:
        check_pawn('black',current_x,current_y)
    elif "black_rook" in currentPiece:
        check_rook('black',current_x,current_y)
    elif "black_knight" in currentPiece:
        check_knight('black',current_x,current_y)
    elif 'black_bishop' in currentPiece:
        check_bishop('black',current_x,current_y)
    elif 'black_queen' in currentPiece:
        check_queen('black',current_x,current_y)
    elif 'black_king' in currentPiece:
        check_king('black',current_x,current_y)
    elif 'white_pawn' in currentPiece:
        check_pawn('white',current_x,current_y)
    elif "white_rook" in currentPiece:
        check_rook('white',current_x,current_y)
    elif "white_knight" in currentPiece:
        check_knight('white',current_x,current_y)
    elif 'white_bishop' in currentPiece:
        check_bishop('white',current_x,current_y)
    elif 'white_queen' in currentPiece:
        check_queen('white',current_x,current_y)
    elif 'white_king' in currentPiece:
        check_king('white',current_x,current_y)
    
    WIN.blit(board,board.get_rect())
    
def check_pawn(color,current_x,current_y):
    if color=='black':
        if current_y==1:
            #TO DRAW CIRCLES I NEED TO SET THE CENTER IN HALF OF THE SQUARE, I.E. CELL_SIZE+CELL_SIZE//2
            if pieces_position[current_x][current_y+1]=='':
                pygame.draw.circle(board, YELLOW, (current_x*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][current_y+1]=True
                if pieces_position[current_x][current_y+2]=='':
                    pygame.draw.circle(board, YELLOW, (current_x*CELL_SIZE+CELL_SIZE//2, (current_y+2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x][current_y+2]=True
            if current_x>=1 and "white" in pieces_position[current_x-1][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y+1]=True
            if current_x<7 and "white" in pieces_position[current_x+1][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y+1]=True
        else:
            if current_y+1<=7 and pieces_position[current_x][current_y+1]=='':
                pygame.draw.circle(board, YELLOW, (current_x*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][current_y+1]=True
            if current_y+1<=7 and current_x-1>=0 and "white" in pieces_position[current_x-1][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y+1]=True
            if current_x+1<=7 and current_y+1<=7 and "white" in pieces_position[current_x+1][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y+1]=True
            if current_y==4:
                en_passant('black',current_x,current_y)
    else:
        if current_y==6:
            #TO DRAW CIRCLES I NEED TO SET THE CENTER IN HALF OF THE SQUARE, I.E. CELL_SIZE+CELL_SIZE//2
            if pieces_position[current_x][current_y-1]=='':
                pygame.draw.circle(board, YELLOW, (current_x*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][current_y-1]=True
                if pieces_position[current_x][current_y-2]=='':
                    pygame.draw.circle(board, YELLOW, (current_x*CELL_SIZE+CELL_SIZE//2, (current_y-2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x][current_y-2]=True
            if current_x>=1 and "black" in pieces_position[current_x-1][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-1]=True
            if current_x<7 and "black" in pieces_position[current_x+1][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y-1]=True
        else:
            if current_y-1>=0 and pieces_position[current_x][current_y-1]=='':
                pygame.draw.circle(board, YELLOW, (current_x*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][current_y-1]=True
            if current_x>=1 and "black" in pieces_position[current_x-1][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-1]=True
            if current_x<7 and "black" in pieces_position[current_x+1][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y-1]=True
            if current_y==3:
                en_passant('white',current_x,current_y)
               
def check_rook(color,current_x,current_y):
    if color=='black':
        for i in range(current_x+1,8):
            if pieces_position[i][current_y]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y]=True
            #if we find a white piece we have to stop there as possible moves    
            elif 'white' in pieces_position[i][current_y]:
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y]=True
                break
            #if we find a black piece we stop
            else:
                break
        for i in range(current_x-1,-1,-1):
            if pieces_position[i][current_y]=='':
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2) 
                isYellow[i][current_y]=True
            elif 'white' in pieces_position[i][current_y]:
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y]=True
                break
            else:
                break
        for i in range(current_y+1,8):
            if pieces_position[current_x][i]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
            #if we find a white piece we have to stop there as possible moves    
            elif 'white' in pieces_position[current_x][i]:
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
                break
            #if we find a black piece we stop
            else:
                break
        for i in range(current_y-1,-1,-1):
            if pieces_position[current_x][i]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
            #if we find a white piece we have to stop there as possible moves    
            elif 'white' in pieces_position[current_x][i]:
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
                break
            #if we find a black piece we stop
            else:
                break
    else:
        for i in range(current_x+1,8):
            if pieces_position[i][current_y]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y]=True
            #if we find a white piece we have to stop there as possible moves    
            elif 'black' in pieces_position[i][current_y]:
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y]=True
                break
            #if we find a black piece we stop
            else:
                break
        for i in range(current_x-1,-1,-1):
            if pieces_position[i][current_y]=='':
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y]=True
            elif 'black' in pieces_position[i][current_y]:
                pygame.draw.circle(board, YELLOW, ((i*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y]=True
                break
            else:
                break
        for i in range(current_y+1,8):
            if pieces_position[current_x][i]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
            #if we find a white piece we have to stop there as possible moves    
            elif 'black' in pieces_position[current_x][i]:
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
                break
            #if we find a black piece we stop
            else:
                break
        for i in range(current_y-1,-1,-1):
            if pieces_position[current_x][i]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
            #if we find a white piece we have to stop there as possible moves    
            elif 'black' in pieces_position[current_x][i]:
                pygame.draw.circle(board, YELLOW, ((current_x*CELL_SIZE+CELL_SIZE//2, (i)*CELL_SIZE+CELL_SIZE//2)), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x][i]=True
                break
            #if we find a black piece we stop
            else:
                break   

def check_knight(color,current_x,current_y):
    #x+2, y+1/y-1
    #x-2, y+1/y-1
    #y+2 x+1/x-1
    #y-2 x+1/x-1
    
    #BLACK KNIGHT MANAGEMENT
    if color=='black':
        if current_x+2<=7:
            if current_y+1<=7 and 'black' not in pieces_position[current_x+2][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x+2)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+2][current_y+1]=True
            if current_y-1>=0 and 'black' not in pieces_position[current_x+2][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x+2)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+2][current_y-1]=True
        if current_x-2>=0:
            if current_y+1<=7 and 'black' not in pieces_position[current_x-2][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x-2)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-2][current_y+1]=True
            if current_y-1>=0 and 'black' not in pieces_position[current_x-2][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x-2)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-2][current_y-1]=True
        if current_y-2>=0:
            if current_x+1<=7 and 'black' not in pieces_position[current_x+1][current_y-2]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y-2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y-2]=True
            if current_x-1>=0 and 'black' not in pieces_position[current_x-1][current_y-2]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-2]=True
        if current_y+2<=7:
            if current_x+1<=7 and 'black' not in pieces_position[current_x+1][current_y+2]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y+2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y+2]=True
            if current_x-1>=0 and 'black' not in pieces_position[current_x-1][current_y+2]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y+2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y+2]=True
                
    #WHITE KNIGHT MANAGEMENT
    else:
        if current_x+2<=7:
            if current_y+1<=7 and 'white' not in pieces_position[current_x+2][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x+2)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+2][current_y+1]=True
            if current_y-1>=0 and 'white' not in pieces_position[current_x+2][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x+2)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+2][current_y-1]=True
        if current_x-2>=0:
            if current_y+1<=7 and 'white' not in pieces_position[current_x-2][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x-2)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-2][current_y+1]=True
            if current_y-1>=0 and 'white' not in pieces_position[current_x-2][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x-2)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-2][current_y-1]=True
        if current_y-2>=0:
            if current_x+1<=7 and 'white' not in pieces_position[current_x+1][current_y-2]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y-2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y-2]=True
            if current_x-1>=0 and 'white' not in pieces_position[current_x-1][current_y-2]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-2]=True
        if current_y+2<=7:
            if current_x+1<=7 and 'white' not in pieces_position[current_x+1][current_y+2]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y+2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y+2]=True
            if current_x-1>=0 and 'white' not in pieces_position[current_x-1][current_y+2]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y+2)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y+2]=True
    
def check_bishop(color,current_x,current_y):
    counter=1
    if color=='black':
        for i in range(current_x+1,8):
            if current_y+counter<=7 and pieces_position[i][current_y+counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y+counter<=7 and 'white' in pieces_position[i][current_y+counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1      
        counter=1
        for i in range(current_x-1,-1,-1):
            if current_y-counter>=0 and pieces_position[i][current_y-counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y-counter>=0 and 'white' in pieces_position[i][current_y-counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1 
        counter=1
        for i in range(current_x+1,8):    
            if current_y-counter>=0 and pieces_position[i][current_y-counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y+counter>=0 and 'white' in pieces_position[i][current_y-counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1     
        counter=1 
        for i in range(current_x-1,-1,-1):
            if current_y+counter<=7 and pieces_position[i][current_y+counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y+counter<=7 and 'white' in pieces_position[i][current_y+counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1      
    else:
        for i in range(current_x+1,8):
            if current_y+counter<=7 and pieces_position[i][current_y+counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y+counter<=7 and 'black' in pieces_position[i][current_y+counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1      
        counter=1
        for i in range(current_x-1,-1,-1):
            if current_y-counter>=0 and pieces_position[i][current_y-counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y-counter>=0 and 'black' in pieces_position[i][current_y-counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1 
        counter=1
        for i in range(current_x+1,8):    
            if current_y-counter>=0 and pieces_position[i][current_y-counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y+counter>=0 and 'black' in pieces_position[i][current_y-counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y-counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y-counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1     
        counter=1 
        for i in range(current_x-1,-1,-1):
            if current_y+counter<=7 and pieces_position[i][current_y+counter]=='':
                #until we find a piece we can proceed to move in that square
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
            #if we find a white piece we have to stop there as possible moves    
            elif current_y+counter<=7 and 'black' in pieces_position[i][current_y+counter]:
                pygame.draw.circle(board, YELLOW, ((i)*CELL_SIZE+CELL_SIZE//2, (current_y+counter)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[i][current_y+counter]=True
                break
            #if we find a white piece we stop
            else:
                break
            counter+=1
            
def check_queen(color,current_x,current_y):
    check_rook(color,current_x,current_y)
    check_bishop(color,current_x,current_y)
    
def check_king(color,current_x,current_y):
    #BLACK KING
    if color=='black':
        if short_castle('black'):
            pygame.draw.circle(board, YELLOW, (7*CELL_SIZE+CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
        if long_castle('black'):
            pygame.draw.circle(board, YELLOW, (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
        if current_x+1<=7:
            if 'black' not in pieces_position[current_x+1][current_y]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y]=True
            if current_y+1<=7: 
                if 'black' not in pieces_position[current_x+1][current_y+1]:
                    pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x+1][current_y+1]=True
                if 'black' not in pieces_position[current_x][current_y+1]:
                    pygame.draw.circle(board, YELLOW, ((current_x)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x][current_y+1]=True
            if current_y-1>=0: 
                if 'black' not in pieces_position[current_x+1][current_y-1]:
                    pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x+1][current_y-1]=True
                if 'black' not in pieces_position[current_x][current_y-1]:
                    pygame.draw.circle(board, YELLOW, ((current_x)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x][current_y-1]=True
        
        if current_x-1>=0:  
            if 'black' not in pieces_position[current_x-1][current_y]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y]=True
            if current_y+1<=7 and 'black' not in pieces_position[current_x-1][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y+1]=True
            if current_y-1>=0 and 'black' not in pieces_position[current_x-1][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-1]=True
    
    #WHITE KING
    else:
        if short_castle('white'):
            pygame.draw.circle(board, YELLOW, (7*CELL_SIZE+CELL_SIZE//2, 7*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
        if long_castle('white'):
            pygame.draw.circle(board, YELLOW, (CELL_SIZE//2, 7*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
        if current_x+1<=7:
            if 'white' not in pieces_position[current_x+1][current_y]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y]=True
            if current_y+1<=7: 
                if 'white' not in pieces_position[current_x+1][current_y+1]:
                    pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x+1][current_y+1]=True
                if 'white' not in pieces_position[current_x][current_y+1]:
                    pygame.draw.circle(board, YELLOW, ((current_x)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x][current_y+1]=True
            if current_y-1>=0: 
                if 'white' not in pieces_position[current_x+1][current_y-1]:
                    pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x+1][current_y-1]=True
                if 'white' not in pieces_position[current_x][current_y-1]:
                    pygame.draw.circle(board, YELLOW, ((current_x)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                    isYellow[current_x][current_y-1]=True
                    
        if current_x-1>=0:  
            if 'white' not in pieces_position[current_x-1][current_y]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y]=True
            if current_y+1<=7 and 'white' not in pieces_position[current_x-1][current_y+1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y+1]=True
            if current_y-1>=0 and 'white' not in pieces_position[current_x-1][current_y-1]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-1]=True
     
#ADD CONSTRAINT THAT WE CAN'T CASTLE IF UNDER ATTACK ON THAT CELL
def short_castle(color):
    if color=='black':
        if blackKingMoved==False and blackRookMoved1==False and pieces_position[5][0]=='' and pieces_position[6][0]=='' and pieces_position[7][0]=='black_rook_1':
            isYellow[7][0]=True
            return True   
    else:
        if whiteKingMoved==False and whiteRookMoved1==False and pieces_position[5][7]=='' and pieces_position[6][7]=='' and pieces_position[7][0]=='white_rook_1':
            isYellow[7][7]=True
            return True

def long_castle(color):
    if color=='black':
        if blackKingMoved==False and blackRookMoved0==False and pieces_position[1][0]=='' and pieces_position[2][0]=='' and pieces_position[3][0]=='' and pieces_position[0][0]=='black_rook_0':
            isYellow[0][0]=True
            return True
    else:
        if whiteKingMoved==False and whiteRookMoved0==False and pieces_position[1][7]=='' and pieces_position[2][7]=='' and pieces_position[3][7]=='' and pieces_position[0][7]=='white_rook_0':
            isYellow[0][7]=True
            return True
    
def en_passant(color,current_x,current_y):
    print(BlackEnPassantPossible)
    if color=='black' and BlackEnPassantPossible[0]:
        if 'white_pawn' in pieces_position[current_x-1][current_y]:
            pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
            isYellow[current_x-1][current_y+1]=True
        elif 'white_pawn' in pieces_position[current_x+1][current_y]:
            pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y+1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
            isYellow[current_x+1][current_y+1]=True
    else:
        if color=='white' and WhiteEnPassantPossible[0]:
            if 'black_pawn' in pieces_position[current_x-1][current_y]:
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-1]=True
            elif 'black_pawn' in pieces_position[current_x+1][current_y]:
                pygame.draw.circle(board, YELLOW, ((current_x+1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x+1][current_y-1]=True
    
def promotion(color,piece,pos):
    global promotionCheck,capture_sound,move_sound
    capture=False
    if color=='black':
        pieces_position[black_pieces[piece].x//CELL_SIZE][black_pieces[piece].y//CELL_SIZE]=''
        black_pieces[piece].x=pos[0]*CELL_SIZE
        black_pieces[piece].y=pos[1]*CELL_SIZE
        #print(pieces_position[pos[0]][pos[1]])
        if 'white' in pieces_position[pos[0]][pos[1]]:
            white_pieces.pop(pieces_position[pos[0]][pos[1]])
            capture_sound.play()
            capture=True
        if not capture:
            move_sound.play()
        redrawChessboard()
        redrawTimer(font,white_text,black_text,SURREND_WHITE_BUTTON,SURREND_BLACK_BUTTON)
        # print(white_pieces,pos[0],pos[1],(pos[1]-1)*CELL_SIZE,(pos[1]-2)*CELL_SIZE)
        #print(black_queen,pos[0]*CELL_SIZE,(pos[1]-1)*CELL_SIZE)
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]-1)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]-2)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]-3)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]-4)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        WIN.blit(board,board.get_rect())
        draw_piecesBeforePromotion(color,pos)
        draw_promotionPieces(color,pos)
        pygame.display.update()
        promotionCheck=True
        waitingForPromotion(color,piece,pos[0],pos[1]-1,pos[1]-2,pos[1]-3,pos[1]-4)
        redrawChessboard()
        #redrawTimer(font,white_text,black_text)
        draw_updatedPieces()
        
    else:
        pieces_position[white_pieces[piece].x//CELL_SIZE][white_pieces[piece].y//CELL_SIZE]=''
        white_pieces[piece].x=pos[0]*CELL_SIZE
        white_pieces[piece].y=pos[1]*CELL_SIZE
        if 'black' in pieces_position[pos[0]][pos[1]]:
            black_pieces.pop(pieces_position[pos[0]][pos[1]])
            capture_sound.play()
            capture=True
        if not capture:
            move_sound.play()
        redrawChessboard()
        redrawTimer(font,white_text,black_text,SURREND_WHITE_BUTTON,SURREND_BLACK_BUTTON)
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]+1)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]+2)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]+3)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(board, GREY, (pos[0]*CELL_SIZE,(pos[1]+4)*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        WIN.blit(board,board.get_rect())
        draw_piecesBeforePromotion(color,pos)
        draw_promotionPieces(color,pos)
        pygame.display.update()
        promotionCheck=True
        waitingForPromotion(color,piece,pos[0],pos[1]+1,pos[1]+2,pos[1]+3,pos[1]+4)
        redrawChessboard()
        #redrawTimer(font,white_text,black_text)
        draw_updatedPieces()
       
       
def waitingForPromotion(color,piece,pos_x,pos_y1,pos_y2,pos_y3,pos_y4):
    global numberPromotedPiece
    global promotionCheck
    running=True
    print("Zio pera pereira")
    while running:
        for event in pygame.event.get():
            if color=='black':
                if event.type == pygame.MOUSEBUTTONUP:
                    current_x,current_y=pygame.mouse.get_pos()
                    current_squareX=current_x//CELL_SIZE
                    current_squareY=current_y//CELL_SIZE
                    if current_squareX==pos_x and current_squareY==pos_y1:
                        newPieceName='black_queen_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1+1]=newPieceName
                        black_pieces[newPieceName]=black_pieces[piece]
                        del black_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
                    elif current_squareX==pos_x and current_squareY==pos_y2:
                        newPieceName='black_rook_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1+1]=newPieceName
                        black_pieces[newPieceName]=black_pieces[piece]
                        del black_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
                    elif current_squareX==pos_x and current_squareY==pos_y3:
                        newPieceName='black_bishop_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1+1]=newPieceName
                        black_pieces[newPieceName]=black_pieces[piece]
                        del black_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
                    elif current_squareX==pos_x and current_squareY==pos_y4:
                        newPieceName='black_knight_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1+1]=newPieceName
                        black_pieces[newPieceName]=black_pieces[piece]
                        del black_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    current_x,current_y=pygame.mouse.get_pos()
                    current_squareX=current_x//CELL_SIZE
                    current_squareY=current_y//CELL_SIZE
                    if current_squareX==pos_x and current_squareY==pos_y1:
                        newPieceName='white_queen_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1-1]=newPieceName
                        white_pieces[newPieceName]=white_pieces[piece]
                        del white_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
                    elif current_squareX==pos_x and current_squareY==pos_y2:
                        newPieceName='white_rook_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1-1]=newPieceName
                        white_pieces[newPieceName]=white_pieces[piece]
                        del white_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
                    elif current_squareX==pos_x and current_squareY==pos_y3:
                        newPieceName='white_bishop_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1-1]=newPieceName
                        white_pieces[newPieceName]=white_pieces[piece]
                        del white_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
                    elif current_squareX==pos_x and current_squareY==pos_y4:
                        newPieceName='white_knight_'+str(numberPromotedPiece)
                        pieces_position[pos_x][pos_y1-1]=newPieceName
                        white_pieces[newPieceName]=white_pieces[piece]
                        del white_pieces[piece]
                        numberPromotedPiece+=1
                        running=False
    promotionCheck=False            
    print(pieces_position)
    
def draw():
    if len(black_pieces)==1 and len(white_pieces)==1:
        return True
  
def confirmedDraw():
    #delete positions in the winning screen
    for i in range(2,6):
        for j in range(3,5):
            pieces_position[i][j]=''
            
    #redraw pieces that are not in the winning rectangle
    for key in black_pieces:
        ignoreNums=key.split('_')
        newKey=ignoreNums[0]+'_'+ignoreNums[1]
        if black_pieces[key].x//CELL_SIZE>=2 and black_pieces[key].x//CELL_SIZE<=5 and black_pieces[key].y//CELL_SIZE>=3 and black_pieces[key].y//CELL_SIZE<=4:
            continue
        else:    
            WIN.blit(BLACK_PIECES_IMGS[newKey],(black_pieces[key].x,black_pieces[key].y))

    for key in white_pieces:
        ignoreNums=key.split('_')
        newKey=ignoreNums[0]+'_'+ignoreNums[1]
        if white_pieces[key].x//CELL_SIZE>=2 and white_pieces[key].x//CELL_SIZE<=5 and white_pieces[key].y//CELL_SIZE>=3 and white_pieces[key].y//CELL_SIZE<=4:
            continue
        else:    
            WIN.blit(WHITE_PIECES_IMGS[newKey],(white_pieces[key].x,white_pieces[key].y))

    # PLAY_WHITE_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=(GRID_SIZE//2, 250), 
    #                         text_input=color.capitalize()+" WON!", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
    while True:
        MENU_TEXT = get_font(50).render("DRAW!", True, "#000080")
        MENU_RECT = MENU_TEXT.get_rect(center=(GRID_SIZE//2, 300))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        QUIT_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=(GRID_SIZE//2, 400), 
                                text_input="MAIN MENU", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        
        WIN.blit(MENU_TEXT,MENU_RECT)
        
        for button in [QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()   
          
def gameOver(color):
    #draw winning rectangle
    #pygame.draw.rect(board,YELLOW,(2*CELL_SIZE,3*CELL_SIZE,4*CELL_SIZE,2*CELL_SIZE))
    
    #delete positions in the winning screen
    for i in range(2,6):
        for j in range(3,5):
            pieces_position[i][j]=''
            
    #redraw pieces that are not in the winning rectangle
    for key in black_pieces:
            ignoreNums=key.split('_')
            newKey=ignoreNums[0]+'_'+ignoreNums[1]
            if black_pieces[key].x//CELL_SIZE>=2 and black_pieces[key].x//CELL_SIZE<=5 and black_pieces[key].y//CELL_SIZE>=3 and black_pieces[key].y//CELL_SIZE<=4:
                continue
            else:    
                WIN.blit(BLACK_PIECES_IMGS[newKey],(black_pieces[key].x,black_pieces[key].y))

    for key in white_pieces:
        ignoreNums=key.split('_')
        newKey=ignoreNums[0]+'_'+ignoreNums[1]
        if white_pieces[key].x//CELL_SIZE>=2 and white_pieces[key].x//CELL_SIZE<=5 and white_pieces[key].y//CELL_SIZE>=3 and white_pieces[key].y//CELL_SIZE<=4:
            continue
        else:    
            WIN.blit(WHITE_PIECES_IMGS[newKey],(white_pieces[key].x,white_pieces[key].y))

    # PLAY_WHITE_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=(GRID_SIZE//2, 250), 
    #                         text_input=color.capitalize()+" WON!", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
    while True:
        MENU_TEXT = get_font(50).render(color.capitalize()+" WON!", True, "#000080")
        MENU_RECT = MENU_TEXT.get_rect(center=(GRID_SIZE//2, 300))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        QUIT_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=(GRID_SIZE//2, 400), 
                                text_input="MAIN MENU", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        
        WIN.blit(MENU_TEXT,MENU_RECT)
        
        for button in [QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(WIN)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def redrawTimer(font,white_text,black_text,white_surrend,black_surrend):
    pygame.draw.rect(board,(0,0,0),(CELL_SIZE*8,0,10,CELL_SIZE*8))
    pygame.draw.rect(board,'#DE3163',(CELL_SIZE*8+10,0,90,CELL_SIZE*8))
    pygame.draw.rect(board,	'#702963',(CELL_SIZE*8+10,CELL_SIZE,90,CELL_SIZE*6))
    WIN.blit(board,board.get_rect())
    WIN.blit(font.render(white_text, True, (0, 0, 0)), (775, 700))
    WIN.blit(font.render(black_text, True, (0, 0, 0)), (775, 35))
    white_surrend.update(WIN)
    black_surrend.update(WIN)

#variables
def main_white():
    running = True
    clock = pygame.time.Clock()
    
    global white_counter,black_counter,white_text,black_text,font,SURREND_WHITE_BUTTON,SURREND_BLACK_BUTTON
    global background_music,winning_sound
    
    
    background_music.stop()
    #creates an event every second so that timer gets decreased every time
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    global WhiteEnPassantPossible
    global BlackEnPassantPossible

    #TURNS! white starts ofc
    currentTurn='white'
    #pieces creation
    white_pieces_creation()
    #drawing chessboard first time
    draw_window_white(True)
    WIN.blit(font.render(white_text, True, (0, 0, 0)), (775, 700))
    WIN.blit(font.render(black_text, True, (0, 0, 0)), (775, 35))
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():

            #Timer!
            if draw():
               confirmedDraw()
               winning_sound.play()
                
            if event.type == pygame.USEREVENT and currentTurn=='white': 
                white_counter -= 1
                numOfMinutes=white_counter//60
                numOfSeconds=white_counter%60
                if numOfMinutes<10:
                    if numOfSeconds<10:
                        white_text = ('0'+str(numOfMinutes)+':'+'0'+str(numOfSeconds)).rjust(3) if white_counter > 0 else gameOver('black')
                    else:
                        white_text = ('0'+str(numOfMinutes)+':'+str(numOfSeconds)).rjust(3) if white_counter > 0 else gameOver('black')
                else:
                    if numOfSeconds<10:
                        white_text = (str(numOfMinutes)+':'+'0'+str(numOfSeconds)).rjust(3) if white_counter > 0 else gameOver('black')
                    else:
                        white_text = (str(numOfMinutes)+':'+str(numOfSeconds)).rjust(3) if white_counter > 0 else gameOver('black')
                
            elif event.type == pygame.USEREVENT and currentTurn=='black':
                black_counter -= 1
                numOfMinutes=black_counter//60
                numOfSeconds=black_counter%60
                if numOfMinutes<10:
                    if numOfSeconds<10:
                        black_text = ('0'+str(numOfMinutes)+':'+'0'+str(numOfSeconds)) if black_counter > 0 else gameOver('white')
                    else:
                        black_text = ('0'+str(numOfMinutes)+':'+str(numOfSeconds)) if black_counter > 0 else gameOver('white')
                else:
                    if numOfSeconds<10:
                        black_text = (str(numOfMinutes)+':'+'0'+str(numOfSeconds)) if black_counter > 0 else gameOver('white')
                    else:
                        black_text = (str(numOfMinutes)+':'+str(numOfSeconds)) if black_counter > 0 else gameOver('white')
                
            redrawTimer(font,white_text,black_text,SURREND_WHITE_BUTTON,SURREND_BLACK_BUTTON)
            #DECLARE VICTORY OF ONE SIDE!                
            if 'black_king' not in black_pieces:
                winning_sound.play()
                gameOver('white')
            if 'white_king' not in white_pieces:
                winning_sound.play()
                gameOver('black')
                
            #close game
            if event.type == pygame.QUIT:
                    running = False
                    
                    
            #When mouse is pushed
            if event.type == pygame.MOUSEBUTTONUP:
                current_x,current_y=pygame.mouse.get_pos()
                current_squareX=current_x//CELL_SIZE
                current_squareY=current_y//CELL_SIZE
                if SURREND_WHITE_BUTTON.checkForInput((current_x,current_y)):
                    winning_sound.play()
                    gameOver('black')
                if SURREND_BLACK_BUTTON.checkForInput((current_x,current_y)):
                    winning_sound.play()
                    gameOver('white')
                if current_squareX<8:
                    if isYellow[current_squareX][current_squareY]==True:
                        currentTurn=movePieces(current_piece,(current_squareX,current_squareY),currentTurn)
                        deleteLastPossibleMoves()
                    elif pieces_position[current_squareX][current_squareY]!='' and currentTurn in pieces_position[current_squareX][current_squareY]: 
                        deleteLastPossibleMoves()
                        current_piece=changeBoxColor(current_squareX,current_squareY)
                    #print(current_piece)
                
                
            pygame.display.update()
        #draw_window_white(starting_position=False)
        
    pygame.quit()
    

def options():
    global button_sound
    while True:
        WIN.blit(BG, (0, 0))

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_TEXT = get_font(50).render("SET GAME TIMER", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=((GRID_SIZE//2)+50, 100))

        OPTION_RECT=pygame.transform.scale(
            pygame.image.load("chess_bot/assets/Quit Rect.png"),(200,100))
        
        TIME1_BUTTON = Button(image=OPTION_RECT, pos=(200, 250), 
                            text_input="1 MIN", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        TIME2_BUTTON = Button(image=OPTION_RECT, pos=(420, 250), 
                            text_input="3 MIN", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        TIME3_BUTTON = Button(image=OPTION_RECT, pos=(640, 250), 
                            text_input="5 MIN", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        TIME4_BUTTON = Button(image=OPTION_RECT, pos=(200, 400), 
                            text_input="10 MIN", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        TIME5_BUTTON = Button(image=OPTION_RECT, pos=(420, 400), 
                            text_input="15 MIN", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        TIME6_BUTTON = Button(image=OPTION_RECT, pos=(640, 400), 
                            text_input="30 MIN", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        QUIT_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=((GRID_SIZE)//2+50, 550), 
                            text_input="RETURN TO MENU", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)

        # CURRENT_HIGLIGHT_BUTTON=TIME4_BUTTON
        # CURRENT_BUTTON_TO_CHANGE=''
        # changeFlag=False
        
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        for button in [TIME1_BUTTON,TIME2_BUTTON,TIME3_BUTTON,TIME4_BUTTON,TIME5_BUTTON,TIME6_BUTTON,QUIT_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TIME1_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    changeTime(0)
                    
                    # CURRENT_BUTTON_TO_CHANGE=TIME1_BUTTON
                    # print(TIME1_BUTTON.base_color)
                    # changeFlag=True
                if TIME2_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    changeTime(1)
                if TIME3_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    changeTime(2)     
                if TIME4_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    changeTime(3)
                if TIME5_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    changeTime(4)
                if TIME6_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    changeTime(5)
                    
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    button_sound.play()
                    main_menu()
                    
        # if changeFlag:     
        #     CURRENT_BUTTON_TO_CHANGE.changeColorPermanently(YELLOW)
        #     CURRENT_BUTTON_TO_CHANGE.update(WIN)
        #     CURRENT_HIGLIGHT_BUTTON.changeColorPermanently("#d7fcd4")
        #     CURRENT_HIGLIGHT_BUTTON.update(WIN)
        #     CURRENT_HIGLIGHT_BUTTON=CURRENT_BUTTON_TO_CHANGE
        #     changeFlag=not changeFlag
        #     print(CURRENT_BUTTON_TO_CHANGE.base_color)
        
        pygame.display.update()


def main_menu():
    
    global startingGreen,startingPieces,isGreen,pieces_position,isYellow,lastSelectedNum,background_music,button_sound

    global black_pieces,white_pieces
    #music
    if background_music.get_num_channels()==0:
        background_music.play(-1)   
        
        
    isGreen=[]
    isYellow=[]
    pieces_position=[]
    for i in range(8):
        isGreen.append(startingGreen*1)
        isYellow.append(startingGreen*1)
        pieces_position.append(startingPieces*1)
    black_pieces={}
    white_pieces={}
    changeTime(lastSelectedNum)
    while True:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=((GRID_SIZE//2)+50, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=((GRID_SIZE//2)+50, 250), 
                            text_input="PLAY", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        OPTIONS_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=((GRID_SIZE//2)+50, 400), 
                            text_input="OPTIONS", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
        QUIT_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Quit Rect.png"), pos=((GRID_SIZE//2)+50, 550), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    main_white()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# def play_menu():
#     while True:
#         WIN.blit(BG, (0, 0))

#         PLAY_MOUSE_POS = pygame.mouse.get_pos()

#         PLAY_TEXT = get_font(50).render("PLAY MENU", True, "#b68f40")
#         PLAY_RECT = PLAY_TEXT.get_rect(center=((GRID_SIZE//2)+50, 100))

#         PLAY_WHITE_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=((GRID_SIZE//2)+50, 250), 
#                             text_input="PLAY WHITE", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
#         PLAY_BLACK_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=((GRID_SIZE//2)+50, 400), 
#                             text_input="PLAY BLACK", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)
#         QUIT_BUTTON = Button(image=pygame.image.load("chess_bot/assets/Play Rect.png"), pos=((GRID_SIZE//2)+50, 550), 
#                             text_input="RETURN TO MENU", font=get_font(20), base_color="#d7fcd4", hovering_color=YELLOW)

#         WIN.blit(PLAY_TEXT, PLAY_RECT)

#         for button in [PLAY_WHITE_BUTTON, PLAY_BLACK_BUTTON, QUIT_BUTTON]:
#             button.changeColor(PLAY_MOUSE_POS)
#             button.update(WIN)
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if PLAY_WHITE_BUTTON.checkForInput(PLAY_MOUSE_POS):
#                     main_white()
#                 if PLAY_BLACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
#                     main_black()
#                 if QUIT_BUTTON.checkForInput(PLAY_MOUSE_POS):
#                     main_menu()

#         pygame.display.update()

def changeTime(num):
    global white_counter,black_counter,white_text,black_text,lastSelectedNum
    white_counter=timers[num]
    black_counter=timers[num]
    white_text=texts[num]
    black_text=texts[num]
    lastSelectedNum=num

if __name__ == "__main__":
    main_menu()
    