import sys
import pygame as pg

pg.init()
font = pg.font.SysFont(None, 80)
screen_length = 750
screen_width = 750
margin_length = 15
margin_width = 15
screen_size = screen_length, screen_width
screen = pg.display.set_mode(screen_size)


def set_background():
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"),
                 pg.Rect(margin_length, margin_width, screen_length - (margin_length * 2),
                         screen_width - (margin_width * 2)), 10)

    i = 1
    while (i * ((screen_length - (margin_length * 2)) // 9)) < screen_length - (margin_length * 2):
        line_width = 5 if i % 3 > 0 else 10
        pg.draw.line(screen, pg.Color("black"),
                     pg.Vector2((i * ((screen_length - (margin_length * 2)) // 9) + margin_length), margin_width),
                     pg.Vector2((i * ((screen_length - (margin_length * 2)) // 9) + margin_length),
                                screen_width - margin_width), line_width)
        pg.draw.line(screen, pg.Color("black"),
                     pg.Vector2(margin_length, (i * ((screen_length - (margin_length * 2)) // 9)) + margin_length),
                     pg.Vector2(screen_length - margin_width, (i * ((screen_length - (margin_length * 2)) // 9)) + margin_length),
                     line_width)
        i += 1


def solving(grid, row, column):
    if column == 9:
        if row == 8:
            return True
        else:
            row += 1
            column = 0

    if grid[row][column] > 0:
        return solving(grid, row, column + 1)

    for number in range(1, 10):
        if valid_move(grid, row, column, number):
            grid[row][column] = number

            if solving(grid, row, column + 1):
                return True

        grid[row][column] = 0

    return False


def valid_move(grid, row, column, number):
    if number in grid[row]:
        return False

    for x in range(9):
        if grid[x][column] == number:
            return False

    top_left_corner_row = row - (row % 3)
    bottom_right_corner_column = column - (column % 3)

    for x in range(3):
        for y in range(3):
            if grid[top_left_corner_row + x][bottom_right_corner_column + y] == number:
                return False
    return True


def draw_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                text = font.render(str(grid[i][j]), True, pg.Color("black"))
                text_rect = text.get_rect(center=((j * ((screen_length - (margin_length * 2)) // 9) + margin_length) + 40,
                                                  (i * ((screen_length - (margin_length * 2)) // 9) + margin_length) + 40))
                screen.blit(text, text_rect)


grid = [[0, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 9, 0, 0],
        [7, 0, 1, 0, 0, 2, 0, 6, 0],
        [0, 2, 0, 0, 0, 0, 0, 8, 0],
        [0, 0, 3, 0, 0, 4, 0, 0, 0],
        [4, 0, 8, 9, 0, 0, 6, 0, 0],
        [6, 0, 4, 0, 0, 7, 0, 1, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 0, 7]]

if solving(grid, 0, 0):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        set_background()
        draw_grid(grid)
        pg.display.flip()