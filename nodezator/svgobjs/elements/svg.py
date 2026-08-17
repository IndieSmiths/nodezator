
### local imports
from ._common import REFS, ContainerElement



class SVG(ContainerElement):
    """Represents an <svg> tag."""

    tag_name = 'svg'

    ### relevant attribute names for tag

    attr_names = (
        'xmlns',
        'width',
        'height',
        'viewBox',
    )

    ### default values for some of those attributes

    xmlns = 'http://www.w3.org/2000/svg'


REFS.SVG = SVG
