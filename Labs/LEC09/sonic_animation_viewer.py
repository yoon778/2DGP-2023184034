"""소닉 스프라이트 시트의 동작을 차례로 보여준다."""
from pico2d import *
from pathlib import Path
from time import perf_counter

WIDTH, HEIGHT = 1200, 800
SCALE = 5
FOLDER = Path(__file__).resolve().parent
FRAME_TIME = 0.1
REPEATS = 5
PAUSE_TIME = 1.0
ANIMATIONS = [
    {'name': '대기', 'frames': [
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
    ]},
    {'name': '발 두드리기', 'frames': [
        (86, 40, 30, 38), (118, 40, 30, 38),
        (150, 40, 30, 38), (182, 40, 29, 38),
    ]},
    {'name': '위 보기', 'frames': [
        (211, 39, 29, 38), (240, 39, 29, 38),
    ]},
    {'name': '숙이기', 'frames': [
        (270, 45, 24, 32), (302, 51, 29, 26),
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
    {'name': '몸 말아 회전', 'frames': [
        (1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29),
        (98, 169, 31, 29), (131, 168, 29, 30), (162, 168, 29, 31),
        (193, 170, 30, 29), (230, 170, 31, 29),
    ]},
    {'name': '공 자세', 'frames': [(268, 170, 30, 30)]},
    {'name': '빠른 회전', 'frames': [
        (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
        (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
    ]},
    {'name': '정면 달리기', 'frames': [
        (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
        (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
    ]},
    {'name': '빠르게 달리기', 'frames': [
        (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
        (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
    ]},
    {'name': '공중 돌기', 'frames': [
        (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
        (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
    ]},
    {'name': '뒤로 넘어지기', 'frames': [
        (184, 341, 40, 28), (232, 341, 39, 27),
    ]},
    {'name': '멈추기', 'frames': [
        (1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
        (99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 36),
        (217, 379, 33, 36), (254, 378, 33, 36),
    ]},
    {'name': '떨어지기', 'frames': [
        (6, 429, 34, 40), (49, 426, 34, 43),
    ]},
    {'name': '균형 잡기', 'frames': [
        (96, 427, 23, 39), (125, 427, 23, 39),
    ]},
]

# 대기 자세는 천천히, 빠르게 움직이는 동작은 짧은 간격으로 보여준다.
TIMES = [0.25, 0.18, 0.30, 0.25, 0.08, 0.08, 0.07, 0.30,
         0.06, 0.085, 0.065, 0.13, 0.18, 0.10, 0.20, 0.24]

# 같은 줄의 바닥 높이를 보존해 잘린 여백 때문에 위아래로 튀지 않게 한다.
for action, seconds in zip(ANIMATIONS, TIMES):
    action['time'] = seconds
    bottom = max(y + h for x, y, w, h in action['frames'])
    action['offsets'] = [(0, bottom - y - h) for x, y, w, h in action['frames']]


def draw_frame(sheet, frame, offset=(0, 0)):
    x, y, w, h = frame
    # 서 있는 기본 자세(높이 39px)의 중심과 바닥을 기준으로 맞춘다.
    draw_x = WIDTH / 2 + offset[0] * SCALE
    draw_y = HEIGHT / 2 + ((h - 39) / 2 + offset[1]) * SCALE
    clear_canvas()
    # 위쪽 기준 이미지 좌표를 pico2d의 아래쪽 기준으로 바꾼다.
    sheet.clip_draw(x, sheet.h - y - h, w, h,
                    draw_x, draw_y, w * SCALE, h * SCALE)
    update_canvas()


def wait(seconds):
    end = perf_counter() + seconds
    while perf_counter() < end:
        for event in get_events():
            if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
                return False
        delay(min(0.01, max(0, end - perf_counter())))
    return True


def play(sheet, action):
    # 프레임 목록 전체를 끝까지 재생해야 한 번으로 센다.
    for repeat in range(REPEATS):
        for frame, offset in zip(action['frames'], action['offsets']):
            draw_frame(sheet, frame, offset)
            if not wait(action.get('time', FRAME_TIME)):
                return False
    # 화면을 지우지 않아 마지막 자세가 그대로 남는다.
    return wait(PAUSE_TIME)


def main():
    image_path = FOLDER / 'sonic-sprite.png'
    if not image_path.is_file():
        print(f'이미지 파일이 필요합니다: {image_path}')
        return
    open_canvas(WIDTH, HEIGHT)
    try:
        hide_lattice()
        try:
            sheet = load_image(str(image_path))
        except OSError:
            print(f'이미지 파일을 읽을 수 없습니다: {image_path}')
            return
        running = True
        while running:
            for action in ANIMATIONS:
                if not play(sheet, action):
                    running = False
                    break
    finally:
        close_canvas()


if __name__ == '__main__':
    main()
