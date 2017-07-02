from . import (
    agencies,
    calendars,
    routes,
    stops,
    stopstimes,
    trips
)
# TODO: check te use of all and slot on this one
__slot__ = [
    agencies,
    calendars,
    routes,
    stops,
    stopstimes,
    trips
]

__all__ = [
    'agencies',
    'calendars',
    'routes',
    'stops',
    'stopstimes',
    'trips'
]