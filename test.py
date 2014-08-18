from __future__ import division
import random
import collections
MAX = 5
MIN = 3

Rect = collections.namedtuple('Rect', ['x', 'y', 'w', 'h'])

class QuadTree(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.objects = []
        self.quadrants = []

    def __repr__(self):
        return 'QuadTree(%s, %s, %s, %s)' % (self.x, self.y, self.w, self.h)

    def insert(self, obj):
        q = self.locate(obj)
        if len(q.objects) > MAX and not q.quadrants:
            q.use_quadrants()
            q = self.locate(obj)
        q.objects.append(obj)

    def locate(self, obj):
        """Returns the QuadTree object where an object belongs"""
        for quad in self.quadrants:
            if quad.can_contain(obj):
                return quad.locate(obj)
        if not self.can_contain(obj):
            raise ValueError("%r can't contain %r" % (self, obj))
        else:
            return self

    def locate_with_parent(self, obj, parent=None):
        """Returns tree and parent tree"""
        for quad in self.quadrants:
            if quad.can_contain(obj):
                return quad.locate_with_parent(obj, self)
        if not self.can_contain(obj):
            raise ValueError("%r can't contain %r" % (self, obj))
        else:
            return self, parent

    def neighbors(self, obj):
        q = self.locate(obj)
        return q.all_contained()

    def all_contained(self):
        if self.quadrants:
            return self.objects + [obj for quad in self.quadrants for obj in quad.objects]
        return self.objects

    def use_quadrants(self):
        w, h = self.w / 2, self.h / 2
        self.quadrants = [QuadTree(x, y, w, h) for x in [self.x, self.x + w]
                                               for y in [self.y, self.y + h]]
        objects, self.objects = self.objects, []
        for obj in objects:
            self.insert(obj)

    def can_contain(self, obj):
        return (obj.x >= self.x and obj.y >= self.y and
                obj.x + obj.w <= self.x + self.w and
                obj.y + obj.h <= self.y + self.h)

    def compact(self):
        if sum(len(q.objects) for q in self.quadrants) < MIN:
            self.objects.extend(q.objects for q in self.quadrants)

    def remove(self, obj):
        q, parent = self.locate_with_parent(obj)
        q.objects.remove(obj)
        if parent:
            parent.compact()

class BaseWorld(object):
    def loop(self):
        for obj in self.objects:
            self.update(obj

class NaiveWorld(BaseWorld):
    def __init__(self, w, h):
        self.objects = []
    def update(self, obj):
        obj.update()
    def add(self, obj):
        self.objects.append()

class QuadTreeWorld(object):
    def __init__(self, w, h):
        self.quadtree = QuadTree(0, 0, w, h)
        self.objects = []
    def update(self, obj):
        self.quadtree.remove()
        obj.update()
        self.quadtree.insert(obj)
    def add(self, obj):
        self.objects.append()
        self.quadtree.insert(obj)

class Asteroid(object):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.w = self.h = size
        self.dx = .5
        self.dy = .5
    def update(self):
        self.x =+ self.dx
        self.y =+ self.dy

def test_tree():
    q = QuadTree(0, 0, 100, 100)
    for _ in range(1000):
        a = Rect(random.randint(0, 90), random.randint(0, 90), 3, 10)
        q.insert(a)
    return q

def main():
    w = NaiveWorld()
    w.add(Asteroid())


