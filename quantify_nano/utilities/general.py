"""General utilities."""
import copy
import importlib
import json
import pathlib
import warnings
from collections.abc import MutableMapping
from typing import Any, Union, Iterator, Type, TypeVar

import numpy as np
import xxhash

from qcodes.utils.helpers import NumpyJSONEncoder


def delete_keys_from_dict(dictionary: dict, keys: set) -> dict:
    """
    Delete keys from dictionary recursively.

    Parameters
    ----------
    dictionary
        to be mutated
    keys
        a set of keys to strip from the dictionary
    Returns
    -------
    :
        a new dictionary that does not included the blacklisted keys
    """
    keys_set = set(keys)  # optimization for the "if key in keys" lookup.

    modified_dict = {}
    for key, value in dictionary.items():
        if key not in keys_set:
            if isinstance(value, MutableMapping):
                modified_dict[key] = delete_keys_from_dict(value, keys_set)
            else:
                modified_dict[key] = value
    return modified_dict


def make_hash(obj: Any):
    """
    Makes a hash from a dictionary, list, tuple or set to any level, that contains
    only other hashable types (including any lists, tuples, sets, and
    dictionaries).

    From: `<https://stackoverflow.com/questions/5884066/hashing-a-dictionary>`_.
    """

    new_hash = xxhash.xxh64()
    if isinstance(obj, (set, tuple, list)):
        return tuple(make_hash(e) for e in obj)

    if isinstance(obj, np.ndarray):
        # numpy arrays behave funny for hashing
        new_hash.update(obj)
        val = new_hash.intdigest()
        new_hash.reset()
        return val

    if not isinstance(obj, dict):
        return hash(obj)

    new_o = copy.deepcopy(obj)
    for key, val in new_o.items():
        new_o[key] = make_hash(val)

    return hash(tuple(frozenset(sorted(new_o.items()))))


def save_json(directory: pathlib.Path, filename: str, data) -> None:
    """
    Utility function to save serializable data to disk.

    Parameters
    ----------
    directory
        The directory where the data needs to be written to
    filename
        The filename of the data
    data
        The serializable data which needs to be saved to disk

    """
    full_path_to_file = directory / filename
    with open(full_path_to_file, "w", encoding="utf-8") as file:
        json.dump(data, file, cls=NumpyJSONEncoder, indent=4)


def load_json(full_path: pathlib.Path) -> dict:
    """
    Utility function to load from a json file to dict.

    Parameters
    ----------
    full_path
        The full path to the json file which needs to be loaded

    """
    with open(full_path, encoding="utf-8") as file:
        return json.load(file)


def load_json_schema(relative_to: Union[str, pathlib.Path], filename: str):
    """
    Load a JSON schema from file. Expects a 'schemas' directory in the same directory
    as `relative_to`.

    .. tip::

        Typical usage of the form
        `schema = load_json_schema(__file__, 'definition.json')`

    Parameters
    ----------
    relative_to
        the file to begin searching from
    filename
        the JSON file to load
    Returns
    -------
    dict
        the schema
    """
    path = pathlib.Path(relative_to).resolve().parent.joinpath("schemas", filename)
    with path.open(mode="r", encoding="utf-8") as file:
        return json.load(file)
