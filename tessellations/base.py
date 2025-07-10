# tessellations/base.py
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt

class Tessellation:
    """A base class for 2D and 3D tessellations."""
    def __init__(self, dim):
        if dim not in [2, 3]:
            raise ValueError("Dimension must be 2 or 3.")
        self.dim = dim
        if self.dim == 2:
            self.bounds = [0, 0, 1, 1]  # minx, miny, maxx, maxy
        else:
            self.bounds = [0, 1, 0, 1, 0, 1]  # xmin, xmax, ymin, ymax, zmin, zmax
        self.cells = []
        self.hyperplanes = []

    def sample(self, *args, **kwargs):
        """The core method to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the sample method.")

    def visualize(self):
        """Visualizes the tessellation."""
        if self.dim == 2:
            if not self.cells:
                print("No cells to visualize. Run the .sample() method first.")
                return
            fig, ax = plt.subplots()
            for cell in self.cells:
                x, y = cell.exterior.xy
                ax.fill(x, y, facecolor='w', edgecolor='k', linewidth=0.7)
            ax.set_aspect('equal', 'box')
            ax.axis('off')
            plt.show()
        else: # 3D
            if not self.hyperplanes:
                print("No hyperplanes to visualize. Run the .sample() method first.")
                return
            
            plotter = pv.Plotter(window_size=[1024, 1024])
            plotter.set_background('white')

            box = pv.Box(bounds=self.bounds)
            
            slices = []
            outlines = []
            for p, n in self.hyperplanes:
                slice_outline = box.slice(normal=n, origin=p)
                if slice_outline.n_points > 0:
                    filled_slice = slice_outline.delaunay_2d()
                    slices.append(filled_slice)
                    outlines.append(slice_outline)

            for s in slices:
                plotter.add_mesh(s, color='darkgrey', show_edges=False)

            for o in outlines:
                plotter.add_mesh(o, color='k', line_width=1)

            plotter.add_mesh(box, style='wireframe', color='black', line_width=2)
            
            plotter.enable_lightkit()
            
            plotter.camera_position = 'iso'
            plotter.enable_parallel_projection()
            
            plotter.show()