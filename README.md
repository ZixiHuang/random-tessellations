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

## Installation

1.  **Create and activate a Conda environment** (recommended):
    ```bash
    conda create --name tessellations python=3.10 -y
    conda activate tessellations
    ```

2.  **Install the required dependencies** into the active environment:
    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

Run the main script from the command line with the following arguments:

`python main.py {type} {dim} {param}`

-   `{type}`: The type of tessellation. Choices: `poisson`, `stit`.
-   `{dim}`: The dimension. Choices: `2d`, `3d`.
-   `{param}`:
    -   For `poisson`, this is `lam` (the intensity of the underlying Poisson point process), a float.
    -   For `stit`, this is `stop_time` (the global stopping time for the cell division process), a float.

### Examples

**2D Poisson Tessellation (lam = 10)**
```bash
python main.py poisson 2d --lam 10
```

**3D STIT Tessellation (stop_time = 20)**
```bash
python main.py stit 3d --stop_time 20
```