# Visual Random Tessellations

This project generates and visualizes random tessellations in 2D and 3D.

## Project Structure

- `tessellations/`: A Python package containing the core OO classes for the tessellations.
- `main.py`: The main executable script for generating tessellations via CLI.
- `requirements.txt`: A list of project dependencies.

---

## Supported Tessellations

The project currently supports:

### 1. Poisson Hyperplane Tessellation (`poisson`)

### 2. STIT Tessellation (`stit`)

### 3. Mondrian Process (`mondrian`)
Axis-aligned recursive partition process. Ignores `--dir_matrix`.

## Installation

1.  **Create and activate a Conda environment** (recommended):
    ```bash
    conda create --name tess_env python=3.10 -y
    conda activate tess_env
    ```

2.  **Install the required dependencies** into the active environment:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the main script from the command line with the following arguments:

`python main.py {type} {dim} [--lam FLOAT | --stop_time FLOAT] [--dir_matrix PATH] [--animate]`

-   `{type}`: The type of tessellation. Choices: `poisson`, `stit`, `mondrian`.
-   `{dim}`: The dimension. Choices: `2d`, `3d`.
-   Parameter flags:
    -   For `poisson`, use `--lam` (intensity of the underlying Poisson point process), a float.
    -   For `stit`, use `--stop_time` (global stopping time for the cell division process), a float.

-   `--dir_matrix PATH` (optional): Path to a CSV or NPY/NPZ file containing a directional distribution matrix.
    -   Each row is a direction vector in R^d.
    -   The row's Euclidean norm is used as its weight.
    -   If weights do not sum to 1, they will be normalized automatically and a note will be printed.
    -   Vectors are normalized to unit length before use.
    -   Ignored for `mondrian`.

-   `--animate` (optional): Animate by plotting generated hyperplanes one by one.
    -   2D: draws each line sequentially using matplotlib.
    -   3D: incrementally adds each sliced plane in a PyVista window.

### Examples

**2D Poisson Tessellation (lam = 10)**
```bash
python main.py poisson 2d --lam 10
```

**3D STIT Tessellation (stop_time = 20)**
```bash
python main.py stit 3d --stop_time 20
```

**Animate 2D Poisson Tessellation**
```bash
python main.py poisson 2d --lam 20 --animate
```

**Animate 3D STIT Tessellation**
```bash
python main.py stit 3d --stop_time 10 --animate
```

**2D Poisson with directional distribution from CSV**
```bash
python main.py poisson 2d --lam 10 --dir_matrix directions.csv
```

Example CSV (3 rows, 2 columns for 2D):
```
1,0
0,2
1,1
```
This defines three directions with weights equal to their norms (1, 2, sqrt(2)), which will be normalized to sum to 1.