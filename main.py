from pico2d import open_canvas, close_canvas
import select_mode
import play_mode
import title_mode as start_mode
import score_mode
import game_framework

open_canvas(250 * 4, 225 * 4)
game_framework.run(start_mode)
close_canvas()
