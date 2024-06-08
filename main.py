from sequencer import spade


file_path:str = "sequencer/tests/test_data/test.txt"
horiz_data = spade.load_spmf_data(file_path)
vert_data = spade.hor_to_vert(horiz_data)

final = spade.spade_sequencing(vert_data, 2)
print(final)