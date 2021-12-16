import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

attributes = -1


# rodzaje oświetlenia pierwszego źródła światła
light_ambient = [0.0, 0.3, 0.2, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

# rodzaje oświetlenia drugiego źródła światła
light_ambient2 = [0.0, 0.0, 0.0, 1.0]
light_diffuse2 = [0.0, 0.0, 1.0, 1.0]
light_specular2 = [1.0, 1.0, 1.0, 1.0]
light_position2 = [5.0, 5.0, -5.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


# ZMIANA ATRYBUTÓW ŹRÓDEŁ ŚWIATŁA
def change_attributes(increase):
    global attributes
    global light_ambient2, light_diffuse2, light_specular2

    # 0, 1, 2 - ambient
    if attributes in [0, 1, 2]:
        if increase:
            if light_ambient2[attributes % 3] <= 0.9:
                light_ambient2[attributes % 3] += 0.1
            print(f"ambient[{attributes % 3}] = {light_ambient2[attributes % 3]}")
        else:
            if light_ambient2[attributes % 3] >= 0.1:
                light_ambient2[attributes % 3] -= 0.1
            print(f"ambient[{attributes % 3}] = {light_ambient2[attributes % 3]}")

        glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient2)

    # 3, 4, 5 - diffuse
    elif attributes in [3, 4, 5]:
        if increase:
            if light_diffuse2[attributes % 3] <= 0.9:
                light_diffuse2[attributes % 3] += 0.1
            print(f"diffuse[{attributes % 3}] = {light_diffuse2[attributes % 3]}")
        else:
            if light_diffuse2[attributes % 3] >= 0.1:
                light_diffuse2[attributes % 3] -= 0.1
            print(f"diffuse[{attributes % 3}] = {light_diffuse2[attributes % 3]}")

        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse2)

    # 6, 7, 8 - specular
    elif attributes in [6, 7, 8]:
        if increase:
            if light_specular2[attributes % 3] <= 0.9:
                light_specular2[attributes % 3] += 0.1
            print(f"specular[{attributes % 3}] = {light_specular2[attributes % 3]}")
        else:
            if light_specular2[attributes % 3] >= 0.1:
                light_specular2[attributes % 3] -= 0.1
            print(f"specular[{attributes % 3}] = {light_specular2[attributes % 3]}")

        glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular2)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # pierwsze źródło światła
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # drugie źródło światła
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular2)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position2)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

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

    global attributes

    # ZMIENIANIE ATRYBÓTÓW DRUGIEGO ŹRÓDŁA ŚWIATŁA
    # 0 - 8 -> wybieramy indeks atrybutów
    # strzałki UP i DOWN -> zwiększają / zmniejszają wartości
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        attributes = 0
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        attributes = 1
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        attributes = 2
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        attributes = 3
    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        attributes = 4
    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        attributes = 5
    if key == GLFW_KEY_7 and action == GLFW_PRESS:
        attributes = 6
    if key == GLFW_KEY_8 and action == GLFW_PRESS:
        attributes = 7
    if key == GLFW_KEY_9 and action == GLFW_PRESS:
        attributes = 8
    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        change_attributes(True)
    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        change_attributes(False)

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


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
