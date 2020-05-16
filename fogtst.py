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

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Variables:
    doubleBuffer = GL_TRUE
    ''' *INDENT-OFF* '''
    plane = [1.0, 0.0, -1.0, 0.0]

    rotX = 5.0
    rotY = -5.0
    zTranslate = -65.0
    fogDensity = 0.02
    cubeList = 1

    scp = [  # [18][3]
        [1.000000, 0.000000, 0.000000],
        [1.000000, 0.000000, 5.000000],
        [0.707107, 0.707107, 0.000000],
        [0.707107, 0.707107, 5.000000],
        [0.000000, 1.000000, 0.000000],
        [0.000000, 1.000000, 5.000000],
        [-0.707107, 0.707107, 0.000000],
        [-0.707107, 0.707107, 5.000000],
        [-1.000000, 0.000000, 0.000000],
        [-1.000000, 0.000000, 5.000000],
        [-0.707107, -0.707107, 0.000000],
        [-0.707107, -0.707107, 5.000000],
        [0.000000, -1.000000, 0.000000],
        [0.000000, -1.000000, 5.000000],
        [0.707107, -0.707107, 0.000000],
        [0.707107, -0.707107, 5.000000],
        [1.000000, 0.000000, 0.000000],
        [1.000000, 0.000000, 5.000000],
    ]

    ambient = [0.1, 0.1, 0.1, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    position = [90.0, 90.0, 0.0, 0.0]
    front_mat_shininess = [30.0]
    front_mat_specular = [0.0, 0.0, 0.0, 1.0]
    front_mat_diffuse = [0.0, 1.0, 0.0, 1.0]
    back_mat_shininess = [50.0]
    back_mat_specular = [0.0, 0.0, 1.0, 1.0]
    back_mat_diffuse = [1.0, 0.0, 0.0, 1.0]
    lmodel_ambient = [0.0, 0.0, 0.0, 1.0]
    fog_color = [0.8, 0.8, 0.8, 1.0]
    ''' *INDENT-ON* '''


variables = Variables()

''' ARGSUSED1 '''


def Key(key, x, y):
    if key == 'd':
        variables.fogDensity *= 1.10
        glFogf(GL_FOG_DENSITY, variables.fogDensity)
        glutPostRedisplay()
    elif key == 'D':
        variables.fogDensity /= 1.10
        glFogf(GL_FOG_DENSITY, variables.fogDensity)
        glutPostRedisplay()
    elif key == b"\x1b":
        exit(0)


''' ARGSUSED1 '''


def SpecialKey(key, x, y):
    if key == GLUT_KEY_UP:
        variables.rotX -= 5
        glutPostRedisplay()
    elif key == GLUT_KEY_DOWN:
        variables.rotX += 5
        glutPostRedisplay()
    elif key == GLUT_KEY_LEFT:
        variables.rotY -= 5
        glutPostRedisplay()
    elif key == GLUT_KEY_RIGHT:
        variables.rotY += 5
        glutPostRedisplay()


def Draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    glTranslatef(0, 0, variables.zTranslate)
    ''' XXX hooky dual axis rotation! '''
    glRotatef(variables.rotY, 0, 1, 0)
    glRotatef(variables.rotX, 1, 0, 0)
    glScalef(1.0, 1.0, 10.0)

    glCallList(variables.cubeList)

    glPopMatrix()

    if variables.doubleBuffer:
        glutSwapBuffers()
    else:
        glFlush()


def Args(argv):
    variables.doubleBuffer = GL_TRUE

    for params in argv:
        if params.find("-sb") == 0:
            variables.doubleBuffer = GL_FALSE
        elif params.find("-db") == 0:
            variables.doubleBuffer = GL_TRUE


def main():
    glutInit(sys.argv)
    Args(sys.argv)

    color_type = GLUT_RGB | GLUT_DEPTH
    color_type |= GLUT_DOUBLE if variables.doubleBuffer else GLUT_SINGLE
    glutInitDisplayMode(color_type)
    glutInitWindowSize(300, 300)
    glutCreateWindow("Fog Test")

    glFrontFace(GL_CW)

    glEnable(GL_DEPTH_TEST)

    glLightfv(GL_LIGHT0, GL_AMBIENT, variables.ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, variables.diffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, variables.position)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, variables.lmodel_ambient)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glMaterialfv(GL_FRONT, GL_SHININESS, variables.front_mat_shininess)
    glMaterialfv(GL_FRONT, GL_SPECULAR, variables.front_mat_specular)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, variables.front_mat_diffuse)
    glMaterialfv(GL_BACK, GL_SHININESS, variables.back_mat_shininess)
    glMaterialfv(GL_BACK, GL_SPECULAR, variables.back_mat_specular)
    glMaterialfv(GL_BACK, GL_DIFFUSE, variables.back_mat_diffuse)

    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_EXP)
    glFogf(GL_FOG_DENSITY, variables.fogDensity)
    glFogfv(GL_FOG_COLOR, variables.fog_color)
    glClearColor(0.8, 0.8, 0.8, 1.0)
    ''' *INDENT-OFF* '''
    glNewList(variables.cubeList, GL_COMPILE)
    glBegin(GL_TRIANGLE_STRIP)
    glNormal3fv(variables.scp[0])
    glVertex3fv(variables.scp[0])
    glNormal3fv(variables.scp[0])
    glVertex3fv(variables.scp[1])
    glNormal3fv(variables.scp[2])
    glVertex3fv(variables.scp[2])
    glNormal3fv(variables.scp[2])
    glVertex3fv(variables.scp[3])
    glNormal3fv(variables.scp[4])
    glVertex3fv(variables.scp[4])
    glNormal3fv(variables.scp[4])
    glVertex3fv(variables.scp[5])
    glNormal3fv(variables.scp[6])
    glVertex3fv(variables.scp[6])
    glNormal3fv(variables.scp[6])
    glVertex3fv(variables.scp[7])
    glNormal3fv(variables.scp[8])
    glVertex3fv(variables.scp[8])
    glNormal3fv(variables.scp[8])
    glVertex3fv(variables.scp[9])
    glNormal3fv(variables.scp[10])
    glVertex3fv(variables.scp[10])
    glNormal3fv(variables.scp[10])
    glVertex3fv(variables.scp[11])
    glNormal3fv(variables.scp[12])
    glVertex3fv(variables.scp[12])
    glNormal3fv(variables.scp[12])
    glVertex3fv(variables.scp[13])
    glNormal3fv(variables.scp[14])
    glVertex3fv(variables.scp[14])
    glNormal3fv(variables.scp[14])
    glVertex3fv(variables.scp[15])
    glNormal3fv(variables.scp[16])
    glVertex3fv(variables.scp[16])
    glNormal3fv(variables.scp[16])
    glVertex3fv(variables.scp[17])
    glEnd()

    glEndList()
    ''' *INDENT-ON* '''

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1.0, 1.0, 200.0)
    glMatrixMode(GL_MODELVIEW)

    glutKeyboardFunc(Key)
    glutSpecialFunc(SpecialKey)
    glutDisplayFunc(Draw)
    glutMainLoop()
    # return 0             ''' ANSI C requires main to return int. '''


main()
