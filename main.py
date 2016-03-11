#!/usr/bin/env python3
##################################################################
# Solutions to the Knight's Distance problem:
#   Given a knight's starting position and a destination
#   position on an infinite chessboard with no obstructions,
#   determine the fewest number of moves to reach the destination
# Mar. 2016
#
#
# Background:
#   The knight must move in an L shape 3 units at a time, two
#   units along one axis and one unit along the other. Since the
#   X & Y signs and the long axis can be varied, there are always
#   8 possible moves.
#
##################################################################
import timeit
from collections import deque

# Generate the 8 possible moves from a given position
def knightMoves(coords):
    out = list()
    out.append((coords[0]+1,coords[1]+2))
    out.append((coords[0]+1,coords[1]-2))
    out.append((coords[0]-1,coords[1]+2))
    out.append((coords[0]-1,coords[1]-2))

    out.append((coords[0]+2,coords[1]+1))
    out.append((coords[0]+2,coords[1]-1))
    out.append((coords[0]-2,coords[1]+1))
    out.append((coords[0]-2,coords[1]-1))

    # This is more clever but only marginally shorter, less readable, and no faster
    #for i in [-1,1]: # X sign
    #    for j in [-1,1]: # Y sign
    #        for k in [0,1]: # Axis
    #            out.append(coords[0]+i*(1+k*1),coords[1]+j*(1+k*1))

    return out

# Naive implementation
def knightsDist_Naive(srcX,srcY,dstX,dstY):
    src = (srcX,srcY)
    dst = (dstX,dstY)

    queue = deque()
    # Tuple: (x,y)
    queue.extend(knightMoves(src))

    # Conduct a search, breadth first
    moves = 1
    while True:
        # Modifying the queue during iteration could cause undefined behavior so run the loop on a list copy instead
        for coords in list(queue):
            if coords == dst:
                return moves
            else:
                queue.extend(knightMoves(coords))
        moves += 1

# Slightly less naive implementation
def knightsDist_Smarter(srcX,srcY,dstX,dstY):
    # Quickly check for sane input
    if srcX == dstX and srcY == dstY:
        return 0

    # And for the one move case
    if dstX-srcX != 0 and dstY-srcY != 0 and abs(dstX-srcX) + abs(dstY-srcY) == 3:
        return 1

    src = (srcX,srcY)
    dst = (dstX,dstY)

    # Use a set to neatly eliminate duplicate coordinates
    queue = set()
    queue = queue.union(knightMoves(src))

    moves = 1
    while True:
        for coords in list(queue):
            if coords == dst:
                return moves
            else:
                # We also know that at an abs(dX)+abs(dY) distance > 3,
                # any move that takes us farther away from the destination is a bad one
                # so half of the options can be eliminated
                testCoords = knightMoves(coords)
                taxicabDist = abs(coords[0]-dst[0]) + abs(coords[1]-dst[1])
                if taxicabDist > 3:
                    for c in testCoords:
                        if abs(c[0]-dst[0]) + abs(c[1]-dst[1]) >= taxicabDist:
                            testCoords.remove(c)
                queue = queue.union(testCoords)

        moves += 1

def runTests(targetFunc):
    # Run some test scenarios and time them for fun
    # Ref: https://en.wikipedia.org/wiki/Knight_%28chess%29#Movement
    timeit_count = 100

    print('Test 1: Single move case - ', end='')
    func = lambda: targetFunc(0,0,2,1)
    assert(func() == 1)
    print('Ok ',end='')
    print('(avg ' + '{:.2E}'.format(timeit.timeit(func,number=timeit_count)/timeit_count) + ' sec)')

    print('Test 2: Adjacent grid case - ', end='')
    func = lambda: targetFunc(0,0,-1,0)
    assert(func() == 3)
    print('Ok ',end='')
    print('(avg ' + '{:.2E}'.format(timeit.timeit(func,number=timeit_count)/timeit_count) + ' sec)')

    print('Test 3: Four move case - ', end='')
    func = lambda: targetFunc(0,0,-2,-2)
    assert(func() == 4)
    print('Ok ',end='')
    print('(avg ' + '{:.2E}'.format(timeit.timeit(func,number=timeit_count)/timeit_count) + ' sec)')

    print('Test 4: Distant case - ', end='')
    func = lambda: targetFunc(0,0,6,-6)
    assert(func() == 4)
    print('Ok ',end='')
    print('(avg ' + '{:.2E}'.format(timeit.timeit(func,number=timeit_count)/timeit_count) + ' sec)')

if __name__ == '__main__':
    print('Knight\'s Distance Algorithms')
    print('### Naive implementation')
    runTests(knightsDist_Naive)

    print()
    print('### Smarter general implementation')
    runTests(knightsDist_Smarter)
