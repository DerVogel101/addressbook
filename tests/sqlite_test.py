from address import Address
from sqlite_interface import SqliteInterface

from datetime import date

import unittest
import random
import os


class TestCsvInterface(unittest.TestCase):

    def setUp(self) -> None:
        self.seed = random.randint(0, 1000)
        self.interface = SqliteInterface(rf"./sqlTest{self.seed}.db")
        self.interface.open()

    # def tearDown(self):
    #     self.interface.save()
    #     self.interface.close()
    #     os.remove(f"./sqlTest{self.seed}.db")

    def test_add_address_id(self):
        a = self.interface.add_address(
            Address(lastname="Huber", firstname="Hans", street="Obere Bahnhofstra e", number="3", zip_code=70173,
                    city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678",
                    email="hans.huber@exaample.de"))
        b = self.interface.add_address(
            Address(lastname="Schmidt", firstname="J rgen", street="K nigstra e", number="1", zip_code=70173,
                    city="Stuttgart", birthdate="1980-02-02", phone="+49 711 5678 9012",
                    email="juergen.schmidt@example.de"))
        c = self.interface.add_address(
            Address(lastname="Fischer", firstname="Monika", street="Marienplatz", number="2", zip_code=70173,
                    city="Stuttgart", birthdate="1970-03-03", phone="+49 711 1234 5679",
                    email="monika.fischer@example.com"))
        d = self.interface.add_address(
            Address(lastname="TodaysBirthday", firstname="John", street="Today Street", number="1", zip_code=12345,
                    city="Today City", birthdate=date.today(), phone="+49 176 1234 5678",
                    email="john.doe@example.com"))
        import doctest
        # assert a == 1
        # assert b == 2
        # assert c == 3
        # assert d == 4
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)
        self.assertEqual(c, 3)
        self.assertEqual(d, 4)

    def test_expect_all(self):
        result = self.interface.get_all()
        assert result == [
            Address(lastname="Huber", firstname="Hans", street="Obere Bahnhofstra e", number="3", zip_code=70173,
                    city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678",
                    email="hans.huber@exaample.de"),
            Address(lastname="Schmidt", firstname="J rgen", street="K nigstra e", number="1", zip_code=70173,
                    city="Stuttgart", birthdate="1980-02-02", phone="+49 711 5678 9012",
                    email="juergen.schmidt@example.de"),
            Address(lastname="Fischer", firstname="Monika", street="Marienplatz", number="2", zip_code=70173,
                    city="Stuttgart", birthdate="1970-03-03", phone="+49 711 1234 5679",
                    email="monika.fischer@example.com"),
            Address(lastname="TodaysBirthday", firstname="John", street="Today Street", number="1", zip_code=12345,
                    city="Today City", birthdate=date.today(), phone="+49 176 1234 5678",
                    email="john.doe@example.com")
        ]

    def test_get(self):
        self.interface.get(0)
        assert self.interface.get(0) == Address(lastname="Huber", firstname="Hans", street="Obere Bahnhofstra e",
                                                number="3", zip_code=70173, city="Stuttgart",
                                                birthdate="1990-01-01", phone="+49 711 1234 5678",
                                                email="hans.huber@exaample.de")

    def test_reopen(self):
        self.interface.close()
        self.interface.open()
        self.test_expect_all()

    def test_update(self):
        assert 0 == self.interface.update(
            0,
            lastname="Schmidt",
            firstname="J rgen",
            street="K nigstra e",
            number="1",
            zip_code=234643,
            city="Belin",
            birthdate="1980-02-10",
            phone="+49 711 5678 9012",
            email="juergen.schmidt@example.de"
        )
        new_address = self.interface.get(0)
        assert new_address == Address(
            lastname="Schmidt",
            firstname="J rgen",
            street="K nigstra e",
            number="1",
            zip_code=234643,
            city="Belin",
            birthdate="1980-02-10",
            phone="+49 711 5678 9012",
            email="juergen.schmidt@example.de")


if __name__ == "__main__":
    unittest.main()
