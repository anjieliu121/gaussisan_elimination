import os, json
import numpy as np
from utils.get_params import *


########################################################################################################################
#                                           absolute errors = abs(true-approx)                                         #
########################################################################################################################
def save_errors(start=k_start, end=k_end):
    # create "errors.json" if it does not exist
    if not os.path.exists("simulated_data/errors.json"):
        with open("simulated_data/errors.json", "w") as f:
            json.dump({}, f)
    # store errors for each k
    for k in range(start, end+1):
        with open("simulated_data/errors.json", "r+") as f:
            data = json.load(f)
            if str(k) not in data:
                x = get_x(k).tolist()
                error = get_error(k).tolist()
                d = {"x": x, "error": error}
                data[k] = d
            # save errors for all k
            f.seek(0)
            json.dump(data, f, indent=4, separators=(',', ': '))
            f.truncate()


########################################################################################################################
#                                           errors at the middle of the beam                                           #
########################################################################################################################
def save_E():
    if not os.path.exists("simulated_data/numbers.json"):
        with open("simulated_data/numbers.json", "w") as f:
            json.dump({}, f)
    with open("simulated_data/numbers.json", "r+") as f:
        numbers = json.load(f)
        # update errors_middle
        if "errors_middle" not in numbers:
            errors_middle = []
        else:
            errors_middle = numbers["errors_middle"]
        k_last = len(errors_middle)  # last k stored in errors_middle
        for k in range(k_last+1, k_end+1):
            e = get_error_middle(k)
            errors_middle.append(e)
        # save errors_middle to a file
        numbers["errors_middle"] = errors_middle
        f.seek(0)
        json.dump(numbers, f, indent=4, separators=(',', ': '))
        f.truncate()
    return np.array(errors_middle)


########################################################################################################################
#                                           condition number of matrix A                                               #
########################################################################################################################
def save_KN():
    if not os.path.exists("simulated_data/numbers.json"):
        with open("simulated_data/numbers.json", "w") as f:
            json.dump({}, f)
    with open("simulated_data/numbers.json", "r+") as f:
        numbers = json.load(f)
        if "condition_numbers" not in numbers:
            KN = []
        else:
            KN = numbers["condition_numbers"]
        k_last = len(KN)  # last stored k in KN
        for k in range(k_start, k_end+1):
            if k > k_last:
                cond = get_condition_number(k)
                KN.append(cond)
        # save KN to a file
        numbers["condition_numbers"] = KN
        f.seek(0)
        json.dump(numbers, f, indent=4, separators=(',', ': '))
        f.truncate()
    return np.array(KN)