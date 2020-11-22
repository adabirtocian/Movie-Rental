from domain.domain import Rental
from domain.validators import IdError, ServiceError
from datetime import datetime
from service.undo_service import FunctionCall, Operation, CascadedOperation


class RentalService:
    def __init__(self, repository, client_repository, movie_repository, client_service, movie_service, undo_service):
        self._rental_repository = repository
        self._client_repository = client_repository
        self._movie_repository = movie_repository
        self._client_service = client_service
        self._movie_service = movie_service
        self._undo_service = undo_service

    def init_json_rentals(self):
        self._rental_repository.add(Rental(1, 2, "2019-11-01", "2019-11-20", "2019-11-25"))
        self._rental_repository.add(Rental(5, 6, "2019-11-10", "2019-11-20", "2019-11-25"))
        self._rental_repository.add(Rental(10, 4, "2019-10-11", "2019-11-02", "2019-10-30"))
        self._rental_repository.add(Rental(7, 3, "2019-05-01", "2019-05-15","2019-05-20"))
        self._rental_repository.add(Rental(1, 3, "2019-06-13", "2019-07-02", "2019-07-20"))
        self._rental_repository.add(Rental(1, 8, "2019-02-14", "2019-02-23","2019-02-24"))
        self._rental_repository.add(Rental(6, 10, "2019-09-17", "2019-09-30", "2019-09-27"))
        self._rental_repository.add(Rental(7, 5, "2019-03-16", "2019-03-23", "2019-03-24"))
        self._rental_repository.add(Rental(4, 5, "2019-11-03", "2019-11-16", "2019-11-20"))

    def init_list_rentals(self):
        self._rental_repository.add(Rental(1, 2, datetime.strptime("2019-11-01", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-11-20", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-11-25", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(5, 6, datetime.strptime("2019-11-10", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-11-20", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-11-25", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(10, 4, datetime.strptime("2019-10-11", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-11-02", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-10-30", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(7, 3, datetime.strptime("2019-05-01", '%Y-%m-%d').date(),
                                                datetime.strptime("2019-05-15", '%Y-%m-%d').date(),
                                                datetime.strptime("2019-05-20", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(1, 3, datetime.strptime("2019-06-13", '%Y-%m-%d').date(),
                                                datetime.strptime("2019-07-02", '%Y-%m-%d').date(),
                                                datetime.strptime("2019-07-20", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(1, 8, datetime.strptime("2019-02-14", '%Y-%m-%d').date(),
                                            datetime.strptime("2019-02-23", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-02-24", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(6, 10, datetime.strptime("2019-09-17", '%Y-%m-%d').date(),
                                                datetime.strptime("2019-09-30", '%Y-%m-%d').date(),
                                                datetime.strptime("2019-09-27", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(7, 5, datetime.strptime("2019-03-16", '%Y-%m-%d').date(),
                                            datetime.strptime("2019-03-23", '%Y-%m-%d').date(),
                                           datetime.strptime("2019-03-24", '%Y-%m-%d').date()))
        self._rental_repository.add(Rental(4, 5, datetime.strptime("2019-11-03", '%Y-%m-%d').date(),
                                            datetime.strptime("2019-11-16", '%Y-%m-%d').date(),
                                            datetime.strptime("2019-11-20", '%Y-%m-%d').date()))

    @staticmethod
    def exists(service, the_id, msg):
        if service.find_by_id(the_id) is None:
            raise IdError("Invalid id for " + msg)

    def eligible_client(self, client_id, rented_date):
        repository_list = self._rental_repository.retrieve_all()
        for rental in repository_list:
            if rental.client_id == client_id and rental.returned_date is None and str(rented_date) > str(rental.due_date):
                return False
        return True

    def available_movie(self, movie_id):
        for rental in self._rental_repository.retrieve_all():
            if rental.movie_id == movie_id and rental.returned_date is None:
                return False
        return True

    def rent_a_movie(self, client_id, movie_id, rented_date, due_date, returned_date):
        self.exists(self._client_repository, client_id, "client")
        self.exists(self._movie_repository, movie_id, "movie")

        if self.eligible_client(client_id, rented_date):
            if self.available_movie(movie_id):
                try:
                    self._rental_repository.add(Rental(client_id, movie_id, rented_date, due_date, returned_date))
                except IdError:
                    raise ServiceError("Rental already added")
            else:
                raise ServiceError("Movie not available")
        else:
            raise ServiceError("Client not eligible")

    def find_rental(self, client_id, movie_id):
        for rental in self._rental_repository.retrieve_all():
            if rental.movie_id == movie_id and rental.client_id == client_id:
                return rental

    def return_a_movie(self, client_id, movie_id, returned_date):
        self.exists(self._client_repository, client_id, "client")
        self.exists(self._movie_repository, movie_id, "movie")

        rental = self.find_rental(client_id, movie_id)
        rental.returned_date = returned_date

    def list_rentals(self):
        return self._rental_repository.retrieve_all()

    def remove_rental_by_client(self, client_id, from_undo=False):
        deleted_rentals = []
        list_repo = self._rental_repository.retrieve_all()
        i = 0
        while i < len(list_repo):
            if list_repo[i].client_id == client_id:
                deleted_rentals.append(list_repo[i])
                self._rental_repository.delete(list_repo[i])
                list_repo = self._rental_repository.retrieve_all()
            else:
                i += 1
        if not from_undo:
            function = FunctionCall(self.remove_rental_by_client, client_id, True)
            reverse_function = FunctionCall(self.add_deleted_rentals, deleted_rentals)
            operation = Operation(function, reverse_function)
            self._undo_service.add_to_cascaded_operation(operation)

    def remove_rental_by_movie(self, movie_id, from_undo=False):
        deleted_rentals = []
        list_repo = self._rental_repository.retrieve_all()
        i = 0
        while i < len(list_repo):
            if list_repo[i].movie_id == movie_id:
                deleted_rentals.append(list_repo[i])
                self._rental_repository.delete(list_repo[i])
                list_repo = self._rental_repository.retrieve_all()
            else:
                i += 1
        if not from_undo:
            function = FunctionCall(self.remove_rental_by_movie, movie_id, True)
            reverse_function = FunctionCall(self.add_deleted_rentals, deleted_rentals)
            operation = Operation(function, reverse_function)
            self._undo_service.add_to_cascaded_operation(operation)

    def add_deleted_rentals(self, deleted_rentals):
        for rental in deleted_rentals:
            self._rental_repository.add(rental)
