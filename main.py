import os
import random
import shutil

from csv_interface import CsvInterface as AddressDatabaseCSV
from sqlite_interface import SqliteInterface as AddressDatabaseSQL
from address import Address

from pprint import pprint

from tests.sqlite_test import TestSqlInterface
from tests.csv_test import TestCsvInterface
import unittest

def sql():
    example_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./tests/ExampleSQLTest.db")
    seed = random.randint(0, 1000)
    shutil.copyfile(example_path, rf"./sqlTest{seed}.db")

    new_address = Address(lastname="Schlüssel", firstname="Kommunikation", street="DQLite Allee", number="12z", zip_code=70173,
                          city="Bielefeld", birthdate="1970-01-01")

    interface = AddressDatabaseSQL(rf"./sqlTest{seed}.db")
    interface.open()

    pprint(interface.get_all())

    print(interface.add_address(new_address))

    interface.save()
    interface.close()

    interface.open()
    pprint(interface.get_all())

    interface.save()
    interface.close()
    os.remove(f"./sqlTest{seed}.db")


def csv():
    example_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "./tests/ExampleCSVTest.csv")  # example_path = f"{'/'.join(os.path.realpath(__file__).split('/')[:-1])}/ExampleCSVTest.csv"
    seed = random.randint(0, 1000)
    shutil.copyfile(example_path, rf"./csvTest{seed}.csv")

    new_address = Address(lastname="Schlüssel", firstname="Kommunikation", street="DQLite Allee", number="12z",
                          zip_code=70173,
                          city="Bielefeld", birthdate="1970-01-01")

    interface = AddressDatabaseCSV(rf"./csvTest{seed}.csv")
    interface.open()

    pprint(interface.get_all())

    print(interface.add_address(new_address))

    interface.save()
    interface.close()

    interface.open()
    pprint(interface.get_all())

    interface.save()
    interface.close()
    os.remove(f"./csvTest{seed}.csv")

if __name__ == "__main__":
    sql()
    csv()
    unittest.main()