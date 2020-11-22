class IdError(Exception):
    pass


class ServiceError(Exception):
    pass


class RepoError(Exception):
    pass


class UndoError(Exception):
    pass

class RepositoryException(Exception):
    pass


class ClientValidator:
    @staticmethod
    def validate_id(client_id):
        '''
        Raises a ValueError if the id is negative
        '''
        if int(client_id) < 0:
                raise ValueError("Client Id must be a positive integer !")

    @staticmethod
    def validate_name(name):
        '''
         Raises a ValueError if the name is too short or too long
        :param name:  client name
        :return: ValueError
        '''
        if len(name) < 3 or len(name) > 100:
            raise ValueError("Invalid client name !")


class MovieValidator:
    @staticmethod
    def validate_id(movie_id):
        '''
        Raises a ValueError if the id is negative
        '''
        if int(movie_id) < 0:
            raise ValueError("Movie Id must be a positive integer !")

    @staticmethod
    def validate_info(info):
        '''
         Raises a ValueError if the the info is too short or too long
        :param info: info about the movie
        :return: ValueError
        '''
        if len(info) < 3 or len(info) > 100:
            raise ValueError("Too short info !")


class RentalValidator:
    @staticmethod
    def validate_due_date(rented_date, due_date):
        '''
        Raises a ValueError if the due_date is set behind the due_date
        :param rented_date: the rented_date of the rental
        :param due_date: the due_date of the rental
        :return: ValueError
        '''
        if str(due_date) < str(rented_date):
            raise ValueError("Invalid due date !")
