from domain.validators import RepositoryException
from repository.repository1 import Repository
import json
from domain.domain import Client, Movie, Rental


class JSONRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = "data_files/" + file_name
        self._read_json_file()

    def _read_json_file(self):
        try:
            f = open(self._file_name, "r")
            objects = json.load(f)
            for attributes in objects["entities"]:
                obj = self._determine_class_type(attributes)
                self.add(obj)
            f.close()
        except EOFError:
            raise RepositoryException("Empty file")
        except IOError:
            raise RepositoryException("Error reading the file")

    def _save_data_to_json_file(self):
        try:
            entities_list = self.retrieve_all()
            data = {"entities": []}
            for entity in entities_list:
                data["entities"].append(vars(entity))
            f = open(self._file_name, "w")
            data = json.dumps(data, indent=2, default=str)
            f.write(data)
            f.close()
        except IOError:
            raise RepositoryException("Error writing to the file")

    def _determine_class_type(self, attributes):
        entity = None
        if self._file_name == "data_files/client.json":
            entity = Client(int(attributes["_id"]), attributes["_name"])
        elif self._file_name == "data_files/movie.json":
            entity = Movie(int(attributes["_id"]), attributes["_title"], attributes["_description"], attributes["_genre"])
        elif self._file_name == "data_files/rental.json":
            entity = Rental(int(attributes["_client_id"]), int(attributes["_movie_id"]), attributes["_rented_date"],
                            attributes["_due_date"], attributes["_returned_date"])
        return entity

    def add(self, entity):
        super().add(entity)
        self._save_data_to_json_file()

    def delete(self, the_id):
        super().delete(the_id)
        self._save_data_to_json_file()

    def update(self, entity):
        super().update(entity)
        self._save_data_to_json_file()