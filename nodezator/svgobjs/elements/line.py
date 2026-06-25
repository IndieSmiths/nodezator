
### local imports
from ._common import REFS, Shape



class Line(Shape):
    """Represents a <line> tag."""

    tag_name = 'line'

    ### relevant attribute names for tag

    attr_names = (
        'x1',
        'y1',
        'x2',
        'y2',
        'stroke',
        'stroke_width',
        'opacity',
        'stroke_opacity',
        'transform',
        'id',
    )

    ### default values for some of those attributes
    x1 = y1 = x2 = y2 = 0


REFS.Line = Line
