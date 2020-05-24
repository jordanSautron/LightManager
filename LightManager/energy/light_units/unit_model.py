

class EnergyUnit():

    # Properties

    @property
    def name(self):
        raise NotImplementedError(self)

    @property
    def type(self):
        raise NotImplementedError(self)

    @property
    def description(self):
        raise NotImplementedError(self)


    # Methods

    def from_watts(self, watts, source_type):
        raise NotImplementedError(self)

    def to_watts(self, energy, source_type):
        raise NotImplementedError(self)