# https://www.opengl.org/archives/resources/code/samples/glut_examples/examples/examples.html
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Variables(object):
    pass


variables = Variables()

WIDTH = 4
HEIGHT = 5
PIECES = 10
OFFSETX = -2
OFFSETY = -2.5
OFFSETZ = -0.5


# Config = [[0 for y in range(WIDTH)] for x in range(HEIGHT)]

class puzzle:
    backptr = None  # type: puzzle
    solnptr = None  # type: puzzle
    pieces = [[0 for y in range(WIDTH)] for x in range(HEIGHT)]
    next = None  # type: puzzle
    hashvalue = 0


HASHSIZE = 10691


class puzzlelist:
    puzzle = None  # type: puzzle
    next = None  # type: puzzlelist


convert = [0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4]
colors = [
    [0, 0, 0],
    [255, 255, 127],
    [255, 255, 127],
    [255, 255, 127],
    [255, 255, 127],
    [255, 127, 255],
    [255, 127, 255],
    [255, 127, 255],
    [255, 127, 255],
    [255, 127, 127],
    [255, 255, 255],
]


def changeState():
    pass


hashtable = [puzzle() for _ in range(HASHSIZE)]
startPuzzle = None  # type: puzzle
puzzles = None  # type: puzzlelist
lastentry = None  # type: puzzlelist

curX = curY = visible = 0

MOVE_SPEED = 0.2
movingPiece = 0
move_x = move_y = 0
curquat = [0.0 for _ in range(4)]
doubleBuffer = 1
depth = 1

xsize = [0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
ysize = [0, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2]
zsize = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.6]

startConfig = [
    [8, 10, 10, 7],
    [8, 10, 10, 7],
    [6, 9, 9, 5],
    [6, 4, 3, 5],
    [2, 0, 0, 1]
]

thePuzzle = [
    [8, 10, 10, 7],
    [8, 10, 10, 7],
    [6, 9, 9, 5],
    [6, 4, 3, 5],
    [2, 0, 0, 1]
]

xadds = [-1, 0, 1, 0]
yadds = [0, -1, 0, 1]
W = 400
H = 300
viewport = [GL_FALSE for _ in range(4)]


def srandom(*args):
    random.seed()


def random():
    return random.random() >> 2


def calc_hash(config):
    value = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            value = value + convert[config[i][j]]
            value *= 6
        return value


def solution(config):
    if config[4][1] == 10 and config[4][2] == 10:
        return 1
    return 0


boxcoords = [
    [0.2, 0.2, 0.9],
    [0.8, 0.2, 0.9],
    [0.8, 0.8, 0.9],
    [0.2, 0.8, 0.9],
    [0.2, 0.1, 0.8],
    [0.8, 0.1, 0.8],
    [0.9, 0.2, 0.8],
    [0.9, 0.8, 0.8],
    [0.8, 0.9, 0.8],
    [0.2, 0.9, 0.8],
    [0.1, 0.8, 0.8],
    [0.1, 0.2, 0.8],
    [0.2, 0.1, 0.2],
    [0.8, 0.1, 0.2],
    [0.9, 0.2, 0.2],
    [0.9, 0.8, 0.2],
    [0.8, 0.9, 0.2],
    [0.2, 0.9, 0.2],
    [0.1, 0.8, 0.2],
    [0.1, 0.2, 0.2],
    [0.2, 0.2, 0.1],
    [0.8, 0.2, 0.1],
    [0.8, 0.8, 0.1],
    [0.2, 0.8, 0.1],
]

boxnormals = [
    [0, 0, 1],  # 0
    [0, 1, 0],
    [1, 0, 0],
    [0, 0, -1],
    [0, -1, 0],
    [-1, 0, 0],
    [0.7071, 0.7071, 0.0000],  # 6
    [0.7071, -0.7071, 0.0000],
    [-0.7071, 0.7071, 0.0000],
    [-0.7071, -0.7071, 0.0000],
    [0.7071, 0.0000, 0.7071],  # 10
    [0.7071, 0.0000, -0.7071],
    [-0.7071, 0.0000, 0.7071],
    [-0.7071, 0.0000, -0.7071],
    [0.0000, 0.7071, 0.7071],  # 14
    [0.0000, 0.7071, -0.7071],
    [0.0000, -0.7071, 0.7071],
    [0.0000, -0.7071, -0.7071],
    [0.5774, 0.5774, 0.5774],  # 18
    [0.5774, 0.5774, -0.5774],
    [0.5774, -0.5774, 0.5774],
    [0.5774, -0.5774, -0.5774],
    [-0.5774, 0.5774, 0.5774],
    [-0.5774, 0.5774, -0.5774],
    [-0.5774, -0.5774, 0.5774],
    [-0.5774, -0.5774, -0.5774],
]

boxfaces = [
    [0, 1, 2, 3],  # 0
    [9, 8, 16, 17],
    [6, 14, 15, 7],
    [20, 23, 22, 21],
    [12, 13, 5, 4],
    [19, 11, 10, 18],
    [7, 15, 16, 8],  # 6
    [13, 14, 6, 5],
    [18, 10, 9, 17],
    [19, 12, 4, 11],
    [1, 6, 7, 2],  # 10
    [14, 21, 22, 15],
    [11, 0, 3, 10],
    [20, 19, 18, 23],
    [3, 2, 8, 9],  # 14
    [17, 16, 22, 23],
    [4, 5, 1, 0],
    [20, 21, 13, 12],
    [2, 7, 8, -1],  # 18
    [16, 15, 22, -1],
    [5, 6, 1, -1],
    [13, 21, 14, -1],
    [10, 3, 9, -1],
    [18, 17, 23, -1],
    [11, 4, 0, -1],
    [20, 12, 19, -1],
]

NBOXFACES = len(boxfaces) // len(boxfaces[0])

''' Draw a box.  Bevel as desired. '''


def drawBox(piece, xoff, yoff):
    xlen = xsize[piece]
    ylen = ysize[piece]
    zlen = zsize[piece]

    glColor3ubv(colors[piece])
    glBegin(GL_QUADS)
    for i in range(18):
        glNormal3fv(boxnormals[i])
        for k in range(4):
            if boxfaces[i][k] == -1:
                continue
            v = boxcoords[boxfaces[i][k]]
            x = v[0] + OFFSETX
            if v[0] > 0.5:
                x += xlen - 1
            y = v[1] + OFFSETY
            if v[1] > 0.5:
                y += ylen - 1
            z = v[2] + OFFSETZ
            if v[2] > 0.5:
                z += zlen - 1
            glVertex3f(xoff + x, yoff + y, z)
    glEnd()
    glBegin(GL_TRIANGLES)
    for i in range(18, NBOXFACES):
        glNormal3fv(boxnormals[i])
        for k in range(3):
            if boxfaces[i][k] == -1:
                continue
            v = boxcoords[boxfaces[i][k]]
            x = v[0] + OFFSETX
            if v[0] > 0.5:
                x += xlen - 1
            y = v[1] + OFFSETY
            if v[1] > 0.5:
                y += ylen - 1
            z = v[2] + OFFSETZ
            if v[2] > 0.5:
                z += zlen - 1
            glVertex3f(xoff + x, yoff + y, z)
    glEnd()


containercoords = [
    [-0.1, -0.1, 1.0],
    [-0.1, -0.1, -0.1],
    [4.1, -0.1, -0.1],
    [4.1, -0.1, 1.0],
    [1.0, -0.1, 0.6],  # 4
    [3.0, -0.1, 0.6],
    [1.0, -0.1, 0.0],
    [3.0, -0.1, 0.0],
    [1.0, 0.0, 0.0],  # 8
    [3.0, 0.0, 0.0],
    [3.0, 0.0, 0.6],
    [1.0, 0.0, 0.6],
    [0.0, 0.0, 1.0],  # 12
    [4.0, 0.0, 1.0],
    [4.0, 0.0, 0.0],
    [0.0, 0.0, 0.0],
    [0.0, 5.0, 0.0],  # 16
    [0.0, 5.0, 1.0],
    [4.0, 5.0, 1.0],
    [4.0, 5.0, 0.0],
    [-0.1, 5.1, -0.1],  # 20
    [4.1, 5.1, -0.1],
    [4.1, 5.1, 1.0],
    [-0.1, 5.1, 1.0],
]

containernormals = [
    [0, -1, 0],
    [0, -1, 0],
    [0, -1, 0],
    [0, -1, 0],
    [0, -1, 0],
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
    [-1, 0, 0],
    [-1, 0, 0],
    [-1, 0, 0],
    [0, 1, 0],
    [0, 0, -1],
    [0, 0, -1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
]

containerfaces = [
    [1, 6, 4, 0],
    [0, 4, 5, 3],
    [1, 2, 7, 6],
    [7, 2, 3, 5],
    [16, 19, 18, 17],

    [23, 22, 21, 20],
    [12, 11, 8, 15],
    [10, 13, 14, 9],

    [15, 16, 17, 12],
    [2, 21, 22, 3],
    [6, 8, 11, 4],

    [1, 0, 23, 20],
    [14, 13, 18, 19],
    [9, 7, 5, 10],

    [12, 13, 10, 11],

    [1, 20, 21, 2],
    [4, 11, 10, 5],

    [15, 8, 19, 16],
    [19, 8, 9, 14],
    [8, 6, 7, 9],
    [0, 3, 13, 12],
    [13, 3, 22, 18],
    [18, 22, 23, 17],
    [17, 23, 0, 12],
]

NCONTFACES = len(containerfaces) // len(containerfaces[0])

''' Draw the container '''


def drawContainer():
    ''' Y is reversed here because the model has it reversed '''

    ''' Arbitrary bright wood-like color '''
    glColor3ub(209, 103, 23)
    glBegin(GL_QUADS)
    for i in range(NCONTFACES):
        v = containernormals[i]
        glNormal3f(v[0], -v[1], v[2])
        for k in range(3, -1, -1):
            v = containercoords[containerfaces[i][k]]
            glVertex3f(v[0] + OFFSETX, -(v[1] + OFFSETY), v[2] + OFFSETZ)
    glEnd()


def drawAll():
    m = [[0.0 for _ in range(4)] for _ in range(4)]
    build_rotmatrix(m, curquat)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -10)
    glMultMatrixf((m[0][0]))  # &
    glRotatef(180, 0, 0, 1)

    if depth:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    else:
        glClear(GL_COLOR_BUFFER_BIT)

    for i in range(PIECES + 1):
        done[i] = 0

    glLoadName(0)
    drawContainer()
    for i in range(HEIGHT):
        for j in range(WIDTH):
            piece = thePuzzle[i][j]
            if piece == 0:
                continue
            if done[piece]:
                continue
            done[piece] = 1
            glLoadName(piece)
            if piece == movingPiece:
                drawBox(piece, move_x, move_y)
            else:
                drawBox(piece, j, i)


def redraw():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 100.0)

    drawAll()

    if doubleBuffer:
        glutSwapBuffers()
    else:
        glFinish()


def solidifyChain(puzzle):
    """

    :type puzzle: puzzle
    """
    i = 0
    while puzzle.backptr:
        i += 1
        puzzle.backptr.solnptr = puzzle
        puzzle = puzzle.backptr
    buf = "%d moves to complete!" % i
    glutSetWindowTitle(buf)


def addConfig(config, back):
    """
    :type back: puzzle
    """
    hashvalue = calc_hash(config)

    newpiece = hashtable[hashvalue % HASHSIZE]
    goto_nomatch = False
    while newpiece is not None:
        if newpiece.hashvalue == hashvalue:

            for i in range(WIDTH):
                for j in range(HEIGHT):
                    if convert[config[j][i]] != convert[newpiece.pieces[j][i]]:
                        goto_nomatch = True
                    if goto_nomatch:
                        break
                if goto_nomatch:
                    break
            if not goto_nomatch:
                return 0
        if goto_nomatch:
            newpiece = newpiece.next

    newpiece = puzzle()
    newpiece.next = hashtable[hashvalue % HASHSIZE]
    newpiece.hashvalue = hashvalue
    newpiece.pieces[0:HEIGHT * WIDTH] = config
    newpiece.backptr = back
    newpiece.solnptr = None
    hashtable[hashvalue % HASHSIZE] = newpiece

    newlistentry = puzzlelist()
    newlistentry.puzzle = newpiece
    newlistentry.next = None

    if lastentry:
        lastentry.next = newlistentry
    else:
        puzzles = newlistentry
    lastentry = newlistentry

    if back is None:
        startPuzzle = newpiece
    if solution(config):
        solidifyChain(newpiece)
        return 1
    return 0
