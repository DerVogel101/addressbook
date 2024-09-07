from address_container_interface import AddressDatabaseInterface
from address import Address
import os, re
import pandas as pd
from dataclasses import dataclass, asdict

class CsvInterface(AddressDatabaseInterface):
    def __init__(self, path):
        self.__path = None
        self.__file = None
        self.set_path(path)
        self.df_memory = None

    @staticmethod  # TODO: check if this works
    def __require_df_memory(func):
        def wrapper(self, *args, **kwargs):
            if self.df_memory is None:
                raise RuntimeError("df_memory is None")
            return func(self, *args, **kwargs)
        return wrapper

    def set_path(self, path):
        if os.path.isabs(path):
            pattern = ""
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

    def open(self):
        self.__file = open(self.__path, 'r')
        with open(self.__path, 'r') as file:
            try:
                self.df_memory = pd.read_csv(file, index_col=["id"])
            except pd.errors.EmptyDataError:
                #self.df_memory = pd.DataFrame(columns=['lastname', 'firstname', 'street', 'number', 'zip_code', 'city', 'birthdate', 'phone', 'email'])
                print("Note: Empty File")
        return None

    @__require_df_memory
    def save(self):
        with open(self.__path, 'a+') as file:
            file.truncate(0)
            self.df_memory.to_csv(file, index=True, index_label="id", header=True)
        return

    @__require_df_memory
    def get_all(self):
        addresses = []
        for row in self.df_memory.iterrows():
            # row[0] is the index
            addresses.append(Address(**row[1].to_dict()))
        return addresses

    @__require_df_memory
    def get(self, __id: int):
        if __id not in self.df_memory.index:
            return None
        row =  self.df_memory.iloc[__id]
        return(Address(**row.to_dict()))
    

    def search(self, search_string: str):
        pass

    @__require_df_memory
    def delete(self, __id: int):
        try:
            self.df_memory.drop(index=__id, inplace=True)
            return __id
        except KeyError:
            return None

    def update(self, __id: int, **kwargs):
        pass

    def add_address(self, address):
        serialized_address = asdict(address)
        new_index = 0
        if self.df_memory is not None and len(self.df_memory.index) > 0:
            new_index = self.df_memory.index[-1] + 1
            self.df_memory = pd.concat([self.df_memory, pd.DataFrame(data=serialized_address, index=[new_index])])
        else: 
            # conacat with None is deprecated thus:
            self.df_memory = pd.DataFrame(data=serialized_address, index=[new_index])
        return None
        

    def get_today_birthdays(self):
        pass
    

# a = CsvInterface("/home/someone/Code/geb_db/test.csv")
a = CsvInterface(r"./test.csv")
a.open()
a.add_address(Address(lastname="a", firstname="a", street="a", number="a", zip_code=12345, city="a", birthdate="2000-01-01", phone="+49 176 1234 5678", email="a@a.de"))
#print(a.get(0))
#a.delete(0)
a.save()
