"""
    This module contains every available light sources
"""

from .source_model import LightSource


sources = [
    LightSource(
        name='Ideal Source',
        type='IDEAL',
        efficacy=683,
        description='Ideal light source with maximum efficacy'
    ),
    LightSource(
        name='LED',
        type='LED',
        efficacy=172,
        description='Light Electro Diode'
    ),
    LightSource(
        name='Neon',
        type='FLUORESCENT',
        efficacy=82,
        description='Fluorescent lamp'
    ),
    LightSource(
        name='Halogen',
        type='HALOGEN',
        efficacy=35,
        description='Tungsten halogen lamp'
    ),
    LightSource(
        name='Incandescent Bulb',
        type='INCANDESCENT_LIGHT_BULB',
        efficacy=18,
        description='Incandescent light bulb'
    )
]

source_by_type = {s.type: s for s in sources}
