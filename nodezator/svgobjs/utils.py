"""General utilities."""

### standard library import
from collections.abc import Iterable



def get_svg_formatted_color(color):
    """Return color in format usable in SVG color attributes."""

    if isinstance(color, str):
        return color

    elif isinstance(color, Iterable):

        _r, _g, _b, *_ = color
        return f'rgb({_r}, {_g}, {_b})'

    elif color is None:
        return 'none'

    else:

        raise TypeError(
            "'color' must be None, string or iterable of integers with 3+ values"
        )
