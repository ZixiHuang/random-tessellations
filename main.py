# run_tessellation.py
import argparse
from tessellations import PoissonTessellation, STITTessellation

def main():
    """Main function to run the tessellation sampler from the command line."""
    parser = argparse.ArgumentParser(description="Generate and visualize 2D/3D tessellations.")
    
    parser.add_argument("type", type=str, choices=['poisson', 'stit'], 
                        help="The type of tessellation to generate.")
    
    parser.add_argument("dim", type=str, choices=['2d', '3d'], 
                        help="The dimension of the tessellation.")
    
    parser.add_argument("--lam", type=float, 
                        default=10,
                        help="Intensity for poisson tessellation.")
    parser.add_argument("--stop_time", type=float, 
                        default=20,
                        help="Stop time for STIT tessellation.")

    args = parser.parse_args()

    dim = 2 if args.dim == '2d' else 3
    
    # Select and instantiate the correct class
    if args.type == 'poisson':
        tess = PoissonTessellation(dim)
        param_name = 'lam'
        param_val = args.lam
    else:
        tess = STITTessellation(dim)
        param_name = 'stop_time'
        param_val = args.stop_time

    print(f"Generating {args.dim} {args.type} tessellation with {param_name}={param_val}...")
    
    # Sample and visualize
    tess.sample(param_val)
    tess.visualize()

if __name__ == '__main__':
    main()