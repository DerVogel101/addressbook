from datetime import date
from typing import Optional
from no_touchy.muple import Muple
from pydantic import field_validator, PositiveInt
from pydantic.dataclasses import dataclass
import sqlite3
import pandas as pd
from contextlib import closing
import re
import phonenumbers


# @dataclass(order=True)
# class AddressVanilla:
#     lastname: str
#     firstname: str
#     street: Optional[str] = None
#     number: Optional[str] = None
#     zip_code: Optional[int] = None
#     city: Optional[str] = None
#     birthdate: Optional[str] = None
#     phone: Optional[str] = None
#     email: Optional[str] = None
#
#     def __post_init__(self):
#         if self.birthdate:
#             self.birthdate = date.fromisoformat(self.birthdate)
#
#     def __str__(self):
#         return (f"{self.lastname} {self.firstname}\n{self.street} {self.number} \n{self.zip_code} {self.city}\n"
#                 f"{self.birthdate}\n{self.phone}\n{self.email}")


@dataclass(order=True)
class Address:
    """
    The Zip code are positive integers, because countries with other formats just aren't real.
    """
    lastname: str
    firstname: str
    street: Optional[str] = None
    number: Optional[str] = None
    zip_code: Optional[PositiveInt] = None
    city: Optional[str] = None
    birthdate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    @field_validator("birthdate")
    def parse_birthdate(cls, v) -> date:
        return date.fromisoformat(v)

    @field_validator("email")
    def validate_email(cls, v) -> str:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  # stackoverflow is love
        if re.match(pattern, v):
            return v
        else:
            raise ValueError("Invalid email address")

    @field_validator("phone")
    def validate_phone(cls, v) -> str:
        try:
            parsed_number = phonenumbers.parse(v, None)
            if phonenumbers.is_valid_number(parsed_number):
                return v
            else:
                raise ValueError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("Invalid phone number")

    def __str__(self):
        return (f"{self.lastname} {self.firstname}\n{self.street} {self.number} \n{self.zip_code} {self.city}\n"
                f"{self.birthdate}\n{self.phone}\n{self.email}")


def save_to_sqlite(addresses: list[dataclass]):
    with closing(sqlite3.connect('addresses.sqlite3')) as conn:
        addresses_df = pd.DataFrame([address_i.__dict__ for address_i in addresses])
        addresses_df.to_sql('addresses', conn, if_exists='append', index=False)


if __name__ == "__main__":
    address = Address(lastname="ADoe", firstname="John", street="Main Street", number="123", zip_code=12345,
                      city="Springfield", birthdate="2000-01-01", phone="+49 176 1234 5678", email="john.doe@doe-mail.io")

    adress3 = Address(lastname="Abc", firstname="a")
    adress4 = Address(lastname="Abc", firstname="b")
    adress5 = Address(lastname="bbc", firstname="a")
    adress6 = Address(lastname="bbc", firstname="b")

    address7 = Address(lastname="bbc", firstname="b", street="Main Street", number="123", zip_code=12345)
    print(repr(address))

    sort_list = [adress4, adress6, adress3, adress5]
    save_to_sqlite([address, adress3, adress4, adress5, adress6])
    save_to_sqlite([address7])
    sort_list.sort()
    print(sort_list)
    print(address.__dict__)
