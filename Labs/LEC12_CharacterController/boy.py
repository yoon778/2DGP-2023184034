from math import pi
from pico2d import (load_image, get_time, get_canvas_width,
                    SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE,
                    SDLK_LSHIFT, SDLK_RSHIFT)
from transitions import Machine

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.keys = set()
        self.shift_keys = set()
        self.image = load_image('animation_sheet.png')
        self.start_idle()
        self.machine = Machine(
            model=self,
            states=[{'name': 'IDLE', 'on_enter': 'start_idle'}, 'SLEEP', 'RUN', 'DASH'],
            transitions=[['sleep', 'IDLE', 'SLEEP'],
                         ['wake', 'SLEEP', 'IDLE'],
                         ['run', ['IDLE', 'SLEEP'], 'RUN'],
                         ['stop', ['RUN', 'DASH'], 'IDLE'],
                         ['dash', 'RUN', 'DASH'],
                         ['slow', 'DASH', 'RUN']],
            initial='IDLE', auto_transitions=False)

    def start_idle(self):
        # 깨어날 때마다 휴식 시간을 새로 잰다.
        self.idle_start = get_time()
        self.frame = 0

    def handle_event(self, event):
        if event.type not in (SDL_KEYDOWN, SDL_KEYUP):
            return
        if event.key in (SDLK_LEFT, SDLK_RIGHT):
            if event.type == SDL_KEYDOWN:
                self.keys.add(event.key)
                self.face_dir = 1 if event.key == SDLK_RIGHT else -1
            else:
                self.keys.discard(event.key)
                if self.keys:
                    self.face_dir = 1 if SDLK_RIGHT in self.keys else -1

            if self.keys and self.state not in ('RUN', 'DASH'):
                self.run()
                if self.shift_keys:
                    self.dash()
            elif not self.keys and self.state in ('RUN', 'DASH'):
                self.stop()
        elif event.key in (SDLK_LSHIFT, SDLK_RSHIFT):
            if event.type == SDL_KEYDOWN:
                self.shift_keys.add(event.key)
            else:
                self.shift_keys.discard(event.key)
            if self.shift_keys and self.state == 'RUN':
                self.dash()
            elif not self.shift_keys and self.state == 'DASH':
                self.slow()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.state == 'SLEEP':
                self.wake()

    def update(self, dt=1 / 60):
        if self.state == 'IDLE':
            self.frame = (self.frame + 10 * dt) % 8
            if get_time() - self.idle_start >= 5:
                self.sleep()
        elif self.state in ('RUN', 'DASH'):
            self.frame = (self.frame + 10 * dt) % 8
            speed = 400 if self.state == 'DASH' else 200
            # 그림의 절반 너비(50)만큼 여유를 두어 화면 안에 유지한다.
            self.x = max(50, min(get_canvas_width() - 50,
                                 self.x + self.face_dir * speed * dt))

    def draw(self):
        if self.state == 'SLEEP':
            # 반시계 방향으로 90도 회전하고 첫 프레임에 고정한다.
            self.image.clip_composite_draw(0, 300, 100, 100, pi / 2, '',
                                           self.x, self.y - 25, 100, 100)
            return
        row = 300 if self.face_dir == 1 else 200
        if self.state in ('RUN', 'DASH'):
            row -= 200
        self.image.clip_draw(int(self.frame) * 100, row, 100, 100, self.x, self.y)
