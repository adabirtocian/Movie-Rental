class Lista:
    def __init__(self):
        self.list = []

    def __setitem__(self, index, value):
        self.list[index] = value

    def __getitem__(self, index):
        return self.list[index]

    def __delitem__(self, index):
        del self.list[index]

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return ListIterator(self)

    def append(self, value):
        return self.list.append(value)

    def remove(self, element):
        self.list.remove(element)


class ListIterator:
    def __init__(self, lista):
        self.lista = lista
        self.pos = 0

    def __next__(self):
        if self.pos >= len(self.lista.list):
            raise StopIteration
        val = self.lista[self.pos]
        self.pos += 1
        return val


def comparison_criteria(a: object(), b: object()):
    if a.name < b.name:
        return True
    return False


def shell_sort(array, comparison_criteria):
    k = len(array) // 2
    while k > 0:
        for i in range(0, len(array) - k):
            if not comparison_criteria(array[i], array[i + k]):
                array[i], array[i + k] = array[i + k], array[i]
                interchanged = True
                j = i
                while interchanged and j - k >= 0 and i >= k:
                    if not comparison_criteria(array[j - k], array[j]):
                        array[j], array[j - k] = array[j - k], array[j]
                    else:
                        interchanged = False
                    j = j - k
        k = k // 2
    return array


def pass_filter_criteria(a: object()):
    if a.id % 2 == 0:
        return True
    return False


def filter(array, pass_filter_criteria):
    new_array = []
    for x in array:
        if pass_filter_criteria(x):
            new_array.append(x)
    return new_array

