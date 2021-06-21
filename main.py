from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
from stl import mesh as meshes
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
import pymesh as msh
import trimesh
from shapely.geometry import LineString, LinearRing, MultiLineString, Polygon
import numpy as np
import math

from descartes import PolygonPatch

from figures import SIZE, BLUE, GRAY, GREEN, DARKGRAY, set_limits, plot_line

print('Solution by Snehil Saluja. Please keep on closing the windows opening while the code runs to proceed further.')

mesh = trimesh.load('./assignment.stl')


def add_shell(ax, x, y, count, air_gap, shell_width, mode="inner"):

    line = LinearRing(zip(x, y))

    if(mode == "inner"):
        shell = +1
        color = GREEN
        loc = 'left'
    elif(mode == "outer"):
        shell = -1
        color = DARKGRAY
        loc = 'right'

    for i in range(1, count+1):
        if(mode == "inner"):
            color = GREEN
            loc = 'left'
        elif(mode == "outer"):
            color = DARKGRAY
            loc = 'right'
        ax.plot(x, y, color=color, lw=shell_width)
        offset = line.parallel_offset((i)*shell*air_gap, loc, join_style=1)
        plot_line(ax, offset, color=color, linewidth=shell_width, zorder=5)

        offset = offset.parallel_offset((i)*shell*air_gap, loc, join_style=1)

    return offset


def plot_maze(ax, line, turn, anyline, air_gap, raster_width):

    if(len(list(line.coords)) > 0):
        coords = list(line.coords)
        if(turn == 'odd'):
            anyline.append((coords[0][0]+air_gap + raster_width, coords[0][1]))
            anyline.append((coords[1][0]-air_gap - raster_width, coords[1][1]))
            turn = 'even'
        elif(turn == 'even'):
            anyline.append((coords[1][0]-air_gap - raster_width, coords[1][1]))
            anyline.append((coords[0][0]+air_gap + raster_width, coords[0][1]))
            turn = 'odd'

        return anyline


def infill(ax, polygon, x, y, air_gap, raster_width):

    i = min(y) + air_gap + raster_width
    turn = 'odd'
    mainmultiline = []
    mainline = []

    while(i < (max(y) - air_gap - raster_width)):
        intersection_line = LineString([(-5000, i), (5000, i)])
        try:
            collect = polygon.intersection(intersection_line)
        except:
            break

        if(isinstance(collect, MultiLineString)):
            if(len(mainline) > 0):
                mainmultiline = [[] for line in list(collect.geoms)]
                turnarray = ['odd' for line in list(collect.geoms)]
                final = LineString(mainline)
                plot_line(ax, final,
                          color=BLUE, linewidth=raster_width)
                mainline = []
                turn = 'odd'
            for j, line in enumerate(list(collect.geoms)):
                plot_maze(
                    ax, line, turnarray[j], mainmultiline[j], air_gap, raster_width)
                if(turnarray[j] == 'even'):
                    turnarray[j] = 'odd'
                elif(turnarray[j] == 'odd'):
                    turnarray[j] = 'even'
            for j, line in enumerate(list(collect.geoms)):
                final = LineString(mainmultiline[j])
                plot_line(ax, final,
                          color=BLUE, linewidth=raster_width)

        elif(isinstance(collect, LineString)):
            if(mainmultiline != []):
                mainmultiline = []
                turn = 'odd'
            plot_maze(ax, collect, turn, mainline, air_gap, raster_width)
            if(turn == 'even'):
                turn = 'odd'
            elif(turn == 'odd'):
                turn = 'even'

        i = i + air_gap + (raster_width)

    if(mainline != []):
        plot_line(ax, LineString(mainline), color=BLUE, linewidth=raster_width)
        mainline = []


def slicer(height, air_gap, width):

    originx = [0, height, 0]
    normalx = [0, 1, 0]

    slice = mesh.section(plane_origin=originx,
                         plane_normal=normalx)

    slice_2D, slice_3D = slice.to_planar()

    polygons = slice_2D.polygons_full
    inside_polygons = slice_2D.polygons_closed

    fig, ax = plt.subplots()

    cent_x, cent_y = slice_2D.centroid

    for polygon in polygons:
        x, y = polygon.exterior.xy

        shell_exterior = add_shell(
            ax, x, y, count=1, air_gap=air_gap, shell_width=width, mode="outer")

    shell_interior = []

    for interior in polygon.interiors:
        x, y = interior.xy
        shell_interior.append(
            add_shell(ax, x, y, count=1, air_gap=air_gap, shell_width=width, mode="inner"))

    new_polygon = Polygon(shell_exterior, shell_interior)

    for polygon in polygons:

        xx, yy = polygon.exterior.xy
        x = np.array(xx)
        y = np.array(yy)

        new_x = np.divide((x + y), 2**0.5)
        new_y = np.divide((y - x), 2**0.5)

        infill(ax, new_polygon, new_x, new_y,
               air_gap=air_gap, raster_width=width)

        ax.axis('equal')

    custom_lines = [Line2D([0], [0], color='black', lw=2),
                    Line2D([0], [0], color='green', lw=2)]

    ax.legend(custom_lines, ['Outer Loops', 'Inner Loops'])

    plt.title('At height - ' + str(height) + " mm")

    plt.show()


def assignment_new():
    print('Running Assignment Code for Level 1')
    print('Please enter the height of figure in mm (enter 50 for the figure given in assignment)')
    height = int(input())

    print('Running for step heights 20 mm cross sections')

    for i in range(10, height+1, 20):
        slicer(i, air_gap=0.5, width=0.5)


def main():

    m = []

    assignment_new()


if __name__ == '__main__':
    main()
