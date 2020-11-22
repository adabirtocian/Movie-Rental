from iterable import Lista, ListIterator


class Repository:
    def __init__(self):
        """
        Initializes a Repository object by creating an empty dict of entities
        """
        self._entities = Lista()

    def __len__(self):
        return len(self._entities)

    def add(self, entity):
        """
        Adds a new entity to the list from repo
        :param entity: the entity
        """
        self._entities.append(entity)

    def delete(self, entity):
        """
        Deletes the object
        :param entity: the given object
        """
        self._entities.remove(entity)

    def retrieve_all(self):
        """
        Returns a list of the values in the entities dict, as a list of objects
        :return: the list (list)
        """
        return self._entities


