from pico2d import *
import game_framework
import game_world
import title_mode
from boy import Boy
from grass import Grass


def handle_events(events=None):
    if events is None:
        events = get_events()
    for index, event in enumerate(events):
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            import pause_mode
            game_framework.push_mode(pause_mode)
            pause_mode.handle_events(events[index + 1:])
            return
        else:
            boy.handle_event(event)



def init(): #초기화
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

def update():
    game_world.update()


def pause():
    global paused_at
    paused_at = get_time()


def resume():
    boy.idle_started_at += get_time() - paused_at

def render():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

