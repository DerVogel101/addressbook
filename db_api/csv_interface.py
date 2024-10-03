import os
import re
from dataclasses import asdict, fields
from datetime import date
from pathlib import Path

import pandas as pd

from address import Address
from address_container_interface import AddressDatabaseInterface


class CsvInterface(AddressDatabaseInterface):
    def __init__(self, path):
        self.__path = None
        self.__df_memory = None
        self.set_path(path)
        self.open()

    @staticmethod  # TODO: check if this works: This *should* work, i do hope it does
    def __require_df_memory(func):
        def wrapper(self, *args, **kwargs):
            if self.__df_memory is None:
                # find default return value
                match func.__name__:
                    case 'search' | 'get_all' | 'get_today_birthdays':
                        return []
                    case _:
                        return None
            return func(self, *args, **kwargs)

        return wrapper

    def set_path(self, path):
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
        if Path(self.__path).is_file():
            with open(self.__path, 'r') as file:
                try:
                    self.__df_memory = pd.read_csv(file, index_col=["id"])
                    # ToDo Check with fileds(Address) and sets if expected structure exists 
                    
                    # Overwrite autogenerated column types
                    if 'number' in self.__df_memory.columns:
                        self.__df_memory['number'] = self.__df_memory['number'].apply(lambda x: str(x))
                except pd.errors.EmptyDataError:
                    print("Note: Empty File")
        elif Path(self.__path).is_dir():
            raise IsADirectoryError("Path is a directory")
        return None

    @__require_df_memory
    def save(self) -> None:
        with open(self.__path, 'a+') as file:
            file.truncate(0)
            self.__df_memory.to_csv(file, index=True, index_label="id", header=True)
        return
    
    def close(self) -> None:
        self.save()
        self.__df_memory = None
        return

    @__require_df_memory
    def get_all(self) -> dict[int: Address]:
        addresses = {}
        for row in self.__df_memory.iterrows():
            # row[0] is the index
            addresses[row[0]] = self.__series_to_address(row[1])
        return addresses

    @__require_df_memory
    def get(self, __id: int) -> Address | None:
        if __id not in self.__df_memory.index:
            return None
        return self.__series_to_address(self.__df_memory.iloc[__id])

    @__require_df_memory
    def search(self, search_string: str) -> dict[int: Address]:
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
        try:
            self.__df_memory.drop(index=__id, inplace=True)
            return __id
        except KeyError:
            return None

    @__require_df_memory
    def update(self, __id: int, **kwargs) -> int | None:
        """
        :raise KeyError: if the address with the given id does not exist
        """
        # pd.options.mode.copy_on_write = False
        try:
            row = self.__df_memory.iloc[__id]
        except IndexError:
            raise KeyError(f"Address with id {__id} does not exist")

        for key, value in kwargs.items():
            if key not in row.keys():
                print("Skipping key, not supported")
                continue
            self.__df_memory.at[__id, key] = value
        return __id

    def add_address(self, address) -> int:
        serialized_address = asdict(address)
        new_index = 0
        if self.__df_memory is not None and len(self.__df_memory.index) > 0:
            new_index = self.__df_memory.index[-1] + 1
            self.__df_memory = pd.concat([self.__df_memory, pd.DataFrame(data=serialized_address, index=[new_index])])
        else:
            # conacat with None is deprecated thus:
            self.__df_memory = pd.DataFrame(data=serialized_address, index=[new_index])
        return new_index

    @__require_df_memory
    def get_today_birthdays(self) -> dict[int: Address]:

        result = self.__df_memory[self.__df_memory.birthdate == date.today().strftime("%Y-%m-%d")]
        address_dict = {}
        for row in result.iterrows():
            address_dict[row[0]] = self.__series_to_address(row[1])
        return address_dict    
    @staticmethod
    def __series_to_address(series: pd.Series) -> Address:
        row_dict = series.to_dict()
        # Manual type conversions
        row_dict['number'] = str(row_dict['number'])

        return Address(**row_dict)

    def __open__(self):
        self.open()
        return self

    def __close__(self):
        self.close()
        return None

    def __iter__(self):
        self.__index = 0
        return self
    
    def __next__(self):
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

    # import unittest
    # import random
    # class TestCsvInterface(unittest.TestCase):
    #
    #     def setUp(self) -> None:
    #         self.seed = random.randint(0, 1000)
    #         self.interface = CsvInterface(rf"./csvTest{self.seed}.csv")
    #
    #     def shutDown(self) -> None:
    #         self.interface = None
    #         os.remove(f"./csvTest{self.seed}.csv")
    #
    #     def test_add_address(self):
    #
    #         a = self.interface.add_address(Address(lastname="Huber", firstname="Hans", street="Obere Bahnhofstra e", number="3", zip_code=70173, city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678", email="hans.huber@exaample.de"))
    #         b = self.interface.add_address(Address(lastname="Schmidt", firstname="J rgen", street="K nigstra e", number="1", zip_code=70173, city="Stuttgart", birthdate="1980-02-02", phone="+49 711 5678 9012", email="juergen.schmidt@example.de"))
    #         c = self.interface.add_address(Address(lastname="Fischer", firstname="Monika", street="Marienplatz", number="2", zip_code=70173, city="Stuttgart", birthdate="1970-03-03", phone="+49 711 1234 5679", email="monika.fischer@example.com"))
    #         d = self.interface.add_address(Address(lastname="TodaysBirthday", firstname="John", street="Today Street", number="1", zip_code=12345, city="Today City", birthdate=date.today(), phone="+49 176 1234 5678", email="john.doe@example.com"))
    #
    #         assert a == 0
    #         assert b == 1
    #         assert c == 2
    #         assert d == 3
    #
    #     def test_expect_all(self):
    #         result = self.interface.get_all()
    #         assert result == [
    #             Address(lastname="Huber", firstname="Hans", street="Obere Bahnhofstra e", number="3", zip_code=70173, city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678", email="hans.huber@exaample.de"),
    #             Address(lastname="Schmidt", firstname="J rgen", street="K nigstra e", number="1", zip_code=70173, city="Stuttgart", birthdate="1980-02-02", phone="+49 711 5678 9012", email="juergen.schmidt@example.de"),
    #             Address(lastname="Fischer", firstname="Monika", street="Marienplatz", number="2", zip_code=70173, city="Stuttgart", birthdate="1970-03-03", phone="+49 711 1234 5679", email="monika.fischer@example.com"),
    #             Address(lastname="TodaysBirthday", firstname="John", street="Today Street", number="1", zip_code=12345, city="Today City", birthdate=date.today(), phone="+49 176 1234 5678", email="john.doe@example.com")
    #         ]
    #
    #
    #     def test_get(self):
    #         self.interface.get(0)
    #         assert self.interface.get(0) == Address(lastname="Huber", firstname="Hans", street="Obere Bahnhofstra e", number="3", zip_code=70173, city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678", email="hans.huber@exaample.de")
    #
    #     def test_reopen(self):
    #         self.interface.close()
    #         self.interface.open()
    #         self.test_expect_all()
    #
    #     def test_update(self):
    #         assert 0 == self.interface.update(
    #             0,
    #             lastname="Schmidt",
    #             firstname="J rgen",
    #             street="K nigstra e",
    #             number="1",
    #             zip_code=234643,
    #             city="Belin",
    #             birthdate="1980-02-10",
    #             phone="+49 711 5678 9012",
    #             email="juergen.schmidt@example.de"
    #         )
    #         new_address = self.interface.get(0)
    #         assert new_address == Address(
    #             lastname="Schmidt",
    #             firstname="J rgen",
    #             street="K nigstra e",
    #             number="1",
    #             zip_code=234643,
    #             city="Belin",
    #             birthdate="1980-02-10",
    #             phone="+49 711 5678 9012",
    #             email="juergen.schmidt@example.de")
    #
    #
    #
    # unittest.main()