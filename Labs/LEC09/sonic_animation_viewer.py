"""소닉 스프라이트 시트의 동작을 차례로 보여준다."""
from pico2d import *

WIDTH, HEIGHT = 1200, 800


def main():
    open_canvas(WIDTH, HEIGHT)
    hide_lattice()
    running = True
    while running:
        clear_canvas()
        update_canvas()
        for event in get_events():
            if event.type == SDL_QUIT:
                running = False
        delay(0.01)
    close_canvas()


if __name__ == '__main__':
    main()
