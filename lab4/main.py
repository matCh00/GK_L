import math
import sys

import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

phi = 0.0
theta = 0.0
delta_x, delta_y = 0, 0
pix2angle = 1.0
scale = 1.0

left_mouse_button_pressed, right_mouse_button_pressed = 0, 0
mouse_x_pos_old, mouse_y_pos_old = 0, 0
delta_x, delta_y = 0, 0


# obliczanie kątów (obracanie obiektu)
def calculate_angles_on_left_mouse_button_pressed(scale, theta, phi):

    if left_mouse_button_pressed:

        # zmiana theta (obrót wokół osi Y)
        theta += delta_x * pix2angle

        # zmiana phi (obrót wokół osi X)
        phi += delta_y * pix2angle

    # skalowanie
    if right_mouse_button_pressed:
        scale += 0.0055 * delta_y

    return scale, theta, phi


# obliczanie radianów (obracanie obiektu)
def calculate_radians_on_left_mouse_button_pressed(scale, theta, phi):

    if left_mouse_button_pressed:

        # zmiana theta (obrót wokół osi Y)
        theta += delta_x * pix2radian

        # zmiana phi (obrót wokół osi X)
        phi += delta_y * pix2radian

    # skalowanie
    if right_mouse_button_pressed:
        scale += 0.0555 * delta_y

    phi %= (2 * math.pi)
    theta %= (2 * math.pi)

    return scale, theta, phi


# obliczanie x, y, z (poruszanie kamery)
def calculate_xyz(scale, phi, theta):

    x_eye = scale * math.cos(theta) * math.cos(phi)
    y_eye = scale * math.sin(phi)
    z_eye = scale * math.sin(theta) * math.cos(phi)

    return x_eye, y_eye, z_eye


# obracanie wokół osi X i Y oraz skalowanie obiektu
def rotate_and_scale():
    global theta, phi, scale

    scale, theta, phi = calculate_angles_on_left_mouse_button_pressed(scale, theta, phi)

    if scale < 0.3:
        scale = 0.3
    elif scale > 1.7:
        scale = 1.7

    # obracanie wokół osi Y
    glRotatef(theta, 0.0, 1.0, 0.0)

    # obracanie wokół osi X
    glRotatef(phi, 1.0, 0.0, 0.0)

    # skalowanie
    glScalef(scale, scale, scale)


# poruszanie kamerą wokół modelu
def move_camera():
    global theta, phi, scale

    scale, theta, phi = calculate_radians_on_left_mouse_button_pressed(scale, theta, phi)

    if scale < 0.01:
        scale = 0.01
    elif scale > 20:
        scale = 20

    x, y, z = calculate_xyz(scale, phi, theta)

    if math.pi / 2 < phi < 3 * math.pi / 2:
        top = -1
    else:
        top = 1

    gluLookAt(x, y, z, 0, 0, 0, 0, top, 0)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta
    global phi
    global scale

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    # 3.0
    # 3.5
    rotate_and_scale()

    # 4.0
    # 4.5
    # move_camera()

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle, pix2radian
    pix2angle = 360.0 / width
    pix2radian = 2 * math.pi / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    # obrót wokół osi y
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    # obrót wokół osi X
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    # obsługa PPM
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
