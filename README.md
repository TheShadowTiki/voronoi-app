# Voronoi-Delaunay Sandbox App

## Overview
The Voronoi-Delaunay Sandbox App is designed for generating and visualizing Voronoi diagrams and Delaunay triangulations. It provides a user-friendly interface for exploring the geometric and computational properties of these fundamental structures in computational geometry. Users can add points incrementally (left click), move points around (with right click + drag), and observe the effect of these changes on the Voronoi diagram and Delaunay triangulation.

This implementation utilizes a custom algorithm to calculate both the Voronoi Diagram and Delaunay Triangulation of input points. This approach differs from traditional methods by employing recursive intersection management and line culling to refine the geometric structures.

To generate the Voronoi Diagram, the algorithm calculates perpendicular bisectors between each pair of input points, forming a set of potential Voronoi edges. These edges are then refined using a recursive culling process to ensure they form valid Voronoi cells around each site. This method directly constructs the Voronoi diagram without relying on dual relationships with the Delaunay triangulation.

The Delaunay Triangulation is derived from the Voronoi cells by identifying connections between sites that share Voronoi edges. Convex hull computations ensure completeness by adding necessary edges for points on the boundary. This novel approach allows for efficient handling of edge cases and boundary conditions.

## Application Interface Demo

https://github.com/user-attachments/assets/5975d880-599c-4e3c-b088-a54cc099df80

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
