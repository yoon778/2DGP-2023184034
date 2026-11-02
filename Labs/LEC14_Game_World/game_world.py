#게임 월드 리스트 초기화
world = [[], []] #빈 리스트


def add_object(o, depth = 0):
    world[depth].append(o)

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return # 함수 제거

#게임 로직
def update():
    # 갱신 중 공이 제거되어도 다음 객체를 건너뛰지 않는다.
    for layer in world:
        for o in layer:
            o.update()

#게임 월드 렌더링
def render():
    for layer in world:
        for o in layer:
            o.draw()
