"""Function to extend VisualRelatedOperations class."""

### local imports

from ....config import APP_REFS

from ....rectsman.main import RectsManager

from ....surfsman.render import render_rect

from ....colorsman.colors import NODE_BODY_BG, COMMENTED_OUT_NODE_BG

from ...socket.surfs import SOCKET_DIAMETER

from ..constants import (
    BODY_CONTENT_OFFSET,
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


def reposition_expanded_elements(self):
    """Reposition objects inside the node in expanded signature mode."""

    ### position all output elements relative to each other

    ## get names of outputs (their order is defined
    ## in the node script)
    output_names = self.ordered_output_type_map.keys()

    ## get name of last output
    last_output_name = list(output_names)[-1]

    ## reference the output socket and output text object maps locally

    osl_map = self.output_socket_live_map
    oto_map = self.output_text_obj_map

    ## iterate over output names, positioning socket's and the their respective
    ## text relative to each other

    top = 0

    for output_name in output_names:
        
        ## retrieve socket and text object rects

        osocket_rect = osl_map[output_name].rect
        text_rect = oto_map[output_name].rect

        ## place socket's horizontal center at 0
        osocket_rect.centerx = 0

        ## align text midright with socket's midleft, with a bit of horizontal
        ## padding
        text_rect.midright = osocket_rect.move(-2, 0).midleft

        ## position text rect and socket rect together as if they were a
        ## single rect by controlling them through a temporary rects manager
        ## instance

        # instantiate temporary rectsman
        _temp_rectsman = RectsManager((text_rect, osocket_rect).__iter__)

        # position rectsman's top
        _temp_rectsman.top = top

        ## define next top as the bottom of the temp rectsman and,
        ## if this is not the last output, also add the constant distance
        ## between outputs

        top = _temp_rectsman.bottom + (

            DISTANCE_BETWEEN_OUTPUTS
            if output_name != last_output_name

            else 0

        )


    ### position all input elements relative to each other

    top = 0

    ## retrieve parameter objects (they're ordered)
    parameters = self.signature_obj.parameters.values()

    ## if there are parameters, store the name of the last one
    ## for future reference

    if parameters:
        last_param_name = list(parameters)[-1].name

    ## reference subparameter unpacking map locally
    subparam_unpacking_map = self.data['subparam_unpacking_map']

    ## let's also reference maps of live instances locally using
    ## variables of low character count, for better code layout

    sub_flmap = self.subparam_up_button_flmap
    sdb_flmap = self.subparam_down_button_flmap
    wl_flmap = self.widget_live_flmap
    sui_flmap = self.subparam_unpacking_icon_flmap
    skl_map = self.subparam_keyword_entry_live_map
    wrb_flmap = self.widget_remove_button_flmap
    pab_map = self.placeholder_add_button_map
    psl_map = self.placeholder_socket_live_map
    prm_map = self.param_rectsman_map
    srm_map = self.subparam_rectsman_map

    isl_flmap = self.input_socket_live_flmap
    pto_map = self.parameter_text_obj_map

    ## reference the lists of visible widgets and remove buttons locally
    ## and clear them

    vws = self.visible_widgets
    vbs = self.visible_remove_widget_buttons

    vws.clear()
    vbs.clear()

    ## iterate over parameter objects positioning each of them

    for param_obj in parameters:

        ## retrieve name of parameter
        param_name = param_obj.name

        ## retrieve the rectsman representing the parameter,
        ## as well as the list of the underlying rects it controls

        param_rectsman = prm_map[param_name]
        param_rects = param_rectsman._get_all_rects.__self__

        ## clear the list
        param_rects.clear()

        ## reference the associated text object's rect
        text_rect = pto_map[param_name].rect

        ## try retrieving the variable kind of the parameter
        try:
            kind = self.var_kind_map[param_name]

        ## if the retrieval fails, then we have a regular parameter

        except KeyError:

            ## reference the input socket and its rect

            input_socket = isl_flmap[param_name]
            isocket_rect = input_socket.rect

            ## socket rect's centerx must be 0
            isocket_rect.centerx = 0

            ## store the input socket's rect as a
            ## parameter's rect
            param_rects.append(isocket_rect)

            ## check whether input socket has a parent

            has_parent = (

                (self.id, param_name) in APP_REFS.gm.parented_sockets_ids
                if hasattr(APP_REFS.gm, 'parented_sockets_ids')

                else hasattr(input_socket, 'parent')

            )

            ## check wheter it has a widget
            has_widget = param_name in wl_flmap

            ## if it has a parent or doesn't have a widget, it means we only
            ## the input socket and the text object in the parameter;
            ##
            ## we align the vertical center of both the text rect
            ## and input socket (with just a bit offset) and perform
            ## the calculation as if they were a single object by
            ## temporarily appending the text rect to the list of
            ## rects managed by the rectsman

            if has_parent or not has_widget:

                ## align text midleft with socket's midright, with a bit of
                ## horizontal padding
                text_rect.midleft = isocket_rect.move(2, 0).midright

                ## add text object's rect and position objects as one

                param_rects.append(text_rect)

                param_rectsman.top = top

                top = param_rectsman.bottom

            ## otherwise, if we have a widget, we perform related setups

            elif has_widget:

                ## reference widget locally
                widget = wl_flmap[param_name]

                ## position it and store it as a visible one

                widget.rect.topleft = isocket_rect.move(8, -1).topright
                vws.append(widget)

                ## store its rect among the parameter's rects
                param_rects.append(widget.rect)

                ## since the widget is beside the socket, the parameter text
                ## will be above the input socket and visible widget

                text_rect.top = top

                param_rectsman.top = text_rect.bottom + 2

                top = param_rectsman.bottom

                ## align text's left with input socket's right
                text_rect.left = isocket_rect.move(2, 0).right

                ## add text object's rect
                param_rects.append(text_rect)

        ## otherwise, we are dealing with a variable parameter

        else:

            ## variable parameters always start with the name of the parameter
            ## on top, so we begin by positioning the text rect on top
            text_rect.top = top

            ##
            param_rects.append(text_rect)

            ## the top for the next object will be below the text rect plus a
            ## constant offset
            top = text_rect.bottom + SUBPARAM_OFFSET_FROM_LABEL

            ## we then retrieve the names of the subparameters sorted
            sorted_subparam_indices = sorted(isl_flmap[param_name])

            ## if there are indeed subparameters, store the name of
            ## the last one (we'll use it soon)

            if sorted_subparam_indices:
                last_subparam_index = sorted_subparam_indices[-1]

            ## retrieve the list of unpacked subparameter indices
            subparams_for_unpacking = subparam_unpacking_map[param_name]

            ## iterate over each subparameter index in order,
            ## repositioning each subparameter as you go

            for subparam_index in sorted_subparam_indices:

                # retrieve rectsman for the subparameter and its list
                # of rects

                subparam_rectsman = srm_map[param_name][subparam_index]
                subparam_rects = subparam_rectsman._get_all_rects.__self__

                # clear the list
                subparam_rects.clear()

                # reference input socket and its rect

                input_socket = isl_flmap[param_name][subparam_index]
                isocket_rect = input_socket.rect

                ## its centerx must be 0
                isocket_rect.centerx = 0

                ## store the input socket's rect as a subparameter's rect
                subparam_rects.append(isocket_rect)

                ## retrieve rects of buttons to move the subparameter,
                ## position them and store their rects as subparameter's rects

                up_button_rect = sub_flmap[param_name][subparam_index].rect
                down_button_rect = sdb_flmap[param_name][subparam_index].rect

                offset_midright = isocket_rect.move(2, 0).midright

                up_button_rect.bottomleft = offset_midright
                down_button_rect.topleft = offset_midright

                subparam_rects.append(up_button_rect)
                subparam_rects.append(down_button_rect)

                ## check whether the subparameter has a parent

                has_parent = (

                    (
                        (self.id, param_name, subparam_index)
                        in APP_REFS.gm.parented_sockets_ids
                    )
                    if hasattr(APP_REFS.gm, 'parented_sockets_ids')

                    else hasattr(input_socket, 'parent')

                )

                ## check whether the subparameter is unpacked
                is_unpacked = subparam_index in subparams_for_unpacking

                ## if the subparameter is unpacked, retrieve the
                ## unpacking icon rect

                if is_unpacked:
                    unpacking_icon_rect = sui_flmap[param_name][subparam_index].rect

                ## if it has a parent...

                if has_parent:
                    
                    ## if it is unpacked...

                    if is_unpacked:

                        # align icon's centery with up button's bottom
                        unpacking_icon_rect.centery = up_button_rect.bottom

                        # align icon's left with up button's right padding it
                        # according to whether th
                        unpacking_icon_rect.left = up_button_rect.right + 3

                        # if parameter is of variable-keyword kind, we also
                        # add horizontal padding to account for the key icon
                        # used

                        if kind == 'var_key':

                            # TODO use width of key icon rather than hardcoded
                            # number
                            unpacking_icon_rect.left += 18

                        # add it to the list of subparameter rects
                        subparam_rects.append(unpacking_icon_rect)


                    ## if it's not unpacked, but of keyword variable kind...

                    elif kind == 'var_key':

                        ## position the keyword entry and add its rect to the
                        ## list of rects of the subparameter

                        keyword_entry = skl_map[subparam_index]

                        keyword_entry.rect.midleft = (
                            up_button_rect.move(18, 0).bottomright
                        )

                        subparam_rects.append(keyword_entry.rect)

                        ## add it to the list of visible widgets
                        vws.append(keyword_entry)

                ## if it doesn't have a parent...

                else:

                    ## reference the widget and its remove button locally

                    widget = wl_flmap[param_name][subparam_index]
                    remove_button = wrb_flmap[param_name][subparam_index]

                    ## add them to the respective lists of visible objects

                    vws.append(widget)
                    vbs.append(remove_button)

                    ## position them and add their rects as part of the
                    ## subparameter

                    widget.rect.topleft = up_button_rect.move(3, 0).topright

                    remove_button.rect.midleft = (
                        widget.rect.right,
                        input_socket.rect.centery,
                    )

                    subparam_rects.append(widget.rect)
                    subparam_rects.append(remove_button.rect)


                    ## if it is unpacked...

                    if is_unpacked:

                        # position the unpacking icon rect and add it to the
                        # list of subparameter rects

                        unpacking_icon_rect.bottomleft = (
                            up_button_rect.move(3, -2).topright
                        )

                        subparam_rects.append(unpacking_icon_rect)

                    ## if not unpacked but is of keyword variable kind...

                    elif kind == 'var_key':

                        ## position the keyword entry and add its rect to the
                        ## list of rects of the subparameter

                        keyword_entry = skl_map[subparam_index]

                        keyword_entry.rect.bottomleft = (
                            up_button_rect.move(3, -2).topright
                        )

                        subparam_rects.append(keyword_entry.rect)

                        ## add it to the list of visible widgets
                        vws.append(keyword_entry)


                # assign top
                subparam_rectsman.top = top

                # define new top
                top = subparam_rectsman.bottom

                # add subparam rectsman to list of rects for the parameter
                param_rects.append(subparam_rectsman)

                # if the subparameter isn't the last one, increment the top
                # with a constant distance between subparameters

                if subparam_index != last_subparam_index:
                    top += DISTANCE_BETWEEN_SUBPARAMS


            ## position the placeholder socket

            ## retrieve the rects from the placeholder
            ## socket and the "add subparameter button"

            psocket_rect = psl_map[param_name].rect
            add_button_rect = pab_map[param_name].rect

            ## position the placeholder socket's centerx at 0
            psocket_rect.centerx = 0

            ## don't forget to adjust text rect's left relative to the
            ## placeholder socket's right
            text_rect.left = psocket_rect.move(2, 0).right

            ## put the "add subparameter button" a bit to the right of the
            ## placeholder socket, both vertically aligned
            add_button_rect.midleft = psocket_rect.move(5, 0).midright

            ## reposition socket rect and button rect together as if they
            ## were a single rect by controlling them through a temporary
            ## rects manager instance

            # instantiate rectsman

            _temp_rectsman = (

                RectsManager(

                    # __iter__ method of tuple containing rect

                    (
                        psocket_rect,
                        add_button_rect,
                    ).__iter__

                )

            )

            # assign the defined top and add 4 pixels, to
            # push them just a bit down for extra padding
            _temp_rectsman.top = top + 4

            # define the bottom of the rectsman as the new top
            # to be used by the next parameter
            top = _temp_rectsman.bottom

            ## add the rects of the placeholder socket and add button as
            ## part of the parameter's rects

            param_rects.append(psocket_rect)
            param_rects.append(add_button_rect)


        ## if the parameter being positioned isn't the last one,
        ## increment the top with the constant distance between parameters

        if param_name != last_param_name:
            top += DISTANCE_BETWEEN_PARAMS


    ###
    midtop = self.rect.midtop if self.rect else self.midtop

    ### now that the output elements are properly positioned relative to
    ### each other and the input elements (if any) are also positioned like
    ### that, we can finally:
    ###
    ### - position all elements relative to each other
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

    orectsman = self.output_rectsman
    top_width = title_rect.width + (CORNER_WIDTH*2) + 40

    if parameters:

        irectsman = self.input_rectsman
        orectsman.right = irectsman.right + SOCKET_DIAMETER

        ### add padding if too similar in width

        if abs(irectsman.width - orectsman.width) < 20:
            orectsman.right += 20

        ###

        _temp_rectsman = RectsManager((irectsman, orectsman).__iter__)

        if _temp_rectsman.width > top_width:

            _temp_rectsman.centerx = title_rect.centerx 

            topleft_corner_rect.left = irectsman.left + SOCKET_RADIUS
            topright_corner_rect.right = orectsman.right - SOCKET_RADIUS

        else:

            irectsman.left = topleft_corner_rect.left - SOCKET_RADIUS
            orectsman.right = topright_corner_rect.right + SOCKET_RADIUS
            
    else:

        if orectsman.width > top_width:

            orectsman.centerx = title_rect.centerx

            topleft_corner_rect.left = orectsman.left - 5
            topright_corner_rect.right = orectsman.right - SOCKET_RADIUS

        else:
            orectsman.right = topright_corner_rect.right - SOCKET_RADIUS


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

    orectsman.top = top

    if parameters:

        irectsman.top = orectsman.bottom + INPUT_OFFSET
        top = irectsman.bottom

    else:
        top = orectsman.bottom


    ## reference the rect of the id text object locally
    id_text_rect = self.id_text_obj.rect

    ## align its centerx with title rect's centerx
    id_text_rect.centerx = title_rect.centerx

    ## align its top with the last defined top; also push it
    ## 4 pixels down for extra padding
    id_text_rect.top = top + 4

    ##
    top = id_text_rect.bottom - 2

    ## position bottom corners

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

        ## if there are parameters...
        self.input_rectsman.left
        if parameters

        ## otherwise...
        else top_rectsman.left - SOCKET_RADIUS

    )

    right = self.output_rectsman.right

    self.rect.width = right - left

    ## height
    self.rect.height = bottom_rectsman.bottom - top_rectsman.top

    ## midtop
    self.rect.midtop = top_rectsman.midtop
