import os
import re
from dataclasses import asdict, fields
from datetime import date
from pathlib import Path

import pandas as pd
import numpy as np
from typing import Callable

from address import Address
from address_container_interface import AddressDatabaseInterface


class CsvInterface(AddressDatabaseInterface):
    """
    A class to interface with a CSV file for storing and retrieving address data.
    Handles reads, writes, and queries from/to a CSV file.
    
    :param path: The path to the CSV file.
    :type path: str | None
    
    Methods:
    ########
    """

    def __init__(self, path: str | None):
        """
        Initializes the CsvInterface. 
        If a path is given, it is set and the file at the path gets opend.

        :param path: the path to the CSV file
        :type path: str, optional
        :rtype: CsvInterface
        """
        self.__path = None
        self.__df_memory = None
        if path is not None:
            self.set_path(path)
            self.open()
        #return self

    @staticmethod
    def __require_df_memory(func: Callable) -> Callable:
        """
        Class-specific decorator.
        Ensures that the object :attr:`__df_memory` is not None
        before calling the decorated function.
        If it is, a default value based on the function name is returne by the wrapper.
        Instead of calling the function.

        :param func: the function to be decorated
        :type func: function
        :return: The :func:`wapper` which can return any
        :rtype: function
        """
        def wrapper(self, *args, **kwargs) -> any:
            """
            :param args: Args passed to the function
            :param kwargs: Kwargs passed to the function
            :return: None, an empty list, or the result of the function
            """
            if self.__df_memory is None:
                match func.__name__:
                    case 'search' | 'get_all' | 'get_today_birthdays':
                        return {}
                    case _:
                        return None
            return func(self, *args, **kwargs)

        return wrapper

    def set_path(self, path: str) -> None:
        """
        Sets the path to the CSV file, checking if the path is valid.
        Changing the path to another file after reading from one is supported.

        :param path: the path to the CSV file
        :type path: str
        :raises KeyError: if the path is invalid
        :return: None, if successful
        :rtype: None
        """
        if os.path.isabs(path):
            match os.name:
                case 'nt':
                    pattern = r"[a-zA-Z]:\\(?:[a-zA-Z0-9]+\\)*[a-zA-Z0-9]+\.csv$"
                case _:
                    pattern = r"^(?:/[^/ ]*)*/?.csv$"
            if re.search(pattern, path):
                self.__path = path
                return None
        else:
            self.__path = os.path.abspath(path)
            return None
        raise KeyError("Invalid path")

    def open(self) -> None:
        """
        Reads the CSV file at the path set in :func:`set_path` 
        or during construction into object memory (:attr:`__df_memory`).
        While reading, the types of some collums in the csv fiele get manualy converted,
        ensureing the correct type will be used.
        After reading, the functuion closes the file. 

        :raises IsADirectoryError: if the path is a directory
        
        :return: None, if secsessfull. Content of the file was loaded as class:`pd.dataframes` in object memory. 
        :rtype: None
        """
        if Path(self.__path).is_file():
            with open(self.__path, 'r') as file:
                try:
                    self.__df_memory = pd.read_csv(file, index_col=["id"])
                    if "number" in self.__df_memory.columns:
                        self.__df_memory["number"] = self.__df_memory["number"].apply(lambda x: str(int(x)) if pd.notnull(x) else None)
                    if "zip_code" in self.__df_memory.columns:
                        self.__df_memory["zip_code"] = self.__df_memory["zip_code"].apply(lambda x: int(x) if pd.notnull(x) else None)
                except pd.errors.EmptyDataError:
                    print("Note: Empty File")
        elif Path(self.__path).is_dir():
            raise IsADirectoryError("Path is a directory")
        return None

    @__require_df_memory
    def save(self) -> None:
        """
        Saves the object memory into the CSV file at the path set in :func:`set_path`.
        The file is opened in 'a+' mode. 

        See :func:`open` for possible Errors.

        :return: None, if save successful
        :rtype: None
        """
        with open(self.__path, 'a+') as file:
            file.truncate(0)
            self.__df_memory.to_csv(file, index=True, index_label="id", header=True)
        return

    def close(self) -> None:
        """
        Saves the current data to the file and then closes the CSV file.
        After this call, the object is in an empty state with only the path set.
        A new path may be set or the file may be re-opened.

        See :func:`save` for possible Errors.

        :rtype: None
        """
        self.save()
        self.__df_memory = None
        return

    @__require_df_memory
    def get_all(self) -> dict[int, Address]:
        """
        Decorated by :func:`__require_df_memory`.
        Fetches all addresses from object memory (the csv file, if one was opened).

        :return: A dictonary with the key beeing the ID of the Address in the CSV file
        :rtype: dict[int, Address]
        """
        addresses = {}
        for row in self.__df_memory.iterrows():
            addresses[row[0]] = self.__series_to_address(row[1])
        return addresses

    @__require_df_memory
    def get(self, id: int) -> Address | None:
        """
        Decorated by :func:`__require_df_memory`
        Retrieves an address by its ID.

        :param id: ID of the Address to return
        :type id: int

        :return: :class:`Address` if an Address with the given id exists
        :rtype: Address | None
        """
        if id not in self.__df_memory.index:
            return None
        return self.__series_to_address(self.__df_memory.iloc[id])

    @__require_df_memory
    def search(self, search_string: str) -> dict[int, Address]:
        """       
        Decorated by :func:`__require_df_memory`.
        Searches for addresses that match the search string.
        The query can inclued any field of Address but should only include one.
        See `detailed_csv_search <detailed_csv_search.rst>`_ for more information.

        :param search_string: The search term to look for
        :type search_string: str
        :return: a dictionary of {ID: :class:`Address`} with all Addresses matchin the query. 
                Empty if no matches where found.
        :rtype: dict[int, Address]
        """
        result = self.__df_memory[
            self.__df_memory.apply(
                lambda row: row
                .astype(str)
                .str
                .contains(search_string, case=False, na=False)
                .any(),
                axis=1)]
        address_dict = {}
        for row in result.iterrows():
            address_dict[row[0]] = self.__series_to_address(row[1])
        return address_dict

    @__require_df_memory
    def delete(self, id: int) -> int | None:
        """
        Decorated by :func:`__require_df_memory`.
        Deletes the address with the given ID from objects memory.

        :param id: ID of the Address to delete.
        :type id: int
        :return: The deleted ID of the deleted address, or None if not found.
        :rtype: int or None
        """
        try:
            self.__df_memory.drop(index=id, inplace=True)
            return id
        except KeyError:
            return None

    @__require_df_memory
    def update(self, id: int, **kwargs) -> int:
        """
        Decorated by :func:`__require_df_memory`
        Updates an address by its ID using the provided kwargs.
        Known keys are all fields in :class:`Address`. All unknown keys will be ignored.

        :param id: the ID of the address to update
        :type id: int
        :param kwargs: key-value pairs of address fileds and its new value
        :type kwargs: any
        :raises KeyError: if the given ID in not associated with any address
        :return: the ID of the updated address
        :rtype: int
        """
        try:
            row = self.__df_memory.loc[id]
        except IndexError:
            raise KeyError(f"Address with id {id} does not exist")

        for key, value in kwargs.items():
            if key not in row.keys():
                print("Skipping key, not supported")
                continue
            self.__df_memory.at[id, key] = value
        return id

    def add_address(self, address: Address) -> int:
        """
        Adds a new address to the objects memory.

        :param address: the :class:`Address` to add
        :type address: Address
        :return: the ID that was assigned to the newly added address
        :rtype: int
        """
        serialized_address = asdict(address)
        new_index = 0
        if self.__df_memory is not None and len(self.__df_memory.index) > 0:
            new_index = -~self.__df_memory.index[-1] # -~ is bitwise not negated, therefore +1 :D
            self.__df_memory = pd.concat([self.__df_memory, pd.DataFrame(data=serialized_address, index=[new_index])])
        else:
            self.__df_memory = pd.DataFrame(data=serialized_address, index=[new_index])
        return new_index

    @__require_df_memory
    def get_today_birthdays(self) -> dict[int, Address]:
        """
        Decorated by :func:`__require_df_memory`.
        Fetches all addresses with today's date as their birthday.

        :return: A dictionary with the id and values of all address that have today set as their birthday
        :rtype: dict[int, Address]
        """
        result = self.__df_memory[self.__df_memory.birthdate == date.today().strftime("%Y-%m-%d")]
        address_dict = {}
        for row in result.iterrows():
            address_dict[row[0]] = self.__series_to_address(row[1])
        return address_dict

    @staticmethod
    def __series_to_address(series: pd.Series) -> Address:
        """
        Converts a :class:`pandas.Series` to an :class:`Address`, ensuring all types are correct.
        Fails of the data series has an unexpected structure.

        :param series: the data series to convert
        :type series: pd.Series
        :return: the converted series as :class:`Address`
        :rtype: Address
        """
        row_dict = series.to_dict()
        for key, value in row_dict.items():
            if value == value and value is not None:
                if key == 'birthdate':
                    row_dict[key] = date.fromisoformat(str(value))
                elif key in ('phone', 'email', 'street', 'number', 'city'):
                    row_dict[key] = str(value)
                elif key == 'zip_code':
                    row_dict[key] = int(value)
            else:
                row_dict[key] = None

        return Address(**row_dict)

    def __enter__(self):
        """
        Enters the runtime context related to this object.
        This function is a warper for :func:`open` and not technically needed,
        for all files get cloed imideatly after a read/write. It just enables the use
        of :code:`with CsvInterface ...`.

        :return: The instance itself.
        :rtype: CsvInterface
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        See :func:`__enter__`. Calls close, their for
        saving the current object to the file and resetting it.

        Gets the for contect manager required parameters
        :param exc_type:
        :param exc_val:
        :param exc_tb:

        :rtype: None
        """
        self.close()
        return None

    def __iter__(self):
        """
        Turns the object istself int an iteratable.

        :return: The object itself, with an index set to 0
        :rtype: CsvInterface
        """
        self.__index = 0
        return self

    def __next__(self) -> Address:
        """
        Return the next address in object memory.
        It keeps track of the position using an index variable.

        :raise StopIteration: If object memory is empty 
            or it was iterated through all elements
        :return: The next address in object memory
        :rtype: Address
        """
        if self.__df_memory is None:
            raise StopIteration
        df_indexes = self.__df_memory.index
        if self.__index < len(df_indexes):
            result = self.get(df_indexes[self.__index])
            self.__index += 1
            return result
        else:
            raise StopIteration