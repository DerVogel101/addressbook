from address_container_interface import AddressDatabaseInterface
from address import Address
import os, re
from pathlib import Path
from datetime import date
import pandas as pd
from dataclasses import dataclass, asdict

class CsvInterface(AddressDatabaseInterface):
    def __init__(self, path):
        self.__path = None
        self.set_path(path)
        self.df_memory = None

    @staticmethod  # TODO: check if this works: This *should* work
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
        if Path(self.__path).is_file():
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
        result = self.df_memory[\
            self.df_memory.apply(\
                    lambda row: row
                                .astype(str)
                                .str
                                .contains(search_string, case=False, na=False)
                                .any(),\
                axis=1)]
        return [Address(**row[1].to_dict()) for row in result.iterrows()]


    @__require_df_memory
    def delete(self, __id: int):
        try:
            self.df_memory.drop(index=__id, inplace=True)
            return __id
        except KeyError:
            return None

    def update(self, __id: int, **kwargs):
        row = None
        try:
            row =  self.df_memory.iloc[__id]
        except KeyError:
            return None
        for key, value in kwargs.items():
            if key not in row.keys():
                print("Skipping key, not supported")
                continue
            row[key] = value
        return __id
         

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
        # return [Address(**row[1].to_dict()) for row in self.df_memory.iterrows() if row[1].birthdate == date.today().strftime("%Y-%m-%d")]

        result = self.df_memory[self.df_memory.birthdate == date.today().strftime("%Y-%m-%d")]
        return [Address(**row[1].to_dict()) for row in result.iterrows()]

    

# a = CsvInterface("/home/someone/Code/geb_db/test.csv")
a = CsvInterface(r"./test.csv")
a.open()
#a.add_address(Address(lastname="a", firstname="a", street="a", number="a", zip_code=12345, city="a", birthdate="2000-01-01", phone="+49 176 1234 5678", email="a@a.de"))
#a.add_address(Address(lastname="Huber", firstname="Hans", street="Obere Bahnhofstra e", number="3", zip_code=70173, city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678", email="hans.huber@exaample.de"))
#a.add_address(Address(lastname="Schmidt", firstname="J rgen", street="K nigstra e", number="1", zip_code=70173, city="Stuttgart", birthdate="1980-02-02", phone="+49 711 5678 9012", email="juergen.schmidt@example.de"))
#a.add_address(Address(lastname="Fischer", firstname="Monika", street="Marienplatz", number="2", zip_code=70173, city="Stuttgart", birthdate="1970-03-03", phone="+49 711 1234 5679", email="monika.fischer@example.com"))
#a.add_address(Address(lastname="TodaysBirthday", firstname="John", street="Today Street", number="1", zip_code=12345, city="Today City", birthdate=date.today(), phone="+49 176 1234 5678", email="john.doe@example.com"))
#print(a.search("Stuttgart"))
print(a.get_today_birthdays())
#a.delete(0)
a.save()
