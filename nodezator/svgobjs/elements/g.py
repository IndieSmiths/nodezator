
### local imports
from ._common import REFS, ContainerElement



class G(ContainerElement):
    """Represents a <g> tag."""

    tag_name = 'g'

    ### relevant attribute names for <g> tag

    attr_names = (
        'fill',
        'stroke',
        'stroke_width',
        'transform',
        'id',
    )


REFS.G = G
