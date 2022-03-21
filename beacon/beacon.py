class Beacon:

    def __init__(self, id, x, y):
        self.id = id
        self.point = (x, y)

    def get_x(self):
        return self.point[0]

    def get_y(self):
        return self.point[1]

