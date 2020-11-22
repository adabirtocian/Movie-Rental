from domain.domain import Client
import random
import re
from service.undo_service import FunctionCall, Operation, CascadedOperation
from domain.validators import IdError


class ClientService:
    def __init__(self, repository, undo_service):
        self._repository = repository
        self._undo_service = undo_service

    def init_list_clients(self):
        client_list = ["Ana", "Florin", "Marius", "Alina", "Iulia", "Paul", "Raul", "Maria", "Vlad", "Paula"]
        for i in range(0, 10):
            the_id = i+1
            name = random.choice(client_list)
            client_list.remove(name)
            self.add_client(the_id, name)

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

    def add_client(self, the_id, name, from_undo=False):
        '''
        Creates a client object that will be added to the list of clients from the repository
        :param from_undo: False if the function eas not called from the undo option, True otherwise
        :param the_id: the client id (int)
        :param name: the client name (string)
        '''
        if self.find_by_id(the_id) is not None:
            raise IdError("Id already exists !")
        self._repository.add(Client(the_id, name))
        if not from_undo:
            function = FunctionCall(self.add_client, the_id, name, True)
            reverse_function = FunctionCall(self.delete_client, the_id, True)
            operation = Operation(function, reverse_function)
            self._undo_service.record_operation(operation)

    def delete_client(self, the_id, from_undo=False):
        '''
        Calls the delete method from the repository in order to delete the client, by the id
        :param from_undo: False if the function eas not called from the undo option, True otherwise
        :param the_id: the client's id
        '''
        if self.find_by_id(the_id) is None:
            raise IdError("Id does not exists")
        client = self.find_by_id(the_id)
        self._repository.delete(client)
        if not from_undo:
            function = FunctionCall(self.delete_client, the_id, True)
            reverse_function = FunctionCall(self.add_client, the_id, client.name, True)
            operation = Operation(function, reverse_function)
            cascaded_operation = CascadedOperation()
            cascaded_operation.add(operation)
            self._undo_service.record_operation(cascaded_operation)

    def update_client(self, the_id, name, from_undo=False):
        '''
        Creates a new client object and calls the update method from the repository for updating the client in the repo
        :param from_undo: False if the function eas not called from the undo option, True otherwise
        :param the_id: the client's id
        :param name: the client's name
        '''
        if self.find_by_id(the_id) is None:
            raise IdError("Id does not exists")
        old_client = self.search_by_id(the_id)
        old_client.name = name
        if not from_undo:
            function = FunctionCall(self.update_client, the_id, name, True)
            reverse_function = FunctionCall(self.update_client, old_client.id, old_client.name, True)
            operation = Operation(function, reverse_function)
            self._undo_service.record_operation(operation)

    def list_clients(self):
        '''
        Returns the list of all client objects from the repository and then returns it
        :return: the list of all clients
        '''
        return self._repository.retrieve_all()

    def search_by_name(self, name):
        matches =[]
        clients_list = self._repository.retrieve_all()
        for client in clients_list:
            if re.search(name, client.name, re.IGNORECASE):
                matches.append(client)
        return matches

    def search_by_id(self, client_id):
        clients_list = self._repository.retrieve_all()
        for client in clients_list:
            if client.id == client_id:
                return client