import sys
import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

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

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

t_clicked, h_clicked = False, False
n1_clicked, n2_clicked, n3_clicked, n4_clicked = False, False, False, False
texture1, texture2, texture3 = Image.open("tekstura.tga"), Image.open("tom.tga"), Image.open("lava.tga")

verticesArray, normalArray = None, None
N = 20


# kwadrat 2D z teksturą
def drawSquare():

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, texture1.size[0], texture1.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, texture1.tobytes("raw", "RGB", 0, -1)
    )

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(4.0, -4.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(4.0, 4.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-4.0, 4.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-4.0, -4.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(4.0, -4.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-4.0, 4.0, 0.0)
    glEnd()


# ostrosłup 3D z teksturą + możliwość ukrycia jednej ściany (przycisk H)
def drawPyramid():

    global h_clicked

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-4.0, -4.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(4.0, -4.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 4.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-4.0, 4.0, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-4.0, -4.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 4.0)
    glEnd()

    if h_clicked:
        glBegin(GL_TRIANGLES)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(4.0, 4.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 4.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-4.0, 4.0, 0.0)
        glEnd()
    else:
        glBegin(GL_TRIANGLES)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(4.0, 4.0, 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-4.0, 4.0, 0.0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0.0, 0.0, 4.0)
        glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(4.0, -4.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(4.0, 4.0, 0.0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(0.0, 0.0, 4.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-4.0, -4.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-4.0, 4.0, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(4.0, -4.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(4.0, -4.0, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-4.0, 4.0, 0.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(4.0, 4.0, 0.0)
    glEnd()


# zmiana tekstur (przełączanie przyciskiem T)
def switchTexture(var):

    global t_clicked
    global texture1, texture2

    if var == 1:

        if t_clicked:
            glTexImage2D(
                GL_TEXTURE_2D, 0, 3, texture2.size[0], texture2.size[1], 0,
                GL_RGB, GL_UNSIGNED_BYTE, texture2.tobytes("raw", "RGB", 0, -1)
            )
        else:
            glTexImage2D(
                GL_TEXTURE_2D, 0, 3, texture1.size[0], texture1.size[1], 0,
                GL_RGB, GL_UNSIGNED_BYTE, texture1.tobytes("raw", "RGB", 0, -1)
            )

    if var == 2:

        if t_clicked:
            glTexImage2D(
                GL_TEXTURE_2D, 0, 3, texture2.size[0], texture2.size[1], 0,
                GL_RGB, GL_UNSIGNED_BYTE, texture2.tobytes("raw", "RGB", 0, -1)
            )
        else:
            glTexImage2D(
                GL_TEXTURE_2D, 0, 3, texture3.size[0], texture3.size[1], 0,
                GL_RGB, GL_UNSIGNED_BYTE, texture3.tobytes("raw", "RGB", 0, -1)
            )


# tworzenie tablicy współrzędnych jajka (lab3)
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


# jajko z nałożoną teksturą
def drawEgg():

    for i in range(0, N - 1):
        for j in range(0, N - 1):

            if i < N / 2:

                glBegin(GL_TRIANGLES)
                glNormal3fv(normalArray[i][j + 1])
                glTexCoord2f((j + 1) / N, 0.1 + 2 * i / N)
                glVertex3f(verticesArray[i][j + 1][0],
                           verticesArray[i][j + 1][1],
                           verticesArray[i][j + 1][2])
                glNormal3fv(normalArray[i][j])
                glTexCoord2f(j / N, 0.1 + 2 * i / N)
                glVertex3f(verticesArray[i][j][0],
                           verticesArray[i][j][1],
                           verticesArray[i][j][2])
                glNormal3fv(normalArray[i + 1][j])
                glTexCoord2f(j / N, 0.1 + 2 * (i + 1) / N)
                glVertex3f(verticesArray[i + 1][j][0],
                           verticesArray[i + 1][j][1],
                           verticesArray[i + 1][j][2])
                glEnd()

                glBegin(GL_TRIANGLES)
                glNormal3fv(normalArray[i][j + 1])
                glTexCoord2f((j + 1) / N, 0.1 + 2 * (i) / N)
                glVertex3f(verticesArray[i][j + 1][0],
                           verticesArray[i][j + 1][1],
                           verticesArray[i][j + 1][2])
                glNormal3fv(normalArray[i + 1][j])
                glTexCoord2f(j / N, 0.1 + 2 * (i + 1) / N)
                glVertex3f(verticesArray[i + 1][j][0],
                           verticesArray[i + 1][j][1],
                           verticesArray[i + 1][j][2])
                glNormal3fv(normalArray[i + 1][j + 1])
                glTexCoord2f((j + 1) / N, 0.1 + 2 * (i + 1) / N)
                glVertex3f(verticesArray[i + 1][j + 1][0],
                           verticesArray[i + 1][j + 1][1],
                           verticesArray[i + 1][j + 1][2])
                glEnd()

            else:
                glBegin(GL_TRIANGLES)
                glNormal3fv(normalArray[i + 1][j])
                glTexCoord2f(j / N, 1 - 2 * (i + 1) / N)
                glVertex3f(verticesArray[i + 1][j][0],
                           verticesArray[i + 1][j][1],
                           verticesArray[i + 1][j][2])
                glNormal3fv(normalArray[i][j])
                glTexCoord2f(j / N, 1 - 2 * i / N)
                glVertex3f(verticesArray[i][j][0],
                           verticesArray[i][j][1],
                           verticesArray[i][j][2])
                glNormal3fv(normalArray[i][j + 1])
                glTexCoord2f((j + 1) / N, 1 - 2 * i / N)
                glVertex3f(verticesArray[i][j + 1][0],
                           verticesArray[i][j + 1][1],
                           verticesArray[i][j + 1][2])
                glEnd()

                glBegin(GL_TRIANGLES)
                glNormal3fv(normalArray[i + 1][j + 1])
                glTexCoord2f((j + 1) / N, 1 - 2 * (i + 1) / N)
                glVertex3f(verticesArray[i + 1][j + 1][0],
                           verticesArray[i + 1][j + 1][1],
                           verticesArray[i + 1][j + 1][2])
                glNormal3fv(normalArray[i + 1][j])
                glTexCoord2f(j / N, 1 - 2 * (i + 1) / N)
                glVertex3f(verticesArray[i + 1][j][0],
                           verticesArray[i + 1][j][1],
                           verticesArray[i + 1][j][2])
                glNormal3fv(normalArray[i][j + 1])
                glTexCoord2f((j + 1) / N, 1 - 2 * i / N)
                glVertex3f(verticesArray[i][j + 1][0],
                           verticesArray[i][j + 1][1],
                           verticesArray[i][j + 1][2])
                glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    createVertices()


def shutdown():
    pass


def render(time):
    global theta
    global n1_clicked, n2_clicked, n3_clicked, n4_clicked

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle

    glRotatef(theta, 0.0, 1.0, 0.0)

    if n1_clicked:
        # 3.0
        drawSquare()

    if n2_clicked:
        # 3.5 4.0
        drawPyramid()

    if n3_clicked:
        # 4.5
        switchTexture(1)
        drawPyramid()

    if n4_clicked:
        # 5.0
        switchTexture(2)
        drawEgg()

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
    global t_clicked, h_clicked
    global n1_clicked, n2_clicked, n3_clicked, n4_clicked

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_T and action == GLFW_PRESS:
        t_clicked = not t_clicked
    if key == GLFW_KEY_H and action == GLFW_PRESS:
        h_clicked = not h_clicked

    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        n1_clicked = not n1_clicked
        n2_clicked, n3_clicked, n4_clicked = False, False, False
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        n2_clicked = not n2_clicked
        n1_clicked, n3_clicked, n4_clicked = False, False, False
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        n3_clicked = not n3_clicked
        n1_clicked, n2_clicked, n4_clicked = False, False, False
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        n4_clicked = not n4_clicked
        n1_clicked, n2_clicked, n3_clicked = False, False, False


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

    window = glfwCreateWindow(400, 400, "przyciski 1-4: zadania", None, None)
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
