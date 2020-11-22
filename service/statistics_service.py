from datetime import datetime


class RentalDays:
    def __init__(self, owner, days):
        self._owner = owner
        self._days = days

    @property
    def owner(self):
        return self._owner

    @property
    def days(self):
        return self._days

    @owner.setter
    def owner(self, owner):
        self._owner = owner

    @days.setter
    def days(self, days):
        self._days = days


class StatisticsService:
    def __init__(self, client_repo, movie_repo, rental_repo):
        self._client_repo = client_repo
        self._movie_repo = movie_repo
        self._rental_repo = rental_repo

    @staticmethod
    def transform_to_list(dictionary, type_repo):
        list_days = []
        for key in dictionary:
            object = type_repo.find_by_id(key)
            list_days.append(RentalDays(object, dictionary[key]))

        return list_days

    def most_rented_movies(self):
        dict_movies = dict()
        repo_list = self._rental_repo.retrieve_all()

        for i in range(len(repo_list)):
            rental = repo_list[i]
            movie = self._movie_repo.find_by_id(rental.movie_id)
            if movie.id in dict_movies:
                dict_movies[movie.id] += len(rental)
            else:
                dict_movies[movie.id] = len(rental)

        list_days = self.transform_to_list(dict_movies, self._movie_repo)
        return list_days

    def most_active_clients(self):
        dict_active_clients = dict()
        repo_list = self._rental_repo.retrieve_all()
        
        for i in range(len(repo_list)):
            rental = repo_list[i]
            client = self._client_repo.find_by_id(rental.client_id)
            if client.id in dict_active_clients:
                dict_active_clients[client.id] += len(rental)
            else:
                dict_active_clients[client.id] = len(rental)

        list_days = self.transform_to_list(dict_active_clients, self._client_repo)
        return list_days

    def late_rentals(self):
        dict_late_rentals = dict()
        repo_list = self._rental_repo.retrieve_all()
        for i in range(len(repo_list)):
            rental = repo_list[i]

            if rental.rented_date is not None:
                dict_late_rentals[rental.id] = rental.len_late()

        list_days = self.transform_to_list(dict_late_rentals, self._rental_repo)
        return list_days





