"""

This module defines the `Address` dataclass, which represents an address with various fields such as lastname, firstname, street, number, zip code, city, birthdate, phone, and email. It includes validation for email, phone, and house number fields.

Usage Example:
--------------
    .. code-block:: python

        example = Address(
            lastname="Doe",
            firstname="John",
            street="Main Street",
            number="1",
            zip_code=12345,
            city="Springfield",
            birthdate="2000-01-01",
            phone="+49 176 1234 5678",
            email="john.doe@example.com"
        )
        print(example)
"""

from dataclasses import field
from datetime import date
from typing import Optional
from pydantic import field_validator, PositiveInt
from pydantic.dataclasses import dataclass
import re
import phonenumbers

@dataclass(order=True)
class Address:
    """
    A dataclass representing an address.

    Attributes:
    -----------
    lastname : str
        The last name of the person.
    firstname : str
        The first name of the person.
    street : Optional[str]
        The street name of the address.
    number : Optional[str]
        The house number of the address.
    zip_code : Optional[PositiveInt]
        The zip code of the address.
    city : Optional[str]
        The city of the address.
    birthdate : Optional[date]
        The birthdate of the person.
    phone : Optional[str]
        The phone number of the person.
    email : Optional[str]
        The email address of the person.

    Methods:
    --------
    validate_email(cls, v) -> str | None:
        Validates the email address format.
    validate_phone(cls, v) -> str | None:
        Validates the phone number format.
    validate_number(cls, v) -> str | None:
        Validates the house number format.
    __str__() -> str:
        Returns a string representation of the address.
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
        """
        Validates the email address format.

        Parameters:
        -----------
        v : str
            The email address to validate.

        Returns:
        --------
        str | None
            The validated email address or None if not provided.

        Raises:
        -------
        ValueError
            If the email address is invalid.
        """
        if v is None:
            return v
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, v):
            return v
        else:
            raise ValueError("Invalid email address")

    @field_validator("phone")
    def validate_phone(cls, v) -> str | None:
        """
        Validates the phone number format.

        Parameters:
        -----------
        v : str
            The phone number to validate.

        Returns:
        --------
        str | None
            The validated phone number or None if not provided.

        Raises:
        -------
        ValueError
            If the phone number is invalid.
        """
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

    @field_validator("number")
    def validate_number(cls, v) -> str | None:
        """
        Validates the house number format.

        Parameters:
        -----------
        v : str
            The house number to validate.

        Returns:
        --------
        str | None
            The validated house number or None if not provided.

        Raises:
        -------
        ValueError
            If the house number is invalid.
        """
        if v is None:
            return v
        pattern = r"^\d+[a-zA-Z]?$"
        if re.match(pattern, v):
            return v
        else:
            raise ValueError("Invalid house number")

    def __str__(self):
        """
        Returns a string representation of the address.

        Returns:
        --------
        str
            A string representation of the address.
        """
        return (f"{self.lastname} {self.firstname}\n{self.street} {self.number} \n{self.zip_code} {self.city}\n"
                f"{self.birthdate}\n{self.phone}\n{self.email}")

if __name__ == "__main__":
    example = Address(
        lastname="Doe",
        firstname="John",
        street="Main Street",
        number="1",
        zip_code=12345,
        city="Springfield",
        birthdate="2000-01-01",
        phone="+49 176 1234 5678",
        email="john.doe@example.com"
    )
    print(example)
