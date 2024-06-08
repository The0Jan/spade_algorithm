from collections import namedtuple, defaultdict

#ToDo
# Create convert
# Test convert
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
    
    for sid,seq in horizontal_format.items():
        new_encountered = []
        for index_i,event_i in enumerate(seq):
            for index_j,event_j in enumerate(seq[index_i+1:]):
                        
                if event_i[1] < event_j[1]:
                    two_seq = event_i[0] + '->' + event_j[0]
                elif event_i[1] > event_j[1]:
                    two_seq = event_j[0] + '->' + event_i[0]
                else:
                    two_seq = ' '.join(sorted([event_i[0], event_j[0]]))

                new_encountered.append(two_seq)
        unique_new_encountered = set(new_encountered)
        for two_seq in unique_new_encountered:
            frequent_two[two_seq] += 1 
    
    frequent_two = {two_seq: count for two_seq, count in frequent_two.items() if count >= min_sup}       

    return frequent_two
    
    
    
    
        
    
def temporal_id_join(item_list_i : IdList, item_list_j : IdList):
    '''
    Given two item id-lists, return a dictionary of new joined id-lists
    indexed by the new correspoding item sequences.
    '''
    joined_lists : dict[str, list[Event[int, int]]] = {}
    
    for event_i in item_list_i.events:
        for event_j in item_list_j.events:
            if event_i.sid == event_j.sid:
                
                if event_i.eid > event_j.eid:
                    sup_seq = item_list_i.seq + '->' + item_list_j.seq[-1]
                    joined_lists[sup_seq].append(Event(event_i.sid, event_i.eid))
                
                elif event_i.eid < event_j.eid:
                    sup_seq = item_list_j.seq + '->' + item_list_i.seq[-1]
                    joined_lists[sup_seq].append(Event(event_i.sid, event_j.eid))

                
                elif item_list_i.seq[-1] == item_list_j.seq[-1]:
                    parted_i = item_list_i.seq.rpartition('-')
                    parted_j = item_list_j.seq.rpartition('-')
                    # do pierwszej strzałki bierz dołącz posortuj i zwróć
                    
                    # oba weź złącz i przesortuj i ze strzalkami dodaj na koniec
                    
                    pass
        
    pass

def prune():
    pass

def enumerate_frequent_seq():
    pass

def spade_sequencing(data, min_sup):
    """
    Perform the spade sequencing algorithm on a dataset

    Args:
        data (_type_): _description_
        min_sup (_type_): _description_
    """
    print(data)
    # Find frequent 1 element 
    freq_one = count_frequent_one_seq(data, min_sup)
    print(freq_one)

    # Find frequent 2 element
    freq_two = count_frequent_two_seq(data, min_sup)
    print(freq_two)
    
    # Equivalence class
    # Dla wszystkich 2 elementowych sekwencji
    # złącz listy id
    # i to podaj do magii jako np. 'D->F': lista [sid:eid]
    # Magic
    
    return