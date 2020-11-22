import mysql.connector
from ui.ui import Ui
from service.rental_service import RentalService
from service.movie_service import MovieService
from service.client_service import ClientService
from service.statistics_service import StatisticsService
from repository.repository1 import Repository
from service.undo_service import UndoService
from repository.file_repository import FileRepository
from repository.binary_file_repository import BinaryRepository
from repository.json_repository import JSONRepository
from repository.db_repository import DatabaseRepository


def read_settings():
    f = open("settings.properties", "r")
    line = f.readline().strip()
    settings_dict = dict()
    while line != "":
        if line[0] != "#":
            line = line.split("=")
            settings_dict[line[0].strip()] = line[1].strip().strip('"')
        line = f.readline().strip()
    f.close()
    if len(settings_dict) == 0:
        raise Exception("Empty settings file")
    return settings_dict


def set_classes(settings_dict):
    repositories = {
        'inmemory': Repository,
        'textfiles': FileRepository,
        'binaryfiles': BinaryRepository,
        'jsonfiles': JSONRepository,
        'database' : DatabaseRepository
    }
    return repositories[settings_dict["repository"]]


if __name__ == '__main__':
    try:
        settings = read_settings()
        repository_type = set_classes(settings)

        if repository_type == Repository:
            client_repository = Repository()
            movie_repository = Repository()
            rental_repository = Repository()
        elif repository_type == DatabaseRepository:
            database = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                passwd="juneAd@^^2019",
                database="mydatabase"
            )
            cursor = database.cursor()
            client_repository = DatabaseRepository(database, cursor, 'clients', ["idClient", "name"])
            movie_repository = DatabaseRepository(database, cursor, 'movies', ["id_movie", "title", "description", "genre"])
            rental_repository = DatabaseRepository(database, cursor, 'rentals', ["id_client", "id_movie", "rented_date", "due_data", "returned_date"])
        else:
            client_repository = repository_type(settings["clients"])
            movie_repository = repository_type(settings["movies"])
            rental_repository = repository_type(settings["rentals"])

        undo_service = UndoService()
        client_service = ClientService(client_repository, undo_service)
        movie_service = MovieService(movie_repository, undo_service)
        rental_service = RentalService(rental_repository, client_repository, movie_repository, client_service, movie_service, undo_service)
        statistics_service = StatisticsService(client_repository, movie_repository, rental_repository)

        ui = Ui(client_service, movie_service, rental_service, statistics_service, undo_service, settings["init_list"])
        ui.start()

    except Exception as ex:
        print(ex)
