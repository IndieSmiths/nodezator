
### local imports
from ._common import REFS, Shape



class Ellipse(Shape):
    """Represents an <ellipse> tag."""

    tag_name = 'ellipse'

    ### relevant attribute names for tag

    attr_names = (
        'rx',
        'ry',
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
    rx = ry = cx = cy = 0


REFS.Ellipse = Ellipse
