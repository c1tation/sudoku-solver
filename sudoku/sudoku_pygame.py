from sudoku_reader import Sudoku_reader
import random
from board import Board
from sudoku import SudokuBoard, Square, Element
import pygame
import sys

class ScreenStuff:
    def __init__(self) -> None:
        self.infoObject = pygame.display.Info()
        self.x_max = self.infoObject.current_w
        self.y_max = self.infoObject.current_h
        self.screen = pygame.display.set_mode((self.x_max, self.y_max))
    
class Text:
    def __init__(self) -> None:
        self.BodoniMT = pygame.font.SysFont('Bodoni MT', 50)
        self.BodoniBold = pygame.font.SysFont('Bodoni MT', 60, True)
        self.BellMTtitle = pygame.font.SysFont('Bell MT', 100)
        self.ComicSansMS = pygame.font.SysFont('Comic Sans MS', 30)
        self.Courier = pygame.font.SysFont('Courier New', 16)
        self.Courier2 = pygame.font.SysFont('Courier New', 17, True)
        self.Courier3 = pygame.font.SysFont('Courier New', 24)

def draw_square(screen, font, x, y, line_width, sqr_sz, base_x, base_y, color):
    number = board.nums[x][y].number
    if number:
        pygame.draw.rect(screen, color, (base_x + x * sqr_sz, base_y + y * sqr_sz, sqr_sz, sqr_sz))
        pygame.draw.rect(screen, (0, 0, 0), (base_x + x * sqr_sz, base_y + y * sqr_sz, sqr_sz, sqr_sz), line_width)
    possible = board.nums[x][y].possibilities
    if number:
        numcol = (0, 0, 0) if board.nums[x][y].locked else (255, 0, 0)
        ren = font.BellMTtitle.render(str(number), True, numcol)
        rec = ren.get_rect(center=(base_x + x * sqr_sz + sqr_sz // 2, base_y + y * sqr_sz + sqr_sz // 2))
        screen.blit(ren, rec)
    else:
        for xi in range(3):
            for yi in range(3):
                if xi * 3 + yi >= len(possible):
                    break
                pygame.draw.rect(screen, color, (base_x + x * sqr_sz + xi * sqr_sz // 3, base_y + y * sqr_sz + yi * sqr_sz // 3, sqr_sz // 3, sqr_sz // 3))
                pygame.draw.rect(screen, (0, 0, 0), (base_x + x * sqr_sz + xi * sqr_sz // 3, base_y + y * sqr_sz + yi * sqr_sz // 3, sqr_sz // 3, sqr_sz // 3), 2)
                ren = font.Courier.render(str(possible[xi * 3 + yi]), True, (0, 0, 0))
                rec = ren.get_rect(center=(base_x + x * sqr_sz + xi * sqr_sz // 3 + sqr_sz // 6, base_y + y * sqr_sz + yi * sqr_sz // 3 + sqr_sz // 6))
                screen.blit(ren, rec)




def draw_screen(scr: ScreenStuff, font: Text, screen: pygame.Surface, board: SudokuBoard):
    screen.fill((0, 0, 0))
    xm, ym = scr.x_max, scr.y_max
    xmid, ymid = xm // 2, ym // 2
    sud_offset = ym // 2
    sqr_sz = ym // 9
    base_x = xmid - sud_offset
    base_y = ymid - sud_offset
    line_width = 3
    thick_line_width = 10
    colors = [(255, 255, 255), (0, 255, 0), (180, 255, 0), (255, 255, 0), (255, 150, 0), (255, 0, 0), (255, 0, 150), (150, 0, 255), (50, 0, 255), (0, 0, 200)]
    for x in range(board.n_cols):
        for y in range(board.n_rows):
            color = colors[len(board.nums[x][y].possibilities)]
            draw_square(screen, font, x, y, line_width, sqr_sz, base_x, base_y, color)
            if x % 3 == 0:
                pygame.draw.line(screen, (0, 0, 0), (base_x + x * sqr_sz, base_y + y * sqr_sz), (base_x + x * sqr_sz, base_y + y * sqr_sz + sqr_sz), thick_line_width)
            if y % 3 == 0:
                pygame.draw.line(screen, (0, 0, 0), (base_x + x * sqr_sz, base_y + y * sqr_sz), (base_x + x * sqr_sz + sqr_sz, base_y + y * sqr_sz), thick_line_width)
    pygame.display.update()

def place_square(board):
    least_possible, mistake = board.entropy() # Find the lowest entropy square
    if mistake: # Start over if a dead end is reached
        board.new_attempt()
        board.entropy()
    else:
        board.observe(least_possible)
        board.entropy()
    return board


if __name__ == '__main__':
    # IMPORTANT !!!: Change file path if necessary !!!!!
    reader = Sudoku_reader("sudoku/sudoku_10.csv")
    # Read text above if the program does not run


    pygame.init()
    pygame.font.init()
    scr = ScreenStuff()
    font = Text()
    next_board = reader.next_board()
    board = SudokuBoard(next_board)
    board._set_up_nums(next_board)
    board._set_up_elems()
    board.entropy()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        sys.exit()
                    case pygame.K_SPACE:
                        if board.check_solved():
                            next_board = reader.next_board()
                            board = SudokuBoard(next_board)
                        board = place_square(board)
                        
        draw_screen(scr, font, scr.screen, board)
        

                        
