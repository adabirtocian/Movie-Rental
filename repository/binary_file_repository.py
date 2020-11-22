import pickle
from domain.validators import RepositoryException
from repository.repository1 import Repository


class BinaryRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = "data_files/" + file_name
        self._read_binary_file()

    def _read_binary_file(self):
        try:
            f = open(self._file_name, "rb")
            objects = pickle.load(f)
            for obj in objects:
                super().add(obj)
            f.close()
        except EOFError:
            raise RepositoryException("Empty file")
        except IOError:
            raise RepositoryException("Error reading the file")

    def _save_data_to_binary_file(self):
        try:
            f = open(self._file_name, "wb")
            entities_list = self.retrieve_all()
            pickle.dump(entities_list, f)
            f.close()
        except IOError:
            raise RepositoryException("Error writing to the file")

    def add(self, entity):
        super().add(entity)
        self._save_data_to_binary_file()

    def delete(self, the_id):
        super().delete(the_id)
        self._save_data_to_binary_file()

    def update(self, entity):
        super().update(entity)
        self._save_data_to_binary_file()