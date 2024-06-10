from collections import namedtuple, defaultdict
import re
Event = namedtuple('Event', ['sid', 'eid'])

class IdList:
    def __init__(self, seq:str, events: list[Event]):
        self.seq = seq
        self.events = events
    
    def __str__(self):
        return f"{self.seq} : {self.events}" 
        
def load_spmf_data(file_path: str) -> list[list[str]]:
    horizontal_data : list[list[str]] = []
    with open(file_path) as data:
        for sequence in data:
            events = sequence.split('-1')
            events.pop()
            events = [item_set.split() for item_set in events]
            horizontal_data.append(events)
    return horizontal_data

def hor_to_vert(hor_data):
    """
    Convert the data from the horizontal format to a vertical one

    Args:
        data (_type_): _description_
    Returns:
        dict(element, list[tuple(sid, eid)])
    """
    vertical_data : dict[str, list[Event[int, int]]] = {}
    for sid, sequence in enumerate(hor_data):
        for eid, event in enumerate(sequence):
            for element in event:
                if element not in vertical_data:
                    vertical_data[element] = [Event(sid, eid)]
                else:
                    vertical_data[element].append(Event(sid,eid))
    return vertical_data

def count_frequent_one_seq(id_lists : dict, min_sup : int):
    """
    Identify one element frequent sequences

    Args:
        id_list (_type_): _description_
        min_sup (_type_): _description_
    """
    frequent_one : dict[str, int] = {}
    for item, entries in id_lists.items():
        support = len(set([event.sid for event in entries]))
        if support >= min_sup:
            frequent_one[item] = support  
    return frequent_one

def count_frequent_two_seq(id_lists : dict, min_sup : int):
    """
    Identify two element frequent sequences

    Args:
        elements (_type_): _description_
        min_sup (_type_): _description_
    """
    # Vertical to horizontal on the fly conversion
    horizontal_format = {}
    
    for item, entries in id_lists.items():
        for event in entries:
            if event.sid not in horizontal_format:
                horizontal_format[event.sid] = [(item, event.eid)]
            else:
                horizontal_format[event.sid].append((item, event.eid))
        
    
    # create counts using horizontal_db
    frequent_two = defaultdict(int)
    
    for _,seq in horizontal_format.items():
        new_encountered = []
        for index_i,event_i in enumerate(seq):
            for _,event_j in enumerate(seq[index_i+1:]):
                        
                if event_i[1] < event_j[1]:
                    two_seq = event_i[0] + '>' + event_j[0]
                elif event_i[1] > event_j[1]:
                    two_seq = event_j[0] + '>' + event_i[0]
                else:
                    two_seq = ' '.join(sorted([event_i[0], event_j[0]]))

                new_encountered.append(two_seq)
        unique_new_encountered = sorted(set(new_encountered))
        for two_seq in unique_new_encountered:
            frequent_two[two_seq] += 1 
    
    frequent_two = {two_seq: count for two_seq, count in frequent_two.items() if count >= min_sup}       

    return frequent_two
    

def temporal_id_join(item_list_i : IdList, item_list_j : IdList) -> dict[str, list[Event]]:
    '''
    Given two item id-lists, return a dictionary of new joined id-lists
    indexed by the new correspoding item sequences.
    '''
    joined_lists : dict[str, list[Event]] = {}
    ## Only joining for sequences with same prefix
    separate_i = separate_prefix(item_list_i.seq) 
    separate_j = separate_prefix(item_list_j.seq)
    if separate_i[0] != separate_j[0]:
        return joined_lists

    for event_i in item_list_i.events:
        for event_j in item_list_j.events:
            if event_i.sid == event_j.sid:
                if event_i.eid > event_j.eid:
                    sup_seq = item_list_j.seq + '>' + separate_i[1]
                    if sup_seq not in joined_lists:
                        joined_lists[sup_seq] = []
                    joined_lists[sup_seq].append(Event(event_i.sid, event_i.eid))

                elif event_i.eid < event_j.eid:
                    sup_seq = item_list_i.seq + '>' + separate_j[1]
                    if sup_seq not in joined_lists:
                        joined_lists[sup_seq] = []
                    joined_lists[sup_seq].append(Event(event_i.sid, event_j.eid))

                elif separate_i[1] != separate_j[1]:
                    if separate_i[1] < separate_j[1]:
                        sup_seq = item_list_i.seq + ' ' + separate_j[1]
                    else:
                        sup_seq = item_list_j.seq + ' ' + separate_i[1]
                    if sup_seq not in joined_lists:
                        joined_lists[sup_seq] = []
                    joined_lists[sup_seq].append(Event(event_i.sid, event_j.eid))
    return joined_lists

def enumerate_frequent_seq(equiv_list : dict[str, list[Event]], min_sup):
    frequent_rest : dict[str, int] = {}
    frequent_elements_all : dict[str, list[Event]] = {}

    for index_i, seq_i in enumerate(equiv_list.keys()):
        frequent_elements_inner : dict[str, list[Event]] = {}
        for _, seq_j in enumerate(list(equiv_list.keys())[index_i + 1:]):
            R = temporal_id_join(IdList(seq_i, equiv_list[seq_i]), IdList(seq_j, equiv_list[seq_j]))
            for seq, id_list in R.items():
                support = len(set([event.sid for event in id_list]))
                if support >= min_sup:
                    frequent_elements_inner[seq] = id_list
                    frequent_rest[seq] = support
                    
        frequent_elements_all.update(frequent_elements_inner)
    if bool(frequent_elements_all):
        rest = enumerate_frequent_seq(frequent_elements_all, min_sup)
        frequent_rest.update(rest)
    return frequent_rest

def spade_sequencing(data, min_sup):
    """
    Perform the spade sequencing algorithm on a dataset

    Args:
        data (_type_): _description_
        min_sup (_type_): _description_
    """
    # Find frequent 1 element 
    print("Frequent one.")
    freq_all = count_frequent_one_seq(data, min_sup)

    # Find frequent 2 element
    print("Frequent two.")
    freq_two = count_frequent_two_seq(data, min_sup)
    
    # Get the Equivalence classes needed for the next step
    print("Equivalence classes.")
    equivalence_classes : dict[str, list[Event]] = {}
    for two_seq in freq_two.keys():
        items = separate_prefix(two_seq)
        R = temporal_id_join(IdList(items[0], data[items[0]]), IdList(items[1], data[items[1]]))
        for sequence, id_list in R.items():
            if sequence in freq_two:
                equivalence_classes[sequence] = id_list

    print("Enumerate frequent seq.")
    freq_rest = enumerate_frequent_seq(equivalence_classes, min_sup)
    
    freq_all.update(freq_two)
    freq_all.update(freq_rest)
    return freq_all

def save_to_file(results: dict, file_path):
    with open(file_path, "w") as results_file:
        for key, value in results.items():
            results_file.write(f"{key} : {value} \n")
            
def separate_prefix(sequence : str):
    split_pos = max(sequence.rfind(' '), sequence.rfind('>'))
    if split_pos == -1:
        return ["", sequence]
    else:
        return [sequence[:split_pos], sequence[split_pos+1:]]
            