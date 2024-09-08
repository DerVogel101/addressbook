from abc import ABC, abstractmethod
from address import Address


class AddressDatabaseInterface(ABC):
    @abstractmethod
    def set_path(self, path: str) -> None:  # FIXME: should be in open
        """
        :raises TypeError: if the path is invalid
        """
        pass

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def get_all(self) -> dict[int: Address]:
        pass

    @abstractmethod
    def get(self, __id: int) -> Address | None:
        pass

    @abstractmethod
    def search(self, search_string: str) -> dict[int: Address]:
        pass

    @abstractmethod
    def delete(self, __id: int) -> int | None:
        """:return: the id of the deleted address if it was found, else None"""
        pass

    @abstractmethod
    def update(self, __id: int, **kwargs) -> int | None:
        """
        :return: the id of the updated address if it was found, else None
        :raises KeyError: if the address with the given id does not exist
        """
        pass

    @abstractmethod
    def add_address(self, address) -> int:
        """:return: the id of the added address"""
        pass

    @abstractmethod
    def get_today_birthdays(self) -> dict[int: Address]:
        pass
