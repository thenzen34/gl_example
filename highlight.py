# https://www.opengl.org/archives/resources/code/samples/glut_examples/examples/examples.html

''' Copyright (c) Mark J. Kilgard, 1994. '''

''' This program is freely distributable without licensing fees 
   and is provided without guarantee or warrantee expressed or 
   implied. This program is -not- in the public domain. '''

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
'''
 *  scene.c
 *  This program demonstrates the use of the GL lighting model.
 *  Objects are drawn using a grey material characteristic. 
 *  A single light source illuminates the objects.
 '''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

global GLUT_STROKE_ROMAN


class Highlight(object):
    BUFSIZE = 512

    TORUS = 1
    TETRAHEDRON = 2
    ICOSAHEDRON = 3

    W = 500
    H = 500

    x = y = 0

    locating = 0
    theObject = 0
    menu_inuse = 0
    mouse_state = 0

    rquad = 2.0
    speed = 0.1

    objectNames = ["Nothing", "Torus", "Tetrahedron", "Icosahedron"]

    def output(self, x, y, *args):
        glPushMatrix()
        glTranslatef(x, y, 0)
        params = list(args)
        fmt = params.pop(0)
        string = fmt % tuple(params)
        for p in string:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(p))

        glPopMatrix()

    ''' Initialize material property and light source. '''

    def myinit(self):
        light_ambient = {0.2, 0.2, 0.2, 1.0}
        light_diffuse = {0.9, 1.0, 1.0, 1.0}
        light_specular = {1.0, 1.0, 1.0, 1.0}
        light_position = {1.0, 1.0, 1.0}

        glLightfv(GL_LIGHT0, GL_AMBIENT, *light_ambient)
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, *light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, *light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, *light_position)

        glEnable(GL_LIGHT0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        glSelectBuffer(self.BUFSIZE)  # , self.selectBuf

        glNewList(self.TORUS, GL_COMPILE)
        glutSolidTorus(0.275, 0.85, 10, 15)
        glEndList()
        glNewList(self.TETRAHEDRON, GL_COMPILE)
        glutSolidTetrahedron()
        glEndList()
        glNewList(self.ICOSAHEDRON, GL_COMPILE)
        glutSolidIcosahedron()
        glEndList()

        glClearColor(0.1, 0.1, 0.1, 0.1)

    def highlightBegin(self):
        glPushAttrib(GL_LIGHTING_BIT | GL_CURRENT_BIT)
        color = [0.0, 1.0, 0.0]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glColor3f(*color)

    def highlightEnd(self):
        glPopAttrib()

    def draw(self):
        glPushMatrix()
        glScalef(1.3, 1.3, 1.3)
        # glRotatef(20.0, 1.0, 0.0, 0.0)

        glRotatef(self.rquad, self.speed, self.speed, self.speed)

        glLoadName(2)
        glPushMatrix()
        if self.theObject == 2:
            self.highlightBegin()
        glTranslatef(-0.75, -0.5, 0.0)
        glRotatef(270.0, 1.0, 0.0, 0.0)
        glCallList(self.TETRAHEDRON)
        if self.theObject == 2:
            self.highlightEnd()
        glPopMatrix()

        glLoadName(1)
        glPushMatrix()
        if self.theObject == 1:
            self.highlightBegin()
        glTranslatef(-0.75, 0.5, 0.0)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        glCallList(self.TORUS)
        if self.theObject == 1:
            self.highlightEnd()
        glPopMatrix()

        glLoadName(3)
        glPushMatrix()
        if self.theObject == 3:
            self.highlightBegin()
        glTranslatef(0.75, 0.0, -1.0)
        glCallList(self.ICOSAHEDRON)
        if self.theObject == 3:
            self.highlightEnd()
        glPopMatrix()

        glPopMatrix()

    def myortho(self):
        if self.W <= self.H:
            glOrtho(-2.5, 2.5, -2.5 * self.H / self.W, 2.5 * self.H / self.W, -10.0, 10.0)
        else:
            glOrtho(-2.5 * self.W / self.H, 2.5 * self.W / self.H, -2.5, 2.5, -10.0, 10.0)

    ''' ARGSUSED '''

    def locate(self, value):
        viewport = [0] * 4

        if self.locating:
            if self.mouse_state == GLUT_ENTERED:
                glRenderMode(GL_SELECT)
                glInitNames()
                glPushName(-1)

                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glLoadIdentity()
                viewport[0] = 0
                viewport[1] = 0
                viewport[2] = self.W
                viewport[3] = self.H
                gluPickMatrix(self.x, self.H - self.y, 5.0, 5.0, viewport)
                self.myortho()
                glMatrixMode(GL_MODELVIEW)
                self.draw()
                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)
                hits = glRenderMode(GL_RENDER)
            else:
                hits = []
            self.processHits(hits)
        self.locating = 0

    def passive(self, newx, newy):
        self.x = newx
        self.y = newy
        if not self.locating:
            self.locating = 1
            glutTimerFunc(1, self.locate, 0)

    def entry(self, state):
        self.mouse_state = state
        if not self.menu_inuse:
            if state == GLUT_LEFT:
                if self.theObject != 0:
                    self.theObject = 0
                    glutPostRedisplay()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw()

        glPushAttrib(GL_ENABLE_BIT)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_LINE_SMOOTH)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 3000, 0, 3000)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        self.output(80, 2800, "Automatically names object under mouse.")
        self.output(80, 100, "Located: %s.", self.objectNames[self.theObject])
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopAttrib()

        glutSwapBuffers()

    def myReshape(self, w, h):
        self.W = w
        self.H = h
        glViewport(0, 0, self.W, self.H)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.myortho()
        glMatrixMode(GL_MODELVIEW)

    def polygon_mode(self, value):
        if value == 1:
            glEnable(GL_LIGHTING)
            glDisable(GL_BLEND)
            glEnable(GL_DEPTH_TEST)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        elif value == 2:
            glDisable(GL_LIGHTING)
            glColor3f(1.0, 1.0, 1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glDisable(GL_DEPTH_TEST)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glutPostRedisplay()

        return value

    def mstatus(self, status, newx, newy):
        if status == GLUT_MENU_NOT_IN_USE:
            self.menu_inuse = 0
            self.passive(newx, newy)
        else:
            self.menu_inuse = 1

    def main_menu(self, value):
        if value == 666:
            exit(0)

    '''  Main Loop
     *  Open window with initial window size, title bar, 
     *  RGBA display mode, and handle input events.
     '''

    def idle(self):
        self.rquad = self.rquad - 0.15

        self.locating = 1
        glutTimerFunc(1, self.locate, 0)

        glutPostRedisplay()

    def main(self):
        glutInit()
        glutInitWindowSize(self.W, self.H)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow("")
        self.myinit()
        glutReshapeFunc(self.myReshape)
        glutDisplayFunc(self.display)
        submenu = glutCreateMenu(self.polygon_mode)
        glutAddMenuEntry("Filled", 1)
        glutAddMenuEntry("Outline", 2)
        glutCreateMenu(self.main_menu)
        glutAddMenuEntry("Quit", 666)
        glutAddSubMenu("Polygon mode", submenu)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        glutPassiveMotionFunc(self.passive)
        glutEntryFunc(self.entry)
        glutMenuStatusFunc(self.mstatus)
        glutIdleFunc(self.idle)
        glutMainLoop()
        # return 0             ' '' ANSI C requires main to return int. '' '

    '''  processHits() prints out the contents of the 
     *  selection array.
     '''

    def processHits(self, hits):
        depth = sys.maxsize
        # i, getThisName
        # names, *ptr
        # newObject

        # print(hits)

        ptr = 0
        newObject = 0

        for hit_record in hits:
            min_depth, max_depth, names = hit_record
            # print(min_depth, max_depth, names)
            getThisName = False
            ptr += 1

            if min_depth <= depth:
                depth = min_depth
                getThisName = True
            if max_depth <= depth:
                depth = max_depth
                getThisName = True

            if getThisName:
                newObject = names.pop()

        if self.theObject != newObject:
            self.theObject = newObject
            # print(newObject)
            glutPostRedisplay()


H = Highlight()
H.main()
