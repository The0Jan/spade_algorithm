import pytest
import spade_algorithm.sequencer.spade as spade

test_file_path:str = "spade_algorithm/sequencer/tests/test_data/test.txt"
test_expanded_file_path:str = "spade_algorithm/sequencer/tests/test_data/test_expanded.txt"

def test_one_element():
    expected_results : dict = {'D': 2, 'A': 4, 'B': 4, 'F': 4}

    horiz_data = spade.load_spmf_data(test_file_path)
    vert_data = spade.hor_to_vert(horiz_data)
    results = spade.count_frequent_one_seq(vert_data, 2)

    assert expected_results == results
    
def test_one_element_expanded():
    expected_results : dict = {'D4': 2, 'A1': 4, 'B2': 4, 'F6': 4}

    horiz_data = spade.load_spmf_data(test_expanded_file_path)
    vert_data = spade.hor_to_vert(horiz_data)
    results = spade.count_frequent_one_seq(vert_data, 2)

    assert expected_results == results
    
def test_two_element():
    expected_results : dict = {'B F': 4, 'B>A': 2, 'D>B': 2, 'D>F': 2, 'F>A': 2, 'A B': 3, 'A F': 3, 'D>A': 2}

    horiz_data = spade.load_spmf_data(test_file_path)
    vert_data = spade.hor_to_vert(horiz_data)
    results = spade.count_frequent_two_seq(vert_data, 2)

    assert expected_results == results

def test_two_element_expanded():
    expected_results : dict = {'B2 F6': 4, 'B2>A1': 2, 'D4>B2': 2, 'D4>F6': 2, 'F6>A1': 2, 'A1 B2': 3, 'A1 F6': 3, 'D4>A1': 2}

    horiz_data = spade.load_spmf_data(test_expanded_file_path)
    vert_data = spade.hor_to_vert(horiz_data)
    results = spade.count_frequent_two_seq(vert_data, 2)

    assert expected_results == results
  

def test_temporal_join_simple_ab(capsys):
    expected_results : dict = {'A B': [spade.Event(0,0), spade.Event(1,0)]}
    
    A = spade.IdList('A', [spade.Event(0,0), spade.Event(1,0)])
    B = spade.IdList('B', [spade.Event(0,0), spade.Event(1,0)])
    
    with capsys.disabled():
        results = spade.temporal_id_join(B, A)
    
    assert expected_results == results
    
def test_temporal_join_simple_a_then_b():
    expected_results : dict = {'A>B': [spade.Event(0,1), spade.Event(1,1)]}
    
    A = spade.IdList('A', [spade.Event(0,0), spade.Event(1,0)])
    B = spade.IdList('B', [spade.Event(0,1), spade.Event(1,1)])
    
    results = spade.temporal_id_join(A, B)
    
    assert expected_results == results

def test_temporal_join_simple_b_then_a():
    expected_results : dict = {'B>A': [spade.Event(0,1), spade.Event(1,1)]}
    
    A = spade.IdList('A', [spade.Event(0,1), spade.Event(1,1)])
    B = spade.IdList('B', [spade.Event(0,0), spade.Event(1,0)])
    
    results = spade.temporal_id_join(A, B)
    
    assert expected_results == results

def test_temporal_join_simple_ab(capsys):
    expected_results : dict = {'A B': [spade.Event(0,0), spade.Event(1,0)]}
    
    A = spade.IdList('A', [spade.Event(0,0), spade.Event(1,0)])
    B = spade.IdList('B', [spade.Event(0,0), spade.Event(1,0)])
    
    with capsys.disabled():
        results = spade.temporal_id_join(B, A)
    
    assert expected_results == results
    
def test_temporal_join_longer_1():
    expected_results : dict = {'A B>B': [spade.Event(0,1), spade.Event(1,1)]}
    
    A = spade.IdList('A B', [spade.Event(0,0), spade.Event(1,0)])
    B = spade.IdList('A>B', [spade.Event(0,1), spade.Event(1,1)])
    
    results = spade.temporal_id_join(A, B)
    
    assert expected_results == results

def test_temporal_join_longer_2():
    expected_results : dict = {'A B C>A B>A': [spade.Event(0,1), spade.Event(1,1)]}
    
    A = spade.IdList('A B C>A>A', [spade.Event(0,1), spade.Event(1,1)])
    B = spade.IdList('A B C>A B', [spade.Event(0,0), spade.Event(1,0)])
    
    results = spade.temporal_id_join(A, B)
    
    assert expected_results == results

def test_temporal_join_longer_expanded():
    expected_results : dict = {'A1 B2 C3>A1 B2>A1': [spade.Event(0,1), spade.Event(1,1)]}
    
    A = spade.IdList('A1 B2 C3>A1>A1', [spade.Event(0,1), spade.Event(1,1)])
    B = spade.IdList('A1 B2 C3>A1 B2', [spade.Event(0,0), spade.Event(1,0)])
    
    results = spade.temporal_id_join(A, B)
    
    assert expected_results == results

def test_temporal_join_different_prefixes():
    expected_results : dict = {}
    
    A = spade.IdList('A D C>G>A', [spade.Event(0,1), spade.Event(1,1)])
    B = spade.IdList('A B C>A B', [spade.Event(0,0), spade.Event(1,0)])
    
    results = spade.temporal_id_join(A, B)
    
    assert expected_results == results

def test_spade_sequencing():
    expected_results : dict = {'D': 2, 'A': 4, 'B': 4, 
                               'F': 4, 'D>B': 2, 'B F': 4, 
                               'A F': 3, 'A B': 3, 'B>A': 2, 
                               'D>F': 2, 'D>A': 2, 'F>A': 2, 
                               'D>B F': 2, 'D>B>A': 2, 'D>B F>A': 2, 
                               'B F>A': 2, 'A B F': 3, 'D>F>A': 2}
    
    horiz_data = spade.load_spmf_data(test_file_path)
    vert_data = spade.hor_to_vert(horiz_data)
    results = spade.spade_sequencing(vert_data, 2)

    assert expected_results == results