from domain.validators import UndoError


class UndoService:
    def __init__(self):
        self._undo_list = []
        self._redo_list = []

    def record_operation(self, operation):
        self._undo_list.append(operation)
        self.clear_redo_list()

    def add_to_cascaded_operation(self, operation):
        self._undo_list[-1].add(operation)

    def clear_redo_list(self):
        self._redo_list.clear()

    def undo(self):
        if len(self._undo_list) == 0:
            raise UndoError("No more undos !")
        else:
            operation = self._undo_list.pop()
            self._redo_list.append(operation)
            operation.undo()

    def redo(self):
        if len(self._redo_list) == 0:
            raise UndoError("No more redos !")
        else:
            operation = self._redo_list.pop()
            self._undo_list.append(operation)
            operation.redo()


class FunctionCall:
    def __init__(self, function, *parameters):
        self._function = function
        self._params = parameters

    def call(self):
        self._function(*self._params)


class Operation:
    def __init__(self, function, reverse_function):
        self._function = function
        self._reverse_function = reverse_function

    def undo(self):
        self._reverse_function.call()

    def redo(self):
        self._function.call()


class CascadedOperation:
    def __init__(self):
        self._operations = []

    def add(self, operation):
        self._operations.append(operation)

    def undo(self):
        for o in self._operations:
            o.undo()

    def redo(self):
        for o in self._operations:
            o.redo()
