"""소닉 스프라이트 시트의 동작을 차례로 보여준다."""
from pico2d import *
from pathlib import Path

WIDTH, HEIGHT = 1200, 800
FOLDER = Path(__file__).resolve().parent
FRAME_TIME = 0.1
ANIMATIONS = [
    {'name': '대기', 'frames': [
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
    ]},
]


def draw_frame(sheet, frame):
    x, y, w, h = frame
    clear_canvas()
    # 위쪽 기준 이미지 좌표를 pico2d의 아래쪽 기준으로 바꾼다.
    sheet.clip_draw(x, sheet.h - y - h, w, h, WIDTH / 2, HEIGHT / 2)
    update_canvas()


def main():
    open_canvas(WIDTH, HEIGHT)
    hide_lattice()
    sheet = load_image(str(FOLDER / 'sonic-sprite.png'))
    running = True
    frame = 0
    frames = ANIMATIONS[0]['frames']
    while running:
        draw_frame(sheet, frames[frame])
        for event in get_events():
            if event.type == SDL_QUIT:
                running = False
        frame = (frame + 1) % len(frames)
        delay(FRAME_TIME)
    close_canvas()


if __name__ == '__main__':
    main()
