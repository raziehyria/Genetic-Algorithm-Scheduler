class Classroom:
    """Represents a Class room with building, room number, maximum capacity and class type"""

    def __init__(self, building, room, max_capacity, room_type):
        self._building = building
        self._room = room
        self._max_capacity = max_capacity
        self._room_type = room_type

    def get_building(self):
        return self._building

    def get_room(self):
        return self._room

    def get_max_capacity(self):
        return self._max_capacity

    def get_type(self):
        return self._room_type

    def __str__(self):
        return "{}{}".format(self.get_building(), self.get_room())
