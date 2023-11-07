from pico2d import open_canvas, close_canvas
import selection_mode
import play_mode
import title_mode as start_mode
import game_framework

open_canvas(500, 450)
game_framework.run(start_mode)
close_canvas()
