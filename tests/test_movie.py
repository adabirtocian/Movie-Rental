import unittest
from domain.validators import MovieValidator as Mv
from domain.domain import Movie
from repository.repository1 import Repository
from service.movie_service import MovieService
from service.undo_service import UndoService


class TestMovie(unittest.TestCase):
    def test_init_list(self):
        repo = Repository()
        undo_service = UndoService()
        Ms = MovieService(repo, undo_service)
        Ms.init_list_movies()
        self.assertEqual(len(Ms.list_movies()), 10)

    def test_create_movie(self):
        m = Movie(1, "Titanic", "Cry", "Drama")
        self.assertEqual(m.genre,"Drama")

        the_id = -1
        with self.assertRaises(ValueError):
            Mv.validate_id(the_id)

        title = "B"
        with self.assertRaises(ValueError):
            Mv.validate_info(title)

        m.id = 2
        self.assertEqual(m.id, 2)

        m.title = "Notebook"
        m.description = "Great movie"
        m.genre = "Romance"
        self.assertEqual(m.title, "Notebook")
        self.assertEqual(m.description, "Great movie")
        self.assertEqual(m.genre, "Romance")

    def test_add_movie(self):
        repo = Repository()
        undo_service = UndoService()
        movie_service = MovieService(repo, undo_service)

        the_id = 1
        title = "Frozen"
        description = "Elsa"
        genre = "Animation"
        movie_service.add_movie(the_id, title, description, genre)
        list_movie = movie_service.list_movies()
        self.assertEqual(len(list_movie), 1)

        the_id1 = 2
        title1 = "Titanic"
        description1 = "Leonardo DiCaprio"
        genre1 = "Drama"
        movie_service.add_movie(the_id1, title1, description1, genre1)
        list_movie = movie_service.list_movies()
        self.assertEqual(len(list_movie), 2)

    def test_update_movie(self):
        repo = Repository()
        undo_service = UndoService()
        movie_service = MovieService(repo, undo_service)

        the_id1 = 1
        title1 = "Titanic"
        description1 = "Leonardo DiCaprio"
        genre1 = "Drama"
        movie_service.add_movie(the_id1, title1, description1, genre1)

        the_id = 1
        title = "Frozen"
        description = "Elsa"
        genre = "Animation"
        movie_service.update_movie(the_id, title, description, genre)
        self.assertEqual(len(movie_service.list_movies()), 1)

    def test_delete_movie(self):
        repo = Repository()
        undo_service = UndoService()
        movie_service = MovieService(repo, undo_service)

        movie_service.add_movie(1, "Interstelar", "Physics real facts", "SF")
        movie_service.add_movie(2, "Notebook", "You will definitely cry", "Romantic")
        movie_service.delete_movie(1)
        list_m = movie_service.list_movies()

        self.assertEqual(len(list_m), 1)

    def test_search(self):
        repo = Repository()
        undo_service = UndoService()
        movie_service = MovieService(repo, undo_service)

        movie_service.add_movie(1, "Interstelar", "Physics real facts", "SF")
        movie_service.add_movie(2, "Notebook", "You will definitely cry", "Romantic")
        movie_service.add_movie(3, "Now you see me", "Magic", "Mistery")
        movie_service.add_movie(4, "Always be my maybe", "", "Romance")
    # by id
        match = movie_service.search_by_id(2)
        self.assertEqual(match.title, "Notebook")
    # by title
        matches = movie_service.search_by_title("no")
        self.assertEqual(matches[0].id, 2)
        self.assertEqual(matches[1].id, 3)
    # by description
        matches = movie_service.search_by_description("cry")
        self.assertEqual(matches[0].id, 2)
    # by genre
        matches = movie_service.search_by_genre("roman")
        self.assertEqual(matches[0].id, 2)
        self.assertEqual(matches[1].id, 4)


if __name__ == '__main__':
    unittest.main()
