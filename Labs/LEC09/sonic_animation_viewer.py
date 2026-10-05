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
    {'name': '걷기', 'frames': [
        (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
        (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
        (206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
        (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
    ]},
    {'name': '달리기', 'frames': [
        (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
        (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
    ]},
    {'name': '정면 달리기', 'frames': [
        (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
        (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
    ]},
    {'name': '빠르게 달리기', 'frames': [
        (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
        (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
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
