import AddressDatabaseInterface from address_container_interface

class CsvInterface(AddressDatabaseInterface):
    def __init__(self, path):
        self.__path = path

    def set_path(self, path):
        self.__path = path

    def open(self):
        pass

    def save(self):
        pass

    def get_all(self):
        pass

    def get(self, __id: int):
        pass

    def search(self, search_string: str):
        pass

    def delete(self, __id: int):
        pass

    def update(self, __id: int, **kwargs):
        pass

    def add_address(self, address):
        pass

    def get_today_birthdays(self):
        pass
    
