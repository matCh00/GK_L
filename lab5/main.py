import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta, phi = 0.0, 0.0
pix2angle = 1.0
r = 5

verticesArray, normalArray = None, None
N = 20
showNormals = False

left_mouse_button_pressed = 0
mouse_x_pos_old, mouse_y_pos_old = 0, 0
delta_x, delta_y = 0, 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

attributes = -1

# rodzaje oświetlenia pierwszego źródła światła
light_ambient = [0.1, 0.1, 0.0, 1.0]
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
            print(f"ambient[{attributes % 3}] = {round(light_ambient2[attributes % 3], 1)}")
        else:
            if light_ambient2[attributes % 3] >= 0.1:
                light_ambient2[attributes % 3] -= 0.1
            print(f"ambient[{attributes % 3}] = {round(light_ambient2[attributes % 3], 1)}")

        glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient2)

    # 3, 4, 5 - diffuse
    elif attributes in [3, 4, 5]:
        if increase:
            if light_diffuse2[attributes % 3] <= 0.9:
                light_diffuse2[attributes % 3] += 0.1
            print(f"diffuse[{attributes % 3}] = {round(light_diffuse2[attributes % 3], 1)}")
        else:
            if light_diffuse2[attributes % 3] >= 0.1:
                light_diffuse2[attributes % 3] -= 0.1
            print(f"diffuse[{attributes % 3}] = {round(light_diffuse2[attributes % 3], 1)}")

        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse2)

    # 6, 7, 8 - specular
    elif attributes in [6, 7, 8]:
        if increase:
            if light_specular2[attributes % 3] <= 0.9:
                light_specular2[attributes % 3] += 0.1
            print(f"specular[{attributes % 3}] = {round(light_specular2[attributes % 3], 1)}")
        else:
            if light_specular2[attributes % 3] >= 0.1:
                light_specular2[attributes % 3] -= 0.1
            print(f"specular[{attributes % 3}] = {round(light_specular2[attributes % 3], 1)}")

        glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular2)


# PORUSZANIE ŹRÓDŁAMI ŚWIATŁA I ICH WIZUALIZACJA
def visualize_and_move_lights():
    global theta, phi, r
    global light_position, light_position2

    x = r * np.cos(np.radians(theta % 360)) * np.cos(np.radians(phi % 360))
    y = r * np.sin(np.radians(phi % 360))
    z = r * np.sin(np.radians(theta % 360)) * np.cos(np.radians(phi % 360))

    light_position = [-x, y, z, 1.0]
    light_position2 = [x, -y, -z, 1.0]

    # transformacja
    glTranslate(-x, y, z)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # odwrócenie transformacji
    glTranslate(x, -y, -z)

    # transformacja
    glTranslate(x, -y, -z)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glLightfv(GL_LIGHT1, GL_POSITION, light_position2)

    # odwrócenie transformacji
    glTranslate(-x, y, z)


# tworzenie tablicy współrzędnych (lab3)
def createVertices():
    global verticesArray, normalArray, N

    verticesArray = np.zeros((N, N, 3))
    normalArray = np.zeros((N, N, 3))

    uArray = [u / (N - 1) for u in range(0, N)]
    vArray = [v / (N - 1) for v in range(0, N)]

    # obliczenie x, y, z dla każdej pary (u v)
    for i in range(0, N):
        for j in range(0, N):

            # wartości x
            verticesArray[i][j][0] = ((-90 * uArray[i] ** 5
                                       + 225 * uArray[i] ** 4
                                       - 270 * uArray[i] ** 3
                                       + 180 * uArray[i] ** 2
                                       - 45 * uArray[i]) * np.cos(np.pi * vArray[j]))
            # wartości y
            verticesArray[i][j][1] = (160 * uArray[i] ** 4
                                      - 320 * uArray[i] ** 3
                                      + 160 * uArray[i] ** 2) - 4.5

            # wartości z
            verticesArray[i][j][2] = ((-90 * uArray[i] ** 5
                                       + 225 * uArray[i] ** 4
                                       - 270 * uArray[i] ** 3
                                       + 180 * uArray[i] ** 2
                                       - 45 * uArray[i]) * np.sin(np.pi * vArray[j]))

            # wektory normalne (jak ze slajdu)
            x_u = (-450 * uArray[i] ** 4
                   + 900 * uArray[i] ** 3
                   - 810 * uArray[i] ** 2
                   + 360 * uArray[i] - 45) * np.cos(np.pi * vArray[j])

            x_v = np.pi * (90 * uArray[i] ** 5
                           - 225 * uArray[i] ** 4
                           + 270 * uArray[i] ** 3
                           - 180 * uArray[i] ** 2
                           + 45 * uArray[i]) * np.sin(np.pi * vArray[j])

            y_u = (640 * uArray[i] ** 3
                   - 960 * uArray[i] ** 2
                   + 320 * uArray[i])

            z_u = (-450 * uArray[i] ** 4
                   + 900 * uArray[i] ** 3
                   - 810 * uArray[i] ** 2
                   + 360 * uArray[i] - 45) * np.sin(np.pi * vArray[j])

            z_v = -np.pi * (90 * uArray[i] ** 5
                            - 225 * uArray[i] ** 4
                            + 270 * uArray[i] ** 3
                            - 180 * uArray[i] ** 2
                            + 45 * uArray[i]) * np.cos(np.pi * vArray[j])

            if i == 0 or i == N:
                normalArray[i][j] = [0, -1, 0]
                continue
            elif i == N / 2:
                normalArray[i][j] = [0, 1, 0]

            # wektor normalny do powierzchni modelu w punkcie odpowiadającym konkretnym wartościom u i v gdzie
            # gdzie y_v = 0
            normalArray[i][j] = [y_u * z_v - z_u * 0, z_u * x_v - x_u * z_v, x_u * 0 - y_u * x_v]

            # długość wektora
            normalVectorLength = np.sqrt(normalArray[i][j][0] ** 2 + normalArray[i][j][1] ** 2 + normalArray[i][j][2] ** 2)

            # NORMALIZACJA - podzielenie wektora przez jego długość (czyni to go wektorem jednostkowym)
            if i < N / 2:
                normalArray[i][j] = np.divide(normalArray[i][j], normalVectorLength)
            else:
                normalArray[i][j] = np.divide(normalArray[i][j], -normalVectorLength)


# funkcja rysująca jajko z trójkątów (lab3)
# DODANIE WEKTORÓW NORMALNYCH DO MODELU JAJKA
def eggOfTriangles():
    global showNormals

    for i in range(0, N - 1):
        for j in range(0, N - 1):
            glBegin(GL_TRIANGLES)

            glNormal3fv(normalArray[i][j])
            glVertex3f(verticesArray[i][j][0], verticesArray[i][j][1], verticesArray[i][j][2])
            glNormal3fv(normalArray[i + 1][j])
            glVertex3f(verticesArray[i + 1][j][0], verticesArray[i + 1][j][1], verticesArray[i + 1][j][2])
            glNormal3fv(normalArray[i][j + 1])
            glVertex3f(verticesArray[i][j + 1][0], verticesArray[i][j + 1][1], verticesArray[i][j + 1][2])
            glEnd()

            glBegin(GL_TRIANGLES)
            glNormal3fv(normalArray[i + 1][j])
            glVertex3f(verticesArray[i + 1][j][0], verticesArray[i + 1][j][1], verticesArray[i + 1][j][2])
            glNormal3fv(normalArray[i][j + 1])
            glVertex3f(verticesArray[i][j + 1][0], verticesArray[i][j + 1][1], verticesArray[i][j + 1][2])
            glNormal3fv(normalArray[i + 1][j + 1])
            glVertex3f(verticesArray[i + 1][j + 1][0], verticesArray[i + 1][j + 1][1], verticesArray[i + 1][j + 1][2])
            glEnd()

            # WYŚWIETLENIE NORMALNYCH NA MODELU
            if showNormals:
                glBegin(GL_LINES)
                glVertex(verticesArray[i][j])
                glVertex(verticesArray[i][j] + normalArray[i][j])
                glEnd()


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

    createVertices()


def shutdown():
    pass


def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    # glRotatef(theta, 0.0, 1.0, 0.0)
    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 40, 40)
    # gluDeleteQuadric(quadric)

    # jajko
    eggOfTriangles()

    # wizualizacja źródeł światła i poruszanie ich
    visualize_and_move_lights()

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

    global attributes, showNormals

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
    if key == GLFW_KEY_N and action == GLFW_PRESS:
        showNormals = not showNormals

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


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
