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
    
    parser.add_argument("param", type=float, 
                        help="The parameter for the tessellation (lam for Poisson, stop_time for STIT).")

    args = parser.parse_args()

    dim = 2 if args.dim == '2d' else 3
    
    # Select and instantiate the correct class
    if args.type == 'poisson':
        tess = PoissonTessellation(dim)
        param_name = 'lam'
        param_val = args.param
    else: # stit
        tess = STITTessellation(dim)
        param_name = 'stop_time'
        param_val = args.param

    print(f"Generating {args.dim} {args.type} tessellation with {param_name}={param_val}...")
    
    # Sample and visualize
    tess.sample(param_val)
    tess.visualize()

if __name__ == '__main__':
    main()