class Room:
    """"""

    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_seatingCapacity(self): return self._seatingCapacity
    def get_number(self): return self._number
