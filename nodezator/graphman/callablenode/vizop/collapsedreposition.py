"""Function to extend VisualRelatedOperations class."""

### local imports

from ....rectsman.main import RectsManager

from ....surfsman.render import render_rect

from ....colorsman.colors import NODE_BODY_BG, COMMENTED_OUT_NODE_BG

from ...socket.surfs import SOCKET_DIAMETER

from ..constants import (
    BODY_CONTENT_OFFSET,
    NODE_OUTLINE_THICKNESS,
    SUBPARAM_OFFSET_FROM_LABEL,
    DISTANCE_BETWEEN_PARAMS,
    DISTANCE_BETWEEN_SUBPARAMS,
    DISTANCE_BETWEEN_OUTPUTS,
    INPUT_OFFSET,
)

from ..surfs import (
    CORNER_WIDTH,
    NODE_ROOFS_MAP,
    NODE_FOOTS_MAP,
)



SOCKET_RADIUS = SOCKET_DIAMETER // 2


def reposition_collapsed_elements(self):
    """Reposition objects inside the node in collapsed signature mode.

    The repositioning is made from the input
    downwards (the top rects manager doesn't need to be
    repositioned, it always stays at the same relative
    position within the node).

    Another administrative task is performed, which is
    updating the height of self.rect.
    """
    ### determine which paramaters/subparameters/outputs will
    ### be shown after hiding unconnected ones
    self.collapse_unconnected_elements()

    ### create a temporary rects manager with its list of rects

    temp_rect_list = []
    temp_rectsman = RectsManager(temp_rect_list.__iter__)

    ### position all visible output elements relative to each other

    ## reference list of visible output sockets
    vos = self.visible_output_sockets

    ## reference the output text object map locally
    oto_map = self.output_text_obj_map

    ## extra setups if there are visible output sockets

    if vos:

        ## reference the last visible output socket, if any
        last_output_socket = vos[-1]

        ## create a collection to hold output related rects and the
        ## respective rects manager

        output_rects = []
        temp_output_rectsman = RectsManager(output_rects.__iter__)

    ## iterate over visible output sockets, positioning socket's and the their
    ## respective text relative to each other

    top = 0

    for output_socket in vos:

        ## retrieve socket and text object rects

        osocket_rect = output_socket.rect
        text_rect = oto_map[output_socket.output_name].rect

        ## align text midright with socket's midleft, with a bit of horizontal
        ## padding
        text_rect.midright = osocket_rect.move(-2, 0).midleft

        ## position text rect and socket rect together as if they were a
        ## single rect by controlling them through a temporary rects manager
        ## instance

        # populate temp rect list
        temp_rect_list.extend((text_rect, osocket_rect))

        # position rects manager's top
        temp_rectsman.top = top

        # position rects manager so socket centerx ends up at 0

        xdiff = osocket_rect.centerx - 0
        temp_rectsman.move_ip(xdiff, 0)

        ## add the socket and text object rects as output rects

        output_rects.append(osocket_rect)
        output_rects.append(text_rect)

        ## define next top as the bottom of the temp rects manager and,
        ## if this is not the last output, also add the constant distance
        ## between outputs

        top = temp_rectsman.bottom + (

            DISTANCE_BETWEEN_OUTPUTS
            if output_name != last_output_name

            else 0

        )

        # clear temp rect list
        temp_rect_list.clear()


    ### position visible parameters

    ## reference list of visible input sockets locally
    vis = self.visible_input_sockets

    ## reference map with input sockets locally
    isl_flmap = self.input_socket_live_flmap

    ## reference map of subparam unpacking icons locally
    sui_flmap = self.subparam_unpacking_icon_flmap

    ## reference map of subparam keyword entries
    skel_map = self.subparam_keyword_entry_live_map

    ## reference subparameter unpacking map locally
    subparam_unpacking_map = self.data["subparam_unpacking_map"]

    ## reference the parameter text object map locally
    pto_map = self.parameter_text_obj_map


    ## restart top
    top = 0

    ## retrieve parameter objects (they're ordered)
    parameters = self.signature_obj.parameters.values()

    ## extra setups if there are visible input sockets

    if vis:

        ## store a reference to the last one
        last_input_socket = vis[-1]

        ## create a collection to hold input related rects and the
        ## respective rects manager

        input_rects = []
        temp_input_rectsman = RectsManager(input_rects.__iter__)

    ## iterate over parameter objects positioning each
    ## of them

    for param_obj in parameters:

        ## retrieve name of parameter
        param_name = param_obj.name

        ## try retrieving the variable kind of the parameter

        try:
            kind = self.var_kind_map[param_name]

        ## if the retrieval fails, then we have a regular parameter

        except KeyError:

            ##
            input_socket = isl_flmap[param_name]

            ## skip if parameter isn't visible

            if input_socket not in vis:
                continue

            ## we have only the input socket, so we align the vertical center
            ## of both the text rect and input socket (with just a bit offset)
            ## and perform the calculation as if they were a single object by
            ## appending the text rect to the list of rects managed by the
            ## temporary rects manager

            # obtain text and socket rects

            text_rect = pto_map[param_name].rect
            isocket_rect = input_socket.rect

            # socket rect's centerx must be 0
            isocket_rect.centerx = 0

            # align text midleft with socket's midright, with a bit of
            # horizontal padding
            text_rect.midleft = isocket_rect.move(2, 0).midright

            # position object as one, with help from temporary rects manager

            temp_rect_list.extend((isocket_rect, text_rect))

            temp_rectsman.top = top

            top = temp_rectsman.bottom

            temp_rect_list.clear()

            ## add the socket and text object rects as input rects

            input_rects.append(isocket_rect)
            input_rects.append(text_rect)


        ## otherwise, we are dealing with a variable parameter

        else:

            ## retrieve the names of the subparameters sorted
            sorted_subparam_indices = sorted(isl_flmap[param_name])

            ## if there are indeed subparameters, store a reference to the
            ## input socket of the last visible subparameter (if there is one)

            if sorted_subparam_indices:

                for subparam_index in reversed(sorted_subparam_indices):

                    input_socket = isl_flmap[param_name][subparam_index]

                    if input_socket in vis:

                        last_subparam_input_socket = input_socket
                        break

                else:
                    last_subparam_input_socket = False

            ## if there aren't any subparameters, the whole parameter isn't
            ## visible anyway, so we skip it

            else:
                continue

            ## if there were subparameters but we didn't managed to find a
            ## visible one to assign as the last visible subparameters,
            ## it meas none of the subparameters are visible, so we also
            ## skip the parameter

            if not last_subparam_input_socket:
                continue

            ## variable parameters always start with the name of the parameter
            ## on top, so we begin by positioning the text rect at the top

            # reference the associated text object's rect

            text_rect = pto_map[param_name].rect
            text_rect.top = top

            ## add the text object rect as an input rect
            input_rects.append(text_rect)

            ## the top for the next object will be below the text rect plus
            ## an offset given as a constant
            top = text_rect.bottom + SUBPARAM_OFFSET_FROM_LABEL

            ## retrieve the list of unpacked subparameter indices
            subparams_for_unpacking = subparam_unpacking_map[param_name]

            ## iterate over each subparameter index in order, repositioning
            ## each visible subparameter as you go

            for subparam_index in sorted_subparam_indices:

                ## check whether the input socket is visible

                input_socket = isl_flmap[param_name][subparam_index]

                if input_socket not in vis:
                    continue

                ## reference input socket's rect
                isocket_rect = input_socket.rect

                ## its centerx must be 0
                isocket_rect.centerx = 0

                ## add the input socket's rect as an input rect
                input_rects.append(isocket_rect)

                # TODO replace hardcoded 18 by key icon's width

                # if subparameter is unpacked...

                if subparam_index in subparams_for_unpacking:

                    unpacking_icon = sui_flmap[param_name][subparam_index]

                    unpacking_icon.rect.midleft = (
                        input_socket.rect.move(2, 0).midright
                        if kind == 'var_pos'
                        else input_socket.rect.move(18, 0).midright
                    )

                    temp_rect_list.append(input_socket.rect)
                    temp_rect_list.append(unpacking_icon.rect)

                    temp_rectsman.top = top

                    top = temp_rectsman.bottom

                    temp_rect_list.clear()

                    ## add the unpacking_icon rect as an input rect
                    input_rects.append(unpacking_icon.rect)

                # if it is of keyword-variable kind...

                elif kind == 'var_key':

                    keyword_entry = skel_map[subparam_index]

                    keyword_entry.rect.midleft = (
                        input_socket.rect.move(18, 0).midright
                    )

                    temp_rect_list.append(input_socket.rect)
                    temp_rect_list.append(keyword_entry.rect)

                    temp_rectsman.top = top

                    top = temp_rectsman.bottom

                    temp_rect_list.clear()

                    ## add the keyword entry's rect as an input rect
                    input_rects.append(keyword_entry.rect)

                # otherwise...

                else:

                    # assign top
                    input_socket.rect.top = top

                    # define new top
                    top = input_socket.rect.bottom


                # if the subparameter isn't the last one, increment the top
                # with the distance between subparameters given as a constant

                if subparam_index != last_subparam_input_socket.subparameter_index:
                    top += DISTANCE_BETWEEN_SUBPARAMS


        ## if the parameter being positioned isn't the last one,
        ## increment the top with the distance between parameters
        ## given as a constant

        if param_name != last_input_socket.parameter_name:
            top += DISTANCE_BETWEEN_PARAMS


    ###
    midtop = self.rect.midtop if self.rect else self.midtop

    ### now that the visible input and output elements (if any) are properly
    ### positioned relative to themselves that, we can finally:
    ###
    ### - position all visible elements relative to each other
    ### - generate missing visuals whose size depend on resulting positions

    (
        topleft_corner_rect,
        topright_corner_rect,
        bottomleft_corner_rect,
        bottomright_corner_rect,

    ) = (

        corner.rect
        for corner in self.corners

    )

    topleft_corner_rect.top = topright_corner_rect.top = midtop[1]

    title_rect = self.title_text_obj.rect
    title_rect.midtop = midtop
    title_rect.move_ip(0, 2)

    topleft_corner_rect.right = title_rect.left - 20
    topright_corner_rect.left = title_rect.right + 20

    top_width = title_rect.width + (CORNER_WIDTH*2) + 40

    if vos and vis:

        irectsman = temp_input_rectsman
        orectsman = temp_output_rectsman

        orectsman.right = irectsman.right + SOCKET_DIAMETER

        ### add padding if too similar in width

        if abs(irectsman.width - orectsman.width) < 20:
            orectsman.right += 20

        ###

        temp_rect_list.extend((irectsman, orectsman))

        if temp_rectsman.width > top_width:

            temp_rectsman.centerx = title_rect.centerx 

            topleft_corner_rect.left = irectsman.left + SOCKET_RADIUS
            topright_corner_rect.right = orectsman.right - SOCKET_RADIUS

        else:

            irectsman.left = topleft_corner_rect.left - SOCKET_RADIUS
            orectsman.right = topright_corner_rect.right + SOCKET_RADIUS

    elif vos:

        orectsman = temp_output_rectsman

        if orectsman.width > top_width:

            orectsman.centerx = title_rect.centerx

            topleft_corner_rect.left = orectsman.left - 5
            topright_corner_rect.right = orectsman.right - SOCKET_RADIUS

        else:
            orectsman.right = topright_corner_rect.right - SOCKET_RADIUS

    elif vis:

        irectsman = temp_input_rectsman

        if irectsman.width > top_width:

            irectsman.centerx = title_rect.centerx

            topleft_corner_rect.left = irectsman.left - 5
            topright_corner_rect.right = irectsman.right - SOCKET_RADIUS

        else:
            irectsman.right = topright_corner_rect.right - SOCKET_RADIUS


    ###

    roof = self.roof

    roof_width = topright_corner_rect.left - topleft_corner_rect.right

    roof.image = NODE_ROOFS_MAP[(roof_width, self.category_color)]

    roof.rect.size = roof.image.get_size()
    roof.rect.midtop = midtop

    ###

    self.sigmode_toggle_button.rect.topleft = (
        topleft_corner_rect.move(-1, -1).bottomright
    )

    ###

    top_rectsman = self.top_rectsman

    top = top_rectsman.bottom + BODY_CONTENT_OFFSET

    ### assign and redefine top

    if vos:

        orectsman.top = top

        if vis:

            irectsman.top = orectsman.bottom + INPUT_OFFSET
            top = irectsman.bottom

        else:
            top = orectsman.bottom

    ###

    ## reference the rect of the id text object locally
    id_text_rect = self.id_text_obj.rect

    ## align its centerx with title rect's centerx
    id_text_rect.centerx = title_rect.centerx

    ## align its top with the last defined top; also push it
    ## 4 pixels down for extra padding
    id_text_rect.top = top + 4

    ###
    top = id_text_rect.bottom - 2

    ### position bottom corners

    bottomleft_corner_rect.top = bottomright_corner_rect.top = top

    bottomleft_corner_rect.left = topleft_corner_rect.left
    bottomright_corner_rect.right = topright_corner_rect.right

    ##

    bg_color = (

        COMMENTED_OUT_NODE_BG
        if self.data.get('commented_out', False)

        else NODE_BODY_BG

    )

    ## generate visual for foot and position it

    foot = self.foot
    foot_rect = foot.rect

    foot_width = roof_width

    foot.image = NODE_FOOTS_MAP[(foot_width, bg_color)]

    foot_rect.size = foot.image.get_size()

    foot_rect.top = top
    foot_rect.left = bottomleft_corner_rect.right

    ###
    bottom_rectsman = self.bottom_rectsman

    ### perform extra administrative task: generate body surface and
    ### update its rect

    body = self.body

    body_rect = body.rect

    body_rect.width = top_rectsman.width
    body_rect.height = bottom_rectsman.top - top_rectsman.bottom

    body_rect.midtop = top_rectsman.midbottom

    body.image = render_rect(*body_rect.size, bg_color)

    ### perform extra administrative task: update size and position
    ### of self.rect

    ## width

    left = (

        ## if there are visible parameters (input sockets)...
        irectsman.left
        if vis

        ## otherwise...
        else top_rectsman.left - SOCKET_RADIUS

    )

    right = (

        ## if there are visible outputs (output sockets)...
        orectsman.right
        if vos

        ## otherwise...
        else top_rectsman.right + SOCKET_RADIUS

    )

    self.rect.width = right - left

    ## height
    self.rect.height = bottom_rectsman.bottom - top_rectsman.top

    ## midtop
    self.rect.midtop = top_rectsman.midtop
