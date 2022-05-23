import numpy as np
import random
import math
import style as s
from PIL import Image, ImageDraw

class Circle:
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        
    def copy(self):
        return Circle(self.x, self.y, self.r, self.c)

class Grid:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.img = Image.new("RGB", (w, h), bg)
        self.drw = ImageDraw.Draw(self.img)
        self.circles = []
        
    def draw_circle(self, c):
        x1 = c.x - c.r
        y1 = c.y - c.r
        x2 = c.x + c.r
        y2 = c.y + c.r
        self.drw.ellipse([x1, y1, x2, y2], fill=s.BORDER_COL)
        self.drw.ellipse([x1+s.B, y1+s.B, x2-s.B, y2-s.B], fill=c.c)
        

    def intersect(self, c1, c2):
        '''
        ARG 1 c1: ORDER MATTERS function returns whether or not c1 intersects.
        '''
        dist = np.sqrt(((c1.x - c2.x) ** 2) + ((c1.y - c2.y) ** 2))
        c_int = dist < (c1.r + c2.r)
        # true if is intersecting

        b_int = c1.x - c1.r <= 0 or c1.y - c1.r <= 0 or \
            c1.x + c1.r >= self.w or c1.y + c1.r >= self.h
        # true if is intersecting

        b_int = not ((not b_int) or s.SPILL)
        c_int = not ((not c_int) or c1.c == c2.c) 
        
        return c_int or b_int

    def try_fill(self, x=None, y=None, r=None, c=None):
        if r is None:
            r = random.randint(s.R_MIN, s.R_MAX)
        if x is None:
            x = random.randint(0, self.w)
        if y is None:
            y = random.randint(0, self.h)
        if c is None:
            col = random.choice(s.COLS)
        
        new_c = Circle(x, y, r, col)

        for c in self.circles:
            if self.intersect(new_c, c):
                return False
                
        print("Found a nice spot for this cool circle!")
        return new_c
        
    def spawn(self, c):
        self.circles.append(c)

    def render(self):
        for c in self.circles:
            self.draw_circle(c)
        
grid = Grid(s.W, s.H, s.BG)

circles = [grid.try_fill() for _ in range(10)]

def log_g(i):
    g = 1 / (s.K * math.log(i + 1, 10))
    
    return g

def bin_g(i):
    denom = 2 + (3 * i) + (-3 * (i**2)) + (i ** 3)
    g = 1 / math.log(s.K * denom, 10)
    
    return g

def lin_g(i):
    return 100 / (i+1)

def unit_g(i):
    
    return 1

curr_r = s.INIT_R
g = log_g

for i in range(1, s.N):
    c = False
    attempts = 0
    while c == False and attempts < s.ATTEMPT_CUTOFF:
        c = grid.try_fill(r=curr_r)
        attempts += 1

    if attempts < s.ATTEMPT_CUTOFF:
        grid.spawn(c.copy())
    else:
        err = "Failed to fit circle %d of size %d"
        print(err % (i, curr_r))

    curr_r = int(s.INIT_R * g(i))
        
        
grid.render()
grid.img.show()
