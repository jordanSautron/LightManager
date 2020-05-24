"""
    This module define Watts Energy Unit
    who is the base energy unit of Blender
"""
import logging
logger = logging.getLogger()

from .unit_model import EnergyUnit
from .. import light_sources


class Watts(EnergyUnit):

    name = 'Watts'
    type = 'WATTS'
    description = 'Default Blender unit (W)'
    need_light_source = True

    def from_lumens(self, lumens, source_type):
        logger.debug('Lumens -> Watts')
        light_source = light_sources.source_by_type.get(source_type)

        if not light_source:
            raise ValueError(f'Invalid source type for: {source_type}')

        light_efficacy = light_source.efficacy
        return lumens / light_efficacy

    def to_lumens(self, watts, source_type):
        logger.debug('Watts -> Lumens')
        light_source = light_sources.source_by_type.get(source_type)

        if not light_source:
            raise ValueError(f'Invalid source type for: {source_type}')

        light_efficacy = light_source.efficacy
        return watts * light_efficacy

Watts = Watts()