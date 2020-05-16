# https://www.opengl.org/archives/resources/code/samples/glut_examples/examples/examples.html
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.raw import GLU as GLU_raw


class Variables(object):
    mat_red_diffuse = [0.7, 0.0, 0.1, 1.0]
    mat_green_diffuse = [0.0, 0.7, 0.1, 1.0]
    mat_blue_diffuse = [0.0, 0.1, 0.7, 1.0]
    mat_yellow_diffuse = [0.7, 0.8, 0.1, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    mat_shininess = [100.0]
    knots = [0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0]
    pts1 = pts2 = pts3 = pts4 = [[[0.0 for _ in range(3)] for _ in range(4)] for _ in range(4)]
    nurb = None
    u = 0
    v = 0


variables = Variables()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glCallList(1)
    glFlush()


def main():
    glutInit(sys.argv)
    glutCreateWindow("molehill")
    glMaterialfv(GL_FRONT, GL_SPECULAR, variables.mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, variables.mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_AUTO_NORMAL)
    glEnable(GL_NORMALIZE)
    variables.nurb = GLU_raw.gluNewNurbsRenderer()
    GLU_raw.gluNurbsProperty(variables.nurb, GLU_SAMPLING_TOLERANCE, 25.0)
    GLU_raw.gluNurbsProperty(variables.nurb, GLU_DISPLAY_MODE, GLU_FILL)

    # Build control points for NURBS mole hills. 
    for u in range(4):
        for v in range(4):
            # Red. 
            variables.pts1[u][v][0] = 2.0 * u
            variables.pts1[u][v][1] = 2.0 * v
            if (u == 1 or u == 2) and (v == 1 or v == 2):
                # Stretch up middle. 
                variables.pts1[u][v][2] = 6.0
            else:
                variables.pts1[u][v][2] = 0.0

            # Green. 
            variables.pts2[u][v][0] = 2.0 * (u - 3.0)
            variables.pts2[u][v][1] = 2.0 * (v - 3.0)
            if (u == 1 or u == 2) and (v == 1 or v == 2):
                if u == 1 and v == 1:
                    # Pull hard on single middle square. 
                    variables.pts2[u][v][2] = 15.0
                else:
                    # Push down on other middle squares. 
                    variables.pts2[u][v][2] = -2.0
            else:
                variables.pts2[u][v][2] = 0.0

            # Blue. 
            variables.pts3[u][v][0] = 2.0 * (u - 3.0)
            variables.pts3[u][v][1] = 2.0 * v
            if (u == 1 or u == 2) and (v == 1 or v == 2):
                if u == 1 and v == 2:
                    # Pull up on single middple square. 
                    variables.pts3[u][v][2] = 11.0
                else:
                    # Pull up slightly on other middle squares. 
                    variables.pts3[u][v][2] = 2.0
            else:
                variables.pts3[u][v][2] = 0.0

            # Yellow. 
            variables.pts4[u][v][0] = 2.0 * u
            variables.pts4[u][v][1] = 2.0 * (v - 3.0)
            if (u == 1 or u == 2 or u == 3) and (v == 1 or v == 2):
                if v == 1:
                    # Push down front middle and right squares. 
                    variables.pts4[u][v][2] = -2.0
                else:
                    # Pull up back middle and right squares. 
                    variables.pts4[u][v][2] = 5.0
            else:
                variables.pts4[u][v][2] = 0.0

    # Stretch up red's far right corner.
    variables.pts1[3][3][2] = 6
    # Pull down green's near left corner a little.
    variables.pts2[0][0][2] = -2
    # Turn up meeting of four corners.
    variables.pts1[0][0][2] = 1
    variables.pts2[3][3][2] = 1
    variables.pts3[3][0][2] = 1
    variables.pts4[0][3][2] = 1

    glMatrixMode(GL_PROJECTION)

    gluPerspective(55.0, 1.0, 2.0, 24.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -15.0)
    glRotatef(330.0, 1.0, 0.0, 0.0)

    glNewList(1, GL_COMPILE)
    # Render red hill.
    glMaterialfv(GL_FRONT, GL_DIFFUSE, variables.mat_red_diffuse)
    GLU_raw.gluBeginSurface(variables.nurb)
    GLU_raw.gluNurbsSurface(variables.nurb, 8, variables.knots, 8, variables.knots,
                            4 * 3, 3, variables.pts1,
                            4, 4, GL_MAP2_VERTEX_3)
    GLU_raw.gluEndSurface(variables.nurb)

    # Render green hill.
    glMaterialfv(GL_FRONT, GL_DIFFUSE, variables.mat_green_diffuse)
    GLU_raw.gluBeginSurface(variables.nurb)
    GLU_raw.gluNurbsSurface(variables.nurb, 8, variables.knots, 8, variables.knots,
                            4 * 3, 3, variables.pts2,
                            4, 4, GL_MAP2_VERTEX_3)
    GLU_raw.gluEndSurface(variables.nurb)

    # Render blue hill.
    glMaterialfv(GL_FRONT, GL_DIFFUSE, variables.mat_blue_diffuse)
    GLU_raw.gluBeginSurface(variables.nurb)
    GLU_raw.gluNurbsSurface(variables.nurb, 8, variables.knots, 8, variables.knots,
                            4 * 3, 3, variables.pts3,
                            4, 4, GL_MAP2_VERTEX_3)
    GLU_raw.gluEndSurface(variables.nurb)

    # Render yellow hill.
    glMaterialfv(GL_FRONT, GL_DIFFUSE, variables.mat_yellow_diffuse)
    GLU_raw.gluBeginSurface(variables.nurb)
    GLU_raw.gluNurbsSurface(variables.nurb, 8, variables.knots, 8, variables.knots,
                            4 * 3, 3, variables.pts4,
                            4, 4, GL_MAP2_VERTEX_3)
    GLU_raw.gluEndSurface(variables.nurb)

    glEndList()

    glutDisplayFunc(display)
    glutMainLoop()
    # return 0             # ANSI C requires main to return int.


main()
