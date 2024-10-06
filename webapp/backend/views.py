from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

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

    @staticmethod
    def resolve_source(source_id):
        if source_id == "server":
            source = Path(ApiGetTables.default_db_path + "." + ApiGetTables.default_db_type)
        else:
            # Else, return in session stored filename from uploaded file
            source =  Path(source_id)
        match source.suffix:
            case ".csv":
                interface = CsvInterface(source)
            case _:
                interface = SqliteInterface(source)
        return interface

    def get(self, request, source_id):   
        all_addresses = {}
        with self.resolve_source(source_id) as interface:
            for key, address in interface.get_all().items():
                address = asdict(address)
                all_addresses[key] = address
        return JsonResponse(all_addresses)
            

        
class ApiEditTable(APIView):

    def post(self, request, source_id, **kwargs):
        address_id = kwargs.get("address_id")
        with ApiGetTables.resolve_source(source_id) as interface:
            if address_id:
                interface.update(address_id, **request.data)
            else:
                interface.add_address(Address(**request.data))
            interface.save()
        return HttpResponse(200)

    def delete(self, request, source_id, address_id):
        with ApiGetTables.resolve_source(source_id) as interface:
            interface.delete(address_id)
            interface.save()
        return HttpResponse(200)