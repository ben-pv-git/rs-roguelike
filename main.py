import pygame as pg
from pathfinder import Pathfinder
from entity import *
from constants import *
from utils import handle_left_click, draw_wall

pg.init()

grid = [[0 for _ in range(GRID_SIZE[X])] for _ in range(GRID_SIZE[Y])]
draw_wall(grid)

player = Player([GRID_SIZE[Y]//2, GRID_SIZE[X]//2])
grid[player.position[Y]][player.position[X]] = GRID_STATES["player"]

melee_enemy = MeleeEnemy([10, 10])
grid[melee_enemy.position[Y]][melee_enemy.position[X]] = GRID_STATES["enemy"]

pf = Pathfinder(grid)

def get_rect(r, c):
    return [(MARGIN + CELL_SIZE) * c + MARGIN, (MARGIN + CELL_SIZE) * r + MARGIN, CELL_SIZE, CELL_SIZE]

while not STOPPED:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            STOPPED = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            col_coord = mouse_pos[X] // (CELL_SIZE + MARGIN)
            row_coord = mouse_pos[Y] // (CELL_SIZE + MARGIN)
            click_pos = [col_coord, row_coord]
            if not (0 <= col_coord < GRID_SIZE[Y] and 0 <= row_coord < GRID_SIZE[X]):
                continue
            if click_pos == melee_enemy.position:
                # if player.position == player.dest_pos:
                #     continue
                if player.dest_pos != [None, None]:
                    grid[player.dest_pos[Y]][player.dest_pos[X]] = GRID_STATES["empty"]
                    player.dest_pos = [None, None]
                player.action_queue.append("attack")
                continue
            handle_left_click(player, grid, click_pos)

    current_time = pg.time.get_ticks()
    if current_time > NEXT_TICK_TIME:
        if player.action_queue:
            action = player.action_queue.popleft()
            if action == "move_player":
                player.is_moving = True
            if action == "attack":
                player.is_moving = False
                player.attack()
                player.is_attacking = False
        
        if player.is_moving: player.move(grid)
        melee_enemy.move(grid, player.position)

        NEXT_TICK_TIME = current_time + TICK_RATE

    SCREEN.fill(BLACK)
    # SCREEN.fill(WHITE)
    for r in range(GRID_SIZE[Y]):
        for c in range(GRID_SIZE[X]):
            color = COLOR_MAP.get(grid[r][c], WHITE)
            pg.draw.rect(SCREEN, color, get_rect(r, c))
            # pg.draw.rect(SCREEN, color, get_rect(r, c), MARGIN+2)

    pg.display.flip()
    CLOCK.tick(FPS)

pg.quit()
