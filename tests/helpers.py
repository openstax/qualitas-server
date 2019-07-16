"""helpers for tests."""

import json
import os


def data_loader(filename):
    directory = os.path.dirname(__file__)
    directory = os.path.join(directory, "data")
    data_file = os.path.join(directory, filename)

    def data_helper():
        with open(data_file) as infile:
            if data_file.endswith('.json'):
                data = json.load(infile)
            else:
                data = infile.read()
        return data

    return data_helper()
