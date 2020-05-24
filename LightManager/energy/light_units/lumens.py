"""
    This module define Lumens Energy Unit
    who is the base energy unit of this addon
"""

import logging
logger = logging.getLogger()

from .unit_model import EnergyUnit
from .. import light_sources


class Lumens(EnergyUnit):

    name = 'Lumens'
    type = 'LUMENS'
    description = 'Lumens light unit (lm)'

    def from_lumens(self, lumens, source_type):
        logger.debug('Lumens -> Lumens')
        return lumens

    def to_lumens(self, lumens, source_type):
        logger.debug('Lumens -> Lumens')
        return lumens


Lumens = Lumens()