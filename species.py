class Specie(object):
    def __init__(self, id):
        self.id = id
        self.population = 1
        self.body_size = 1

        self.left = None
        self.right = None


class SpeciesArea(object):
    def __init__(self):
        self.species_head = None
        self.species_tail = None
        self._count = 0

    @property
    def count(self):
        return self._count

    def add_specie_left(self):
        self._count+= 1
        specie = Specie(self._count)

        if not self.species_head:
            self.species_head = specie
            self.species_tail = specie
            return

        self.species_head.left = specie
        specie.right = self.species_head
        self.species_head = specie


    def add_specie_right(self):
        self._count+= 1
        specie = Specie(self._count)

        if not self.species_head:
            self.species_head = specie
            self.species_tail = specie
            return

        self.species_tail.right = specie
        specie.left =  self.species_tail
        self.species_tail = specie

    def remove(self, specie):
        if specie.left:
            specie.left.right = specie.right

        if specie.right:
            specie.right.left = specie.left

    class myiter(object):
        def __init__(self, list):
            self.list = list
            self.current = list.species_head

        def __next__(self):
            if not self.current:
                raise StopIteration
            else:
                value = self.current
                self.current = self.current.right
                return value

    def __iter__(self):
        return SpeciesArea.myiter(self)



