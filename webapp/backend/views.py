from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.http import JsonResponse

from pathlib import Path
from dataclasses import asdict
from db_api.csv_interface import CsvInterface
from db_api.sqlite_interface import SqliteInterface
from db_api.address import Address

class ServeVue(APIView):
    def get(self, request):

        return render(request, 'index.html')


class ApiGetTables(APIView):
    default_db_path = "./db"
    default_db_type = "csv"

    def get(self, request, source_id):
        source = Path(self.default_db_path + "." + self.default_db_type) if source_id == "server" else None # ToD: Implement logic for uploaded files
        match source.suffix:
            case ".csv":
                interface = CsvInterface(source)
            case _:
                interface = SqliteInterface(source)
        all_addresses = {}
        with interface as interface:
            for key, address in interface.get_all().items():
                address = asdict(address)
                all_addresses[key] = address
        return JsonResponse(all_addresses)
            

        
        