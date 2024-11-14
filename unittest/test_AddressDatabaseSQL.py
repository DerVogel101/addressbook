# -*- coding: UTF-8 -*-
# ${topic}
# Name: wolke
# Date: 2024-08-19
# macOS: 14.2.1  Python: 3.12
import random, os
import shutil
from copy import copy
from datetime import date
from unittest import TestCase
from address import Address
from sqlite_interface import SqliteInterface as AddressDatabaseSQL
from sqlite_interface import SqliteInterface
from faker import Faker

class TestAddressDatabaseSQL(TestCase):

    def setUp(self):
        self.faker = Faker()
        self.test_db_extension = "sqlite"
        self.existing_test_db_filepath = r"C:\Users\janir\Documents\addrbook\unittest\test_addresses.sqlite"
        self.__dummy_filenames = []
        self.__address_db = AddressDatabaseSQL(self.existing_test_db_filepath)  # create an instance of the class
        self.__address_db.open()

    def tearDown(self):
        self.__address_db.close()
        for filename in self.__dummy_filenames:
            if os.path.exists(filename):
                os.remove(filename)

    def __get_random_db_filename__(self) -> str:
        self.__dummy_filenames.append("".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=30)) + f".{self.test_db_extension}")
        return self.__dummy_filenames[-1]


    def __get_random_address__(self) -> Address:
        return Address(firstname=self.faker.first_name(), lastname=self.faker.last_name(),
                       zip_code=self.faker.postcode(),
                       city=self.faker.city(), street=self.faker.street_name(), number=self.faker.building_number(),
                       birthdate=self.faker.date_of_birth(), phone="+49 0421 101", email=self.faker.email())

    def test_set_path(self):
        temp_adb = eval(type(self.__address_db).__name__)(self.existing_test_db_filepath)  # create a new instance of the same class
        if temp_adb._SqliteInterface__sql_path != self.existing_test_db_filepath:
            self.fail("set_path failed")
        temp_adb.close()


    def test_open_existing_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same file
        temp_adb.set_path(self.existing_test_db_filepath)
        try:
            temp_adb.open()
            temp_adb.close()
        except FileNotFoundError as fe:
            raise fe
        except Exception as e:
            self.fail(f"Open {temp_adb} failed: {e}")


    def test_open_non_existing_db(self):
        # get random filename of 20 letters
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(self.__get_random_db_filename__())
        try:
            temp_adb.open()
            # check if file exists
            self.assertTrue(os.path.exists(temp_adb._SqliteInterface__sql_path), "open failed. File not found")
        except FileNotFoundError as fe:
            self.fail(f"Opening non existing db {self.__address_db.filepath} failed: {fe}")
        temp_adb.close()

    def test_save_to_new_db(self):
        """save a second file and check if it exists and is not empty"""
        rnd_filename = self.__get_random_db_filename__()
        ## copy db to random generated filename
        # shutil.copy(self.existing_db_filepath, rnd_filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(self.__get_random_db_filename__())
        temp_adb.open()
        print(self.__address_db.get_all().values())
        for address in self.__address_db.get_all().values():
            temp_adb.add_address(address)
        try:
            # write entries to new db
            temp_adb.save()
            # check if file exists
            self.assertTrue(os.path.exists(temp_adb._SqliteInterface__sql_path), "save failed. File not found")
            # check if file bigger than 0
            self.assertTrue(os.path.getsize(temp_adb._SqliteInterface__sql_path) > 0, "save failed. File empty")
            # check if all entries  are copied
            for address in temp_adb.get_all().values():
                self.assertIn (address,  self.__address_db.get_all().values(), "save failed. Files are not the same")
            # check if number of entries are the same
            self.assertEqual(len(self.__address_db.get_all().values()), len(temp_adb.get_all().values()), "save failed. Files are not the same")
            temp_adb.close()
        except FileNotFoundError as fe:
            raise fe
        except Exception as e:
            self.fail(f"Save {self.__address_db._SqliteInterface__sql_path} failed: {e}")


    def test_add_address_to_empty_db(self):
        # create random filename of 20 letters
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(self.__get_random_db_filename__())        # test first with empty db, second run with populated db
        temp_adb.open()
        new_address = self.__get_random_address__()
        old_len = len(temp_adb.get_all())
        self.assertEqual(old_len, 0, "add_address failed. Address container not empty")
        temp_adb.add_address(new_address)
        new_len = len(temp_adb.get_all())
        self.assertEqual(new_len, 1, "add_address failed. length of address container is not 1")
        self.assertEqual(new_len, old_len+1, "add_address failed. length of address container did not increase by 1")
        temp_adb.close()


    def test_add_address_to_non_empty_db(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_test_db_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(self.__get_random_db_filename__())
        temp_adb.open()
        old_len = len(temp_adb.get_all())
        for i in range(1, 101):
            new_address = self.__get_random_address__()
            temp_adb.add_address(new_address)
            new_len = len(temp_adb.get_all())
            self.assertEqual(new_len, old_len + i,
                             "add_address failed. length of address container did not increase by 1")
        temp_adb.close()   # close the file

    def test_add_and_delete_to_empty_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(self.__get_random_db_filename__())
        temp_adb.open()
        old_len = len(temp_adb.get_all())
        ## add 100 addresses
        for i in range(1, 101):
            new_address = self.__get_random_address__()
            temp_adb.add_address(new_address)
            new_len = len(temp_adb.get_all())
            self.assertEqual(new_len, old_len + i,
                             "add_address failed. length of address container did not increase by 1")
        ## get all keys and delete all addresses
        keys = tuple(temp_adb.get_all().keys())
        self.assertEqual(len(keys), 100, "add_address failed. Address container not filled with 100 addresses")
        for key in keys:
            temp_adb.delete(key)
        self.assertEqual(len(temp_adb.get_all()), 0, "delete failed. Address container not empty after deleting all addresses")
        temp_adb.close()


    def test_delete_from_empty_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(self.__get_random_db_filename__())
        temp_adb.open()
        for i in (-1, 0,10, 100):
            index = temp_adb.delete(i)
            self.assertIsNone(index, "delete failed. Returned index is not None")
        temp_adb.close()


    def test_delete_all_from_non_empty_db(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_test_db_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(filename)
        temp_adb.open()
        indizes = tuple(temp_adb.get_all().keys())
        for index in indizes:
            res = temp_adb.delete(index)
            self.assertIsNotNone(res, "Could not delete existing address. Returned index is None")
        temp_adb.close()


    '''check entries in db'''
    def test_emptyness_of_db(self):
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(self.__get_random_db_filename__())
        temp_adb.open()
        # check if db is empty
        self.assertEqual(len(temp_adb.get_all().keys()), 0, 'Empty db does not seem empty')
        temp_adb.close()


    def test_datatypes(self):
        for address in self.__address_db.get_all().values():
            self.assertEqual(isinstance(address, Address), True,
                             f"get failed. Entry in db not a valid Address object")


    def test_search_for_lastname(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_test_db_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(filename)
        temp_adb.open()
        tmp_address = self.__get_random_address__()
        # get a random address from the database
        ind = tuple(temp_adb.get_all().keys())[0]
        existing_address = temp_adb.get(ind)
        new_address = copy(existing_address)
        new_address.lastname = tmp_address.lastname
        new_address.phone = tmp_address.phone
        ## add the same address twice
        temp_adb.add_address(new_address)
        temp_adb.add_address(new_address)
        for add in (existing_address, new_address):
            found_addresses = temp_adb.search(add.lastname)
            if add not in found_addresses.values():
                self.fail(f"search failed. Address: {add} not in found addresses")
            if add == new_address and not len(found_addresses) >= 2:
                self.fail(f"search failed. Address: {add} found only once")
        temp_adb.close()


    def test_search_for_phone(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_test_db_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()
        temp_adb.set_path(filename)
        temp_adb.open()
        tmp_address = self.__get_random_address__()
        ind = tuple(temp_adb.get_all().keys())[0]
        existing_address = self.__address_db.get(ind)
        new_address = copy(existing_address)
        new_address.lastname = tmp_address.lastname
        new_address.phone = tmp_address.phone
        ## add the same address twice
        temp_adb.add_address(new_address)
        temp_adb.add_address(new_address)
        for add in (existing_address, new_address):
            found_addresses = temp_adb.search(add.phone)
            if len(found_addresses) == 0:  # not even found once
                self.fail(f"search failed. Address: {add} not even found once")
            if add not in found_addresses.values():
                self.fail(f"search failed. Address: {add} not in found addresses")
            if add == new_address and not len(found_addresses) >= 2:
                self.fail(f"search failed. Address: {add} found only once")
        temp_adb.close()


    def test_update(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_test_db_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(filename)
        temp_adb.open()
        # changing 2 addresses first and last
        for i in (0, -1):
            ind = tuple(temp_adb.get_all().keys())[i]
            new_address = self.__get_random_address__()
            temp_adb.update(ind, lastname=new_address.lastname, phone=new_address.phone)
            self.assertEqual(temp_adb.get(ind).lastname, new_address.lastname, "update failed. Lastname not updated")
            self.assertEqual(temp_adb.get(ind).phone, new_address.phone, "update failed. Phone not updated")
        temp_adb.close()


    def test_get_todays_birthdays(self):
        filename = self.__get_random_db_filename__()
        shutil.copy(self.existing_test_db_filepath, filename)
        temp_adb = eval(type(self.__address_db).__name__)()  # create a new instance of the same class
        temp_adb.set_path(filename)
        temp_adb.open()
        # add 4 addresses with different birthdates
        delta_years = (12, 20, 3, 7)
        for dy in delta_years:
            add_today = self.__get_random_address__()
            add_today.birthdate = date.today().replace(year=date.today().year-dy)
            temp_adb.add_address(add_today)
            temp_adb.save()
        birthdates = temp_adb.get_todays_birthdays()
        self.assertEqual(len(birthdates), len(delta_years), f"get_todays_birthdays failed. Not all birthdates (must be {len(delta_years)} found")
        for address in birthdates.values():
            if address.birthdate.month != date.today().month or address.birthdate.day != date.today().day:
                self.fail("get_todays_birthdays failed. Not all birthdates are today")
        temp_adb.close()

if __name__ == '__main__':
    from unittest import main
    main()