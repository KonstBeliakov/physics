import pygame as pg


def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** .5


def dist(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** .5


def point_in_square(point_pos, square_pos, square_size):
    return square_pos[0] + square_size[0] >= point_pos[0] >= square_pos[0] and \
        square_pos[1] + square_size[1] >= point_pos[1] >= square_pos[1]


def itersection_of_segments(a1, a2, b1, b2):
    a1, a2 = min(a1, a2), max(a1, a2)
    b1, b2 = min(b1, b2), max(b1, b2)

    return a1 <= b1 <= a2 or a1 <= b2 <= a2 or b1 <= a1 <= b2 or b1 <= a2 <= b2


def squares_intersection(pos1, size1, pos2, size2):
    return itersection_of_segments(pos1[0], pos1[0] + size1[0], pos2[0], pos2[0] + size2[0]) and \
        itersection_of_segments(pos1[1], pos1[1] + size1[1], pos2[1], pos2[1] + size2[1])


def sign(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    return 1


def rotate(surface, angle, position):
    img = pg.transform.rotozoom(surface, angle, 1)
    img_rect = img.get_rect(center=position)
    return img, img_rect


class Line():
    def __init__(self, k, b):
        self.k = k
        self.b = b

    def __init__(self, a, b, c, d):
        if abs(c - a) < 0.01:
            if d > b:
                self.k = 10_000
            else:
                self.k = -10_000
        else:
            self.k = (d - b) / (c - a)
        self.b = b - (self.k * a)

    def y(self, x):
        return self.k * x + self.b

    def print(self):
        print(f'y = {self.k}x + {self.b}')


class Segment():
    def __init__(self, a, b, c, d):
        if abs(a - c) < .1:
            c += .1
        if abs(b - d) < .1:
            d += .1
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __init__(self, pos1, pos2):
        self.a, self.b = pos1
        self.c, self.d = pos2
        if abs(self.a - self.c) < .1:
            self.c += .1
        if abs(self.b - self.d) < .1:
            self.d += .1


def line_intersection(line1, line2):
    if line1.k == line2.k:
        return None
    x = (line2.b - line1.b) / (line1.k - line2.k)
    return x, line1.y(x)


def line_segments_intersection(segment1, segment2):
    a1, b1, c1, d1 = segment1.a, segment1.b, segment1.c, segment1.d
    a2, b2, c2, d2 = segment2.a, segment2.b, segment2.c, segment2.d
    t = line_intersection(Line(a1, b1, c1, d1), Line(a2, b2, c2, d2))

    if t is None:
        return None
    a1, c1 = min(a1, c1), max(a1, c1)
    b1, d1 = min(b1, d1), max(b1, d1)

    a2, c2 = min(a2, c2), max(a2, c2)
    b2, d2 = min(b2, d2), max(b2, d2)

    if max(a1, a2) <= t[0] <= min(c1, c2) and max(b1, b2) <= t[1] <= min(d1, d2):
        return t
    return None


def rect_intersection(a, b, c, d, a2, b2, c2, d2):
    segments1 = [Segment(a, b), Segment(b, c), Segment(c, d), Segment(d, a)]
    segments2 = [Segment(a2, b2), Segment(b2, c2), Segment(c2, d2), Segment(d2, a2)]

    for s1 in segments1:
        for s2 in segments2:
            if line_segments_intersection(s1, s2):
                return True
    return False
