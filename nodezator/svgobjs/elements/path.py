
### local imports
from ._common import REFS, Shape



class Path(Shape):
    """Represents a <path> tag."""

    tag_name = 'path'

    ### relevant attribute names for tag

    attr_names = (
        'd',
        'fill',
        'stroke',
        'stroke_width',
        'opacity',
        'fill_opacity',
        'stroke_opacity',
        'transform',
        'id',
    )


REFS.Path = Path
