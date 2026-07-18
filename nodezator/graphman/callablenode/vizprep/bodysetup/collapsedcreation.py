"""Facility for visuals related node class extension."""

### standard library import
from itertools import chain


### third-party imports

from pygame import Rect

from pygame.draw import line as draw_line


### local imports

from .....config import APP_REFS

from .....surfsman.draw import blit_aligned
from .....surfsman.render import render_rect

from .....textman.render import render_text

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



def get_collapsed_body_surface(self):
    """Return surface for node's body in collapsed signature mode."""
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

        'midtop',  ## retrieve pos from this
        'midtop',  ## assign pos to this

    )

    ### offset for blitting surfaces onto body's surf
    offset = tuple(-coordinate for coordinate in self.body.rect.topleft)

    ### reference list of visible output sockets locally
    vos = self.visible_output_sockets

    ### blit labels on the body surface, beside each output
    ### socket so the name of each output socket is visible
    ### on the node

    ## retrieve names of outputs in the order they appear
    ordered_output_names = self.ordered_output_type_map.keys()

    ## reference map from where to retrive output sockets
    osl_map = self.output_socket_live_map

    ## reference the output text object map locally
    oto_map = self.output_text_obj_map

    ## iterate over names of outputs, blitting the text surface for each name
    ## on the body surface

    for output_name in ordered_output_names:
        
        ## skip if respective socket is not visible

        if osl_map[output_name] not in vos:
            continue

        ## draw

        text_obj = oto_map[output_name]
        text_rect = text_obj.rect

        _topleft = text_rect.topleft

        text_rect.move_ip(offset)

        text_obj.draw_on_surf(body_surf)

        text_rect.topleft = _topleft


    ### iterate over the name of each parameter, blitting text surfaces
    ### representing them on the body of the node in the appropriate locations

    ## reference input socket map locally for easier/quick access
    isl_flmap = self.input_socket_live_flmap

    ## reference unpacking icon map locally
    sui_flmap = self.subparam_unpacking_icon_flmap

    ## reference list of visible output sockets locally
    vis = self.visible_input_sockets

    ## reference the parameter text object map locally
    pto_map = self.parameter_text_obj_map

    parameters_names = self.signature_obj.parameters.keys()

    for param_name in parameters_names:

        ### retrieve the rectsman of the parameter
        param_rectsman = self.param_rectsman_map[param_name]


        ### for each parameter with visible input socket(s),
        ### temporarily position text object relative to node's body
        ### and draw it;
        ###
        ### in the case of subparameters, also draw the unpacking icon if/where
        ### needed;

        ## try retrieving the variable kind of the parameter
        try:
            var_kind = self.var_kind_map[param_name]

        ## if a KeyError is raised, then we have a regular
        ## parameter here...

        except KeyError:

            ## skip this parameter if it's input socket is not visible

            if isl_flmap[param_name] not in vis:
                continue

            ## draw

            text_obj = pto_map[param_name]
            text_rect = text_obj.rect

            _topleft = text_rect.topleft

            text_rect.move_ip(offset)

            text_obj.draw_on_surf(body_surf)

            text_rect.topleft = _topleft


        ## otherwise, we have a parameter of variable kind
        ## here...

        else:

            ## retrieve the names of the subparameters sorted

            sorted_subparam_indices = (
                sorted(self.input_socket_live_flmap[param_name])
            )

            ## skip parameter if it has no subparameters

            if not sorted_subparam_indices:
                continue

            ## skip this parameter if none of its input sockets are visible

            for input_socket in isl_flmap[param_name].values():

                if input_socket in vis:
                    break

            else:
                continue

            ## draw text object

            text_obj = pto_map[param_name]
            text_rect = text_obj.rect

            _topleft = text_rect.topleft

            text_rect.move_ip(offset)

            text_obj.draw_on_surf(body_surf)

            text_rect.topleft = _topleft

            ## if the subparameter for the visible socket is marked
            ## for unpacking, draw the unpacking icon beside the socket

#            for subparam_index in sorted_subparam_indices:
#
#                socket = isl_flmap[param_name][subparam_index]
#
#                if socket not in vis:
#                    continue
#
#                unpacking_icon = sui_flmap[param_name].get(subparam_index)
#
#                if not unpacking_icon:
#                    continue
#
#                icon_rect = unpacking_icon.rect
#
#                _topleft = icon_rect.topleft
#
#                icon_rect.move_ip(offset)
#
#                unpacking_icon.draw_on_surf(body_surf)
#
#                icon_rect.topleft = _topleft


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

    ### if there's a keyword-variable parameter in the node, only for the
    ### subparameters whose input socket are visible, blit the keyword key icon
    ### beside each keyword entry or subparameter unpacking icon for that
    ### parameter (if there's any subparameter);
    ###
    ### the motivation is purely aesthetic, but from my experience the effect
    ### improves readability, since it makes it easier to spot keyword entry
    ### widgets at a glance

    if 'var_key' in self.var_kind_map.values():

        param_name = next(

            key

            for key, value in self.var_kind_map.items()
            if value == 'var_key'

        )

        subparam_input_sockets_map = isl_flmap[param_name]

        for subparam_index, obj in chain(
            self.subparam_keyword_entry_live_map.items(),
            self.subparam_unpacking_icon_flmap[param_name].items(),
        ):

            if subparam_input_sockets_map[subparam_index] not in vis:
                continue

            ## obtain the midleft coordinates of the object
            ## (a bit offset to left), but changed so that it is relative
            ## to the origin of the body surface

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

            ## assign the midleft coordinates calculated to the midright
            ## coordinates of the keyword key's rect, then blit it in that
            ## position

            KEYWORD_KEY_RECT.midright = x, y

            body_surf.blit(
                KEYWORD_KEY_SURF,
                KEYWORD_KEY_RECT,
            )


    ### finally return the body surface
    return body_surf
