"""소닉 스프라이트 시트의 동작을 차례로 보여준다."""
from pico2d import *
from pathlib import Path

WIDTH, HEIGHT = 1200, 800
FOLDER = Path(__file__).resolve().parent
FIRST_FRAME = (1, 39, 29, 39)


def main():
    open_canvas(WIDTH, HEIGHT)
    hide_lattice()
    sheet = load_image(str(FOLDER / 'sonic-sprite.png'))
    running = True
    while running:
        clear_canvas()
        x, y, w, h = FIRST_FRAME
        # 위쪽 기준 이미지 좌표를 pico2d의 아래쪽 기준으로 바꾼다.
        sheet.clip_draw(x, sheet.h - y - h, w, h, WIDTH / 2, HEIGHT / 2)
        update_canvas()
        for event in get_events():
            if event.type == SDL_QUIT:
                running = False
        delay(0.01)
    close_canvas()


if __name__ == '__main__':
    main()
