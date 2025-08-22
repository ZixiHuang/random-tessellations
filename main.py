# run_tessellation.py
import argparse
import os
import numpy as np
from tessellations import PoissonTessellation, STITTessellation, MondrianTessellation

def main():
    """Main function to run the tessellation sampler from the command line."""
    parser = argparse.ArgumentParser(description="Generate and visualize 2D/3D tessellations.")
    
    parser.add_argument("type", type=str, choices=['poisson', 'stit', 'mondrian'], 
                        help="The type of tessellation to generate.")
    
    parser.add_argument("dim", type=str, choices=['2d', '3d'], 
                        help="The dimension of the tessellation.")
    
    parser.add_argument("--lam", type=float, 
                        default=10,
                        help="Intensity for poisson tessellation.")
    parser.add_argument("--stop_time", type=float, 
                        default=20,
                        help="Stop time for STIT tessellation.")

    parser.add_argument(
        "--dir_matrix",
        type=str,
        default=None,
        help=(
            "Optional path to a CSV or NPY file specifying a directional distribution matrix. "
            "Each row is a direction vector; its norm is used as the weight. "
            "If weights do not sum to 1, they will be normalized with a note."
        ),
    )

    parser.add_argument(
        "--animate",
        action="store_true",
        help="Animate by plotting generated hyperplanes one by one.",
    )

    args = parser.parse_args()

    dim = 2 if args.dim == '2d' else 3
    
    # Load optional directional distribution matrix
    direction_matrix = None
    if args.dir_matrix is not None:
        if not os.path.exists(args.dir_matrix):
            raise FileNotFoundError(f"Directional matrix file not found: {args.dir_matrix}")
        try:
            if args.dir_matrix.lower().endswith((".npy", ".npz")):
                loaded = np.load(args.dir_matrix)
                if isinstance(loaded, np.lib.npyio.NpzFile):
                    # Heuristic: take the first array
                    first_key = list(loaded.keys())[0]
                    direction_matrix = loaded[first_key]
                else:
                    direction_matrix = loaded
            else:
                # CSV or text
                direction_matrix = np.loadtxt(args.dir_matrix, delimiter=",")
        except Exception as e:
            raise ValueError(f"Failed to load direction matrix from {args.dir_matrix}: {e}")

        # Validate dimensionality
        if direction_matrix.ndim != 2:
            raise ValueError("Direction matrix must be 2D (rows = directions, cols = dimensions).")
        expected_cols = 2 if args.dim == '2d' else 3
        if direction_matrix.shape[1] != expected_cols:
            raise ValueError(
                f"Direction matrix shape mismatch: expected {expected_cols} columns for {args.dim}, "
                f"got {direction_matrix.shape[1]}"
            )

    # Select and instantiate the correct class
    if args.type == 'poisson':
        tess = PoissonTessellation(dim, direction_matrix=direction_matrix)
        param_name = 'lam'
        param_val = args.lam
    elif args.type == 'stit':
        tess = STITTessellation(dim, direction_matrix=direction_matrix)
        param_name = 'stop_time'
        param_val = args.stop_time
    else:
        tess = MondrianTessellation(dim)
        param_name = 'stop_time'
        param_val = args.stop_time

    print(f"Generating {args.dim} {args.type} tessellation with {param_name}={param_val}...")
    
    # Sample and visualize
    tess.sample(param_val)
    tess.visualize(animate=args.animate)

if __name__ == '__main__':
    main()