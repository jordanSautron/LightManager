from .unit_model import EnergyUnit
from .. import light_sources


class Watts(EnergyUnit):

    name = 'Watts'
    type = 'Watts'
    description = 'Default Blender unit (W)'

    def from_watts(self, watts, source_type):
        return watts

    def to_watts(self, watts, source_type):
        return watts

Watts = Watts()