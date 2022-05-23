import numpy as np
import random
import math
import sys
import style as s
from PIL import Image, ImageDraw

class Circle:
    def __init__(self, x, y, r, c):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        self.fill = c[0]
        self.border = c[1]
        
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
        self.drw.ellipse([x1+s.B, y1+s.B, x2-s.B, y2-s.B], fill=c.fill)

    def draw_border(self, c):
        x1 = c.x - c.r
        y1 = c.y - c.r
        x2 = c.x + c.r
        y2 = c.y + c.r
        self.drw.ellipse([x1, y1, x2, y2], fill=c.border)
        

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
                
        return new_c
        
    def spawn(self, c):
        self.circles.append(c)

    def render(self):
        for c1 in self.circles:
            self.draw_border(c1)
        for c2 in self.circles:
            self.draw_circle(c2)
        
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
    return 1 - ((1 / (s.K * s.N + 1)) * i)

def unit_g(i):
    
    return 1

def inv_exp_g(i):
    term = 1 - (1 / (((1000 * s.N) - 1) * s.K)) * i ** 2
    return term


curr_r = s.INIT_R
g = lin_g

BAR = "▂"
B_LEN = 80

print("Generating image...")

for i in range(1, s.N):
    c = False
    attempts = 0

    complete = int(i // (s.N / B_LEN)) + 1

    sys.stdout.write("\033[92m")
    sys.stdout.write(BAR * complete)
    sys.stdout.write("\033[90m")
    sys.stdout.write(BAR * (B_LEN - complete))
    sys.stdout.write("\b" * B_LEN)
    sys.stdout.flush()
                
    while c == False and attempts < s.ATTEMPT_CUTOFF:
        c = grid.try_fill(r=curr_r)
        attempts += 1

    if attempts < s.ATTEMPT_CUTOFF:
        grid.spawn(c.copy())

    curr_r = int(s.INIT_R * g(i))


print("\nRendering image...")
grid.render()
grid.img.show()
grid.img.save("img.png")
