world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI
collision_pairs = {}

def add_oject(o, depth=1):
    world[depth].append(o)

def add_objects(ol, depth=1):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

def update():
    for layer in world:
        for o in layer[:]:
            o.update()

def render():
    for layer in world:
        for o in layer[:]:
            o.draw()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b:return False
    if right_a < left_b:return False
    if top_a <  bottom_b:return False
    if bottom_a > top_b:return False
    return True


def clear():
    for layer in world:
        layer.clear()
    collision_pairs.clear()

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]

    if a is not None:
        collision_pairs[group][0].append(a)
    if b is not None:
        collision_pairs[group][1].append(b)

def handle_collisions():
    for group, (left, right) in collision_pairs.items():
        # 충돌 중 공이 제거되어도 같은 프레임의 다음 공까지 검사한다.
        for a in left[:]:
            for b in right[:]:
                if a not in left:
                    break
                if b in right and collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
