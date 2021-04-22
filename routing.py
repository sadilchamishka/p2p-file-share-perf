class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RoutingTable(metaclass=Singleton):

    def __init__(self):
        self.table = []

    # make this method atomic
    def add(self, ip, port):
        self.table.append((ip, port))

    def get(self):
        return self.table

    # make this method atomic
    def remove(self, node):
        return self.table.remove(node)
