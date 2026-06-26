import pygame
from gamestate import GameState

# ---- palette ----
PANEL_BG = (28, 28, 30)
PANEL_BG_ALT = (38, 38, 42)
SEPARATOR = (70, 70, 74)
TEXT_COLOR = (232, 232, 232)
TEXT_MUTED = (150, 150, 154)
CLOCK_BG = (48, 48, 52)
CLOCK_BG_ACTIVE = (96, 122, 72)
CLOCK_BG_LOW = (150, 60, 60)


class Button:
    """A simple rectangular text button."""

    def __init__(self, rect, text, font, base_color, hover_color, text_color=(240, 240, 240)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        label = self.font.render(self.text, True, self.text_color)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class Clock:
    """A countdown clock for one side."""

    def __init__(self, seconds):
        self.time = float(seconds)

    def tick(self, dt, active):
        if active and self.time > 0:
            self.time = max(0.0, self.time - dt)

    def is_flagged(self):
        return self.time <= 0

    def format(self):
        total = int(self.time)
        return f"{total // 60:02d}:{total % 60:02d}"

    def draw(self, screen, font, rect, active):
        if self.time <= 30:
            bg = CLOCK_BG_LOW
        elif active:
            bg = CLOCK_BG_ACTIVE
        else:
            bg = CLOCK_BG
        pygame.draw.rect(screen, bg, rect, border_radius=4)
        label = font.render(self.format(), True, TEXT_COLOR)
        screen.blit(label, label.get_rect(center=rect.center))


class SidePanel:
    """Right-hand panel: scrolling move list + resign / draw buttons."""

    def __init__(self, x, y, width, height, fonts):
        self.rect = pygame.Rect(x, y, width, height)
        self.title_font = fonts["title"]
        self.move_font = fonts["mono"]
        self.btn_font = fonts["body"]
        self.row_h = 26

        btn_h = 42
        btn_w = (width - 30) // 2
        by = y + height - btn_h - 15
        self.resign_btn = Button((x + 10, by, btn_w, btn_h), "Resign",
                                 self.btn_font, (150, 58, 58), (185, 80, 80))
        self.draw_btn = Button((x + 20 + btn_w, by, btn_w, btn_h), "Draw",
                               self.btn_font, (70, 92, 124), (92, 116, 152))

        self.list_top = y + 52
        self.list_bottom = by - 15

    def draw(self, screen, moves):
        pygame.draw.rect(screen, PANEL_BG, self.rect)

        title = self.title_font.render("MOVES", True, TEXT_COLOR)
        screen.blit(title, (self.rect.x + 15, self.rect.y + 16))
        pygame.draw.line(screen, SEPARATOR,
                         (self.rect.x + 10, self.rect.y + 46),
                         (self.rect.right - 10, self.rect.y + 46))

        self._draw_moves(screen, moves)
        self.resign_btn.draw(screen)
        self.draw_btn.draw(screen)

    def _draw_moves(self, screen, moves):
        # strip the "white: " / "black: " prefix -> bare notation
        sans = [m.split(":", 1)[1].strip() if ":" in m else m for m in moves]

        # group into (move_number, white, black) rows
        rows = []
        for i in range(0, len(sans), 2):
            white = sans[i]
            black = sans[i + 1] if i + 1 < len(sans) else ""
            rows.append((i // 2 + 1, white, black))

        max_rows = max(0, (self.list_bottom - self.list_top) // self.row_h)
        # auto-scroll: keep the most recent moves visible
        visible = rows[-max_rows:] if len(rows) > max_rows else rows

        num_w = 38
        col_w = (self.rect.width - 30 - num_w) // 2
        x = self.rect.x + 15
        for idx, (n, white, black) in enumerate(visible):
            y = self.list_top + idx * self.row_h
            if idx % 2 == 0:
                pygame.draw.rect(screen, PANEL_BG_ALT,
                                 (self.rect.x + 5, y - 2, self.rect.width - 10, self.row_h))
            screen.blit(self.move_font.render(f"{n}.", True, TEXT_MUTED), (x, y))
            screen.blit(self.move_font.render(white, True, TEXT_COLOR), (x + num_w, y))
            if black:
                screen.blit(self.move_font.render(black, True, TEXT_COLOR), (x + num_w + col_w, y))

    def update_hover(self, mouse_pos):
        self.resign_btn.update_hover(mouse_pos)
        self.draw_btn.update_hover(mouse_pos)

    def handle_click(self, mouse_pos):
        if self.resign_btn.is_clicked(mouse_pos):
            return "resign"
        if self.draw_btn.is_clicked(mouse_pos):
            return "draw"
        return None


# human-readable result text for the game-over banner
RESULT_TEXT = {
    GameState.CHECKMATE_WHITE_WINS: "Checkmate - White wins",
    GameState.CHECKMATE_BLACK_WINS: "Checkmate - Black wins",
    GameState.DRAW_STALEMATE: "Draw - Stalemate",
    GameState.DRAW_INSUFFICIENT: "Draw - Insufficient material",
    GameState.DRAW_FIFTY_MOVE: "Draw - Fifty-move rule",
    GameState.DRAW_THREEFOLD: "Draw - Threefold repetition",
    GameState.DRAW_AGREEMENT: "Draw - By agreement",
    GameState.RESIGN_WHITE_WINS: "White wins - Black resigned",
    GameState.RESIGN_BLACK_WINS: "Black wins - White resigned",
    GameState.TIMEOUT_WHITE_WINS: "White wins on time",
    GameState.TIMEOUT_BLACK_WINS: "Black wins on time",
}


def draw_game_over(screen, font, board_rect, gamestate):
    """Dim the board and print the result across its middle."""
    text = RESULT_TEXT.get(gamestate, "Game Over")

    overlay = pygame.Surface(board_rect.size, pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, board_rect.topleft)

    band = pygame.Surface((board_rect.width, 64), pygame.SRCALPHA)
    band.fill((0, 0, 0, 210))
    screen.blit(band, (board_rect.x, board_rect.centery - 32))

    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, label.get_rect(center=board_rect.center))
