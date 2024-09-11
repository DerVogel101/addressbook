from dataclasses import field
from datetime import date
from typing import Optional
from no_touchy.muple import Muple
from pydantic import field_validator, PositiveInt
from pydantic.dataclasses import dataclass
import re
import phonenumbers


@dataclass(order=True)
class Address:
    """
    The Zip codes are positive integers, because countries with other formats just aren't real.
    """
    lastname: str
    firstname: str
    street: Optional[str] = field(default=None)
    number: Optional[str] = field(default=None)
    zip_code: Optional[PositiveInt] = field(default=None)
    city: Optional[str] = field(default=None)
    birthdate: Optional[date] = field(default=None)
    phone: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)

    @field_validator("email")
    def validate_email(cls, v) -> str | None:
        if v is None:
            return v
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  # stackoverflow is love
        if re.match(pattern, v):
            return v
        else:
            raise ValueError("Invalid email address")

    @field_validator("phone")
    def validate_phone(cls, v) -> str | None:
        if v is None:
            return v
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
    example = Address(lastname="Doe", firstname="John", street="Main Street", number="1", zip_code=12345, city="Springfield", birthdate="2000-01-01", phone="+49 176 1234 5678", email="john.doe@example.com")
    print(example)
