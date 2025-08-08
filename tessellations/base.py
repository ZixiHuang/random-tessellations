# tessellations/base.py
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt

class Tessellation:
    """A base class for 2D and 3D tessellations."""
    def __init__(self, dim, direction_matrix=None):
        if dim not in [2, 3]:
            raise ValueError("Dimension must be 2 or 3.")
        self.dim = dim
        if self.dim == 2:
            self.bounds = [0, 0, 1, 1]  # minx, miny, maxx, maxy
        else:
            self.bounds = [0, 1, 0, 1, 0, 1]  # xmin, xmax, ymin, ymax, zmin, zmax
        self.cells = []
        self.hyperplanes = []

        # Optional directional distribution over normals
        self.direction_unit_vectors = None  # shape (k, dim)
        self.direction_probabilities = None  # shape (k,)
        if direction_matrix is not None:
            self._set_direction_matrix(direction_matrix)

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

    # --- Directional distribution helpers ---
    def _set_direction_matrix(self, direction_matrix):
        """Configure a discrete directional distribution from a matrix.

        Each row is a direction vector in R^dim. The row's Euclidean norm is
        the weight. Vectors are normalized to unit length for use as normals.
        Weights are normalized to sum to 1; if renormalization is required,
        a message is printed.
        """
        mat = np.asarray(direction_matrix, dtype=float)
        if mat.ndim != 2:
            raise ValueError("Direction matrix must be 2D (rows = directions, cols = dimensions).")
        if mat.shape[1] != self.dim:
            raise ValueError(f"Direction matrix must have exactly {self.dim} columns; got {mat.shape[1]}.")

        # Compute norms (weights) and filter out zero rows (zero weight)
        row_norms = np.linalg.norm(mat, axis=1)
        positive_mask = row_norms > 0
        if not np.any(positive_mask):
            raise ValueError("Direction matrix contains no non-zero rows; cannot form a distribution.")

        unit_vectors = mat[positive_mask] / row_norms[positive_mask][:, None]
        weights = row_norms[positive_mask]
        weight_sum = float(weights.sum())
        if not np.isclose(weight_sum, 1.0):
            print(f"Note: Directional weights normalized to sum to 1 (original sum = {weight_sum:.6f}).")
        probabilities = weights / weight_sum

        self.direction_unit_vectors = unit_vectors
        self.direction_probabilities = probabilities

    def _sample_direction(self):
        """Sample a unit direction according to the configured distribution, or isotropically if none."""
        if self.direction_unit_vectors is None or self.direction_probabilities is None:
            v = np.random.standard_normal(size=self.dim)
            return v / np.linalg.norm(v)
        idx = np.random.choice(self.direction_unit_vectors.shape[0], p=self.direction_probabilities)
        return self.direction_unit_vectors[idx]