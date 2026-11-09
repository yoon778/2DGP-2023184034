from pico2d import (SDL_KEYDOWN, SDL_KEYUP, SDL_QUIT, SDLK_ESCAPE, SDLK_LEFT,
                    SDLK_RIGHT, SDLK_p, get_events)

import game_framework
import play_mode
import title_mode


released_keys = []


def init():
    released_keys.clear()


def finish():
    released_keys.clear()


def update():
    pass


def render():
    play_mode.render()


def handle_events(events=None):
    if events is None:
        events = get_events()
    for index, event in enumerate(events):
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_p:
                releases = released_keys[:]
                game_framework.pop_mode()
                for release in releases:
                    play_mode.boy.handle_event(release)
                play_mode.handle_events(events[index + 1:])
                return
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
                game_framework.change_mode(title_mode)
                return
        if event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            released_keys.append(event)
