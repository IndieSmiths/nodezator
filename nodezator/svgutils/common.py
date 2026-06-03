"""Common SVG-related utilities."""

### standard library imports

from collections.abc import Iterable

from xml.dom.minidom import parseString

from re import sub



def format_color(color):
    """Return color in format usable by 'fill' attribute of SVG shapes."""

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


def yield_transformed_svgs(svg_text, id_string, transform_data):

    doc = parseString(svg_text)
    svg = doc.firstChild

    ###

    for element in doc.getElementsByTagName('*'):

        if element.hasAttribute('id'):
            element.setIdAttribute('id')

    ###
    element = doc.getElementById(id_string)

    for transform_name, *deltas in transform_data:

        _change_transform(element, transform_name, *deltas)
        yield svg.toxml()


def _change_transform(element, transform_name, value_string):

    if not value_string:
        raise ValueError("'value_string' must not be empty")

    ###

    if element.hasAttribute('transform'):

        transform = element.getAttribute('transform')

        ##

        if transform_name in transform:

            new_transform = sub(
                f'({transform_name}\(.*\))',
                f'{transform_name}({value_string})',
                transform,
            )

        ##

        else:

            transform_text = f'{transform_name}({value_string})'

            if transform:
                new_transform = f'{transform} {transform_text}'

            else:
                new_transform = transform_text

    ###
    else:
        new_transform = f'{transform_name}({value_string})'

    ###
    element.setAttribute('transform', new_transform)

