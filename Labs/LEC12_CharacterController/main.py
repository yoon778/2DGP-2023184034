from pico2d import *
from time import perf_counter
import random

from boy import Boy 
from grass import Grass

# Game object class here




def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)


def reset_world():
    global world
    global boy

    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world(dt):
    for o in world:
        o.update(dt)
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
last_time = perf_counter()
while running:
    start_time = perf_counter()
    # 잠깐 멈췄다가 돌아와도 캐릭터가 한 번에 크게 이동하지 않게 한다.
    dt = min(start_time - last_time, 0.1)
    last_time = start_time
    handle_events()
    update_world(dt)
    render_world()
    delay(max(0, 1 / 60 - (perf_counter() - start_time)))
# finalization code
close_canvas()
