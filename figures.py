from math import sqrt
from shapely import affinity
from plotscalecorrection import LineDataUnits

GM = (sqrt(5)-1.0)/2.0
W = 8.0
H = W*GM
SIZE = (W, H)

BLUE = '#6699cc'
GRAY = '#999999'
DARKGRAY = '#333333'
YELLOW = '#ffcc33'
GREEN = '#339933'
RED = '#ff3333'
BLACK = '#000000'


def plot_line(ax, ob, color=GRAY, zorder=1, linewidth=3, alpha=1):
    x, y = ob.xy

    line = LineDataUnits(x, y, color=color, linewidth=linewidth,
                         solid_capstyle='butt', zorder=zorder, alpha=alpha)

    ax.add_line(line)
