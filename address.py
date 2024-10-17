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

    :param lastname: The last name of the person.
    :type lastname: str
    :param firstname: The first name of the person.
    :type firstname: str
    :param street: The street name of the address.
    :type street: str, optional
    :param number: The house number of the address.
    :type number: str, optional
    :param zip_code: The zip code of the address.
    :type zip_code: PositiveInt, optional
    :param city: The city of the address.
    :type city: str, optional
    :param birthdate: The birthdate of the person.
    :type birthdate: date, optional
    :param phone: The phone number of the person.
    :type phone: str, optional
    :param email: The email address of the person.
    :type email: str, optional

     Methods:
    :func:`validate_email` Validates the email address format.

    :func:`validate_phone` Validates the phone number format.

    :func:`validate_number` Validates the house number format.

    :func:`__str__` Returns a string representation of the address.
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

        :param v: The email address to validate.
        :type v: str

        :returns: The validated email address or None if not provided.
        :rtype: str | None

        :raises ValueError: If the email address is invalid.
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
        The phone number must be a valid international phone number.

        .. todo:: Sometimes the phone number shows as valid even if it is not.

        :param v: The phone number to validate.
        :type v: str

        :return: The validated phone number or None if not provided.
        :rtype: str | None

        :raises ValueError: If the phone number is invalid.
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
        Accepts House numbers seen in Germany, e.g. 1, 1a, 1A, 1b, 1B, etc.

        :param v: The house number to validate.
        :type v: str

        :returns: The validated house number or None if not provided.
        :rtype: str | None

        :raises ValueError: If the house number is invalid.
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

        :return: A string representation of the address.
        :rtype: str
        """

        return (f"{self.lastname} {self.firstname}\n{self.street} {self.number} \n{self.zip_code} {self.city}\n"
                f"{self.birthdate}\n{self.phone}\n{self.email}")
