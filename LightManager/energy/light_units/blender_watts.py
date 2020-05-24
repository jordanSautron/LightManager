"""
    This module define Watts Energy Unit
    who is the base energy unit of Blender
"""
import logging
from .unit_model import EnergyUnit
from .. import light_sources


class BlenderWatts(EnergyUnit):

    name = 'Default'
    type = 'BLENDER_WATTS'
    description = 'Default Blender unit'

    def from_lumens(self, lumens, source_type):
        logging.debug('Lumens -> Watts')
        light_source = light_sources.source_by_type.get('IDEAL')

        light_efficacy = light_source.efficacy
        return lumens / light_efficacy

    def to_lumens(self, watts, source_type):
        logging.debug('Watts -> Lumens')
        light_source = light_sources.source_by_type.get('IDEAL')

        light_efficacy = light_source.efficacy
        return watts * light_efficacy

BlenderWatts = BlenderWatts()