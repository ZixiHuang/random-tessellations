# tessellations/poisson.py
import numpy as np
from shapely.geometry import box, LineString
from shapely.ops import split
import pyvista as pv
from .base import Tessellation

class PoissonTessellation(Tessellation):
    """Generates a Poisson hyperplane tessellation."""
    def sample(self, lam):
        if self.dim == 2:
            minx, miny, maxx, maxy = self.bounds
            initial_cell = box(minx, miny, maxx, maxy)
            metric = initial_cell.area
        else:
            initial_cell = pv.Box(bounds=self.bounds)
            metric = initial_cell.volume
        
        self.cells = [initial_cell]
        n_hyperplanes = np.random.poisson(lam * metric)

        if self.dim == 2:
            points = np.random.uniform(
                (self.bounds[0], self.bounds[1]),
                (self.bounds[2], self.bounds[3]),
                size=(n_hyperplanes, self.dim)
            )
        else:
            points = np.random.uniform(self.bounds[::2], self.bounds[1::2], size=(n_hyperplanes, self.dim))
        
        if n_hyperplanes > 0:
            normals = np.array([self._sample_direction() for _ in range(n_hyperplanes)], dtype=float)
        else:
            normals = np.zeros((0, self.dim), dtype=float)
        self.hyperplanes = list(zip(points, normals))

        for p, n in zip(points, normals):
            new_cells = []
            for cell in self.cells:
                self._clip_and_add(cell, p, n, new_cells)
            self.cells = new_cells
        return self

    def _clip_and_add(self, cell, p, n, new_cells):
        try:
            if self.dim == 2:
                # Construct a line whose direction is perpendicular to the normal n
                t = np.array([-n[1], n[0]], dtype=float)
                line = LineString([p - t * 1000, p + t * 1000])
                split_result = list(split(cell, line).geoms)
                new_cells.extend(split_result)
            else:
                c1 = cell.clip(normal=n, origin=p, invert=False)
                c2 = cell.clip(normal=n, origin=p, invert=True)
                if c1.n_points > 0: new_cells.append(c1)
                if c2.n_points > 0: new_cells.append(c2)
        except Exception:
            new_cells.append(cell)