import unittest
from domain.domain import Rental, Client, Movie
from domain.validators import RentalValidator as Rv
from service.rental_service import RentalService
from service.client_service import ClientService
from service.movie_service import MovieService
from repository.repository1 import Repository
from domain.validators import ServiceError, IdError
from datetime import datetime
from service.undo_service import UndoService


class TestRental(unittest.TestCase):
    def test_init_list(self):
        repo = Repository()
        repo_client = Repository()
        repo_movie = Repository()
        undo_service = UndoService()
        Rs = RentalService(repo, repo_client, repo_movie, undo_service)
        Rs.init_list_rentals()
        self.assertEqual(len(Rs.list_rentals()), 9)

    def test_create_rental(self):
        r = Rental(1, 2, "2019-11-12", "2019-11-29", "2019-11-28")
        self.assertEqual(r.id, "1-2")
        self.assertEqual(r.returned_date, "2019-11-28")
        self.assertEqual(r.movie_id, 2)
        self.assertEqual(r.client_id, 1)
        self.assertEqual(r.due_date, "2019-11-29")
        self.assertEqual(r.rented_date, "2019-11-12")
        date = "2019-11-20"
        with self.assertRaises(ValueError):
            Rv.validate_due_date("2019-11-29", date)

        r.client_id = 2
        self.assertEqual(r.client_id, 2)

        r.movie_id = 1
        self.assertEqual(r.movie_id, 1)

        r.rented_date = "2018-01-01"
        self.assertEqual(r.rented_date, "2018-01-01")

        r.due_date = datetime.strptime("2018-01-25", '%Y-%m-%d').date()
        self.assertEqual(str(r.due_date), "2018-01-25")

        r.returned_date = datetime.strptime("2018-01-30", '%Y-%m-%d').date()
        self.assertEqual(str(r.returned_date), "2018-01-30")

        self.assertEqual(r.len_late(), 5)

        r1 = Rental(3, 4, datetime.strptime("2019-11-10", '%Y-%m-%d').date(),
                    datetime.strptime("2019-11-25", '%Y-%m-%d').date(), None)
        self.assertEqual(r1.len_late(), 9)

    def test_add_rentals(self):
        repoRentals = Repository()
        repoClient = Repository()
        repoMovie = Repository()
        undo_service = UndoService()
        serviceC = ClientService(repoClient, undo_service)
        serviceM = MovieService(repoMovie,undo_service)
        serviceC.add_client(2, "Ana",False)
        serviceC.add_client(5, "Ion", False)
        serviceC.add_client(1, "Paula",False)
        serviceM.add_movie(6, "Frozen", "Ice and songs", "Animation", False)
        serviceM.add_movie(2, "Titanic", "a", "Romance", False)

        service = RentalService(repoRentals, repoClient, repoMovie, undo_service)
        service.rent_a_movie(2, 6, "2019-05-15", "2019-05-26", None)
        service.rent_a_movie(5, 2, "2019-05-15", "2019-05-26", "2019-05-25")

    # Rent a movie
        with self.assertRaises(IdError):  # client does not exist
            service.rent_a_movie(3, 6, "2019-05-20", "2019-06-07", None)

        with self.assertRaises(ServiceError):   # client eligible
            service.rent_a_movie(2, 2, "2019-05-29", "2019-06-15", None)

        with self.assertRaises(ServiceError):       # movie not available
            service.rent_a_movie(5, 6, "2019-05-20", "2019-06-07", None)

        with self.assertRaises(ServiceError):       # rental already added
            service.rent_a_movie(5, 2, "2019-05-15", "2019-05-26", "2019-05-25")

        with self.assertRaises(ValueError):     # invalid due date
            Rv.validate_due_date("2019-11-26", "2019-10-02")

    # Return a movie
        with self.assertRaises(IdError):      # client does not exist
            service.return_a_movie(3, 6, "2019-05-26")

        with self.assertRaises(IdError):      # movie does not exist
            service.return_a_movie(2, 1, "2019-05-26")

        service.return_a_movie(2, 6, "2019-05-25") # return a movie
        self.assertEqual(len(serviceM.list_movies()), 2)       # 2 valid rentals

    def test_delete_rentals(self):
        repoRentals = Repository()
        repoClient = Repository()
        repoMovie = Repository()
        undo_service = UndoService()
        serviceC = ClientService(repoClient, undo_service)
        serviceM = MovieService(repoMovie, undo_service)
        serviceC.add_client(2, "Ana", False)
        serviceC.add_client(5, "Ion", False)
        serviceC.add_client(1, "Paula", False)
        serviceM.add_movie(6, "Frozen", "Ice and songs", "Animation", False)
        serviceM.add_movie(2, "Titanic", "a", "Romance", False)

        service = RentalService(repoRentals, repoClient, repoMovie, undo_service)
        service.rent_a_movie(2, 6, "2019-05-15", "2019-05-26", None)
        service.rent_a_movie(5, 2, "2019-05-15", "2019-05-26", "2019-05-25")

        serviceC.delete_client(2, False)
    # Remove rental by client id
        service.remove_rental_by_client(2, False)
        self.assertEqual(len(service.list_rentals()), 1)

        serviceM.delete_movie(2, False)
    # Remove rental by movie id
        service.remove_rental_by_movie(2, False)
        self.assertEqual(len(service.list_rentals()), 0)


if __name__ == '__main__':
    unittest.main()