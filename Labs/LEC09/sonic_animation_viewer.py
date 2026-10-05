"""소닉 스프라이트 시트의 동작을 차례로 보여준다."""
from pico2d import *
from pathlib import Path

WIDTH, HEIGHT = 1200, 800
FOLDER = Path(__file__).resolve().parent


def main():
    open_canvas(WIDTH, HEIGHT)
    hide_lattice()
    sheet = load_image(str(FOLDER / 'sonic-sprite.png'))
    running = True
    while running:
        clear_canvas()
        sheet.draw(WIDTH / 2, HEIGHT / 2)
        update_canvas()
        for event in get_events():
            if event.type == SDL_QUIT:
                running = False
        delay(0.01)
    close_canvas()


if __name__ == '__main__':
    main()
