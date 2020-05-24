from . import lumens, watts

units = [
    watts.Watts,
    lumens.Lumens
]

units_by_type = {u.type: u for u in units}