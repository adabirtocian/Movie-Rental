from repository.repository1 import Repository


class DatabaseRepository(Repository):
    def __init__(self, database, cursor, table, fields):
        super().__init__()
        self._database = database
        self._cursor = cursor
        self._table = table
        self._fields = fields

    def generate_fields_name(self):
        if self._table == 'clients':
            return ' (' + str(self._fields[0]) + ',' + str(self._fields[1]) + ')' + ' VALUES(%s, %s)'
        elif self._table == 'movies':
            return ' (' + str(self._fields[0]) + ',' + str(self._fields[1]) + ',' + str(self._fields[2]) + ',' + \
                   str(self._fields[3]) + ')' +' VALUES(%s, %s, %s, %s)'
        else:
            return ' (' + str(self._fields[0]) + ',' + str(self._fields[1]) + ',' + str(self._fields[2]) + ',' + \
                   str(self._fields[3]) + ','+ str(self._fields[4]) + ')' +' VALUES(%s, %s, %s, %s, %s)'

    def add(self, object):
        super().add(object)
        fields = self.generate_fields_name()
        command = 'INSERT INTO ' + self._table + fields
        values = object.tuple_fields()
        self._cursor.execute(command, values)
        self._database.commit()

    def delete(self, object):
        super().delete(object.id)
        command = 'DELETE FROM ' + self._table + ' WHERE ' + str(self._fields[0]) + ' VALUES(%s)'
        self._cursor.execute(command, object.id)
        self._database.commit()

    def update(self, object):
        super().update(object)
        command = 'UPDATE ' + self._table + ' WHERE ' + self._fields[0] + ' VALUES(%s)'
        values = object.tuple_fields()
        self._cursor.execute(command, values)
        self._database.commit()

    def list_all(self):
        command = 'SELECT * FROM ' + self._table
        self._cursor.execute(command)
        list_all = self._cursor.fetchall()
        return list_all
