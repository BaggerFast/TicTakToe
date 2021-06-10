class Field:
    def __init__(self, sign, size, cell_count):
        self.cell_count = cell_count
        self.map = [[sign] * size for _ in range(size)]
        self.map_of_rects = [[0] * size for _ in range(size)]
