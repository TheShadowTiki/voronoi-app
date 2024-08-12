# Voronoi-Delaunay Sandbox App

## Overview
The Voronoi-Delaunay Sandbox App is designed for generating and visualizing Voronoi diagrams and Delaunay triangulations. It provides a user-friendly interface for exploring the geometric and computational properties of these fundamental structures in computational geometry. Users can add points incrementally (left click), move points around (with right click + drag), and observe the effect of these changes on the Voronoi diagram and Delaunay triangulation.

This implementation utilizes a custom algorithm to calculate both the Voronoi Diagram and Delaunay Triangulation of input points. This approach differs from traditional methods by employing recursive intersection management and line culling to refine the geometric structures.

To generate the Voronoi Diagram, the algorithm calculates perpendicular bisectors between each pair of input points, forming a set of potential Voronoi edges. These edges are then refined using a recursive culling process to ensure they form valid Voronoi cells around each site. This method directly constructs the Voronoi diagram without relying on dual relationships with the Delaunay triangulation.

The Delaunay Triangulation is derived from the Voronoi cells by identifying connections between sites that share Voronoi edges. Convex hull computations ensure completeness by adding necessary edges for points on the boundary. This novel approach allows for efficient handling of edge cases and boundary conditions.

## Application Interface Demo

https://github.com/user-attachments/assets/5975d880-599c-4e3c-b088-a54cc099df80

# Voronoi Diagram Construction Algorithm

## Overview

This algorithm constructs a Voronoi diagram from a set of input sites within a specified boundary. It calculates Voronoi edges and cells through the use of geometric bisectors and recursive culling of line segments.

## Pseudocode

```plaintext
Algorithm VoronoiDiagram

Input: 
  sites: List of site points (x, y) in 2D space
  boundary: Rectangular boundary defining the diagram limits

Output:
  voronoiEdges: List of line segments forming Voronoi edges
  voronoiCells: List of polygons representing Voronoi cells

Procedure:
  1. Initialize boundaryLines with lines defining the rectangular boundary.
  
  2. For each pair of sites (site1, site2):
     a. Compute the midpoint between site1 and site2.
     b. Calculate the perpendicular bisector of the line connecting site1 and site2.
     c. Store the bisector in a data structure (e.g., dictionary) for later use.

  3. Initialize empty lists voronoiEdges and voronoiCells.

  4. For each site in sites:
     a. Initialize currentBoundary as a copy of boundaryLines.
     b. Find all intersections between bisector lines for the current site and currentBoundary.
     c. Select the line segment closest to the site as the starting point.
     d. Perform recursive culling to trim line segments:
        i.   Call RecursiveCull(line, intersection, site) for the starting line.
        ii.  Add resulting line segments to voronoiEdges.
        iii. Order the line segments to form a closed polygon and add to voronoiCells.

  5. Return voronoiEdges and voronoiCells as the result.

Procedure RecursiveCull(line, intersection, site):
  1. Determine the opposite line segment sharing the intersection.
  2. Adjust the current line's endpoints to the intersection, if necessary.
  3. Remove irrelevant intersections from the current line's list.
  4. Mark the current line as complete.
  5. Sort intersections of the current line to find the next closest.
  6. If there are more intersections:
     a. Select the next intersection as the closest point.
     b. Determine the connected line segment for the next intersection.
     c. If the connected line is not complete:
        i.   Call RecursiveCull(connectedLine, nextIntersection, site).
  7. Return the trimmed line segments to be added to the Voronoi cell.

End Algorithm
```

## Installation

1. **Create a virtual environment:**
   ```sh
   conda create -n voronoi python=3.9
   conda activate voronoi

2. **Install Requirements:**
   ```sh
   pip install -r requirements.txt
3. **Run Application:**
   ```sh
   python voronoi_app.py  
