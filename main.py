from sqlite_interface import SqliteInterface
import os
from address import Address

if __name__ == "__main__":
    # Test the SqliteInterface
    USE_WITH = True
    SQLITE_PATH = "./test.db"
    addr1 = Address(
        lastname="Gunther", firstname="Hari", street="Main.cpp", number="-1", zip_code=404,
        city="Gravity Falls", birthdate="2024-09-07", phone="+49 176 1234 5678",
        email="anomaly@krampf.xd"
    )
    addr2 = Address(
        lastname="Gunther", firstname="Häri", street="Main.cpp", number="-1", zip_code=404,
        city="Gravity Falls", birthdate="2024-09-07", phone="+49 176 1234 5678",
        email="anomaly@krampf.xd"
    )

    with SqliteInterface(SQLITE_PATH) as interface:

        interface.open()

        # Raises ValueError because the path is already set and the connection is open
        try:
            interface.set_path(SQLITE_PATH)
        except ValueError as e:
            print(repr(e) + " from " + repr(e.__cause__))

        interface.save()

    interface = SqliteInterface()
    interface.set_path(SQLITE_PATH)
    interface.open()

    print(interface.get_all())
    for id_, address in interface:
        print(id_, address)

    interface.close()

    os.remove(SQLITE_PATH)
