import math
import sys
import random
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):

    glClear(GL_COLOR_BUFFER_BIT)

    # simpleTriangle()
    # drawTriangle(-100, -100, 100)

    # drawRectangle(-50, 50, 100, 100)

    # random.seed(8)
    # c1 = random.randint(0, 1)
    # c2 = random.randint(0, 1)
    # c3 = random.randint(0, 1)
    # d = random.uniform(0.5, 2.5)
    # deformatedTriangle(0, 0, 40, 40, d, c1, c2, c3)

    # drawFractal1(-100, 100, 200, 200, 5)

    drawFractal2(0, -90, 30, math.pi/2.0, 0.8, math.pi/6.0, 12)

    glFlush()


# prostokąt z 6 punktów
def simpleTriangle():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

    glFlush()


# prostokąt z 4 punktów, (x,y) to współżędne lewego górnego rogu
def drawRectangle(x, y, a, b):

    if x < -100:
        x = -100
    if y > 100:
        y = 100
    if x + b > 100:
        x = 100 - b
    if y - a < -100:
        y = -100 + a

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(x, y)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x, y - b)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x + a, y - b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 0.0)
    glVertex2f(x, y)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x + a, y)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x + a, y - b)
    glEnd()


# trójkąt, (a,b) to współżędne lewego dolnego rogu
def drawTriangle(a, b, d):

    glBegin(GL_TRIANGLES)
    glColor3f(0.8, 0.5, 0.1)
    glVertex2f(a, b)
    glColor3f(0.2, 0.0, 0.4)
    glVertex2f(a + d, b)
    glColor3f(1.0, 0.0, 0.3)
    glVertex2f(a, d + b)
    glEnd()


# losowy trójkąt, (x,y) to współżędne lewego dolnego rogu
def deformatedTriangle(x, y, a, b, d, c1, c2, c3):

    glBegin(GL_TRIANGLES)
    glColor3f(c1, c2, c3)
    glVertex2f(x * d, y * d)
    glColor3f(c2, c3, c1)
    glVertex2f(x * d, (y + b) * d)
    glColor3f(c3, c1, c2)
    glVertex2f((x + a) * d, y * d)
    glEnd()


# dywan Sierpińskiego
def drawFractal1(x, y, a, b, level):

    k = 3.0

    if level > 0:
        new_x = x + (b / k)
        new_y = y - (a / k)
        new_a = a / k
        new_b = b / k
        drawRectangle(new_x, new_y, new_a, new_b)

        if level > 1:
            for i in range(0, 3):
                for j in range(0, 3):
                    if i == 1 and j == 1:
                        continue
                    drawFractal1(x + (new_b * i), y - (new_a * j), new_a, new_b, level - 1)


def fractal2(x, y, len, angle):

    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + len * math.cos(angle), y + len * math.sin(angle))
    glEnd()


# inny fraktal
def drawFractal2(x, y, len, angle, len_div, angle_dif, depth):

    fractal2(x, y, len, angle)

    if depth <= 0:
        return

    # lewa gałąź
    drawFractal2(x + len * math.cos(angle), y + len * math.sin(angle), len * len_div, angle - angle_dif, len_div, angle_dif, depth - 1)

    # prawa gałąź
    drawFractal2(x + len * math.cos(angle), y + len * math.sin(angle), len * len_div, angle + angle_dif, len_div, angle_dif, depth - 1)


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)
    startup()

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()
    glfwTerminate()


if __name__ == '__main__':
    main()
