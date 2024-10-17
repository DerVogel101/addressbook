Search from sqlite\_database
============================

.. code-block:: python
    :linenos:

    def search(self, search_string: str) -> list[dict]:
        cursor = self.__conn.cursor()
        cursor.row_factory = sqlite3.Row
        query = """
            SELECT * FROM addresses WHERE
            lastname LIKE ? OR
            firstname LIKE ? OR
            street LIKE ? OR
            number LIKE ? OR
            zip_code LIKE ? OR
            city LIKE ? OR
            birthdate LIKE ? OR
            phone LIKE ? OR
            email LIKE ?
        """
        cursor.execute(query, [f'%{search_string}%'] * 9)
        result = cursor.fetchall()
        cursor.row_factory = None
        return [dict(row) for row in result]

The `search` function performs a search on the `addresses` table in the SQLite database. It uses the `LIKE` operator to find rows where any of the specified columns contain the `search_string`.

- **Parameters**:
  - `search_string` (str): The string to search for in the database.

- **Returns**:
  - `list[dict]`: A list of dictionaries, where each dictionary represents a row in the `addresses` table that matches the search criteria.

Implementation Details
----------------------
The `search` function uses the following steps to perform the search:

1. **Create a Cursor**: A cursor object is created using `self.__conn.cursor()`.
2. **Set Row Factory**: The `row_factory` attribute of the cursor is set to `sqlite3.Row` to enable fetching rows as dictionaries.
3. **Define Query**: A SQL query is defined to search for the `search_string` in multiple columns (`lastname`, `firstname`, `street`, `number`, `zip_code`, `city`, `birthdate`, `phone`, `email`).
4. **Execute Query**: The query is executed with the `search_string` parameter applied to all columns.
5. **Fetch Results**: The results are fetched using `cursor.fetchall()`.
6. **Reset Row Factory**: The `row_factory` attribute of the cursor is reset to `None`.
7. **Return Results**: The results are returned as a list of dictionaries.

Example Usage
-------------
.. code-block:: python

    my_database = SqliteDatabase("./example.db")
    search_string = "John"
    results = my_database.search(search_string)
    for result in results:
        print(result)