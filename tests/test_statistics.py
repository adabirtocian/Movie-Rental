import unittest
from repository.repository1 import Repository
from service.rental_service import RentalService
from service.statistics_service import StatisticsService
from service.statistics_service import RentalDays
from service.client_service import ClientService
from service.movie_service import MovieService
from domain.domain import Client
from service.undo_service import UndoService

class TestStatistics(unittest.TestCase):

    def test_most_rented_movies(self):
        repoR = Repository()
        repoC = Repository()
        repoM = Repository()
        undo_service = UndoService()
        service_client = ClientService(repoC, undo_service)
        service_client.init_list_clients()

        service_movie = MovieService(repoM, undo_service)
        service_movie.init_list_movies()

        service = RentalService(repoR, repoC, repoM, undo_service)
        service.init_list_rentals()

        statistics = StatisticsService(repoC, repoM, repoR)
        most_rented_list = statistics.most_rented_movies()
        most_rented_list = sorted(most_rented_list, key=lambda rental: rental.days, reverse=True)

        rental_days = most_rented_list[0]
        owner = service_movie.search_by_id(3)
        self.assertEqual(rental_days.owner, owner)
        self.assertEqual(rental_days.days, 56)

    def test_most_active_clients(self):
        repoR = Repository()
        repoC = Repository()
        repoM = Repository()
        undo_service = UndoService()
        service_client = ClientService(repoC, undo_service)
        service_client.init_list_clients()

        service_movie = MovieService(repoM, undo_service)
        service_movie.init_list_movies()

        service = RentalService(repoR, repoC, repoM, undo_service)
        service.init_list_rentals()

        statistics = StatisticsService(repoC, repoM, repoR)
        most_active_clients = statistics.most_active_clients()
        most_active_clients = sorted(most_active_clients, key=lambda rental: rental.days, reverse=True)

        self.assertEqual(len(most_active_clients), 6)
        rental_days = most_active_clients[0]
        owner = service_client.search_by_id(1)
        self.assertEqual(rental_days.owner, owner)
        self.assertEqual(rental_days.days, 71)

    def test_late_rentals(self):
        repoR = Repository()
        repoC = Repository()
        repoM = Repository()
        undo_service = UndoService()
        service_client = ClientService(repoC, undo_service)
        service_client.init_list_clients()

        service_movie = MovieService(repoM, undo_service)
        service_movie.init_list_movies()

        service = RentalService(repoR, repoC, repoM, undo_service)
        service.init_list_rentals()

        statistics = StatisticsService(repoC, repoM, repoR)
        late_rentals = statistics.late_rentals()
        self.assertEqual(len(late_rentals), 7)


class TestRentalDays(unittest.TestCase):
    def test_setters(self):
        c = Client(1, "Ana")
        r = RentalDays(c, 22)
        self.assertEqual(r.owner, c)
        self.assertEqual(r.days, 22)

        c1 = Client(2, "Maria")
        r.owner = c1
        r.days = 13
        self.assertEqual(r.owner, c1)
        self.assertEqual(r.days, 13)


if __name__ == '__main__':
    unittest.main()