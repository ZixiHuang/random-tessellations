# Tessellation Sampler Project

This project generates and visualizes Poisson and STIT tessellations in 2D and 3D using a command-line interface.

## Project Structure

- `tessellations/`: A Python package containing the core OO classes for the tessellations.
- `main.py`: The main executable script for generating tessellations via CLI.
- `requirements.txt`: A list of project dependencies.

---

## Installation ⚙️

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

## Usage 🚀

Run the main script from the command line with the following arguments:

`python main.py {type} {dim} {param}`

-   `{type}`: The type of tessellation. Choices: `poisson`, `stit`.
-   `{dim}`: The dimension. Choices: `2d`, `3d`.
-   `{param}`: A numeric parameter.
    -   For `poisson`, this is `lam` (intensity), a float.
    -   For `stit`, this is `n_iter` (number of iterations), an integer.

### Examples

**2D Poisson Tessellation (lam = 12.5)**
```bash
python main.py poisson 2d 12.5
```

**3D STIT Tessellation (30 iterations)**
```bash
python main.py stit 3d 30
```