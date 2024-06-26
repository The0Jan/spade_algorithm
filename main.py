import argparse
import time
from sequencer import spade

def return_parsed_args():
    parser = argparse.ArgumentParser(description = "Sequence a file in SPMF format using the SPADE algorithm.")
    parser.add_argument("--data", type=str, help="Data file path")
    parser.add_argument("--save", type=str, help="Save file path")
    parser.add_argument("--min_sup", default=2, type=int, help="Minimal support for algorithm")
    args = parser.parse_args()
    return args

def main(args):
    print(f"Dataset:{args.data} |Minimal support:{args.min_sup}")
    horiz_data = spade.load_spmf_data(args.data)
    vert_data = spade.hor_to_vert(horiz_data)

    start = time.time()
    final = spade.spade_sequencing(vert_data, args.min_sup)
    end = time.time()
    
    print(f"Elapsed time:{round(end - start, 3)} seconds.")
    spade.save_to_file(final, args.save)


if __name__ == "__main__":
    args = return_parsed_args()
    main(args)