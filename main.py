import argparse
import timeit
from sequencer import spade

def return_parsed_args():
    parser = argparse.ArgumentParser(description = "Sequence a file in SPMF format using the SPADE algorithm.")
    parser.add_argument("--data", type=str, help="Data file path")
    parser.add_argument("--save", type=str, help="Save file path")
    parser.add_argument("--min_sup", default=2, type=int, help="Minimal support for algorithm")
    args = parser.parse_args()
    return args

def main(args):
    horiz_data = spade.load_spmf_data(args.data)
    vert_data = spade.hor_to_vert(horiz_data)
    
    start = timeit.timeit()
    final = spade.spade_sequencing(vert_data, args.min_sup)
    end = timeit.timeit()
    
    print("Elapsed time:", start - end)
    spade.save_to_file(final, args.save)


if __name__ == "__main__":
    args = return_parsed_args()
    main(args)