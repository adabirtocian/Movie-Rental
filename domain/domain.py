from datetime import date


class Movie:
    def __init__(self, movie_id, title, description, genre):
        self._id = movie_id
        self._title = title
        self._description = description
        self._genre = genre

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def genre(self):
        return self._genre

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @genre.setter
    def genre(self, new_genre):
        self._genre = new_genre

    def __str__(self):
        return "movieId: " + str(self._id) + ", title: " + str(self._title) + ", description: " + \
               str(self._description) + ", genre: " + str(self._genre)

    def __eq__(self, other):
        return self.id == other.id

    def tuple_fields(self):
        return (self._id, self._title, self._description, self._genre)


class Client:
    def __init__(self, the_id, name):
        self._id = the_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @name.setter
    def name(self, new_name):
        self._name = new_name

    def __str__(self):
        return "clientId: " + str(self._id) + ", clientName: " + str(self._name)

    def __eq__(self, other):
        return self.id == other.id

    def tuple_fields(self):
        return (self._id, self._name)


class Rental:
    def __init__(self, client_id, movie_id, rented_date, due_date, returned_date):
        self._id = str(client_id) + "-" + str(movie_id)
        self._movie_id = movie_id
        self._client_id = client_id
        self._rented_date = rented_date
        self._due_date = due_date
        self._returned_date = returned_date

    @property
    def id(self):
        return self._id

    @property
    def movie_id(self):
        return self._movie_id

    @property
    def client_id(self):
        return self._client_id

    @property
    def rented_date(self):
        return self._rented_date

    @property
    def due_date(self):
        return self._due_date

    @property
    def returned_date(self):
        return self._returned_date

    @client_id.setter
    def client_id(self, new_id):
        self._client_id = new_id

    @movie_id.setter
    def movie_id(self, new_id):
        self._movie_id = new_id

    @rented_date.setter
    def rented_date(self, new_date):
        self._rented_date = new_date

    @due_date.setter
    def due_date(self, new_date):
        self._due_date = new_date

    @returned_date.setter
    def returned_date(self, new_date):
        self._returned_date = new_date

    def __str__(self):
        return "rentalId: " + str(self._id) + ", clientId: " + str(self._client_id) + ", movieId: " + \
               str(self._movie_id) + ", rentedDate: " + str(self._rented_date) + ", dueDate: " + str(self._due_date) \
               + ", returnedDate:" + str(self._returned_date)

    def __len__(self):
        if self.returned_date is not None:
            return (self.returned_date - self.rented_date).days
        else:
            return (date.today() - self.rented_date).days

    def __eq__(self, other):
        return self.id == other.id

    def len_late(self):
        if self.returned_date is not None:
            return (self.returned_date - self.due_date).days
        else:
            return (date.today() - self.due_date).days

    def tuple_fields(self):
        return (self._id, self._client_id, self._movie_id, self._rented_date, self._due_date, self._returned_date)