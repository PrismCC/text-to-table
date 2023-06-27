import table_visualization_utils as tutils

def get_constructed_data(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            res.append(tutils.Table(line))
    return res