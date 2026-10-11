import pygame as pg
from entity import *
from constants import *
from utils import handle_left_click, draw_wall, get_click_pos, draw_grid

pg.init()

grid = [[0 for _ in range(GRID_SIZE[X])] for _ in range(GRID_SIZE[Y])]
draw_wall(grid)

player = Player(PLAYER_STARTING_POS)
grid[player.position[Y]][player.position[X]] = GRID_STATES["player"]

melee_enemy = MeleeEnemy(ENEMY_STARTING_POS)
grid[melee_enemy.position[Y]][melee_enemy.position[X]] = GRID_STATES["enemy"]

next_tick_time = pg.time.get_ticks() + TICK_RATE

while not STOPPED:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            STOPPED = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            click_pos, is_out_of_bounds = get_click_pos()
            if is_out_of_bounds:
                continue
            if click_pos == melee_enemy.position:
                if player.is_moving:
                    grid[player.dest_pos[Y]][player.dest_pos[X]] = GRID_STATES["empty"]
                    player.dest_pos = player.position
                    player.path = None
                player.action_queue.appendleft("attack")
                continue
            handle_left_click(player, grid, click_pos)

    current_time = pg.time.get_ticks()
    if current_time > next_tick_time:
        if player.action_queue:
            action = player.action_queue.popleft()
            if action == "move_player":
                player.move(grid)
            if action == "attack":
                player.attack()
        melee_enemy.move(player.position, grid)
        next_tick_time = current_time + TICK_RATE

    draw_grid(grid)

    pg.display.flip()
    CLOCK.tick(FPS)

pg.quit()
