class Identifiable:

    NEXT_ID_BY_CLASS = {}

    def __init__(self):
        key = self.__class__
        id_num = self.NEXT_ID_BY_CLASS.get(key, 1)
        self.NEXT_ID_BY_CLASS[key] = id_num + 1
        self.id = id_num

    def __str__(self):
        return f"{type(self).__name__}(id={self.id})"

