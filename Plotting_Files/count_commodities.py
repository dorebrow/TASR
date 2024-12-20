#File: count_commodities
#Purpose: Gives the count of the number of commodities in a processed network .json file.

import json

def count_non_empty_lists(filename):
    """
    Count the number of non-empty lists in the dictionary stored in the file.

    :param filename: Name of the file containing the JSON data.
    :return: Count of non-empty lists.
    """
    with open(filename, 'r') as file:
        data = json.load(file)

    non_empty_count = 0

    for key, value in data.items():
        if isinstance(value, list):
            non_empty_count += sum(1 for sublist in value if sublist) 

    return non_empty_count

filename = 'Processed_Networks/AustinPaths.json'
result = count_non_empty_lists(filename)
print(f"Number of non-empty lists: {result}")
