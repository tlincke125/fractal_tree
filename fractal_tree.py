import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import line
import math
import sys

    

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


class Line:
    def __init__(self, x0: float, x1: float, y0: float, y1: float):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def draw(self, pixels, color = 255):
        x0_ = constrain(int(round(self.x0)), 0, pixels.shape[1] - 1)
        x1_ = constrain(int(round(self.x1)), 0, pixels.shape[1] - 1)
        y0_ = constrain(int(round(self.y0)), 0, pixels.shape[0] - 1)
        y1_ = constrain(int(round(self.y1)), 0, pixels.shape[0] - 1)



        if x1_ >= pixels.shape[1]:
            x1_ = pixels.shape[1] - 1

        if x0_ < 0:
            x0_ = 0

        if y1_ >= pixels.shape[0]:
            y1_ = pixels.shape[0] - 1

        if y0_ < 0:
            y0_ = 0

        rr, cc = line(y0_, x0_, y1_, x1_)

        pixels[rr, cc] = color 


class Fractal:
    def __init__(self, height, width):
        self.lines = []
        self.height = height
        self.width = width

        self.pixels = np.full((height, width), 0, dtype=np.uint16)

        self.origin = (3 * height / 4, width / 2)


    def execute(self, itterations, frac_1, frac_2, angle_1=90, angle_2=90):

        angle_1 = np.radians(angle_1)
        angle_2 = np.radians(angle_2)

        self.pixels = np.full((self.height, self.width), 0, dtype=np.uint16)

        self.draw_next(self.width / 2 - 1, self.origin[1] - 1, self.height - 1, self.origin[0] - 1, itterations, frac_1 = frac_1, frac_2 = frac_2, angle_1 = angle_1, angle_2 = angle_2)


    ##
    # @brief appends a new line to lines.
    #
    # if plane = 'x':
    #   draw a horizontal line
    # if plane = 'y':
    #   draw a vertical line
    #
    # num is the number iteration, decrements recursively
    def draw_next(self, x0, x1, y0, y1, num, frac_1, frac_2, angle_1, angle_2):

        # Recursive break condition
        num = num - 1
        if num <= 0:
            return


        # Starting Vector (to be rotated)
        A = np.array([x1 - x0, y1 - y0]).reshape(2, 1)

        # Rotation about the right
        R1 = np.array([[np.cos(angle_1), -np.sin(angle_1)], [np.sin(angle_1), np.cos(angle_1)]])

        # Rotation about the left (negative angle)
        R2 = np.array([[np.cos(-angle_2), -np.sin(-angle_2)], [np.sin(-angle_2), np.cos(-angle_2)]])
         


        self.lines.append(Line(x0, x1, y0, y1))

        dist = np.sqrt((x1 - x0)**2 + (y1 - y0)**2)


        right = frac_1 * np.matmul(R1, A) + np.array([x1, y1]).reshape(2, 1)
        left = frac_2 * np.matmul(R2, A) + np.array([x1, y1]).reshape(2, 1)

        
        self.draw_next(x1, right[0][0], y1, right[1][0], num, frac_1, frac_2, angle_1, angle_2)
        self.draw_next(x1, left[0][0], y1, left[1][0], num, frac_1, frac_2, angle_1, angle_2)




    def draw(self):
        for line in self.lines:
            line.draw(pixels = self.pixels)

        plt.axis('off')
        plt.imshow(self.pixels, cmap='Greys') 
        plt.show()
        

if __name__ == '__main__':
    f = Fractal(700, 700)


    f.execute(16, 0.7, 0.65, angle_1 = 60, angle_2 = 40)
    f.draw()
