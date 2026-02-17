import pygame
import utils
from collections import defaultdict

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
        self.turn = 0
        self.last_eaten = 0
        # state of the board
        self.board_signatures = defaultdict(int)
        # used for board signature
        self.en_passant_target = None
        # check if pawn is getting promoted
        self.pawn_promotion = None
        self.anim = None
        
    def get_piece_pos(self, piece):
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] == piece:
                    return (i, j)
    
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
        
    def square_to_pixel(self, row, col):
        """
        Board coords -> top-left pixel coords, rispettando flip e border.
        """
        r, c = self.board_to_screen(row, col)
        x = c * self.tile_size
        y = self.border + r * self.tile_size
        return x, y


    def get_all_pieces(self, color):
        """
        Get all pieces of a certain color.
        
        Returns piece and piece_pos
        """
        pieces = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] != 0 and self.grid[row][col].is_white == color:
                    pieces.append((self.grid[row][col], (row, col)))
        
        return pieces
        
    def draw(self, screen, color, legal_moves, in_promotion, selected_square = None):
        self.draw_chessboard(screen, color)
        if not in_promotion:
            if selected_square:
                r, c = selected_square
                r, c = self.board_to_screen(r, c)
                rect = pygame.Rect(
                    c * self.tile_size,
                    self.border + r * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(screen, (112, 41, 99), rect)
            if self.last_move:
                sr, sc = self.last_move["from"]
                er, ec = self.last_move["to"]
                sr, sc = self.board_to_screen(sr, sc)
                er, ec = self.board_to_screen(er, ec)
                rect = pygame.Rect(sc * self.tile_size,
                                   self.border + sr * self.tile_size,
                                   self.tile_size, self.tile_size)
                pygame.draw.rect(screen, (128, 0, 128), rect)
                rect = pygame.Rect(ec * self.tile_size,
                                   self.border + er * self.tile_size,
                                   self.tile_size, self.tile_size)
                pygame.draw.rect(screen, (207, 159, 255), rect)
                
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
            self.tile_size // 2 - 15)
            
    def draw_pieces(self, screen):
        anim_piece = None
        anim_to = None

        if self.anim:
            anim_piece = self.anim["piece"]
            anim_to = self.anim["to"]

        # draw all pieces except the animated one at destination square
        for i in range(8):
            for j in range(8):
                piece = self.grid[i][j]
                if piece != 0:
                    if self.anim and piece is anim_piece and (i, j) == anim_to:
                        continue  # lo disegniamo dopo, in interpolazione
                    r, c = self.board_to_screen(i, j)
                    piece.draw(screen, self.tile_size, self.border, (r, c))

        # draw animated piece on top
        if self.anim:
            t = self.anim["t"] / self.anim["duration"]
            if t < 0: t = 0
            if t > 1: t = 1

            sx, sy = self.anim["start_px"]
            ex, ey = self.anim["end_px"]

            x = sx + (ex - sx) * t
            y = sy + (ey - sy) * t

            screen.blit(self.anim["piece"].sprite, (x, y))
  
    def generate_promotion_pieces(self, spritesheet, scale):
        promo_sprites = {
            True: {  # white
                "Q": Queen(spritesheet, scale, True),
                "R": Rook(spritesheet, scale, True),
                "B": Bishop(spritesheet, scale, True),
                "K": Knight(spritesheet, scale, True),
            },
            False: { # black
                "Q": Queen(spritesheet, scale, False),
                "R": Rook(spritesheet, scale, False),
                "B": Bishop(spritesheet, scale, False),
                "K": Knight(spritesheet, scale, False),
            },
        }
        
        return promo_sprites
    
    def promote_pawn(self, pos, chosen_key, is_white, spritesheet, scale):
        r, c = pos

        if chosen_key == "Q":
            self.grid[r][c] = Queen(spritesheet, scale, is_white)
        elif chosen_key == "R":
            self.grid[r][c] = Rook(spritesheet, scale, is_white)
        elif chosen_key == "B":
            self.grid[r][c] = Bishop(spritesheet, scale, is_white)
        else:
            self.grid[r][c] = Knight(spritesheet, scale, is_white)

    def iter_legal_moves(self, color_is_white):
        """
        Returns all of the tuples of the possible moves of the pieces.
        """
        pieces = self.get_all_pieces(color_is_white)
        final_moves = []
        for piece, pos in pieces:
            moves = piece.get_legal_moves(pos, self)
            if moves:
                # append also the piece so we know what to move
                final_moves.append((piece, pos, moves))
        
        return final_moves
    
    def iter_pseudo_moves(self, color_is_white):
        pieces = self.get_all_pieces(color_is_white)
        out = []
        for piece, pos in pieces:
            moves = piece.get_pseudo_legal_moves(pos, self)
            if moves:
                out.append((piece, tuple(pos), moves))
        return out

    def is_empty(self, row, col):
        # empty space
        return self.grid[row][col] == 0

    def is_enemy(self, row, col, is_white):
        if self.is_empty(row, col):
            return False
        # if is_white is not == to current is_white we have an enemy
        return self.grid[row][col].is_white != is_white
    
    def move_piece(self, piece, from_pos, to_pos, record_undo=False):
        """
            Args:
                - piece (ChessPiece): piece we want to move
                - from_pos (tuple): starting position
                - to_pos (tuple): ending position
                
            Returns a way to undo the move, checks also special conditions
            such as castle, en passant and also updates current turn
            and last time something was eaten.
        """
        s_row, s_col = from_pos
        e_row, e_col = to_pos

        has_eaten = False
        prev_pawn_promotion = self.pawn_promotion
        self.pawn_promotion = None

        captured = self.grid[e_row][e_col]

        # --- UNDO RECORD ---
        undo = None
        if record_undo:
            undo = {
                "from": from_pos,
                "to": to_pos,
                "piece": piece,
                "captured": captured,
                "last_move": self.last_move,
                "turn": self.turn,
                "last_eaten": self.last_eaten,
                "en_passant_target": self.en_passant_target,
                "pawn_promotion": prev_pawn_promotion,
                # ripristino flag pezzo
                "piece_first_move": getattr(piece, "first_move", None),
                "piece_castle": getattr(piece, "castle", None),
                # per mosse speciali
                "en_passant_capture": None,  # (r,c,captured_piece)
                "castle_rook": None,         # (r_from,c_from,r_to,c_to, rook, rook_castle_prev)
            }

        # --- EN PASSANT ---
        if isinstance(piece, Pawn):
            if s_col != e_col and self.is_empty(e_row, e_col):
                # pawn catturato sta su (s_row, e_col)
                ep_captured = self.grid[s_row][e_col]
                if record_undo:
                    undo["en_passant_capture"] = (s_row, e_col, ep_captured)
                self.grid[s_row][e_col] = 0
                has_eaten = True
                self.en_passant_target = ()

        # --- CASTLE ---
        if isinstance(piece, King) and abs(e_col - s_col) == 2:
            if e_col == 6:  # short
                rook = self.grid[s_row][7]
                if record_undo:
                    undo["castle_rook"] = (s_row, 7, s_row, 5, rook, rook.castle)
                self.grid[s_row][5] = rook
                self.grid[s_row][7] = 0
                rook.castle = False

            elif e_col == 2:  # long
                rook = self.grid[s_row][0]
                if record_undo:
                    undo["castle_rook"] = (s_row, 0, s_row, 3, rook, rook.castle)
                self.grid[s_row][3] = rook
                self.grid[s_row][0] = 0
                rook.castle = False

        # --- CAPTURE NORMAL ---
        if self.grid[e_row][e_col] != 0:
            has_eaten = True

        # --- MOVE PIECE ---
        self.grid[e_row][e_col] = piece
        self.grid[s_row][s_col] = 0

        # --- PROMOTION CHECK ---
        if isinstance(piece, Pawn):
            piece.first_move = False
            last_rank = 0 if piece.is_white else 7
            if e_row == last_rank:
                self.pawn_promotion = (e_row, e_col, piece.is_white)

        # --- UPDATE CASTLING FLAGS ---
        if isinstance(piece, Rook):
            piece.castle = False
        if isinstance(piece, King):
            piece.castle = False

        # --- LAST MOVE ---
        self.last_move = {
            "piece": piece,
            "from": from_pos,
            "to": to_pos,
            "eaten": has_eaten,
            "double_step": isinstance(piece, Pawn) and abs(from_pos[0] - to_pos[0]) == 2
        }

        # --- TURN ---
        if has_eaten:
            self.last_eaten = self.turn
        self.turn += 1

        # --- START ANIMATION (render-only) ---
        if not record_undo:
            duration = 0.2  # seconds
            sx, sy = self.square_to_pixel(s_row, s_col)
            ex, ey = self.square_to_pixel(e_row, e_col)

            self.anim = {
                "piece": piece,
                "from": (s_row, s_col),
                "to": (e_row, e_col),
                "start_px": (sx, sy),
                "end_px": (ex, ey),
                "t": 0.0,
                "duration": duration,
            }

        return undo

    def update_animation(self, dt):
        if not self.anim:
            return
        self.anim["t"] += dt
        if self.anim["t"] >= self.anim["duration"]:
            self.anim = None

    def undo_move(self, undo):
        fr, fc = undo["from"]
        tr, tc = undo["to"]
        piece = undo["piece"]

        # ripristina pezzi base
        self.grid[fr][fc] = piece
        self.grid[tr][tc] = undo["captured"]

        # ripristina en passant capture
        if undo["en_passant_capture"] is not None:
            r, c, cap = undo["en_passant_capture"]
            self.grid[r][c] = cap

        # ripristina castle rook
        if undo["castle_rook"] is not None:
            r_from, c_from, r_to, c_to, rook, rook_castle_prev = undo["castle_rook"]
            self.grid[r_from][c_from] = rook
            self.grid[r_to][c_to] = 0
            rook.castle = rook_castle_prev

        # ripristina flag del pezzo mosso
        if undo["piece_first_move"] is not None:
            piece.first_move = undo["piece_first_move"]
        if undo["piece_castle"] is not None:
            piece.castle = undo["piece_castle"]

        # ripristina stato globale
        self.last_move = undo["last_move"]
        self.turn = undo["turn"]
        self.last_eaten = undo["last_eaten"]
        self.en_passant_target = undo["en_passant_target"]
        self.pawn_promotion = undo["pawn_promotion"]

    def get_king_square(self, is_white):
        for row in range(8):
            for col in range(8):
                if isinstance(self.grid[row][col], King) and self.grid[row][col].is_white == is_white: 
                    return (row, col)
                
    def can_en_passant(self, pos, direction):
        if not self.last_move:
            return None
        
        lm = self.last_move
        
        if not lm["double_step"]:
            return None
        
        # same row
        if (lm["to"][0] - pos[0]) == 0:
            # check if they are adjacent
            # enemy pawn on the left
            if abs(pos[1] - lm["to"][1]) == 1:
                return (pos[0]+direction,lm["to"][1]) 
                
        return None
        
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
            return False, None

        if not king.castle or not rook.castle:
            return False, None

        if (not self.is_empty(row, 5)) or (not self.is_empty(row, 6)):
            return False, None

        # king is in check or other square are attacked
        if self.is_square_attacked((row, col), enemy_pieces):
            return False, None
        if self.is_square_attacked((row, 5), enemy_pieces) or self.is_square_attacked((row, 6), enemy_pieces):
            return False, None

        return True, (row, 6)
            
    def can_long_castle(self, king_pos, enemy_color):
        row, col = king_pos
        enemy_pieces = self.get_all_pieces(enemy_color)

        king = self.grid[row][col]
        rook = self.grid[row][0]

        if (not isinstance(king, King)) or (not isinstance(rook, Rook)):
            return False, None

        if not king.castle or not rook.castle:
            return False, None

        # squares between rook and king: 1,2,3 must be empty
        if (not self.is_empty(row, 1)) or (not self.is_empty(row, 2)) or (not self.is_empty(row, 3)):
            return False, None

        if self.is_square_attacked((row, col), enemy_pieces):
            return False, None
        if self.is_square_attacked((row, 3), enemy_pieces) or self.is_square_attacked((row, 2), enemy_pieces):
            return False, None

        return True, (row, 2)

    def checkmate(self, king_pos, color):
        row, col = king_pos
        pieces = self.get_all_pieces(color)
        enemy_pieces = self.get_all_pieces(not color)
        # king cannot move and is under attack
        if not self.grid[row][col].get_legal_moves(king_pos, self) and self.is_square_attacked(king_pos, enemy_pieces):
            for piece, piece_pos in pieces:
                # if at least one piece as a legal move we don't have a checkmate position
                if piece.get_legal_moves(piece_pos, self):
                    return False
            return True
        else:
            return False

    def any_legal_move(self, color):
        """
        Checks if any legal move is possible, used for draw.
        """
        pieces = self.get_all_pieces(color)
        for piece, piece_pos in pieces:
            if piece.get_legal_moves(piece_pos, self):
                return True
        return False 
    
    def check_insufficient_material(self):
        white_pieces = self.get_all_pieces(True)
        black_pieces = self.get_all_pieces(False)
        
        total = len(white_pieces) + len(black_pieces)
        # just the kings left
        if total == 2:
            return True
        # check if pattern is king + bishop, king or king + knight, king
        if total == 3:
            print(white_pieces)
            print(black_pieces)
            bigger = white_pieces if len(white_pieces) == 2 else black_pieces
            for piece, _ in bigger:
                # we check only bishop or knight because the king is implicit
                if isinstance(piece, Bishop) or isinstance(piece, Knight):
                    return True
        # if king + bishop vs king + bishop with bishops of the same color
        if total == 4:
            if len(white_pieces) == 2 and len(black_pieces) == 2:
                w_minor = next(((p, pos) for p, pos in white_pieces if not isinstance(p, King)), None)
                b_minor = next(((p, pos) for p, pos in black_pieces if not isinstance(p, King)), None)

                if w_minor and b_minor:
                    wp, wpos = w_minor
                    bp, bpos = b_minor
                    
                    # check if the bishops are the same color
                    if isinstance(wp, Bishop) and isinstance(bp, Bishop):
                        w_color = (wpos[0] + wpos[1]) % 2
                        b_color = (bpos[0] + bpos[1]) % 2
                        return w_color == b_color
                
        return False
    
    def position_signature(self, side_to_move_is_white: bool):
        """
        Saves the signature of the board, used to check draws.
        """
        # board placement
        board = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p == 0:
                    # empty squares
                    board.append(".")
                else:
                    # upper case for white, lowercase for black
                    ch = p.name[0].upper() 
                    if not p.is_white:
                        ch = ch.lower()
                    board.append(ch)
        board_str = "".join(board)

        # castling rights
        rights = []
        # white
        w_king_pos = self.get_king_square(True)
        if w_king_pos:
            wk = self.grid[w_king_pos[0]][w_king_pos[1]]
            if isinstance(wk, King) and wk.castle:
                if isinstance(self.grid[7][7], Rook) and self.grid[7][7] != 0 and self.grid[7][7].is_white and self.grid[7][7].castle:
                    rights.append("K")
                if isinstance(self.grid[7][0], Rook) and self.grid[7][0] != 0 and self.grid[7][0].is_white and self.grid[7][0].castle:
                    rights.append("Q")
        # black
        b_king_pos = self.get_king_square(False)
        if b_king_pos:
            bk = self.grid[b_king_pos[0]][b_king_pos[1]]
            if isinstance(bk, King) and bk.castle:
                if isinstance(self.grid[0][7], Rook) and self.grid[0][7] != 0 and (not self.grid[0][7].is_white) and self.grid[0][7].castle:
                    rights.append("k")
                if isinstance(self.grid[0][0], Rook) and self.grid[0][0] != 0 and (not self.grid[0][0].is_white) and self.grid[0][0].castle:
                    rights.append("q")
        castling = "".join(rights) if rights else "-"

        # en passant target
        ep = self.en_passant_target if self.en_passant_target else "-"

        # side to move
        stm = "w" if side_to_move_is_white else "b"

        return (board_str, stm, castling, ep)

    def record_position(self, side_to_move_is_white):
        """
        Records the new position and returns the count number.
        """
        sig = self.position_signature(side_to_move_is_white)
        if sig in self.board_signatures:
            self.board_signatures[sig] += 1
        else:
            self.board_signatures[sig] = 1
        
        return self.board_signatures[sig]
     
    def compute_current_score(self, is_white_color):
        """
        Computes total score of the player (used for minmax algo)
        """
        score = 0
        pieces = self.get_all_pieces(is_white_color)
        for piece, _ in pieces:
            score += piece.value
            
        return score


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
        
    def get_pseudo_legal_moves(self, position, grid):
        raise NotImplementedError
        
    def get_legal_moves(self, position, grid: Grid):
        row, col = position
        # get_pseudo_legal_moves will be in each piece.
        pseudo_moves = self.get_pseudo_legal_moves(position, grid)
        king_pos = grid.get_king_square(self.is_white)
        legal_moves = []
        for move in pseudo_moves:
            move_r, move_c = move
            # modify the grid with the plausible move
            temp = grid.grid[move_r][move_c]
            grid.grid[move_r][move_c] = grid.grid[row][col]
            grid.grid[row][col] = 0
            # we get the enemy pieces here in case we got a capture with the move
            enemy_pieces = grid.get_all_pieces(not self.is_white)

            # check if the king is in dange
            if not grid.is_square_attacked(king_pos, enemy_pieces):
                legal_moves.append(move)
            # swap back the grid
            grid.grid[row][col] = grid.grid[move_r][move_c]
            grid.grid[move_r][move_c] = temp
    
        return legal_moves

class Pawn(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 0, 32, 32, scale)
        self.value = 10
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
                attacks.append((r, c))
        return attacks 
        
    def get_pseudo_legal_moves(self, position, grid: Grid):
        row, col = position
        direction = -1 if self.is_white else 1
        moves = []
        # check first square
        if 0 <= row+direction < 8 and grid.is_empty(row+direction, col):
            moves.append((row+direction, col))  
            # check second square if pawn never moved
            if self.first_move:
                if grid.is_empty(row+(direction*2), col) and row+(direction*2) >= 0:
                    moves.append((row+(direction*2), col))
        if col + 1 < 8 and grid.is_enemy(row + direction, col + 1, self.is_white):
            moves.append((row + direction, col + 1))
        if col - 1 >= 0 and grid.is_enemy(row + direction, col - 1, self.is_white):
            moves.append((row + direction, col - 1))
        
        en_passant = grid.can_en_passant(position, direction)
        if en_passant != None:
            moves.append(en_passant)

        return moves
    
class Rook(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 32, 32, 32, scale)
        self.value = 50
        self.is_white = is_white
        super().__init__("rook", sprite)
        self.castle = True       
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_pseudo_legal_moves(position, grid)
        
    def get_pseudo_legal_moves(self, position, grid: Grid):
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
        self.value = 30
        self.is_white = is_white
        super().__init__("bishop", sprite)
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_pseudo_legal_moves(position, grid)
        
    def get_pseudo_legal_moves(self, position, grid: Grid):
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
        self.value = 30
        self.is_white = is_white
        super().__init__("knight", sprite)
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_pseudo_legal_moves(position, grid)
        
    def get_knight_moves(self, position, grid: Grid, directions):
        row, col = position
        dr, dc = directions
        r = row + dr
        c = col + dc
        
        if 0 <= r < 8 and 0 <= c < 8 and (grid.is_empty(r,c) or grid.is_enemy(r,c, self.is_white)):
            return (r,c)
                
    def get_pseudo_legal_moves(self, position, grid: Grid):
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
        self.value = 90
        self.is_white = is_white
        super().__init__("queen", sprite)
        
    def get_attack_squares(self, position, grid: Grid):
        return self.get_pseudo_legal_moves(position, grid)
        
    def get_pseudo_legal_moves(self, position, grid: Grid):
        
        directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (1, -1), (-1, 1), (1, 1)
        ]
        return utils.sliding_moves(self, position, grid, directions)
    
class King(ChessPiece):
    def __init__(self, spritesheet, scale, is_white=True):
        sprite = spritesheet.get_sprite(0+32*is_white, 160, 32, 32, scale)
        self.value = 900
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
            return (r,c)
        
        
    def get_pseudo_legal_moves(self, position, grid: Grid):
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
    
    def get_legal_moves(self, position, grid):
        row, col = position
        # get_pseudo_legal_moves will be in each piece.
        pseudo_moves = self.get_pseudo_legal_moves(position, grid)
        legal_moves = []
        for move in pseudo_moves:
            move_r, move_c = move
            king_pos = (move_r, move_c)
            # modify the grid with the plausible move
            temp = grid.grid[move_r][move_c]
            grid.grid[move_r][move_c] = grid.grid[row][col]
            grid.grid[row][col] = 0
            # we get the enemy pieces here in case we got a capture with the move
            enemy_pieces = grid.get_all_pieces(not self.is_white)
            
            # check if the king is in dange
            if not grid.is_square_attacked(king_pos, enemy_pieces):
                legal_moves.append(move)
            # swap back the grid
            grid.grid[row][col] = grid.grid[move_r][move_c]
            grid.grid[move_r][move_c] = temp
    
        return legal_moves