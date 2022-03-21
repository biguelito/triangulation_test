
from beacon.beacon import Beacon

class Beacons:

    def __init__(self):
        self.beacons = {}
        return

    def adicionar(self, beacon):
        self.beacons[beacon.id] = beacon
        return

    def criar(self, id, x, y):
        beacon = Beacon(id, x, y)
        self.beacons[beacon.id] = beacon
        return

    def get_beacon(self, id):
        if id in self.beacons.keys():
            return self.beacons[id]
        return None

    def get_beacons(self):
        return self.beacons.values()