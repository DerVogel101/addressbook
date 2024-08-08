from abc import ABC, abstractmethod
from pydantic.dataclasses import dataclass
from address import Address


class AddressContainerInterface(ABC):
    @abstractmethod
    def set_path(self, path) -> None:
        pass

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def get_all(self) -> dict[str: Address]:
        pass

    @abstractmethod
    def get(self, __id: int) -> Address:
        pass

    @abstractmethod
    def search(self, search_string: str) -> dict[str: Address]:
        pass

    @abstractmethod
    def delete(self, __id: int) -> int:
        """:return: the id of the deleted address if it was found, else -1"""
        pass

    @abstractmethod
    def update(self, __id: int, **kwargs) -> int:
        """:return: the id of the updated address if it was found, else -1"""
        pass

    @abstractmethod
    def add_address(self, address) -> int:
        """:return: the id of the added address"""
        pass

    @abstractmethod
    def get_today_birthdays(self) -> dict[str: Address]:
        pass