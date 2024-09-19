# Sqlite Interface Documentation

## Diagram

![Ein Bild, das Text, Screenshot, Software, Multimedia-Software enthält.
Automatisch generierte Beschreibung](media/471f6ef3a3b586d2d47f2cf14c5e9456.png)

## Search Implemantation

The SqliteInterface implements the search method like this:

```python
result_search = self.__squirrel_lite.search(search_string)
return {row['id']: Address(**row) for row in result_search}
```

the methods sents the value to search for to the search method in
sqlite_database.py

```python
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
```

Sqlite is then set to return Row objects that i can convert to dicts
