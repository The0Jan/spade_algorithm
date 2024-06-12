from spmf import Spmf
import time
BIN_PATH = "spmf_file/"

def spmf_sequence(data_file, output_file, min_sup):
    start = time.time()
    spmf = Spmf("SPADE", spmf_bin_location_dir = BIN_PATH ,input_filename=data_file,
            output_filename=output_file, arguments=[min_sup])
    spmf.run()
    end = time.time()
    print(f"Data file:{data_file} | Minimal support:{min_sup}")
    print(f"Elapsed time:{round(end - start, 3)} seconds.")


def spmf_sequence_multiple(data_file, output_file_editable, seq_count, sup_list):
    for min_sup in sup_list:
        spmf_sequence(data_file, output_file_editable.format(min_sup), min_sup/seq_count)

spmf_sequence_multiple("data/pfden.txt", "results_spfm/pfden_results_{0}.txt", 35, [12, 16, 20])
spmf_sequence_multiple("data/bike.txt", "results_spfm/bike_results_{0}.txt", 21078, [500, 750, 1000] )
spmf_sequence_multiple("data/online_retail.txt", "results_spfm/online_retail_results_{0}.txt", 4383, [1500, 1600, 1700])