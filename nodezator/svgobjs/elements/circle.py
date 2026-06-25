
### local imports
from ._common import REFS, Shape



class Circle(Shape):
    """Represents a <circle> tag."""

    tag_name = 'circle'

    ### relevant attribute names for tag

    attr_names = (
        'r',
        'cx',
        'cy',
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
    r = cx = cy = 0


REFS.Circle = Circle
