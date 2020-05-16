# for 3DSage Simple 3D Modeling Program - OpenGL Tutorial https://www.youtube.com/watch?v=exQ43PFWJBU
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

global cx, cy, cz, cn


class Quads:
    x1 = y1 = z1 = 0
    x2 = y2 = z2 = 0
    x3 = y3 = z3 = 0
    x4 = y4 = z4 = 0
    r = g = b = 0.0
    state = 0
    total = 0


Q = [Quads() for x in range(100)]


def addQuads():
    global cn

    Q[0].state += 1
    if Q[0].state > 4:
        Q[0].state = 1
    st = Q[0].state

    if st in [1]:
        Q[0].total += 1
        cn = Q[0].total
        Q[cn].x1 = cx
        Q[cn].y1 = cy
        Q[cn].z1 = cz
    if st in [1, 2]:
        Q[cn].x2 = cx
        Q[cn].y2 = cy
        Q[cn].z2 = cz
    if st in [1, 2, 3]:
        Q[cn].x3 = cx
        Q[cn].y3 = cy
        Q[cn].z3 = cz
    if st in [1, 2, 3, 4]:
        Q[cn].x4 = cx
        Q[cn].y4 = cy
        Q[cn].z4 = cz


def drawQuads():
    for i in range(Q[0].total + 1):
        glPushMatrix()
        glBegin(GL_QUADS)
        glColor3f(Q[i].r, Q[i].g, Q[i].b)
        glVertex3f(Q[i].x1, Q[i].y1, Q[i].z1)
        glVertex3f(Q[i].x2, Q[i].y2, Q[i].z2)
        glVertex3f(Q[i].x3, Q[i].y3, Q[i].z3)
        glVertex3f(Q[i].x4, Q[i].y4, Q[i].z4)
        glEnd()
        glPopMatrix()


def theCube():
    global cx, cy, cz
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(cx, cy, cz)
    glutSolidCube(0.4)
    glPopMatrix()


def drawGrid():
    for i in range(40):
        glPushMatrix()
        if i < 20:
            glTranslatef(0, 0, i)
        else:
            glTranslatef(i - 20, 0, 0)
            glRotatef(-90, 0, 1, 0)
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        # glLineWidth(1.0)
        glVertex3f(0.0, -0.1, 0.0)
        glVertex3f(19.0, -0.1, 0.0)
        glEnd()
        glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-13.0, 0.0, -45)
    glRotatef(40, 1, 1, 0)

    drawGrid()
    drawQuads()
    theCube()
    glutSwapBuffers()


def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(35, 1.0, 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.2, 0.2, 0.2, 1)


def keyboard(*args):
    global cx, cy, cz
    key = args[0]
    if key == b'w':
        cz -= 1
    elif key == b's':
        cz += 1
    elif key == b'a':
        cx -= 1
    elif key == b'd':
        cx += 1
    elif key == b'q':
        cy -= 1
    elif key == b'z':
        cy += 1
    elif key == b'\x20':
        addQuads()
    elif key == b'r':
        Q[cn].r = 1
        Q[cn].g = 0
        Q[cn].b = 0
    elif key == b'g':
        Q[cn].r = 0
        Q[cn].g = 1
        Q[cn].b = 0
    elif key == b'b':
        Q[cn].r = 0
        Q[cn].g = 0
        Q[cn].b = 1
    elif key == b'y':
        Q[cn].r = 1
        Q[cn].g = 1
        Q[cn].b = 0

    glutPostRedisplay()


def main():
    global cx, cy, cz, cn
    cx = cy = cz = cn = 0

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow("")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    init()

    glutMainLoop()
    return 0


main()
