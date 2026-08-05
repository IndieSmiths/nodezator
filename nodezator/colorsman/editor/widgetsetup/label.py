"""Label creation for the colors editor class."""

### local imports

from ....textman.render import render_text

from ....surfsman.render import combine_surfaces
from ....surfsman.icon import render_layered_icon

from ....classes2d.single import Object2D
from ....classes2d.collections import List2D

from ...colors import BLACK, WINDOW_BG, WINDOW_FG

from .constants import FONT_HEIGHT, TEXT_PADDING



def setup_labels(self):
    """Create and set up labels.

    Function meant to be injected in the ColorsEditor
    class. Handles the creation of labels.
    """

    ### gather text for labels

    labels_texts = (

        ## color properties/representations

        "Hue",
        "Lightness",
        "Saturation",
        "Value",
        "Red",
        "Green",
        "Blue",
        "Hex",
        "HTML name",
        "pygame name",
        "Alpha",

        ## others

        "Current colors:",
        "More:",

    )

    ### iterate over label text data, building a custom list while you
    ### instantiate the labels

    self.labels = (

        List2D(

            Object2D.from_surface(

                surface=render_text(

                    text=text,
                    font_height=FONT_HEIGHT,
                    padding=TEXT_PADDING,
                    foreground_color=WINDOW_FG,
                    background_color=WINDOW_BG,

                ),

                name=text,

            )

            for text in labels_texts

        )

    )

    ### create and store a special label to use as the title for the
    ### colors editor widget

    ## load/render surfaces;
    ##
    ## note that we don't use padding for the text, cause we'll blit it onto
    ## a new surface ahead and that surface has enough space;

    icon_surf = (

        render_layered_icon(
            chars=[chr(ordinal) for ordinal in range(106, 113)],
            dimension_name="height",
            dimension_value=30,
            colors=[
                BLACK,
                *(
                    (r, g, b)
                    for r in (0, 255)
                    for g in (0, 255)
                    for b in (0, 255)
                    if sum((r, g, b))
                ),
            ],
            background_width=32,
            background_height=32,
        )

    )

    text_surf = (

        render_text(
            text="Colors editor",
            font_height=FONT_HEIGHT,
            foreground_color=WINDOW_FG,
            background_color=WINDOW_BG,
        )

    )

    ## combine surfs into a single one in a new object

    self.title_obj = (

        Object2D.from_surface(

            combine_surfaces(
                surfaces=[icon_surf, text_surf],
                retrieve_pos_from='midright',
                assign_pos_to='midleft',
                offset_pos_by=(0, 0),
                padding=0,
                background_color=WINDOW_BG,
            )

        )

    )

    ## finally, store the title object as a label
    self.labels.append(self.title_obj)
