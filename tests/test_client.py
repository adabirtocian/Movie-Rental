import unittest
from domain.domain import Client
from domain.validators import ClientValidator as Cv
from service.client_service import ClientService
from service.undo_service import UndoService
from repository.repository1 import Repository
from domain.validators import IdError, UndoError


class TestClient(unittest.TestCase):
    def test_init_list(self):
        repo = Repository()
        undo_service = UndoService()
        Cs = ClientService(repo, undo_service)
        Cs.init_list_clients()
        self.assertEqual(len(repo), 10)

    def test_create_client(self):
        c1 = Client(1, "Popescu Alin")
        self.assertEqual(c1.id, 1)
        self.assertEqual(c1.name, "Popescu Alin")

        c1.id = 2
        c1.name = "Ana"
        self.assertEqual(c1.id, 2)
        self.assertEqual(c1.name, "Ana")

        the_id = -2
        name = "Maria"
        with self.assertRaises(ValueError):
            Cv.validate_id(the_id)
            Cv.validate_name(name)

        the_id2 = 2
        name2 = "A"
        with self.assertRaises(ValueError):
            Cv.validate_id(the_id2)
            Cv.validate_name(name2)

    def test_add_client(self):
        the_id = 1
        name = "Popescu Alin"
        repo = Repository()
        undo_service = UndoService()
        client_service = ClientService(repo, undo_service)
        client_service.add_client(the_id, name)
        list_clients = client_service.list_clients()
        self.assertEqual(len(list_clients), 1)

        with self.assertRaises(IdError):       # client already added
            client_service.add_client(1, "Mara Pop")

    def test_update_client(self):
        repo = Repository()
        undo_service = UndoService()
        client_service = ClientService(repo, undo_service)
        client_service.add_client(1, "Popescu Alin")
        client_service.update_client(1, "Ionescu George")
        list_clients = client_service.list_clients()
        self.assertEqual(len(list_clients), 1)
        with self.assertRaises(IdError):        # client does not exist
            client_service.update_client(2, "Mara")

    def test_delete_client(self):
        repo = Repository()
        undo_service = UndoService()
        client_service = ClientService(repo, undo_service)
        client_service.add_client(1, "Popescu Alin")
        client_service.add_client(2, "Ionescu Maria")
        client_service.add_client(3, "Trifan Ion")
        client_service.delete_client(2)
        list_clients = client_service.list_clients()
        self.assertEqual(len(list_clients), 2)
        with self.assertRaises(IdError):    # client does not exist
            client_service.delete_client(4)

    def test_search(self):
        repo = Repository()
        undo_service = UndoService()
        client_service = ClientService(repo, undo_service)
        client_service.add_client(1, "Popescu Alin")
        client_service.add_client(2, "Ionescu Maria")
        client_service.add_client(3, "Trifan Ion")
        client_service.add_client(4, "Muresan Alina")

        # by id
        match = client_service.search_by_id(1)
        self.assertEqual(match.id, 1)

        # by name
        match = client_service.search_by_name("alin")
        self.assertEqual(match[0].name, "Popescu Alin")
        self.assertEqual(match[1].name, "Muresan Alina")


if __name__ == '__main__':
    unittest.main()
