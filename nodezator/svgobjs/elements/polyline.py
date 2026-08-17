
### local imports
from ._common import REFS, Shape



class PolyLine(Shape):
    """Represents a <polyline> tag."""

    tag_name = 'polyline'

    ### relevant attribute names for tag

    attr_names = (
        'points',
        'stroke',
        'stroke_width',
        'opacity',
        'stroke_opacity',
        'transform',
        'id',
    )


REFS.PolyLine = PolyLine
