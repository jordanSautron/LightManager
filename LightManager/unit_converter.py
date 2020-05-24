

ENERGY_UINTS = {
    'WATTS': {
        'name': 'Watts',
        'description': 'Default Blender unit',
        'idx': 0
    },
    'LUMENS': {
        'name': 'Lumens',
        'description': 'Default Blender unit',
        'idx': 1
    },
    # 'CANDELA': {
    #     'name': 'Candela',
    #     'description': 'Default Blender unit',
    #     'idx': 0
    # },
    # 'LUX': {
    #     'name': 'Lux',
    #     'description': 'Default Blender unit',
    #     'idx': 0
    # }
}


LIGHT_SOURCES = {
    'PURE': {
        'name': 'Pure light',
        'description': 'Ideal light source with maximum efficacy',
        'efficacy': 683,
        'idx': 0
    },
    'INCANDESCENT_LIGHT_BULB': {
        'name': 'Incandescent Bulb',
        'description': 'Incandescent light bulb',
        'efficacy': 15,
        'idx': 1
    },
    'HALOGEN': {
        'name': 'Halogen',
        'description': 'Tungsten halogen lamp',
        'efficacy': 20,
        'idx': 2
    },
    'FLUORESCENT': {
        'name': 'Neon',
        'description': 'Fluorescent lamp',
        'efficacy': 60,
        'idx': 3
    },
    'LED': {
        'name': 'LED',
        'description': 'Light Electro Diode',
        'efficacy': 90,
        'idx': 4
    }
}


def lumens_to_watts(lumens, light_type):
    
    light_info = LIGHT_SOURCES.get(light_type)

    if not light_info:
        raise ValueError(f'Invalid light type: {light_type}')

    return lumens / light_info['efficacy']


def watts_to_lumens(watts, light_type):
    
    light_info = LIGHT_SOURCES.get(light_type)

    if not light_info:
        raise ValueError(f'Invalid light type: {light_type}')

    return watts * light_info['efficacy']
