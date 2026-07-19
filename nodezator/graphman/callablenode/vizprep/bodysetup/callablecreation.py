"""Facility for visuals related node class extension."""

### third-party import
from pygame.draw import line as draw_line


### local imports

from .....surfsman.draw import blit_aligned

from .....colorsman.colors import NODE_OUTLINE

from ...surfs import BODY_HEAD_SURFS_MAP

from ...constants import NODE_OUTLINE_THICKNESS



def get_callable_body_surface(self):
    """Return surface for node's body in callable mode."""

    ### reference the top rectsman locally
    top_rectsman = self.top_rectsman

    ### reference the body's height locally
    body_height = self.body.rect.height

    ### reference surface for the body of the node
    body_surf = self.body.image

    ### obtain body head surf from corresponding map

    BODY_HEAD_SURF = (

        BODY_HEAD_SURFS_MAP[

            (
                top_rectsman.width,
                self.title_text_obj.rect.height - top_rectsman.height + 3,
                self.category_color,
            )

        ]

    )

    ### blit the body head surface in the top of the
    ### body surface; such head surface has a color equal
    ### to that of the top of the node, so it makes the top
    ### part of the body appear as if merged with its top

    blit_aligned(

        ## surface to blit
        BODY_HEAD_SURF,

        ## target surface
        body_surf,

        'topleft',  ## retrieve pos from this
        'topleft',  ## assign pos to this

    )


    ### outline the sides of the body surface

    ## define lines represented by pairs of points

    # calculate and store the result from subtracting the outline thickness
    # from the body width
    #
    # we'll call this the 'offset_width', and it is the x coordinate from where
    # we'll define the points of the line on the right side of the node;
    #
    # this is needed because the thickness of the lines are blitted from left
    # to right and thus wouldn't appear if the line were placed right on top of
    # the right side; instead, it must be offset to the left by subtracting the
    # thickness
    offset_width = self.body.rect.width - NODE_OUTLINE_THICKNESS

    # defining lines

    lines = (

        # line on left side
        ((0, 0), (0, body_height)),

        # line on right side
        ((offset_width, 0), (offset_width, body_height)),

    )

    # drawing lines

    for point_a, point_b in lines:

        draw_line(
            body_surf,
            NODE_OUTLINE,
            point_a,
            point_b,
            NODE_OUTLINE_THICKNESS,
        )

    ### separate body head from rest of the body by drawing
    ### a horizontal line between those areas

    line_y = BODY_HEAD_SURF.get_height()

    draw_line(

        body_surf,

        # line color
        NODE_OUTLINE,

        # line start, end
        (0, line_y),
        (body_surf.get_width(), line_y),

        # width
        2,

    )


    ### finally return the body surface
    return body_surf
