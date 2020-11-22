from datetime import datetime
from domain.validators import ClientValidator as ClientValidator
from domain.validators import MovieValidator as MovieValidator
from domain.validators import RentalValidator as RentalValidator
from domain.validators import UndoError
from iterable import shell_sort, comparison_criteria, filter, pass_filter_criteria


class Ui:
    def __init__(self, client_service, movie_service, rental_service, statistics_service, undo_service, init_list_type):
        self._client_service = client_service
        self._movie_service = movie_service
        self._rental_service = rental_service
        self._statistics_service = statistics_service
        self._undo_service = undo_service
        self._init_list_type = init_list_type

    @staticmethod
    def print_menu():
        print("\nOptions: \n"
              "1. Manage the list of clients or movies\n"
              "2. Rent or return a movie\n"
              "3. Search for clients or movies\n"
              "4. Statistics\n"
              "5. Undo\n"
              "6. Redo\n"
              "0. Exit")

    def start(self):
        options = {"1": self._manage_clients_or_movies,
                   "2": self._rent_or_return_movie,
                   "3": self._search,
                   "4": self._statistics,
                   "5": self._undo,
                   "6": self._redo
                   }

        if self._init_list_type != "False":
            self._client_service.init_list_clients()
            self._movie_service.init_list_movies()
            self._rental_service.init_list_rentals()

        while True:
            self.print_menu()
            option = input("Enter the option number: ").strip()
            if option == "0":
                break
            try:
                options[option]()
            except KeyError:
                print("\nInvalid option")

# ==== OPTION 1 ========================================================================================================

    def _manage_clients_or_movies(self):
        sub_options = {"1": self._manage_clients,
                       "2": self._manage_movies
                       }
        while True:
            sub_option = input("\n1. Manage the list of clients\n"
                               "2. Manage the list of movies\n"
                               "0. Go back\n"
                               "Enter a sub-option number:").strip()
            if sub_option == "0":
                break
            try:
                sub_options[sub_option]()
            except KeyError:
                print("\nInvalid sub-option")

    # CLIENTS
    def _manage_clients(self):
        operations = {
            "1": self._add_client,
            "2": self._remove_client,
            "3": self._update_client,
            "4": self._list_clients
        }
        while True:
            operation = input("\n1. Add a new client\n"
                              "2. Remove a client\n"
                              "3. Update a client's info\n"
                              "4. List all the clients\n"
                              "0. Go Back\n"
                              "Enter an operation number:").strip()
            if operation == "0":
                break
            try:
                operations[operation]()
            except KeyError:
                print("\nInvalid operation")
            except Exception as ex:
                print(ex)

    def _add_client(self):
        the_id = input("Id: ")
        ClientValidator.validate_id(the_id)
        name = input("Name: ")
        ClientValidator.validate_name(name)
        self._client_service.add_client(int(the_id), name)

    def _remove_client(self):
        the_id = input('Id of the client to be removed: ')
        ClientValidator.validate_id(the_id)
        self._client_service.delete_client(int(the_id))
        self._rental_service.remove_rental_by_client(int(the_id))

    def _update_client(self):
        the_id = input("Id: ")
        ClientValidator.validate_id(the_id)
        name = input("Name: ")
        ClientValidator.validate_name(name)
        self._client_service.update_client(int(the_id), name)

    def _list_clients(self):
        clients_list = self._client_service.list_clients()
        clients_list = shell_sort(clients_list, comparison_criteria)
        for client in clients_list:
            print(str(client))

    # MOVIES
    def _manage_movies(self):
        operations = {
            "1": self._add_movie,
            "2": self._remove_movie,
            "3": self._update_movie,
            "4": self._list_movies
        }
        while True:
            operation = input("\n1. Add a new movie\n"
                              "2. Remove a movie\n"
                              "3. Update a movie's info\n"
                              "4. List all the movies\n"
                              "0. Go Back\n"
                              "Enter an operation number:").strip()
            if operation == "0":
                break
            try:
                operations[operation]()
            except KeyError:
                print("\nInvalid operation")
            except Exception as ex:
                print(ex)

    def _add_movie(self):
        the_id = input("Id: ")
        MovieValidator.validate_id(the_id)
        title = input("Title: ")
        MovieValidator.validate_info(title)
        description = input("Description: ")
        MovieValidator.validate_info(description)
        genre = input("Genre: ")
        MovieValidator.validate_info(genre)
        self._movie_service.add_movie(int(the_id), title, description, genre)

    def _remove_movie(self):
        the_id = input('Id of the movie to be removed: ')
        MovieValidator.validate_id(the_id)
        self._movie_service.delete_movie(int(the_id))
        self._rental_service.remove_rental_by_movie(int(the_id))

    def _update_movie(self):
        the_id = input("Id: ")
        MovieValidator.validate_id(the_id)
        title = input("Title: ")
        MovieValidator.validate_info(title)
        description = input("Description: ")
        MovieValidator.validate_info(description)
        genre = input("Genre: ")
        MovieValidator.validate_info(genre)
        self._movie_service.update_movie(int(the_id), title, description, genre)

    def _list_movies(self):
        movies_list = self._movie_service.list_movies()
        for movie in movies_list:
            print(str(movie))

# ==== OPTION 2 ========================================================================================================
    def _rent_or_return_movie(self):
        operations = {
            "1": self._rent_movie,
            "2": self._return_movie,
            "3": self._list_rentals
        }
        while True:
            operation = input("\n1. Rent a movie\n"
                              "2. Return a movie\n"
                              "3. List all rentals\n"
                              "0. Go Back\n"
                              "Enter an operation number:").strip()
            if operation == "0":
                break
            try:
                operations[operation]()
            except KeyError:
                print("\nInvalid operation")
            except Exception as ex:
                print(ex)

    def _rent_movie(self):
        client_id = input("Client id: ")
        ClientValidator.validate_id(client_id)

        movie_id = input("Movie id: ")
        MovieValidator.validate_id(movie_id)

        rented_date_str = input("Rented date (yyyy-MM-dd): ")
        rented_date = datetime.strptime(rented_date_str, '%Y-%m-%d').date()
        due_date_str = input("Due date (yyyy-MM-dd): ")
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        RentalValidator.validate_due_date(rented_date, due_date)

        self._rental_service.rent_a_movie(int(client_id), int(movie_id), rented_date, due_date, None)
        list_rentals = self._rental_service.list_rentals()
        self._list_rentals()

    def _return_movie(self):
        client_id = input("Client id: ")
        ClientValidator.validate_id(client_id)

        movie_id = input("Movie id: ")
        MovieValidator.validate_id(movie_id)

        returned_date_str = input("Returned date(yyyy-MM-dd): ")
        returned_date = datetime.strptime(returned_date_str, '%Y-%m-%d').date()

        self._rental_service.return_a_movie(int(client_id), int(movie_id), returned_date)
        self._late_rentals()

    def _list_rentals(self):
        list_rentals = self._rental_service.list_rentals()
        #list_rentals = filter(list_rentals, filter_criteria)
        for r in list_rentals:
            print(r)

# ==== OPTION 3 ========================================================================================================
    def _search(self):
        operations = {
            "1": self._search_clients,
            "2": self._search_movies
        }

        while True:
            operation = input("\n1. Search a client\n"
                              "2. Search a movie\n"
                              "0. Go back\n"
                              "Enter an operation number: ").strip()
            if operation == '0':
                break
            else:
                try:
                    operations[operation]()
                except KeyError:
                    print("\nInvalid operation")
                except Exception as ex:
                    print(ex)

    # CLIENTS
    def _search_clients(self):
        fields ={
            "1": self._search_clients_by_id,
            "2": self._search_clients_by_name
        }

        while True:
            field = input("\n1. Search by id\n"
                          "2. Search by name\n"
                          "0. Go back\n"
                          "Enter the option: ").strip()

            if field == '0':
                break
            else:
                try:
                    fields[field]()
                except KeyError:
                    print("\nInvalid operation")
                except Exception as ex:
                    print(ex)

    def _search_clients_by_id(self):
        client_id = input("Client id: ")
        match = self._client_service.search_by_id(int(client_id))
        print(match)

    def _search_clients_by_name(self):
        user_input = input("Client name: ")
        matches = self._client_service.search_by_name(user_input)
        for m in matches:
            print(m)

    # MOVIES
    def _search_movies(self):
        fields = {
            "1": self._search_movies_by_id,
            "2": self._search_movies_by_title,
            "3": self._search_movies_by_description,
            "4": self._search_movies_by_genre
        }

        while True:
            field = input("\n1. Search by id\n"
                          "2. Search by title\n"
                          "3. Search by description\n"
                          "4. Search by genre\n"
                          "0. Go back\n"
                          "Enter the option: ").strip()

            if field == '0':
                break
            else:
                try:
                    fields[field]()
                except KeyError:
                    print("\nInvalid operation")
                except Exception as ex:
                    print(ex)

    def _search_movies_by_id(self):
        movie_id = input("Movie id: ")
        match = self._movie_service.search_by_id(int(movie_id))
        print(match)

    def _search_movies_by_title(self):
        title = input("Title: ")
        matches = self._movie_service.search_by_title(title)
        for m in matches:
            print(m)

    def _search_movies_by_description(self):
        description = input("Description: ")
        matches = self._movie_service.search_by_description(description)
        for m in matches:
            print(m)

    def _search_movies_by_genre(self):
        genre = input("Genre: ")
        matches = self._movie_service.search_by_genre(genre)
        for m in matches:
            print(m)

# ==== OPTION 4 ========================================================================================================
    def _statistics(self):
        operations = {
            "1": self._most_rented_movies,
            "2": self._most_active_clients,
            "3": self._late_rentals
        }
        while True:
            operation = input("\n1. Most rented movies\n"
                              "2. Most active clients\n"
                              "3. Late rentals\n"
                              "0. Go Back\n"
                              "Enter an operation number:").strip()
            if operation == "0":
                break
            try:
                operations[operation]()
            except KeyError:
                print("\nInvalid operation")
            except Exception as ex:
                print(ex)

    def _most_rented_movies(self):
        most_rented_list = self._statistics_service.most_rented_movies()
        most_rented_list = sorted(most_rented_list, key=lambda rental: rental.days, reverse=True)
        for i in range(len(most_rented_list)):
            obj = most_rented_list[i]
            print(obj.owner, "\nRented days: ", obj.days, "\n")

    def _most_active_clients(self):
        active_clients_list = self._statistics_service.most_active_clients()
        active_clients_list = sorted(active_clients_list, key=lambda rental: rental.days, reverse=True)
        for i in range(len(active_clients_list)):
            obj = active_clients_list[i]
            print(obj.owner, "\nRented days: ", obj.days, "\n")

    def _late_rentals(self):
        late_rentals = self._statistics_service.late_rentals()
        late_rentals = sorted(late_rentals, key=lambda  rental: rental.days, reverse=True)
        for i in range(len(late_rentals)):
            obj = late_rentals[i]
            print(obj.owner, "\nLate for ", obj.days, " days\n")

# ==== OPTION 5 ========================================================================================================

    def _undo(self):
        try:
            self._undo_service.undo()
            print("Undo performed")
        except UndoError as e:
            print(e)

    def _redo(self):
        try:
            self._undo_service.redo()
            print("Redo performed")
        except UndoError as e:
            print(e)