"""
PoissonLib.py

numpy based Poisson disc code

from https://scipython.com/blog/poisson-disc-sampling-in-python/

Modified by Brian N. Norman to work as a library

usage

from Helpers.PoissonLib import *

samples=getSamples(k,r,w,h)

k is the number of samples in radius r within a rectangular area w*h

this code runs 10x faster than the previous Poisson.py python implementation

"""

import numpy as np

'''

initialise the samples list

These values are overwritten when getSamples(...) is called

'''


# values passed in
r=5
k=30
width,height=64,64

# calculated values
samples=[]
rx2=r*2
rxx2=r**2
PIx2=np.pi*2
nx,ny=0,0
a=0
cells=None
coords_list=None

def init(K=30,R=5,W=64,H=64):

    global r,k,width,height,coords_list,cells,nx,ny,samples,rx2,rxx2,PIx2,a

    k,r,width,height=K,R,W,H

    samples=[]

    # used in loops - silly to keep calculating it
    rx2=R*2
    rxx2=R**2
    PIx2=np.pi*2

    width, height = W, W

    # Cell side length
    a = R/np.sqrt(2)
    # Number of cells in the x- and y-directions of the grid
    nx, ny = int(W / a) + 1, int(H / a) + 1

    # A list of coordinates in the grid of cells
    coords_list = [(ix, iy) for ix in range(nx) for iy in range(ny)]
    # Initilalize the dictionary of cells: each key is a cell's coordinates, the
    # corresponding value is the index of that cell's point's coordinates in the
    # samples list (or None if the cell is empty).
    cells = {coords: None for coords in coords_list}

def get_cell_coords(pt):
    """Get the coordinates of the cell that pt = (x,y) falls in."""
    global a
    return int(pt[0] // a), int(pt[1] // a)


def get_neighbours(coords):
    """Return the indexes of points in cells neighbouring cell at coords.

    For the cell at coords = (x,y), return the indexes of points in the cells
    with neighbouring coordinates illustrated below: ie those cells that could
    contain points closer than r.

                                     ooo
                                    ooooo
                                    ooXoo
                                    ooooo
                                     ooo

    """

    global nx,ny,cells

    dxdy = [(-1,-2),(0,-2),(1,-2),(-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),
            (-2,0),(-1,0),(1,0),(2,0),(-2,1),(-1,1),(0,1),(1,1),(2,1),
            (-1,2),(0,2),(1,2),(0,0)]
    neighbours = []
    for dx, dy in dxdy:
        neighbour_coords = coords[0] + dx, coords[1] + dy
        if not (0 <= neighbour_coords[0] < nx and
                0 <= neighbour_coords[1] < ny):
            # We're off the grid: no neighbours here.
            continue
        neighbour_cell = cells[neighbour_coords]
        if neighbour_cell is not None:
            # This cell is occupied: store this index of the contained point.
            neighbours.append(neighbour_cell)
    return neighbours

def point_valid(pt):
    """Is pt a valid point to emit as a sample?

    It must be no closer than r from any other point: check the cells in its
    immediate neighbourhood.

    """
    global rxx2
    cell_coords = get_cell_coords(pt)
    for idx in get_neighbours(cell_coords):
        nearby_pt = samples[idx]
        # Squared distance between or candidate point, pt, and this nearby_pt.
        distance2 = (nearby_pt[0]-pt[0])**2 + (nearby_pt[1]-pt[1])**2
        if distance2 < rxx2:
            # The points are too close, so pt is not a candidate.
            return False
    # All points tested: if we're here, pt is valid
    return True


def get_point(k, refpt):
    """Try to find a candidate point relative to refpt to emit in the sample.

    We draw up to k points from the annulus of inner radius r, outer radius 2r
    around the reference point, refpt. If none of them are suitable (because
    they're too close to existing points in the sample), return False.
    Otherwise, return the pt.

    """
    global r,rx2,PIx2,height,width
    i = 0

    while i < k:
        rho, theta = np.random.uniform(r, rx2), np.random.uniform(0, PIx2)
        pt = refpt[0] + rho*np.cos(theta), refpt[1] + rho*np.sin(theta)
        if not (0 < pt[0] < width and 0 < pt[1] < height):
            # This point falls outside the domain, so try again.
            continue
        if point_valid(pt):
            return pt
        i += 1
    # We failed to find a suitable point in the vicinity of refpt.
    return False

def getSamples(k,r,w,h):

    global coords_list,cells,a,mx,ny,samples,rx2,rxx2,PIx2,width,height

    init(k,r,w,h)

    # Pick a random point to start with.
    pt = (np.random.uniform(0, w), np.random.uniform(0, h))
    samples = [pt]

    # Our first sample is indexed at 0 in the samples list...
    cells[get_cell_coords(pt)] = 0

    # ... and it is active, in the sense that we're going to look for more points
    # in its neighbourhood.
    active = [0]

    nsamples = 1

    # As long as there are points in the active list, keep trying to find samples.
    while active:
        # choose a random "reference" point from the active list.
        idx = np.random.choice(active)
        refpt = samples[idx]
        # Try to pick a new point relative to the reference point.
        pt = get_point(k, refpt)
        if pt:
            # Point pt is valid: add it to the samples list and mark it as active
            samples.append(pt)
            nsamples += 1
            active.append(len(samples)-1)
            cells[get_cell_coords(pt)] = len(samples) - 1
        else:
            # We had to give up looking for valid points near refpt, so remove it
            # from the list of "active" points.
            active.remove(idx)

        # trap errant code - there cannot be width*height samples (no gaps)
        if len(samples)>width*height:
            print "Poissonlib.getSamples() exceeded limit."
            break

    return samples
