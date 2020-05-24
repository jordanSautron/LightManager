

class EnergyUnit():

    # Attributes

    need_light_source = False  # Set to True if the unit need the light source to be expose to the user

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

    def from_lumens(self, lumens, source_type):
        raise NotImplementedError(self)

    def to_lumens(self, energy, source_type):
        raise NotImplementedError(self)