from collections import deque
import numpy as np
from shapely.geometry import box, LineString
from shapely.ops import split
import pyvista as pv
from .base import Tessellation


class MondrianTessellation(Tessellation):
    """Axis-aligned STIT-like process (Mondrian process).

    Recursively splits an axis-aligned box with exponential waiting times.
    The split rate for a cell is the sum of its side lengths; the split
    dimension is chosen with probability proportional to that side's length;
    the cut location is uniform along that side.
    """

    def __init__(self, dim, direction_matrix=None):
        # Ignore any directional matrix; Mondrian splits are axis-aligned only
        super().__init__(dim)
        if direction_matrix is not None:
            print("Note: Directional distribution is ignored for Mondrian process (axis-aligned only).")

    def sample(self, stop_time: float):
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
                # Rectangle side lengths
                cminx, cminy, cmaxx, cmaxy = cell.bounds
                lengths = np.array([max(cmaxx - cminx, 0.0), max(cmaxy - cminy, 0.0)], dtype=float)
            else:
                # Box side lengths
                b = cell.bounds  # [xmin, xmax, ymin, ymax, zmin, zmax]
                lengths = np.array([
                    max(b[1] - b[0], 0.0),
                    max(b[3] - b[2], 0.0),
                    max(b[5] - b[4], 0.0),
                ], dtype=float)

            rate = float(lengths.sum())
            if rate <= 1e-12:
                self.cells.append(cell)
                continue

            lifetime = np.random.exponential(1.0 / rate)
            if birth_time + lifetime > stop_time:
                self.cells.append(cell)
                continue

            current_time = birth_time + lifetime

            # Choose split dimension proportional to side length
            probs = lengths / rate
            axis = int(np.random.choice(len(lengths), p=probs))

            if self.dim == 2:
                cminx, cminy, cmaxx, cmaxy = cell.bounds
                if axis == 0:
                    c = np.random.uniform(cminx, cmaxx)
                    # Vertical line x = c
                    line = LineString([(c, cminy - 1e3), (c, cmaxy + 1e3)])
                    p = np.array([c, 0.5 * (cminy + cmaxy)])
                    n = np.array([1.0, 0.0])
                else:
                    c = np.random.uniform(cminy, cmaxy)
                    # Horizontal line y = c
                    line = LineString([(cminx - 1e3, c), (cmaxx + 1e3, c)])
                    p = np.array([0.5 * (cminx + cmaxx), c])
                    n = np.array([0.0, 1.0])

                self.hyperplanes.append((p, n))

                try:
                    parts = list(split(cell, line).geoms)
                    if len(parts) < 2:
                        # Degenerate split; keep cell
                        self.cells.append(cell)
                        continue
                except Exception:
                    self.cells.append(cell)
                    continue

                for new_cell in parts:
                    active_cells.append((new_cell, current_time))

            else:  # 3D
                b = cell.bounds
                if axis == 0:
                    c = np.random.uniform(b[0], b[1])
                    n = np.array([1.0, 0.0, 0.0])
                    p = np.array([c, 0.5 * (b[2] + b[3]), 0.5 * (b[4] + b[5])])
                elif axis == 1:
                    c = np.random.uniform(b[2], b[3])
                    n = np.array([0.0, 1.0, 0.0])
                    p = np.array([0.5 * (b[0] + b[1]), c, 0.5 * (b[4] + b[5])])
                else:
                    c = np.random.uniform(b[4], b[5])
                    n = np.array([0.0, 0.0, 1.0])
                    p = np.array([0.5 * (b[0] + b[1]), 0.5 * (b[2] + b[3]), c])

                self.hyperplanes.append((p, n))

                try:
                    c1 = cell.clip(normal=n, origin=p, invert=False)
                    c2 = cell.clip(normal=n, origin=p, invert=True)
                    parts = []
                    if c1.n_points > 0 and c1.n_cells > 0:
                        parts.append(c1)
                    if c2.n_points > 0 and c2.n_cells > 0:
                        parts.append(c2)
                    if len(parts) < 2:
                        self.cells.append(cell)
                        continue
                except Exception:
                    self.cells.append(cell)
                    continue

                for new_cell in parts:
                    active_cells.append((new_cell, current_time))

        return self

