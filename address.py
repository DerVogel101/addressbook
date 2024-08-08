from dataclasses import dataclass
from datetime import date
from typing import Optional
from no_touchy.muple import Muple


@dataclass(order=True, unsafe_hash=True)
class Address:
    lastname: str
    firstname: str
    street: Optional[str] = None
    number: Optional[str] = None
    zip_code: Optional[int] = None
    city: Optional[str] = None
    birthdate: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    def __post_init__(self):
        if self.birthdate:
            self.birthdate = date.fromisoformat(self.birthdate)

    def __str__(self):
        return (f"{self.lastname} {self.firstname}\n{self.street} {self.number} \n{self.zip_code} {self.city}\n"
                f"{self.birthdate}\n{self.phone}\n{self.email}")


if __name__ == "__main__":
    address = Address("ADoe", "John", "Main Street", "123", 12345,
                      "Springfield", "2000-01-01", "+49123456789", "john.doe@doe-mail.io")

    adress2 = Address("Doe", "John", "Main Street", "123", 12345,
                      "Springfield", "2000-01-01", "+49123456789", "john.doe@doe-mail.io")

    adress3 = Address("Abc", "a")
    adress4 = Address("Abc", "b")
    adress5 = Address("bbc", "a")
    adress6 = Address("bbc", "b")

    print(adress3 < adress4)

    sort_list = [adress4, adress6, adress3, adress5]
    sort_list.sort()
    print(sort_list)