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
RED=(136,8,8)
YELLOW=(236,234,152)
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


board=pygame.Surface((CELL_SIZE*8,CELL_SIZE*8))
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

#handles the deletion of multiple red squares, we have at most once 
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

#TO DO!
#once a yellow square is touched, we need to move the pieces
#update positions and remove eaten ones
def movePieces(piece,pos,currentTurn):
    if currentTurn=='white':
        currentTurn='black'
    else:
        currentTurn='white'
    current_piece=pieces_position[pos[0]][pos[1]]
    print(piece,current_piece)
    if 'black' in piece:
        if 'king' in piece:
            #long castle
            if 'black_rook_0' in current_piece:
                pieces_position[black_pieces[piece].x//CELL_SIZE][black_pieces[piece].y//CELL_SIZE]=''
                #updating black pieces to draw figures
                black_pieces['black_rook_0'].x=3*CELL_SIZE
                black_pieces[piece].x=2*CELL_SIZE
                #updating grid to check for future movements
                pieces_position[2][0]=piece
                pieces_position[3][0]='black_rook_0'
                
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
                pieces_position[6][0]=piece
                pieces_position[5][0]='black_rook_1'
                
                #To ensure castle can't be used again
                blackRookMoved0=True
                blackRookMoved1=True
                blackKingMoved=True
        #normalize new position as the starting of the square
        # print(pos[0],pos[1])
        # print((pos[0]//8*8),(pos[1]//8)*8)
        else:
            if current_piece=='black_rook_0':
                blackRookMoved0=True
            elif current_piece=='black_rook_1':
                blackRookMoved1=True
            #NEED TO REDRAW EACH PIECE IN NEW POSITION!!
            if 'white' in current_piece:
                white_pieces.pop(current_piece)
            pieces_position[black_pieces[piece].x//CELL_SIZE][black_pieces[piece].y//CELL_SIZE]=''
            black_pieces[piece].x=pos[0]*CELL_SIZE
            black_pieces[piece].y=pos[1]*CELL_SIZE
            pieces_position[pos[0]][pos[1]]=piece
        
        #draw_updatedPieces()
        #WIN.blit(BLACK_PIECES_IMGS[newKey],(black_pieces[piece].x,black_pieces[piece].y))
        
    else:
        if 'king' in piece:
            #long castle
            if 'white_rook_0' in current_piece:
                pieces_position[white_pieces[piece].x//CELL_SIZE][white_pieces[piece].y//CELL_SIZE]=''
                #updating black pieces to draw figures
                white_pieces['white_rook_0'].x=3*CELL_SIZE
                white_pieces[piece].x=2*CELL_SIZE
                #updating grid to check for future movements
                pieces_position[2][7]=piece
                pieces_position[3][7]='white_rook_0'
                
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
                pieces_position[6][7]=piece
                pieces_position[5][7]='white_rook_1'
                
                #To ensure castle can't be used again
                whiteRookMoved0=True
                whiteRookMoved1=True
                whiteKingMoved=True
                
        else:
            if current_piece=='white_rook_0':
                whiteRookMoved0=True
            elif current_piece=='white_rook_1':
                whiteRookMoved1=True
            if 'black' in current_piece:
                black_pieces.pop(current_piece)
            pieces_position[white_pieces[piece].x//CELL_SIZE][white_pieces[piece].y//CELL_SIZE]=''
            white_pieces[piece].x=pos[0]*CELL_SIZE
            white_pieces[piece].y=pos[1]*CELL_SIZE
            pieces_position[pos[0]][pos[1]]=piece
    redrawChessboard()
    draw_updatedPieces()
    return currentTurn
    
#Changes the color of the box to red if we want to move a piece
def changeBoxColor(current_squareX,current_squareY):
    print(current_squareX,current_squareY)
    #If we already have a RED square we have to remove it
    redrawChessboard()
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
                pygame.draw.circle(board, YELLOW, ((current_x-1)*CELL_SIZE+CELL_SIZE//2, (current_y-1)*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3, 3*CELL_SIZE//2)
                isYellow[current_x-1][current_y-1]=True
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
            elif current_y-counter>=0 and 'white' in pieces_position[i][current_y]:
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
            elif current_y-counter>=0 and 'black' in pieces_position[i][current_y]:
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
        if blackKingMoved==False and blackRookMoved1==False and pieces_position[5][0]=='' and pieces_position[6][0]=='':
            isYellow[7][0]=True
            return True   
    else:
        if whiteKingMoved==False and whiteRookMoved1==False and pieces_position[5][7]=='' and pieces_position[6][7]=='':
            isYellow[7][7]=True
            return True

def long_castle(color):
    if color=='black':
        if blackKingMoved==False and blackRookMoved0==False and pieces_position[1][0]=='' and pieces_position[2][0]=='' and pieces_position[3][0]=='':
            isYellow[0][0]=True
            return True
    else:
        if whiteKingMoved==False and whiteRookMoved0==False and pieces_position[1][7]=='' and pieces_position[2][7]=='' and pieces_position[3][7]=='':
            isYellow[0][7]=True
            return True
    
    
def draw_window_black(starting_position):
    #fill the background with a different color and update it
    #WIN.fill(WHITE)
    if starting_position:
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

    #TURNS! white starts ofc
    currentTurn='white'
    #pieces creation
    white_pieces_creation()
    #drawing chessboard first time
    draw_window_white(True)
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            #When mouse is pushed
            if event.type == pygame.MOUSEBUTTONUP:
                current_x,current_y=pygame.mouse.get_pos()
                current_squareX=current_x//CELL_SIZE
                current_squareY=current_y//CELL_SIZE
                if isYellow[current_squareX][current_squareY]==True:
                    currentTurn=movePieces(current_piece,(current_squareX,current_squareY),currentTurn)
                    deleteLastPossibleMoves()
                if pieces_position[current_squareX][current_squareY]!='' and currentTurn in pieces_position[current_squareX][current_squareY]: 
                    deleteLastPossibleMoves()
                    current_piece=changeBoxColor(current_squareX,current_squareY)
                    #print(current_piece)
                
                
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
    