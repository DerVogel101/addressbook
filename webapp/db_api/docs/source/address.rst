Address module
==============


This module defines the `Address` dataclass, which represents an address with various fields such as lastname, firstname, street, number, zip code, city, birthdate, phone, and email. It includes validation for email, phone, and house number fields.
The 'Address' dataclass uses a dataclass from Pydantic, instead of the standard dataclass from the 'dataclasses' module, to provide additional validation and type checking for the fields.

Usage Example:
--------------
    .. code-block:: python
        :linenos:

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


.. automodule:: address
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __str__
