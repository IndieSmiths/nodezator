
### local imports
from ._common import REFS, Shape



class Rect(Shape):
    """Represents a <rect> tag."""

    tag_name = 'rect'

    ### relevant attribute names for tag

    attr_names = (
        'x',
        'y',
        'width',
        'height',
        'fill',
        'stroke',
        'stroke_width',
        'opacity',
        'fill_opacity',
        'stroke_opacity',
        'transform',
        'id',
    )

    ### default values for some of those attributes
    x = y = width = height = 0


REFS.Rect = Rect
