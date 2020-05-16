# https://www.opengl.org/archives/resources/code/samples/glut_examples/examples/examples.html


''' Copyright (c) Mark J. Kilgard, 1994. '''

'''*
 * (c) Copyright 1993, Silicon Graphics, Inc.
 * ALL RIGHTS RESERVED 
 * Permission to use, copy, modify, and distribute this software for 
 * any purpose and without fee is hereby granted, provided that the above
 * copyright notice appear in all copies and that both the copyright notice
 * and this permission notice appear in supporting documentation, and that 
 * the name of Silicon Graphics, Inc. not be used in advertising
 * or publicity pertaining to distribution of the software without specific,
 * written prior permission. 
 *
 * THE MATERIAL EMBODIED ON THIS SOFTWARE IS PROVIDED TO YOU "AS-IS"
 * AND WITHOUT WARRANTY OF ANY KIND, EXPRESS, IMPLIED OR OTHERWISE,
 * INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY OR
 * FITNESS FOR A PARTICULAR PURPOSE.  IN NO EVENT SHALL SILICON
 * GRAPHICS, INC.  BE LIABLE TO YOU OR ANYONE ELSE FOR ANY DIRECT,
 * SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY
 * KIND, OR ANY DAMAGES WHATSOEVER, INCLUDING WITHOUT LIMITATION,
 * LOSS OF PROFIT, LOSS OF USE, SAVINGS OR REVENUE, OR THE CLAIMS OF
 * THIRD PARTIES, WHETHER OR NOT SILICON GRAPHICS, INC.  HAS BEEN
 * ADVISED OF THE POSSIBILITY OF SUCH LOSS, HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE
 * POSSESSION, USE OR PERFORMANCE OF THIS SOFTWARE.
 * 
 * US Government Users Restricted Rights 
 * Use, duplication, or disclosure by the Government is subject to
 * restrictions set forth in FAR 52.227.19(c)(2) or subparagraph
 * (c)(1)(ii) of the Rights in Technical Data and Computer Software
 * clause at DFARS 252.227-7013 and/or in similar or successor
 * clauses in the FAR or the DOD or NASA FAR Supplement.
 * Unpublished-- rights reserved under the copyright laws of the
 * United States.  Contractor/manufacturer is Silicon Graphics,
 * Inc., 2011 N.  Shoreline Blvd., Mountain View, CA 94039-7311.
 *
 * OpenGL(TM) is a trademark of Silicon Graphics, Inc.
 '''

from enum import Enum
from math import *
from random import uniform, seed

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def rand():
    return uniform(0, 1)


class StarsSpeed(Enum):
    NORMAL = 0
    WEIRD = 1


class StarsType(Enum):
    STREAK = 0
    CIRCLE = 1


class starRec(object):
    type = StarsType.STREAK
    x = [0.0] * 2
    y = [0.0] * 2
    z = [0.0] * 2
    offsetX = 0
    offsetY = 0
    offsetR = 0
    rotation = 0


class Variables:
    MAXSTARS = 400
    MAXPOS = 10000
    MAXWARP = 10
    MAXANGLES = 6000

    doubleBuffer = GL_TRUE

    windW = 300
    windH = 300

    flag = StarsSpeed.NORMAL
    starCount = MAXSTARS % 2
    speed = 1.0
    nitro = 0

    stars = [starRec() for _ in range(MAXSTARS)]
    sinTable = [0.0 for _ in range(MAXANGLES)]


variables = Variables()


def Sin(angle):
    return variables.sinTable[angle]


def Cos(angle):
    return variables.sinTable[(angle + (variables.MAXANGLES / 4)) % variables.MAXANGLES]


def NewStar(n, d):
    if rand() % 4 == 0:
        variables.stars[n].type = StarsType.CIRCLE
    else:
        variables.stars[n].type = StarsType.STREAK

    variables.stars[n].x[0] = (rand() % variables.MAXPOS - variables.MAXPOS / 2)
    variables.stars[n].y[0] = (rand() % variables.MAXPOS - variables.MAXPOS / 2)
    variables.stars[n].z[0] = (rand() % variables.MAXPOS + d)
    variables.stars[n].x[1] = variables.stars[n].x[0]
    variables.stars[n].y[1] = variables.stars[n].y[0]
    variables.stars[n].z[1] = variables.stars[n].z[0]
    if rand() % 4 == 0 and variables.flag == StarsSpeed.WEIRD:
        variables.stars[n].offsetX = (rand() % 100 - 100 / 2)
        variables.stars[n].offsetY = (rand() % 100 - 100 / 2)
        variables.stars[n].offsetR = (rand() % 25 - 25 / 2)
    else:
        variables.stars[n].offsetX = 0.0
        variables.stars[n].offsetY = 0.0
        variables.stars[n].offsetR = 0.0


def RotatePoint(x, y, rotation):
    tmpX = x * Cos(rotation) - y * Sin(rotation)
    tmpY = y * Cos(rotation) + x * Sin(rotation)
    return tmpX, tmpY


def MoveStars():
    offset = variables.speed * 60.0

    for n in range(variables.starCount):
        variables.stars[n].x[1] = variables.stars[n].x[0]
        variables.stars[n].y[1] = variables.stars[n].y[0]
        variables.stars[n].z[1] = variables.stars[n].z[0]
        variables.stars[n].x[0] += variables.stars[n].offsetX
        variables.stars[n].y[0] += variables.stars[n].offsetY
        variables.stars[n].z[0] -= offset
        variables.stars[n].rotation += variables.stars[n].offsetR
        if variables.stars[n].rotation > variables.MAXANGLES:
            variables.stars[n].rotation = 0.0


def StarPoint(n):
    x0 = variables.stars[n].x[0] * variables.windW / variables.stars[n].z[0]
    y0 = variables.stars[n].y[0] * variables.windH / variables.stars[n].z[0]
    x0, y0 = RotatePoint(x0, y0, variables.stars[n].rotation)
    x0 += variables.windW / 2.0
    y0 += variables.windH / 2.0

    if 0.0 <= x0 < variables.windW and y0 >= 0.0 and y0 < variables.windH:
        return GL_TRUE
    else:
        return GL_FALSE


def ShowStar(n):
    x0 = variables.stars[n].x[0] * variables.windW / variables.stars[n].z[0]
    y0 = variables.stars[n].y[0] * variables.windH / variables.stars[n].z[0]
    x0, y0 = RotatePoint(x0, y0, variables.stars[n].rotation)
    x0 += variables.windW / 2.0
    y0 += variables.windH / 2.0

    if 0.0 <= x0 < variables.windW and 0.0 <= y0 < variables.windH:
        if variables.stars[n].type == StarsType.STREAK:
            x1 = variables.stars[n].x[1] * variables.windW / variables.stars[n].z[1]
            y1 = variables.stars[n].y[1] * variables.windH / variables.stars[n].z[1]
            x1, y1 = RotatePoint(x1, y1, variables.stars[n].rotation)
            x1 += variables.windW / 2.0
            y1 += variables.windH / 2.0

            glLineWidth(variables.MAXPOS / 100.0 / variables.stars[n].z[0] + 1.0)
            glColor3f(1.0, (variables.MAXWARP - variables.speed) / variables.MAXWARP,
                      (variables.MAXWARP - variables.speed) / variables.MAXWARP)
            if fabs(x0 - x1) < 1.0 and fabs(y0 - y1) < 1.0:
                glBegin(GL_POINTS)
                glVertex2f(x0, y0)
                glEnd()
            else:
                glBegin(GL_LINES)
                glVertex2f(x0, y0)
                glVertex2f(x1, y1)
                glEnd()

        else:
            width = variables.MAXPOS / 10.0 / variables.stars[n].z[0] + 1.0
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_POLYGON)
            for i in range(8):
                x = x0 + width * Cos(i * variables.MAXANGLES / 8.0)
                y = y0 + width * Sin(i * variables.MAXANGLES / 8.0)
                glVertex2f(x, y)
            glEnd()


def UpdateStars():
    glClear(GL_COLOR_BUFFER_BIT)
    for n in range(variables.starCount):
        if variables.stars[n].z[0] > variables.speed or (
                variables.stars[n].z[0] > 0.0 and variables.speed < variables.MAXWARP):
            if StarPoint(n) == GL_FALSE:
                NewStar(n, variables.MAXPOS)
        else:
            NewStar(n, variables.MAXPOS)


def ShowStars():
    glClear(GL_COLOR_BUFFER_BIT)
    for n in range(variables.starCount):
        if variables.stars[n].z[0] > variables.speed or (
                variables.stars[n].z[0] > 0.0 and variables.speed < variables.MAXWARP):
            ShowStar(n)


def Init():
    seed()  # srand((unsigned int) time(NULL))
    for n in range(variables.MAXSTARS):
        NewStar(n, 100)
    angle = 0.0
    for n in range(variables.MAXANGLES):
        variables.sinTable[n] = sin(angle)
        angle += pi / (variables.MAXANGLES / 2.0)
    glClearColor(0.5, 0.5, 0.5, 0.5)
    glDisable(GL_DITHER)


def Reshape(width, height):
    variables.windW = width
    variables.windH = height

    glViewport(0, 0, variables.windW, variables.windH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-0.5, variables.windW + 0.5, -0.5, variables.windH + 0.5)
    glMatrixMode(GL_MODELVIEW)


''' ARGSUSED1 '''


def Key(key, x, y):
    if key == ' ':
        variables.flag = StarsSpeed.WEIRD if variables.flag == StarsSpeed.NORMAL else StarsSpeed.NORMAL
    elif key == 't':
        variables.nitro = 1
    elif key == b"\x1b":
        exit(0)


def Idle():
    MoveStars()
    UpdateStars()
    if variables.nitro > 0:
        variables.speed = (variables.nitro / 10) + 1.0
        if variables.speed > variables.MAXWARP:
            variables.speed = variables.MAXWARP

        if ++variables.nitro > variables.MAXWARP * 10:
            variables.nitro = -variables.nitro
    elif variables.nitro < 0:
        variables.nitro += 1
        variables.speed = (-variables.nitro / 10) + 1.0
        if variables.speed > variables.MAXWARP:
            variables.speed = variables.MAXWARP

    glutPostRedisplay()


def Display():
    ShowStars()
    if variables.doubleBuffer:
        glutSwapBuffers()
    else:
        glFlush()


def Visible(state):
    if state == GLUT_VISIBLE:
        glutIdleFunc(Idle)
    else:
        glutIdleFunc(None)


def Args(argv):
    variables.doubleBuffer = GL_TRUE

    for params in argv:
        if params.find("-sb") == 0:
            variables.doubleBuffer = GL_FALSE
        elif params.find("-db") == 0:
            variables.doubleBuffer = GL_TRUE


def main():
    glutInitWindowSize(variables.windW, variables.windH)
    glutInit(sys.argv)
    Args(sys.argv)

    color_type = GLUT_RGB
    color_type |= GLUT_DOUBLE if variables.doubleBuffer else GLUT_SINGLE
    glutInitDisplayMode(color_type)
    glutCreateWindow("Stars")

    Init()

    glutReshapeFunc(Reshape)
    glutKeyboardFunc(Key)
    glutVisibilityFunc(Visible)
    glutDisplayFunc(Display)
    glutMainLoop()
    # return 0             ''' ANSI C requires main to return int. '''


main()
