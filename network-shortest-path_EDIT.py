"""Network 01: Shortest path

"""

import compas
import json

from compas.utilities import pairwise
from compas.datastructures import Network
from compas.topology import dijkstra_path
from compas.visualization import NetworkPlotter

# make a network from a sample file

with open('data.json', 'r') as f:
    lines = json.load(f)

pointList = []

for k, v in lines.items():
    subList = []
    subList.append(v["pt0"])
    subList.append(v["pt1"])
    pointList.append(subList)


network = Network.from_lines(pointList)

adjacency = {key: network.vertex_neighbours(key) for key in network.vertices()}

weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

# gkey_key = {geometric_key(network.vertex_coordinates(key),'3f'): key for key in network.ver}

# make a few edges heavier
# for example to simulate traffic problems

# heavy = [(7, 17), (9, 19)]

# for u, v in heavy:
#     weight[(u, v)] = 1000.0
#     weight[(v, u)] = 1000.0


# make an interactive plotter
# for finding shortest paths from a given start to a given end
# and through an additional user-selected point

plotter = NetworkPlotter(network, figsize=(20, 16), fontsize=16)


# choose start and end
# and set an initial value for the via point

start = 3
via = 0
end = 90


# define the function that computes the shortest path
# based on the current via

def via_via(via):

    # compute the shortest path from start to via
    # and from via to end
    # combine the paths

    path1 = dijkstra_path(adjacency, weight, start, via)
    path2 = dijkstra_path(adjacency, weight, via, end)
    path = path1 + path2[1:]

    edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if v not in network.edge[u]:
            u, v = v, u
        edges.append([u, v])


    # update the plot

    vertexcolor = {}
    vertexcolor[start] = '#00ff00'
    vertexcolor[end] = '#00ff00'
    vertexcolor[via] = '#FF00F6'

    plotter.clear_vertices()
    plotter.clear_edges()

    plotter.draw_vertices(text={key: key for key in (start, via, end)},
                          textcolor={key: '#ffffff' for key in path[1:-1]},
                          facecolor=vertexcolor,
                          radius=3,
                          picker=20)

    plotter.draw_edges(color={(u, v): '#ff0000' for u, v in edges},
                       width={(u, v): 4.0 for u, v in edges})
                       # text={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()},
                       # fontsize=8.0)


# define a listener for picking points
# whenever a new point is picked
# it will call the via_via function
# with the picked point as via point

index_key = network.index_key()

def on_pick(e):
    index = e.ind[0]
    via = index_key[index]
    via_via(via)
    plotter.update()


# initialize
# and start

via_via(via)

plotter.register_listener(on_pick)
plotter.show()