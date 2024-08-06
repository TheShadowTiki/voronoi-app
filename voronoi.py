# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 19:41:42 2023

@author: mikoz
"""

from shapely.geometry import Polygon
from shapely.plotting import plot_polygon
from voronoi_packages import Line, Point, Intersection
import numpy as np
import matplotlib.pyplot as plt
from random import randrange
from copy import deepcopy
from itertools import chain
from scipy.spatial import ConvexHull
from collections import OrderedDict

def order_lines(lines):
    ordered_lines = [lines[0]]
    lines.remove(lines[0])
    
    while len(lines) > 0:
        for i, line in enumerate(lines):
            if ordered_lines[-1][1].eq(line[0]):
                ordered_lines.append(line)
                lines.pop(i)
                break
            elif ordered_lines[0][0].eq(line[1]):
                ordered_lines.insert(0, line)
                lines.pop(i)
                break
                
    return ordered_lines

def bisect_lines(sites, bound):
    bisect_lines = {k:[] for k in sites}
    for s1 in range(len(sites)):
        for s2 in range(len(sites)):
            if s1 != s2:
                mid = ((sites[s1].x + sites[s2].x)/2, (sites[s1].y + sites[s2].y)/2)
                perp = (-(sites[s2].y-sites[s1].y)/sites[s1].distance(sites[s2]), (sites[s2].x-sites[s1].x)/sites[s1].distance(sites[s2]))
                bisect_lines[sites[s1]].append(Line((mid[0]-perp[0]*bound, mid[1]-perp[1]*bound), (mid[0]+perp[0]*bound, mid[1]+perp[1]*bound)))
    return bisect_lines

def find_intersections(b_lines, boundary):
    lines = b_lines + boundary
    for l1 in range(len(lines)):
        for l2 in range(l1+1, len(lines)):
            intr = lines[l1].intersects(lines[l2])
            if intr:
                intr.seg1 = lines[l1]
                intr.seg2 = lines[l2]
                lines[l1].add_intr(intr)
                lines[l2].add_intr(intr)

def cull_intersection(intr, site, line):
    line2 = intr.seg1 if line is intr.seg2 else intr.seg2
    if not line2.same_side(line.end, site):
        line.end.x = intr.x
        line.end.y = intr.y
    elif not line2.same_side(line.start, site):
        line.start.x = intr.x
        line.start.y = intr.y
    
    to_remove = []
    for i in line.intr_list:
        if i is not intr and not line2.same_side(i, site):
            to_remove.append(i)
    for r in to_remove: r.remove()

def cull_line(line, intr, site, iteration=0):
    recurse1 = intr.seg1 if line is intr.seg2 else intr.seg2
    cull_intersection(intr, site, line)

    line.sort_intr(intr)

    recurse2 = None
    if len(line.intr_list) > 1:
        closest_intr = line.intr_list[1]
        recurse2 = closest_intr.seg1 if line is closest_intr.seg2 else closest_intr.seg2
        cull_intersection(closest_intr, site, line)
    line.complete = True
        
    ret = []
    r = None
    if not recurse1.complete:
        r = cull_line(recurse1, intr, site, iteration=iteration+1)
        ret.extend(r[0])
        iteration = r[1]
    if recurse2 != None and not recurse2.complete:
        r2 = cull_line(recurse2, closest_intr, site, iteration=iteration+1 if r == None else r[1]+1)
        ret.extend(r2[0])
    ret.append(line)
    return (ret, iteration)

def compute_voronoi(sites, bound):
    #Boundary
    boundary = [Line((bound[0],bound[0]),(bound[1],bound[0])), Line((bound[1],bound[0]),(bound[1],bound[1])), Line((bound[1],bound[1]), (bound[0],bound[1])), Line((bound[0],bound[1]), (bound[0],bound[0]))]
    
    #Bisect Lines
    b_lines = bisect_lines(sites, bound[1]-bound[0])
    
    voronoi_edges = []
    voronoi_cells = []
    #Loop through Sites
    for i in range(len(sites)):
        curr_boundary = deepcopy(boundary)
        find_intersections(b_lines[sites[i]], curr_boundary)
        first_line = min(b_lines[sites[i]]+curr_boundary, key=lambda l : sites[i].distance_to_line(l))
        first_intr = min(first_line.intr_list, key=lambda l : sites[i].distance(l))
        result = cull_line(first_line, first_intr, sites[i])[0]
        voronoi_edges.extend(result)
        voronoi_cells.append(order_lines(result))
        
    return (voronoi_edges, voronoi_cells)

def get_voronoi_vertices(voronoi_edges):
    voronoi_points = []
    for l in voronoi_edges:
        voronoi_points.extend((tuple([round(p,1) for p in l.tup_rep()[0]]), tuple([round(p,1) for p in l.tup_rep()[1]])))
    return list(OrderedDict.fromkeys(voronoi_points))

def compute_delaunay(sites, voronoi_cells):
    delaunay_tri = []
    polygons = []
    delaunay_points = np.array([[s.x, s.y] for s in sites])
    con_hull = ConvexHull(delaunay_points) if len(delaunay_points) > 2 else None
    for c in range(len(voronoi_cells)):
        for c2 in range(c+1, len(voronoi_cells)):
            if [[l for l in voronoi_cells[c] if l == l2] for l2 in voronoi_cells[c2]] != [[] for i in range(len(voronoi_cells[c2]))]:
                delaunay_tri.append(Line(sites[c], sites[c2]))
        polygons.append(Polygon(list(chain(*[l.tup_rep() for l in voronoi_cells[c]]))))
    
    if con_hull != None:            
        for simplex in con_hull.simplices:
            l = Line(delaunay_points[simplex][0,:], delaunay_points[simplex][1,:])
            if [d for d in delaunay_tri if d == l] == []:
                delaunay_tri.append(l)
    
    return (delaunay_tri, polygons)

if __name__ == '__main__':
    #Sites
    num_sites = 10
    bound = (0, 50)
    sites = [Point(randrange(bound[0]+1,bound[1]-1), randrange(bound[0]+1,bound[1]-1)) for i in range(num_sites)]
    voronoi_edges, voronoi_cells = compute_voronoi(sites, bound=bound)
    
    #Plot setup
    plt.figure(figsize=(16,16))
    plt.xlim(bound[0]-1, bound[1]+1)
    plt.ylim(bound[0]-1, bound[1]+1)
    
    #Visualize site
    for s in sites:
        s.plot()
        
    #Visualize voronoi edges
    for l in voronoi_edges:
        l.plot()
    
    voronoi_points = get_voronoi_vertices(voronoi_edges)
    for p in voronoi_points:
        plt.plot(*p, marker='o', markersize=10)
    
    delaunay_tri, polygons = compute_delaunay(sites, voronoi_cells)
    for poly in polygons:
        plot_polygon(poly, add_points=False, color=list(np.random.random(3))+[0.3])
    
    for d in delaunay_tri:
        d.plot(color='red')
    
    plt.show()