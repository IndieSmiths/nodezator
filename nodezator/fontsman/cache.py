"""Facility for pygame.font.Font/SysFont objects storage/sharing.

In other words, here we obtain a cached fonts for font files or fonts
available in the system. Such fonts will render text surfaces with the
given height in pixels, or at least as close as possible without
surpassing that height.

This module provides 01 object of interest for when we want to reuse fonts.
The other objects are support objects not meant to be imported/touched in
any way.

The one you want to import is the FontsDatabase instance called FONTS_DB.

This is an example of its usage:

font = FONTS_DB[font_key][height]

The font_key can be a pathlib.Path object or a string. When the font is to
be created from a font file, you should use a pathlib.Path object pointing
to that file. When the font is to be created from a system font, that is,
a font available in your system, then you just need to provide a string
representing the name of that font.

You can get the names of all available system fonts with a call to
pygame.font.get_fonts(), which returns a list of strings representing
such names. According to pygame-ce's documentation, this works on most
systems, but not in some, in which case an empty list is returned instead.
"""

### standard library imports

from pathlib import Path

from warnings import warn


### third-party imports
from pygame.font import Font, SysFont



SPACE_CHARACTER = '\N{space}'


class FontsDatabase(dict):
    """Dict used to store maps related to font files.

    Extends the built-in dict.
    """

    def __missing__(self, font_key):
        """Create, store and return dict for given key.

        That is, the key is a string representing a path
        wherein to find a font file.

        Parameters
        ==========
        font_key (pathlib.Path or string)
            represents the path wherein to find the font (when
            a pathlib.Path is used) or the name of a font available
            in the system (when a string is used).
        """
        ### we create a font map for the key, store and return it

        font_map = FontsMap(font_key)
        self[font_key] = font_map
        return font_map


FONTS_DB = FontsDatabase()


class FontsMap(dict):
    """Map to store pygame.font.Font/SysFont instances."""

    def __init__(self, font_key):
        """Store image path.

        Parameters
        ==========
        font_key (pathlib.Path or string)
            represents the path wherein to find the font (when
            a pathlib.Path is used) or the name of a font available
            in the system (when a string is used).
        """
        self.font_key = font_key

    def __missing__(self, height):
        """Store and return font rendered w/ given height.

        Parameters
        ==========
        height (positive integer)
            represents the height in pixels of text surfaces created from
            this font.
        """
        font = get_font(self.font_key, height)
        self[height] = font
        return font


def get_font(font_key, desired_height):
    """Return font obj whose text surfs are equal or close to desired height.

    The font object will be a pygame.font.Font or SysFont instance. That is,
    a Font when font_key is a pathlib.Path instance pointing to a font file,
    or a SysFont when font_key is a string representing the name of a font
    available in the system.

    This equal or close height is achieved by trial and error, that is,
    instantiating fonts and using their 'size' method.

    This is so because each font has a different ratio between the size
    argument provided and the actual height in pixels of its rendered
    text surfaces. Such ratio even changes within the font itself depending on
    the specific size used.

    Since instantiating pygame.font.Font/SysFont and using its .size() method
    is very quick, this is fast enough as to not be noticeable.

    Furthermore, this is done only once per font and desired height, since the
    resulting font object is cached for reuse in the FontsMap object that
    makes use of this funtion.

    Coming up with a font which renders text surfaces of the exact
    desired height is not always possible.

    For instance, you cannot have a pygame.font.Font from an "ubuntu medium"
    font file with surfaces of height 36. This is so because such font, when
    instantiated with size 31, renders surfaces of height 35 and
    when instantiated with size 32 renders surfaces of height 37.

    In such case, as explained earlier, we will return the font whose surfaces
    get as close as possible to 37 in height, which is the one instantiated
    with size 31 and whose surfaces are of height 35.

    However, it must be noted that obtaining a font for a specific height
    doesn't mean all rendered text surfaces will have that height. It depends
    on the characters being rendered. For our calculations we use the height
    of a text surface rendered containing a single space character.

    Also note that we don't use pygame.font.Font.get_height() because it
    returns the average of the height of each glyph in the font. Instead, as
    explained earlier, we use the height of a text surface rendered from a
    single space character (using .size() to simulate the rendering process).
    """
    ### first of all make sure the desired height is within an acceptable
    ### range
    raise_if_unattainable(desired_height, desired_height, font_key)

    ### create a set to keep track of the attempted sizes
    attempted_sizes = set()

    ### create variable to store the chosen font
    chosen_font = None

    ### pick the font class to use based on the class of the font key
    font_class = Font if isinstance(font_key, Path) else SysFont

    ### define an initial font size (the second parameter to Font/SysFont's
    ### constructor) that takes into account the difference between the given
    ### font size and the resulting surface's height
    ###
    ### in other words, we take into account the proportion of the font size
    ### that is turned into actual height of the surface

    ## let's define a font size that is equal to the desired height
    size = desired_height

    ## calculate the height of a space character rendered with a font of this
    ## given size
    surf_height = font_class(font_key, size).size(SPACE_CHARACTER)[1]

    ## now change the size taking into account the proportion of this size
    ## that was turned into actual surface height;
    ##
    ## that is, if the surface was taller than the size (remember, this size
    ## we are using is equal to the desired height), the size will end up
    ## smaller and vice-versa; this way the size ends up closer to producing
    ## a surface height of the desired height
    size = round(size * (size / surf_height))

    ### create variable to store highest height achieved which doesn't surpass
    ### the desired height (but can be equal)
    highest_achieved = 0

    ### we'll now enter a "while loop" with 02 exit points:
    ###
    ### 1) if while trying different sizes, we come up with
    ###    one we already attempted, it means that we are
    ###    out of viable options, so we have no choice but
    ###    to exit the loop; this condition is the one
    ###    passed to the "while" statement;
    ###
    ### 2) if we find a size which produces the desired
    ###    height; this condition is inside the body of
    ###    the "while loop" (in an "if block" with a
    ###    "break" statement)

    while size not in attempted_sizes:

        ### create font and calculate the height of the
        ### surface of an arbitrary character (space) when
        ### rendered

        raise_if_unattainable(desired_height, size, font_key)

        font = font_class(font_key, size)
        surf_height = font.size(SPACE_CHARACTER)[1]

        ### store current size as an attempted one since
        ### we just tried it
        attempted_sizes.add(size)

        ### if we reached a font whose rendered surface
        ### satisfies our height requirement, we can break
        ### out of the loop after storing the surf height
        ### as the highest achieved one and the font as the
        ### chosen one

        if surf_height == desired_height:

            highest_achieved = surf_height
            chosen_font = font

            break

        ### otherwise, we come up with another value for
        ### the size by incrementing/decrementing the
        ### current one according to whether the height
        ### of the surface we obtained is lower/higher
        ### than the desired one;

        ### TODO fix: this logic used here doesn't always hold up
        ### (that is, sometimes the surf_height is so high that even
        ### reducing the font size to 0 or below won't produce a surf
        ### of height lower or equal to the desired height; and, when
        ### font size gets below 0, as expected, an error is raised
        ###
        ### must ponder what to do in this case;

        else:
            size += 1 if surf_height < desired_height else -1

        ### if the height of the text surface is higher
        ### than the ones achieved until now but still
        ### below the desired height, consider it the
        ### highest height achieved until now, and its
        ### font as the chosen one (at least for now)

        if highest_achieved < surf_height < desired_height:

            highest_achieved = surf_height
            chosen_font = font

    ### if the highest height achieved isn't the desired
    ### one, issue an warning to notify the user and return
    ### the respective font

    if highest_achieved != desired_height:

        warn(
            f"Couldn't get height {desired_height} from {font_key!r} font;"
            f" using height {highest_achieved} instead"
        )

    ### finally return the chosen font
    return chosen_font


def raise_if_unattainable(desired_height, attempted_size, font_key):
    """Detect when technical limitations of font interpolation
    will prevent creation of certain font sizes.
    """
    sizes = [desired_height, attempted_size]

    if any(map(lambda s: s < 0 or s >= 65536, sizes)):

        raise ValueError(
            f"Font of height {desired_height}"
            f" can't be achieved with {font_key!r} font"
        )
