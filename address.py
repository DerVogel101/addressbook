from datetime import date
from typing import Optional
from no_touchy.muple import Muple
from pydantic import field_validator, PositiveInt
from pydantic.dataclasses import dataclass
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
    The Zip codes are positive integers, because countries with other formats just aren't real.
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


if __name__ == "__main__":
    pass
