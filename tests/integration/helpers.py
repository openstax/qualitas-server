"""helpers for integration tests."""

import json
import os


def data_loader(filename):
    directory = os.path.dirname(__file__)
    directory = os.path.join(directory, "data")
    data_file = os.path.join(directory, filename)

    def data_helper():
        with open(data_file) as infile:
            data = json.load(infile)
        return data

    return data_helper()
