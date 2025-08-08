# tessellations/stit.py
from collections import deque
import numpy as np
from shapely.geometry import box, LineString
from shapely.ops import split
import pyvista as pv
from .base import Tessellation

class STITTessellation(Tessellation):
    """Generates a Stable Iterative Tessellation based on a recursive splitting process."""
    def sample(self, stop_time):
        """
        Generates the tessellation using a time-based recursive splitting process.
        """
        if self.dim == 2:
            minx, miny, maxx, maxy = self.bounds
            initial_cell = box(minx, miny, maxx, maxy)
        else:
            initial_cell = pv.Box(bounds=self.bounds)
        
        active_cells = deque([(initial_cell, 0.0)])
        self.cells = []
        self.hyperplanes = []

        while active_cells:
            cell, birth_time = active_cells.popleft()

            if self.dim == 2:
                metric = cell.area
            else:
                metric = cell.volume

            if metric <= 1e-9:
                self.cells.append(cell)
                continue

            lifetime = np.random.exponential(1.0 / metric)

            if birth_time + lifetime > stop_time:
                self.cells.append(cell)
            else:
                current_time = birth_time + lifetime

                cell_bounds = cell.bounds
                if self.dim == 2:
                    low = (cell_bounds[0], cell_bounds[1])
                    high = (cell_bounds[2], cell_bounds[3])
                    p = np.random.uniform(low, high, size=2)
                else: # 3D
                    p = np.random.uniform(cell_bounds[::2], cell_bounds[1::2], size=3)

                n = self._sample_direction()
                self.hyperplanes.append((p, n))

                split_cells = []
                self._clip_and_add(cell, p, n, split_cells)

                for new_cell in split_cells:
                    active_cells.append((new_cell, current_time))
        
        return self

    def _clip_and_add(self, cell, p, n, new_cells):
        try:
            if self.dim == 2:
                line = LineString([p - 1000 * n, p + 1000 * n])
                new_cells.extend(list(split(cell, line).geoms))
            else:
                c1 = cell.clip(normal=n, origin=p, invert=False)
                c2 = cell.clip(normal=n, origin=p, invert=True)
                if c1.n_points > 0 and c1.n_cells > 0: new_cells.append(c1)
                if c2.n_points > 0 and c2.n_cells > 0: new_cells.append(c2)
        except Exception:
            new_cells.append(cell)