from address import Address
from sqlite_database import save_to_sqlite

if __name__ == "__main__":
    address = Address(lastname="ADoe", firstname="John", street="Main Street", number="123", zip_code=12345,
                      city="Springfield", birthdate="2000-01-01", phone="+49 176 1234 5678",
                      email="john.doe@doe-mail.io")

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

