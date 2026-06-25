
### local imports
from ._common import REFS, Shape



class Polygon(Shape):
    """Represents a <polygon> tag."""

    tag_name = 'polygon'

    ### relevant attribute names for <polygon> tag

    attr_names = (
        'points',
        'fill',
        'stroke',
        'stroke_width',
        'opacity',
        'fill_opacity',
        'stroke_opacity',
        'transform',
        'id',
    )


REFS.Polygon = Polygon
