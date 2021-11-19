import random
import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


# obrót
def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


# rysowanie linii XYZ
def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


# wstęp do tworzenia jajek
def createVertices(N):

    # tablica wierzchołków
    vertices = np.zeros((N, N, 3))

    # N-elementowe tablice wartości dla u i v
    uArray = [u / (N - 1) for u in range(0, N)]  # <0,1>
    vArray = [v / (N - 1) for v in range(0, N)]  # <0,1>

    # obliczenie x, y, z dla każdej pary (u v)
    for i in range(0, N):
        for j in range(0, N):

            # wartości x
            vertices[i][j][0] = ((-90 * uArray[i] ** 5 + 225 * uArray[i] ** 4 - 270 * uArray[i] ** 3
                                   + 180 * uArray[i] ** 2 - 45 * uArray[i]) * np.cos(np.pi * vArray[j]))
            # wartości y
            vertices[i][j][1] = (160 * uArray[i] ** 4 - 320 * uArray[i] ** 3 + 160 * uArray[i] ** 2) - 0.05

            # wartości z
            vertices[i][j][2] = ((-90 * uArray[i] ** 5 + 225 * uArray[i] ** 4 - 270 * uArray[i] ** 3
                                   + 180 * uArray[i] ** 2 - 45 * uArray[i]) * np.sin(np.pi * vArray[j]))

    return vertices


# funkcja rysująca jajko z punktów
def eggOfPoints():

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)

    # tworzenie punktów o współrzędnych (x,y,z)
    for i in range(0, N):
        for j in range(0, N):
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

    glEnd()


# funkcja rysująca jajko z linii
def eggOfLines():

    glColor3f(1.0, 1.0, 1.0)

    for i in range(0, N - 1):
        for j in range(0, N - 1):

            # łączenie elementów (i,j) z elementami (i+1,j)
            glBegin(GL_LINES)
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex3f(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
            glEnd()

            # łączenie elementów (i,j) z elementami (i,j+1)
            glBegin(GL_LINES)
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex3f(vertices[i][j + 1][0], vertices[i][j + 1][1], vertices[i][j + 1][2])
            glEnd()


# funkcja rysująca jajko z trójkątów
def eggOfTriangles():

    for i in range(0, N - 1):
        for j in range(0, N - 1):

            glBegin(GL_TRIANGLES)

            # każdy trójkąt ma inny kolor
            # połaczenie elementu (i,j) z elementami (i+1,j) oraz (i,j+1)
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glColor3f(colors[i + 1][j][1], colors[i + 1][j][2], colors[i + 1][j][3])
            glVertex3f(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
            glColor3f(colors[i][j + 1][2], colors[i][j + 1][3], colors[i][j + 1][4])
            glVertex3f(vertices[i][j + 1][0], vertices[i][j + 1][1], vertices[i][j + 1][2])
            glEnd()

            glBegin(GL_TRIANGLES)

            # każdy trójkąt ma inny kolor
            # rysowanie trójkąta dopełniającego -> połaczenie elementu (i+1,j+1) z elementami (i+1,j) oraz (i,j+1)
            glColor3f(colors[i + 1][j][3], colors[i + 1][j][4], colors[i + 1][j][5])
            glVertex3f(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
            glColor3f(colors[i][j + 1][4], colors[i][j + 1][5], colors[i][j + 1][6])
            glVertex3f(vertices[i][j + 1][0], vertices[i][j + 1][1], vertices[i][j + 1][2])
            glColor3f(colors[i + 1][j + 1][5], colors[i + 1][j + 1][6], colors[i + 1][j + 1][7])
            glVertex3f(vertices[i + 1][j + 1][0], vertices[i + 1][j + 1][1], vertices[i + 1][j + 1][2])
            glEnd()

            # glBegin(GL_TRIANGLES)
            #
            # # usunięcie czarnej kreski
            # if j == N - 2:
            #     glColor3f(colors[i][0][0], colors[i][0][1], colors[i][0][2])
            # else:
            #     glColor3f(colors[i][j + 1][0], colors[i][j + 1][1], colors[i][j + 1][2])
            # glVertex3f(vertices[i][j + 1][0], vertices[i][j + 1][1], vertices[i][j + 1][2])
            # glColor3f(colors[i + 1][j][0], colors[i + 1][j][1], colors[i + 1][j][2])
            # glVertex3f(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
            #
            # if j == N - 2:
            #     glColor3f(colors[i + 1][0][0], colors[i + 1][0][1], colors[i + 1][0][2])
            # else:
            #     glColor3f(colors[i + 1][j + 1][0], colors[i + 1][j + 1][1], colors[i + 1][j + 1][2])
            # glVertex3f(vertices[i + 1][j + 1][0], vertices[i + 1][j + 1][1], vertices[i + 1][j + 1][2])
            # glEnd()


# funkcja rysująca jajko z prymitywów paskowych
def eggOfTriangleStrips():

    glBegin(GL_TRIANGLE_STRIP)

    for i in range(N - 1):
        for j in range(N - 1):

            # każdy trójkąt ma inny kolor
            # budowanie warstwy modelu za pomocą jednego paska
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glColor3f(colors[i][j + 1][0], colors[i][j + 1][1], colors[i][j + 1][2])
            glVertex3f(vertices[i][j + 1][0], vertices[i][j + 1][1], vertices[i][j + 1][2])
            glColor3f(colors[i + 1][j][0], colors[i + 1][j][1], colors[i + 1][j][2])
            glVertex3f(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
            glColor3f(colors[i + 1][j + 1][0], colors[i + 1][j + 1][1], colors[i + 1][j + 1][2])
            glVertex3f(vertices[i + 1][j + 1][0], vertices[i + 1][j + 1][1], vertices[i + 1][j + 1][2])
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # obracanie obiektu
    spin(time * 180 / 3.1415)

    # rysowanie osi x,y,z
    axes()

    # eggOfPoints()

    # eggOfLines()

    # eggOfTriangles()

    eggOfTriangleStrips()

    glFlush()


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():

    global N
    global vertices
    global colors

    # ilość wierzchołków
    N = 30

    # tablica wierzchołków
    vertices = createVertices(N)

    # tablica losowych kolorów
    colors = np.zeros((N, N, 8))
    for i in range(0, N):
        for j in range(0, N - 1):
            for k in range(0, 8):
                colors[i][j][k] = random.random()  # <0,1>


    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()