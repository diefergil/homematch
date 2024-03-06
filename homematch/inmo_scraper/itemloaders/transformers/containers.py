from typing import Dict, List


import numpy as np


def convert_container_to_dict(container_items: List[str]) -> Dict[str, str]:
    container_items = np.array(container_items)
    list_of_dict_values = np.array([":" in x for x in container_items])

    values_index = np.argwhere(list_of_dict_values == True).flatten()
    keys_index = values_index - 1
    clean_values = list(
        map(lambda x: x.replace(": ", ""), container_items[values_index])
    )

    tags = dict(zip(container_items[keys_index], clean_values))
    tags["others"] = list(
        np.delete(container_items, np.concatenate([keys_index, values_index]))
    )

    return tags
