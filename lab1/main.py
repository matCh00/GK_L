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

    draw(-90, -90, 40, 40)

    random.seed(8)
    c1 = random.randint(0, 1)
    c2 = random.randint(0, 1)
    c3 = random.randint(0, 1)
    d = random.uniform(0.5, 2.5)
    draw2(0, -90, 40, 40, d, c1, c2, c3)

    #glClear(GL_COLOR_BUFFER_BIT)  # wyczyszczenie poprzednich obrazków

    #drawFractal1(0, 0, 200, 200)

    #drawFractal2(0, 0, 75, 75)

    #drawFractal2(-75, 75, 25, 25)

    glFlush()


def draw(x, y, a, b):
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x, y)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, y + b)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(x + a, y)
    glEnd()


def draw2(x, y, a, b, d, c1, c2, c3):
    glBegin(GL_TRIANGLES)
    glColor3f(c1, c2, c3)
    glVertex2f(x * d, y * d)
    glColor3f(c2, c3, c1)
    glVertex2f(x * d, (y + b) * d)
    glColor3f(c3, c1, c2)
    glVertex2f((x + a) * d, y * d)
    glEnd()


def drawFractal1(x, y, a, b):
    a /= 2
    b /= 2
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a, y + b)
    glVertex2f(x + a, y - b)
    glVertex2f(x + a, y + b)
    glEnd()

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a, y - b)
    glVertex2f(x - a, y + b)
    glVertex2f(x + a, y - b)
    glEnd()


def drawFractal2(x, y, a, b):  # (x,y) to środek, a i b to wymiary
    a /= 2
    b/= 2
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a, y + b)
    glVertex2f(x + a, y - b)
    glVertex2f(x + a, y + b)
    glEnd()

    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_TRIANGLES)
    glVertex2f(x - a, y - b)
    glVertex2f(x - a, y + b)
    glVertex2f(x + a, y - b)
    glEnd()

    # drawFractal2(x, y, a, b, r * r)


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
