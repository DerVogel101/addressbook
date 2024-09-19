from address import Address
from csv_interface import CsvInterface

from datetime import date
from pydantic import ValidationError
from freezegun import freeze_time

import unittest
import random
import shutil
import os


class TestCsvInterface(unittest.TestCase):

    def setUp(self) -> None:
        example_path = f"{os.path.realpath(__file__).strip(f"{__name__}.py")}ExampleCSVTest.csv"
        self.seed = random.randint(0, 1000)
        shutil.copyfile(example_path, rf"./csvTest{self.seed}.csv")
        self.interface = CsvInterface(rf"./csvTest{self.seed}.csv")
        self.interface.open()

    def tearDown(self):
        self.interface.save()
        self.interface.close()
        os.remove(f"./csvTest{self.seed}.csv")

    def test_add_address_id(self):
        before = len(self.interface.get_all())
        a = self.interface.add_address(
            Address(lastname="Jürgen", firstname="Hans", street="Obere Bahnhofstraße", number="12", zip_code=70173,
                    city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678",
                    email="hans.huber@exaample.de"))
        b = self.interface.add_address(
            Address(lastname="Müller", firstname="Jürgen", street="Königstraße", number="3", zip_code=70173,
                    city="Stuttgart", birthdate="1980-02-02", phone="+49 711 5678 9012",
                    email="juergen.schmidt@example.de"))
        c = self.interface.add_address(
            Address(lastname="Angler", firstname="Monika", street="Marienplatz", number="6", zip_code=70173,
                    city="Stuttgart", birthdate="1970-03-03", phone="+49 711 1234 5679",
                    email="monika.fischer@example.com"))
        result = len(self.interface.get_all())
        self.assertEqual(result, before+3)
        self.assertEqual(a, 3)
        self.assertEqual(b, 4)
        self.assertEqual(c, 5)

    def test_expect_all(self):
        result = self.interface.get_all()
        assert result == {
            0: Address(lastname='Huber', firstname='Hans', street='Obere Bahnhofstra e', number='3', zip_code=70173,
                       city='Stuttgart', birthdate=date(1990, 1, 1), phone='+49 711 1234 5678',
                       email='hans.huber@exaample.de'),
            1: Address(lastname='Schmidt', firstname='J rgen', street='K nigstra e', number='1', zip_code=70173,
                       city='Stuttgart', birthdate=date(1980, 2, 2), phone='+49 711 5678 9012',
                       email='juergen.schmidt@example.de'),
            2: Address(lastname='Fischer', firstname='Monika', street='Marienplatz', number='2', zip_code=70173,
                       city='Stuttgart', birthdate=date(1970, 3, 3), phone='+49 711 1234 5679',
                       email='monika.fischer@example.com')}

    def test_get(self):
        result = self.interface.get(0)
        self.assertEqual(result,
                         Address(lastname='Huber', firstname='Hans', street='Obere Bahnhofstra e', number='3',
                                 zip_code=70173,
                                 city='Stuttgart', birthdate=date(1990, 1, 1), phone='+49 711 1234 5678',
                                 email='hans.huber@exaample.de'))
        result = self.interface.get(1)
        self.assertEqual(result,
                         Address(lastname='Schmidt', firstname='J rgen', street='K nigstra e', number='1',
                                 zip_code=70173,
                                 city='Stuttgart', birthdate=date(1980, 2, 2), phone='+49 711 5678 9012',
                                 email='juergen.schmidt@example.de'))
        result = self.interface.get(2)
        self.assertEqual(result,
                         Address(lastname='Fischer', firstname='Monika', street='Marienplatz', number='2',
                                 zip_code=70173,
                                 city='Stuttgart', birthdate=date(1970, 3, 3), phone='+49 711 1234 5679',
                                 email='monika.fischer@example.com'))

    def test_reopen(self):
        a = self.interface.add_address(
            Address(lastname="Jürgen", firstname="Hans", street="Obere Bahnhofstraße", number="12", zip_code=70173,
                    city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678",
                    email="hans.huber@exaample.de"))
        self.interface.save()
        self.interface.close()
        self.interface.open()
        result = self.interface.get(a)
        self.assertEqual(result,
                         Address(lastname="Jürgen", firstname="Hans", street="Obere Bahnhofstraße", number="12",
                                 zip_code=70173,
                                 city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678",
                                 email="hans.huber@exaample.de"))

    def test_update(self):
        self.assertEqual(0, self.interface.update(
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
        ))
        new_address = self.interface.get(0)
        self.assertEqual(new_address, Address(lastname="Schmidt", firstname="J rgen", street="K nigstra e", number="1",
                                              zip_code=234643, city="Belin", birthdate="1980-02-10",
                                              phone="+49 711 5678 9012", email="juergen.schmidt@example.de"))

    def test_add_address_with_missing_req_fields(self):
        with self.assertRaises((ValidationError, TypeError)):
            self.interface.add_address(
                Address(lastname="Jürgen", street="Obere Bahnhofstraße", number="12", zip_code=70173,
                        city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678"))

    def test_get_non_existent_address(self):
        result = self.interface.get(9999)  # Non-existent ID
        self.assertIsNone(result)

    def test_update_non_existent_address(self):
        with self.assertRaises(KeyError):
            self.interface.update(
                9999,  # Non-existent ID
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

    def test_delete(self):
        self.assertEqual(0, self.interface.delete(0))
        self.assertIsNone(self.interface.get(0))

    @freeze_time("1990-01-01")
    def test_get_today_birthdays(self):
        result = self.interface.get_today_birthdays()
        self.assertEqual(result,
                         {0:
                              Address(lastname='Huber', firstname='Hans', street='Obere Bahnhofstra e', number='3',
                                      zip_code=70173,
                                      city='Stuttgart', birthdate=date(1990, 1, 1), phone='+49 711 1234 5678',
                                      email='hans.huber@exaample.de')})

    def test_delete_non_existent_address(self):
        result = self.interface.delete(9999)
        self.assertIsNone(result)

    def test_invalid_house_number(self):
        with self.assertRaises(ValidationError):
            self.interface.add_address(
                Address(lastname="Jürgen", firstname="Hans", street="Obere Bahnhofstraße", number="a12", zip_code=70173,
                        city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678"))
        with self.assertRaises(ValidationError):
            self.interface.add_address(
                Address(lastname="Jürgen", firstname="Hans", street="Obere Bahnhofstraße", number="1a2", zip_code=70173,
                        city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678"))
        with self.assertRaises(ValidationError):
            self.interface.add_address(
                Address(lastname="Jürgen", firstname="Hans", street="Obere Bahnhofstraße", number="a", zip_code=70173,
                        city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678"))
        try:
            self.interface.add_address(
                Address(lastname="Jürgend", firstname="Hanfs", street="Obere Bahnhofstraße", number="12a", zip_code=70173,
                        city="Stuttgart", birthdate="1990-01-01", phone="+49 711 1234 5678"))
        except ValidationError as e:
            raise AssertionError("House number should not be invalid") from e


if __name__ == "__main__":
    unittest.main()
