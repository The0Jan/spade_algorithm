import pytest
import spade_algorithm.sequencer.spade as spade

test_file_path:str = "spade_algorithm/sequencer/tests/test_data/test.txt"


def test_one_element():
    expected_results : dict = {'D': 2, 'A': 4, 'B': 4, 'F': 4}

    horiz_data = spade.load_spmf_data(test_file_path)
    vert_data = spade.hor_to_vert(horiz_data)
    results = spade.count_frequent_one_seq(vert_data, 2)

    assert expected_results == results
    
def test_two_element():
    expected_results : dict = {'B F': 4, 'B->A': 2, 'D->B': 2, 'D->F': 2, 'F->A': 2, 'A B': 3, 'A F': 3, 'D->A': 2}

    horiz_data = spade.load_spmf_data(test_file_path)
    vert_data = spade.hor_to_vert(horiz_data)
    results = spade.count_frequent_two_seq(vert_data, 2)

    assert expected_results == results