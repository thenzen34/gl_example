# https://www.opengl.org/archives/resources/code/samples/glut_examples/examples/examples.html


''' Copyright (c) Mark J. Kilgard, 1997. '''

''' This program is freely distributable without licensing fees 
   and is provided without guarantee or warrantee expressed or 
   implied. This program is -not- in the public domain. '''

''' This program was requested by Patrick Earl hopefully someone else
   will write the equivalent Direct3D immediate mode program. '''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Variables(object):
    light_diffuse = [1.0, 0.0, 0.0, 1.0]
    ''' Red diffuse light. '''
    light_position = [1.0, 1.0, 1.0, 0.0]
    ''' Infinite light location. '''
    n = [  # ''' Normals for the 6 faces of a cube. '''
        [-1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0],
        [0.0, -1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, -1.0]
    ]
    faces = [  # ''' Vertex indices for the 6 faces of a cube. '''
        [0, 1, 2, 3], [3, 2, 6, 7], [7, 6, 5, 4],
        [4, 5, 1, 0], [5, 6, 2, 1], [7, 4, 0, 3]
    ]
    v = [[0 for _ in range(3)] for _ in range(8)]
    ''' Will be filled in with X,Y,Z vertexes. '''


variables = Variables()


def draw_box():
    for i in range(6):
        glBegin(GL_QUADS)
        glNormal3fv(variables.n[i])
        glVertex3fv(variables.v[variables.faces[i][0]])
        glVertex3fv(variables.v[variables.faces[i][1]])
        glVertex3fv(variables.v[variables.faces[i][2]])
        glVertex3fv(variables.v[variables.faces[i][3]])
        glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_box()
    glutSwapBuffers()


def init():
    ''' Setup cube vertex data. '''
    variables.v[0][0] = variables.v[1][0] = variables.v[2][0] = variables.v[3][0] = -1
    variables.v[4][0] = variables.v[5][0] = variables.v[6][0] = variables.v[7][0] = 1
    variables.v[0][1] = variables.v[1][1] = variables.v[4][1] = variables.v[5][1] = -1
    variables.v[2][1] = variables.v[3][1] = variables.v[6][1] = variables.v[7][1] = 1
    variables.v[0][2] = variables.v[3][2] = variables.v[4][2] = variables.v[7][2] = 1
    variables.v[1][2] = variables.v[2][2] = variables.v[5][2] = variables.v[6][2] = -1

    ''' Enable a single OpenGL light. '''
    glLightfv(GL_LIGHT0, GL_DIFFUSE, variables.light_diffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, variables.light_position)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

    ''' Use depth buffering for hidden surface elimination. '''
    glEnable(GL_DEPTH_TEST)

    ''' Setup the view of the cube. '''
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.0,  # ''' field of view in degree '''
                   1.0,  # ''' aspect ratio '''
                   1.0,  # ''' Z near '''
                   10.0  # ''' Z far '''
                   )
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0.0, 0.0, 5.0,  # ''' eye is at (0,0,5) '''
              0.0, 0.0, 0.0,  # ''' center is at (0,0,0) '''
              0.0, 1.0, 0.)  # ''' up is in positive Y direction '''

    ''' Adjust cube position to be asthetic angle. '''
    glTranslatef(0.0, 0.0, -1.0)
    glRotatef(60, 1.0, 0.0, 0.0)
    glRotatef(-20, 0.0, 0.0, 1.0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("red 3D lighted cube")
    glutDisplayFunc(display)
    init()
    glutMainLoop()
    # return 0             ''' ANSI C requires main to return int. '''


main()
