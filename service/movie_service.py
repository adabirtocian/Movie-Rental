from domain.domain import Movie
import random
import re

from domain.validators import IdError
from service.undo_service import FunctionCall, Operation, CascadedOperation


class MovieService:
    def __init__(self, repository, undo_service):
        self._repository = repository
        self._undo_service = undo_service

    def init_list_movies(self):
        title_list = ["Titanic", "Interstellar", "Notebook", "Now you see me 1", "BirdBox", "Pokemon", "Contratiempo",
                      "Always be my maybe", "Joker", "The Lion King"]
        description_list = ["Titanic sinks", "Physics facts", "Makes you cry", "Magic tricks", "Walking blind",
                            "For children", "Spanish movie", "Famous couple", "mentally-troubled comedian Arthur Fleck",
                            "Walt Disney Pictures"]
        genre_list = ["Romance", "Science-fiction", "Drama", "Mistery", "Thrillers", "Animation", "Crime", "Adventure",
                      "Comedy", "History"]
        for i in range(0, 10):
            the_id = i + 1
            title = random.choice(title_list)
            title_list.remove(title)
            description = random.choice(description_list)
            description_list.remove(description)
            genre = random.choice(genre_list)
            genre_list.remove(genre)
            self.add_movie(the_id, title, description, genre)

    def find_by_id(self, the_id):
        """
        Finds the object the this given id
        :param the_id: the object id
        :return: the object
        """
        for x in self._repository.retrieve_all():
            if x.id == the_id:
                return x
        return None

    def add_movie(self, the_id, title, description, genre, from_undo=False):
        '''
        Creates a movie object that will be added to the list of movies from the repository
        :param from_undo: False if the function eas not called from the undo option, True otherwise
        :param the_id: the movie id
        :param title: the movie title
        :param description: the movie description
        :param genre: the movie genre
        '''
        if self.find_by_id(the_id) is not None:
            raise IdError("Id already exists !")
        self._repository.add(Movie(the_id, title, description, genre))
        if not from_undo:
            function = FunctionCall(self.add_movie, the_id, title, description, genre, True)
            reverse_function = FunctionCall(self.delete_movie, the_id, True)
            operation = Operation(function, reverse_function)
            self._undo_service.record_operation(operation)

    def delete_movie(self, the_id, from_undo=False):
        '''
        Calls the delete method from the repository in order to delete the movie, by the id
        :param from_undo: False if the function eas not called from the undo option, True otherwise
        :param the_id: the movie id
        '''
        if self.find_by_id(the_id) is None:
            raise IdError("Id does not exists")
        movie = self.search_by_id(the_id)
        self._repository.delete(movie)
        if not from_undo:
            function = FunctionCall(self.delete_movie, the_id, True)
            reverse_function = FunctionCall(self.add_movie, the_id, movie.title, movie.description, movie.genre, True)
            operation = Operation(function, reverse_function)
            cascaded_operation = CascadedOperation()
            cascaded_operation.add(operation)
            self._undo_service.record_operation(cascaded_operation)

    def update_movie(self, the_id, title, description, genre, from_undo=False):
        '''
        Creates a new movie object and calls the update method from the repository for updating the movie in the repo
        :param from_undo: False if the function eas not called from the undo option, True otherwise
        :param the_id: the movie id
        :param title: the movie title
        :param description: the movie description
        :param genre: the movie genre
        '''
        if self.find_by_id(the_id) is None:
            raise IdError("Id does not exists")
        movie = self.search_by_id(the_id)
        movie.title = title
        movie.genre = genre
        movie.description = description
        if not from_undo:
            function = FunctionCall(self.update_movie, movie.id, movie.title, movie.description, movie.genre, True)
            reverse_function = FunctionCall(self.update_movie, movie.id, movie.title, movie.description, movie.genre, True)
            operation = Operation(function, reverse_function)
            self._undo_service.record_operation(operation)

    def list_movies(self):
        '''
        Returns the list of all movie objects from the repository and then returns it
        :return: the list of all movies
        '''
        return self._repository.retrieve_all()

    def search_by_id(self, movie_id):
        movies_list = self._repository.retrieve_all()
        for movie in movies_list:
            if movie.id == movie_id:
                return movie

    def search_by_title(self, title):
        matches = []
        movies_list = self._repository.retrieve_all()
        for movie in movies_list:
            if re.search(title, movie.title, re.IGNORECASE):
                matches.append(movie)
        return matches

    def search_by_description(self, description):
        matches = []
        movies_list = self._repository.retrieve_all()
        for movie in movies_list:
            if re.search(description, movie.description, re.IGNORECASE):
                matches.append(movie)
        return matches

    def search_by_genre(self, genre):
        matches = []
        movies_list = self._repository.retrieve_all()
        for movie in movies_list:
            if re.search(genre, movie.genre, re.IGNORECASE):
                matches.append(movie)
        return matches
