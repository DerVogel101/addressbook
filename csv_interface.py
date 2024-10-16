import os
import re
from dataclasses import asdict, fields
from datetime import date
from pathlib import Path

import pandas as pd
import numpy as np

from address import Address
from address_container_interface import AddressDatabaseInterface


class CsvInterface(AddressDatabaseInterface):
    """
    A class to interface with a CSV file for storing and retrieving address data.

    Attributes:
    -----------
    __path : str
        The path to the CSV file.
    __df_memory : pd.DataFrame
        The in-memory DataFrame storing the address data.

    Methods:
    --------
    __require_df_memory(func):
        A decorator to ensure the DataFrame is loaded in memory before executing the function.

    set_path(path: str) -> None:
        Sets the path to the CSV file.

    open() -> None:
        Opens the CSV file and loads its content into a DataFrame.

    save() -> None:
        Saves the current state of the DataFrame to the CSV file.

    close() -> None:
        Saves the DataFrame and clears it from memory.

    get_all() -> dict[int, Address]:
        Retrieves all addresses from the DataFrame.

    get(__id: int) -> Address | None:
        Retrieves an address by its ID.

    search(search_string: str) -> dict[int, Address]:
        Searches for addresses that match the search string.

    delete(__id: int) -> int | None:
        Deletes an address by its ID.

    update(id: int, **kwargs) -> int | None:
        Updates an address by its ID.

    add_address(address: Address) -> int:
        Adds a new address to the DataFrame.

    get_today_birthdays() -> dict[int, Address]:
        Retrieves addresses with birthdays today.

    __series_to_address(series: pd.Series) -> Address:
        Converts a Pandas Series to an Address object.

    __enter__() -> CsvInterface:
        Enters the runtime context related to this object.

    __exit__(exc_type, exc_val, exc_tb) -> None:
        Exits the runtime context related to this object.

    __iter__() -> CsvInterface:
        Returns an iterator object.

    __next__() -> Address:
        Returns the next address in the DataFrame.
    """

    def __init__(self, path):
        """
        Initializes the CsvInterface with the path to the CSV file.

        Parameters:
        -----------
        path : str
            The path to the CSV file.
        """
        self.__path = None
        self.__df_memory = None
        self.set_path(path)
        self.open()

    @staticmethod
    def __require_df_memory(func):
        """
        A decorator to ensure the DataFrame is loaded in memory before executing the function.

        Parameters:
        -----------
        func : function
            The function to be decorated.

        Returns:
        --------
        function
            The wrapped function.
        """
        def wrapper(self, *args, **kwargs):
            if self.__df_memory is None:
                match func.__name__:
                    case 'search' | 'get_all' | 'get_today_birthdays':
                        return []
                    case _:
                        return None
            return func(self, *args, **kwargs)

        return wrapper

    def set_path(self, path):
        """
        Sets the path to the CSV file.

        Parameters:
        -----------
        path : str
            The path to the CSV file.

        Raises:
        -------
        KeyError
            If the path is invalid.
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
        Opens the CSV file and loads its content into a DataFrame.

        Raises:
        -------
        IsADirectoryError
            If the path is a directory.
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
        Saves the current state of the DataFrame to the CSV file.
        """
        with open(self.__path, 'a+') as file:
            file.truncate(0)
            self.__df_memory.to_csv(file, index=True, index_label="id", header=True)
        return

    def close(self) -> None:
        """
        Saves the DataFrame and clears it from memory.
        """
        self.save()
        self.__df_memory = None
        return

    @__require_df_memory
    def get_all(self) -> dict[int, Address]:
        """
        Retrieves all addresses from the DataFrame.

        Returns:
        --------
        dict[int, Address]
            A dictionary with address IDs as keys and Address objects as values.
        """
        addresses = {}
        for row in self.__df_memory.iterrows():
            addresses[row[0]] = self.__series_to_address(row[1])
        return addresses

    @__require_df_memory
    def get(self, __id: int) -> Address | None:
        """
        Retrieves an address by its ID.

        Parameters:
        -----------
        __id : int
            The ID of the address to retrieve.

        Returns:
        --------
        Address | None
            The Address object if found, else None.
        """
        if __id not in self.__df_memory.index:
            return None
        return self.__series_to_address(self.__df_memory.iloc[__id])

    @__require_df_memory
    def search(self, search_string: str) -> dict[int, Address]:
        """
        Searches for addresses that match the search string.

        Parameters:
        -----------
        search_string : str
            The string to search for.

        Returns:
        --------
        dict[int, Address]
            A dictionary with address IDs as keys and Address objects as values.
        """
        result = self.__df_memory[
            self.__df_memory.apply(
                lambda row: row
                .astype(str)
                .str
                .contains(search_string, case=False, na=False)
                .any(),
                axis=1)]
        return [self.__series_to_address(row[1]) for row in result.iterrows()]

    @__require_df_memory
    def delete(self, __id: int) -> int | None:
        """
        Deletes an address by its ID.

        Parameters:
        -----------
        __id : int
            The ID of the address to delete.

        Returns:
        --------
        int | None
            The ID of the deleted address if it was found, else None.
        """
        try:
            self.__df_memory.drop(index=__id, inplace=True)
            return __id
        except KeyError:
            return None

    @__require_df_memory
    def update(self, id: int, **kwargs) -> int | None:
        """
        Updates an address by its ID.

        Parameters:
        -----------
        id : int
            The ID of the address to update.
        kwargs : dict
            The fields to update.

        Returns:
        --------
        int | None
            The ID of the updated address if it was found.

        Raises:
        -------
        KeyError
            If the address with the given ID does not exist.
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

    def add_address(self, address) -> int:
        """
        Adds a new address to the DataFrame.

        Parameters:
        -----------
        address : Address
            The Address object to add.

        Returns:
        --------
        int
            The ID of the added address.
        """
        serialized_address = asdict(address)
        new_index = 0
        if self.__df_memory is not None and len(self.__df_memory.index) > 0:
            new_index = -~self.__df_memory.index[-1]
            self.__df_memory = pd.concat([self.__df_memory, pd.DataFrame(data=serialized_address, index=[new_index])])
        else:
            self.__df_memory = pd.DataFrame(data=serialized_address, index=[new_index])
        return new_index

    @__require_df_memory
    def get_today_birthdays(self) -> dict[int, Address]:
        """
        Retrieves addresses with birthdays today.

        Returns:
        --------
        dict[int, Address]
            A dictionary with address IDs as keys and Address objects as values.
        """
        result = self.__df_memory[self.__df_memory.birthdate == date.today().strftime("%Y-%m-%d")]
        address_dict = {}
        for row in result.iterrows():
            address_dict[row[0]] = self.__series_to_address(row[1])
        return address_dict

    @staticmethod
    def __series_to_address(series: pd.Series) -> Address:
        """
        Converts a Pandas Series to an Address object.

        Parameters:
        -----------
        series : pd.Series
            The Pandas Series to convert.

        Returns:
        --------
        Address
            The converted Address object.
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

        Returns:
        --------
        CsvInterface
            The CsvInterface object.
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context related to this object.

        Parameters:
        -----------
        exc_type : type
            The exception type.
        exc_val : Exception
            The exception value.
        exc_tb : traceback
            The traceback object.
        """
        self.close()
        return None

    def __iter__(self):
        """
        Returns an iterator object.

        Returns:
        --------
        CsvInterface
            The CsvInterface object.
        """
        self.__index = 0
        return self

    def __next__(self):
        """
        Returns the next address in the DataFrame.

        Returns:
        --------
        Address
            The next Address object.

        Raises:
        -------
        StopIteration
            If there are no more addresses.
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


if __name__ == "__main__":
    interface = CsvInterface(r"tests/ExampleCSVTest.csv")
    interface.open()
    interface.add_address(Address(lastname='Huber', firstname='Hans', street='Obere Bahnhofstra e', number='3', zip_code=70173,
            city='Stuttgart', birthdate=date(1990, 1, 1), phone='+49 711 1234 5678',
            email='hans.huber@exaample.de'))

    interface.add_address(Address(lastname='Schmidt', firstname='J rgen', street='K nigstra e', number='1', zip_code=70173,
               city='Stuttgart', birthdate=date(1980, 2, 2), phone='+49 711 5678 9012',
               email='juergen.schmidt@example.de'))

    interface.add_address(Address(lastname='Fischer', firstname='Monika', street='Marienplatz', number='2', zip_code=70173,
               city='Stuttgart', birthdate=date(1970, 3, 3), phone='+49 711 1234 5679',
               email='monika.fischer@example.com'))
    interface.save()
    interface.close()
