from .unit_model import EnergyUnit
from .. import light_sources


class Lumens(EnergyUnit):

    name = 'Lumens'
    type = 'LUMENS'
    description = 'Lumens light unit (lm)'

    def from_watts(self, watts, source_type):
        light_source = light_sources.source_by_type.get(source_type)

        if not light_source:
            raise ValueError(f'Invalid source type for: {source_type}')

        light_efficacy = light_source.efficacy
        return watts * light_efficacy

    def to_watts(self, lumens, source_type):
        light_source = light_sources.source_by_type.get(source_type)

        if not light_source:
            raise ValueError(f'Invalid source type for: {source_type}')

        light_efficacy = light_source.efficacy
        return lumens / light_efficacy

Lumens = Lumens()