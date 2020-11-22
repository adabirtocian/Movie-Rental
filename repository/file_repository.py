from domain.domain import Client, Movie, Rental
from domain.validators import RepositoryException
from repository.repository1 import Repository
from datetime import datetime


class FileRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = "data_files/" + file_name
        self._read_file()

    def _read_file(self):
        try:
            f = open(self._file_name, "r")
            line = f.readline().strip()
            while line != "":
                params = line.split(",")
                attributes = {}
                for attr in params:
                    attr = attr.strip()
                    attr = attr.split(":")
                    attributes[attr[0].strip()] = attr[1].strip()
                entity = self._determine_class_type(attributes)
                super().add(entity)
                line = f.readline().strip()
            f.close()
        except IOError:
            raise RepositoryException("Error reading the file")

    def _determine_class_type(self, attributes):
        entity = None
        if self._file_name == "data_files/client_text.txt":
            entity = Client(int(attributes["clientId"]), attributes["clientName"])
        elif self._file_name == "data_files/movie_text.txt":
            entity = Movie(int(attributes["movieId"]), attributes["title"], attributes["description"], attributes["genre"])
        elif self._file_name == "data_files/rental_text.txt":
            rented_date = datetime.strptime(attributes["rentedDate"], "%Y-%M-%d").date()
            due_date = datetime.strptime(attributes["dueDate"], "%Y-%M-%d").date()
            returned_date = datetime.strptime(attributes["returnedDate"], "%Y-%M-%d").date()
            entity = Rental(int(attributes["clientId"]), int(attributes["movieId"]), rented_date, due_date, returned_date)
        return entity

    def _save_data_to_file(self):
        try:
            f = open(self._file_name, "w")
            entities_list = self.retrieve_all()
            for entity in entities_list:
                f.write(str(entity) + "\n")
            f.close()
        except IOError:
            raise RepositoryException("Error writing to the file")

    def add(self, entity):
        super().add(entity)
        self._save_data_to_file()

    def delete(self, the_id):
        super().delete(the_id)
        self._save_data_to_file()

    def update(self, entity):
        super().update(entity)
        self._save_data_to_file()

