"""Facility for visuals related node class extension."""

### standard library import
from itertools import chain


### third-party imports

from pygame import Rect

from pygame.draw import line as draw_line


### local imports

from .....surfsman.draw import blit_aligned

from ...surfs import (
    BODY_HEAD_SURFS_MAP,
    KEYWORD_KEY_SURF,
    KEYWORD_KEY_RECT,
)

from ...constants import NODE_OUTLINE_THICKNESS

from .....colorsman.colors import (
    NODE_OUTLINE,
    NODE_BODY_BG,
    COMMENTED_OUT_NODE_BG,
    NODE_LABELS,
)



def get_expanded_body_surface(self):
    """Return surface for node's body in expanded signature mode."""

    ### reference the top rectsman locally
    top_rectsman = self.top_rectsman

    ### reference the body's height locally
    body_height = self.body.rect.height

    ### create a surface for the body of the node

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

    ### define color used for node bg, depending on whether the node is
    ### commented out or not

    node_bg_color = (

        COMMENTED_OUT_NODE_BG
        if self.data.get('commented_out', False)

        else NODE_BODY_BG

    )

    ### offset for blitting surfaces onto body's surf
    offset = tuple(-coordinate for coordinate in self.body.rect.topleft)

    ### blit output name labels on the body surface

    ## retrieve names of outputs in the order they appear
    ordered_output_names = self.ordered_output_type_map.keys()

    ## reference the output text object map locally
    oto_map = self.output_text_obj_map

    ## iterate over names of output names, blitting the text surface
    ## for each name on the body surface

    for output_name in ordered_output_names:

        text_obj = oto_map[output_name]
        text_rect = text_obj.rect

        _topleft = text_rect.topleft

        text_rect.move_ip(offset)

        text_obj.draw_on_surf(body_surf)

        text_rect.topleft = _topleft


    ### iterate over the name of each parameter, blitting text surfaces
    ### representing them on the body of the node in the appropriate locations

    ## reference the parameter text object map locally
    pto_map = self.parameter_text_obj_map

    ## grab names of parameters
    parameters_names = self.signature_obj.parameters.keys()

    for param_name in parameters_names:

        text_obj = pto_map[param_name]
        text_rect = text_obj.rect

        _topleft = text_rect.topleft

        text_obj.rect.move_ip(offset)

        text_obj.draw_on_surf(body_surf)

        text_rect.topleft = _topleft


    ### outline the sides of the body surface

    ## define lines represented by pairs of points

    # calculate and store the result from subtracting
    # the outline thickness from the body width
    #
    # we'll call this the 'offset_width', and it is
    # the x coordinate from where we'll define the points
    # of the line on the right side of the node;
    #
    # this is needed because the thickness of the lines
    # are blitted from left to right and thus
    # wouldn't appear if the line were placed
    # right on top of the right side; instead, it must be
    # offset to the left by subtracting the thickness
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

    ### if there's a keyword-variable parameter in the
    ### node, blit the keyword key icon beside each
    ### keyword entry or subparameter unpacking icon
    ### for that parameter (if there's any subparameter);
    ###
    ### the motivation is purely aesthetic, but
    ### from my experience the effect improves readability,
    ### since it makes it easier to spot keyword entry
    ### widgets among other entry widgets the node might
    ### be using

    if "var_key" in self.var_kind_map.values():

        param_name = next(
            key for key, value in self.var_kind_map.items() if value == "var_key"
        )

        for obj in chain(
            self.live_keyword_entries,
            self.subparam_unpacking_icon_flmap[param_name].values(),
        ):

            ## obtain the midleft coordinates of the
            ## object (a bit offset to left), but
            ## changed so that it is relative to the origin
            ## of the body surface

            x, y = (
                # get object's rect
                obj.rect
                # get new rect moved a bit to the left
                .move(-2, 0)
                # and yet another one moved from there so its
                # position is relative to the origin of the
                # body surface
                .move(offset)
                # then grab its midleft coordinates
                .midleft
            )

            ## assign the midleft coordinates calculated
            ## to the midright coordinates of
            ## the keyword key's rect, then blit it in that
            ## position

            KEYWORD_KEY_RECT.midright = x, y

            body_surf.blit(
                KEYWORD_KEY_SURF,
                KEYWORD_KEY_RECT,
            )

    ### finally return the body surface
    return body_surf
