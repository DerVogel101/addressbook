Search csv_interface
====================
.. code-block:: python
    :linenos:

    @__require_df_memory
    def search(self, search_string: str) -> dict[int, Address]:
    result = self.__df_memory[
                self.__df_memory.apply(
                    lambda row: row
                    .astype(str)
                    .str
                    .contains(search_string, case=False, na=False)
                    .any(),
                    axis=1)]
            address_dict = {}
    for row in result.iterrows():
        address_dict[row[0]] = self.__series_to_address(row[1])
    return address_dict
    

Siehe auch :func:`csv_interface.CsvInterface.search`.

Die Funktion `search()` verwendet den Decorator `@__require_df_memory`, welcher sicherstellt, dass die Funktion, wenn keine Daten in `__df_memory`
vorhanden sind, gar nicht ausgeführt wird und stattdessen ein Default-Wert zurückgegeben wird (hier ein leeres Directory).
Sie bekommt einen String, `search_string`, in dem der gesuchte Wert übergeben wird und gibt ein ggf. leeres Dictionary mit allen gefundenen Datenreihen 
(und ihren ID, im DataFrame), die den `search_string` beinhalten zurück.

Implementierung der Suchfunktion
---------------------------------
Bei der Implementierung der Suchfunktion werden vor allem durch Pandas zur Verfügung gestellte Funktionen/Methoden verwendet,
um die Übersichtlichkeit und Effizienz der Suche zu gewährleisten.

In `result` werden alle auf den Such-String zutreffenden DataFrames gespeichert. Gesucht werden sie, indem ein durch die Pandas `apply()`-Funktion
generierter DataFrame (welcher gleich groß ist wie die Datenreihe selbst) als Index der Datenreihe (`__df_memory`) übergeben wird. Dies funktioniert
dank der speziellen Implementierung von `__getitem__()` in der Pandas DataFrame-Klasse.

Der dafür erstellte DataFrame wird erzeugt, indem die `apply()`-Methode auf die
gegebene Datenreihe (`__df_memory`) ausgeführt wird. Dieser wird eine (hier anonyme, Lambda-) Funktion
übergeben sowie `axis=1`, was dafür sorgt, dass jede Reihe des DataFrames (eine Data-Serie, `pd.Series` nach der anderen)
an die anonyme Funktion übergeben wird. Die Lambda-Funktion nimmt dann die Reihen an und führt die eigentliche Suche durch.
Dafür wird zunächst (mittels der `astype(str)`-Methode) sichergestellt, dass jedes Element in der Datenreihe ein String ist.
Anschließend können dann mit `.str` Operationen direkt auf die Strings in der Datenreihe angewendet werden.

So wird, dank der Pandas-Implementierung, `.contains()` auf jeden String in der Datenreihe angewendet. `contains()` überprüft,
ob der Such-String in dem String, auf den es angewendet wurde, enthalten ist, und gibt, wenn ja, `True` zurück. Hier wurde zusätzlich
sichergestellt, dass bei `NaN` `False` zurückgegeben wird und dass die Suche Groß-/Kleinschreibung nicht beachtet. 
Dadurch wird z.B.: aus der Datenreihe `{lastname: „Scholz“, firstname: „Olaf“, city: „Berlin“}` bei einem Search-string von „berlin“ die 
Datenreihe `{lastname: False, firstnale: False, city: True}`. 

Letztlich wird `any()` auf die von `contains()` erstellte Datenreihe aus `True`/`False` aufgerufen, wodurch `True` zurückgegeben wird,
solange `contains()` einen (oder mehr) Treffer gefunden hat (/die Datenreihe mindestens ein `True` enthält). 
Da diese Funktion auf jede Reihe angewendet wird, entsteht ein DataFrame, in dem jede Reihe nur ein `True`/`False` beinhaltet und sich
so als Index eignet. 

Anschließend werden die gefundenen Datenreihen in den Datentyp `Address` umgewandelt und als Dictionary, bei dem
der Key die ID der Adresse im DataFrame ist, zurückgegeben. Die Umwandlung geschieht mittels einer weiteren Funktion, die sicherstellt,
dass alle Felder korrekt umgewandelt werden.
