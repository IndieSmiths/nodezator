
### third-party import
from pygame import Rect

### local imports

from ...pygamesetup.constants import SCREEN_RECT

from ...classes2d.single import Object2D
from ...classes2d.collections import List2D



def position_elements_and_get_boundaries(self):

    ### collection to gather all objects and manipulate them
    all_objs = List2D()

    ### reference colors panel locally
    colors_panel = self.colors_panel

    all_objs.append(colors_panel)

    ### reference all labels

    (

        ## color properties/representations

        scale_label_hue,
        scale_label_lightness,
        scale_label_saturation,
        scale_label_value,
        scale_label_red,
        scale_label_green,
        scale_label_blue,
        label_hex,
        label_html_name,
        label_pygame_name,
        scale_label_alpha,

        ## others

        label_current_colors,
        label_more,
        label_title,

    ) = self.labels

    all_objs.append(label_title)

    ### reference all buttons (except entries)

    (

        move_left_button,
        move_right_button,
        remove_color_button,
        add_color_button,
        sort_colors_button,
        reverse_order_button,
        shuffle_button,
        remove_duplicates_button,
        html_colors_button,
        pygame_colors_button,
        import_colors_button,
        export_colors_button,
        ok_button,
        cancel_button,
        color_add_option_menu,
        color_sorting_holder,
        alpha_checkbutton,
        alpha_checkbutton_label,
        view_button,

        *_, # not interested in entries at this point

    ) = self.buttons


    ### position colors panel under label title
    colors_panel.rect.top = label_title.rect.move(0, 10).bottom

    ### position label for current colors under colors panel
    label_current_colors.rect.topleft = colors_panel.rect.move(0, 5).bottomleft

    ### position "More" label under label for current colors
    label_more.rect.topleft = label_current_colors.rect.move(0, 5).bottomleft

    ### group and position buttons to the right of those labels

    ## create a collection to hold items temporarily in order to assist
    ## in positioning them relative to each other and to other objects
    temp_list2d = List2D()

    ## position buttons

    for label, objects in (

        (

            label_current_colors,

            (

                move_left_button,
                move_right_button,
                remove_color_button,
                add_color_button,
                color_add_option_menu,
                sort_colors_button,
                color_sorting_holder,
                reverse_order_button,
                shuffle_button,
                remove_duplicates_button,
                view_button,

            ),

        ),

        (

            label_more,

            (
                html_colors_button,
                pygame_colors_button,
                import_colors_button,
                export_colors_button,
            ),

        ),

    ):

        temp_list2d.extend(objects)

        temp_list2d.rect.snap_rects_ip(
            retrieve_pos_from='midright',
            assign_pos_to='midleft',
            offset_pos_by=(5, 0),
        )

        temp_list2d.rect.midleft = label.rect.move(5, 0).midright

        temp_list2d.clear()

        ## also use the opportunity to reference labels and objects

        all_objs.append(label)
        all_objs.extend(objects)


    ### position related scales, labels and entries relative to each other

    ## create a collection to hold items temporarily in order to assist
    ## in positioning them relative to each other and to other objects

    (

        scale_group,
        label_group,
        entry_group,

    ) = groups = [List2D() for _ in range(3)]

    scale_group.extend(self.scales)

    label_group.extend((
        scale_label_hue,
        scale_label_lightness,
        scale_label_saturation,
        scale_label_value,
        scale_label_red,
        scale_label_green,
        scale_label_blue,
        scale_label_alpha,
    ))

    entry_group.extend(self.scale_entries)

    ## calculate highest width and height for labels, which will be useful in
    ## further steps
    label_widths, label_heights = zip(*(item.rect.size for item in label_group))

    ## since text may vary in size, we position the labels relative to each
    ## other vertically first (we could've used the entries as well, since
    ## they also vary in size depending on the font's height)

    distance_between_bottoms = (

        ## highest height
        max(label_heights)

        ## plus arbitrary padding
        + 15

    )

    label_group.rect.snap_rects_ip(
        retrieve_pos_from='bottomleft',
        assign_pos_to='bottomleft',
        offset_pos_by=(0, distance_between_bottoms),
    )

    ## position the other groups relative to the labels

    distance_between_lefts = (

        ## highest width
        max(label_widths)

        ## plus arbitrary padding
        + 5

    )

    for scale, label, entry in zip(*groups):

        scale.rect.bottomright = label.rect.move(-5, 0).bottomleft

        entry.rect.bottomleft = (
            label.rect.move(distance_between_lefts, 0).bottomleft
        )

    ### position label and checkbutton related to the alpha scale next to it

    alpha_scale = scale_group[-1]

    alpha_checkbutton.rect.midright = alpha_scale.rect.move(-10, 0).midleft
    alpha_checkbutton_label.rect.midright = (
        alpha_checkbutton.rect.move(-2, -2).midleft
    )

    ### 

    control_area_objs = List2D()

    for group in groups:

        control_area_objs.extend(group)
        group.clear()

    control_area_objs.extend((alpha_checkbutton, alpha_checkbutton_label))

    ### position other entries and their related labels relative to this
    ### last group of scale-label-entry triplets (and the alpha related
    ### widgets we just added to it)

    row = List2D()

    x = 0

    for pair in (

        (label_hex, self.hex_entry),
        (label_html_name, self.html_name_entry),
        (label_pygame_name, self.pygame_name_entry),

    ):

        row.extend(pair)

        label, entry = pair

        label.rect.x = x
        entry.rect.bottomleft = label.rect.move(5, 0).bottomright

        x = entry.rect.right + 20

    distance_between_bottoms = (

        ## highest height
        row.rect.height

        ## plus arbitrary padding
        + 10

    )

    row.rect.bottomleft = (
        control_area_objs.rect.move(0, distance_between_bottoms).bottomleft
    )

    control_area_objs.extend(row)

    ###

    _temp_obj = Object2D()
    _temp_obj.rect = control_area_objs.rect.inflate(20, 20)
    _temp_obj.rect.topleft = label_more.rect.move(0, 10).bottomleft
    control_area_objs.rect.center = _temp_obj.rect.center
    control_area_objs.append(_temp_obj)

    all_objs.extend(control_area_objs)


    ### finally, position remaining buttons relative to all objects so far

    row.clear()
    row.extend((cancel_button, ok_button))

    row.rect.snap_rects_ip(
        retrieve_pos_from='midright',
        assign_pos_to='midleft',
        offset_pos_by=(5, 0),
    )

    distance_between_bottoms = (

        ## highest height
        row.rect.height

        ## plus arbitrary padding
        + 10

    )

    row.rect.bottomright = (
        all_objs.rect.move(0, distance_between_bottoms).bottomright
    )

    all_objs.extend(row)

    all_objs.rect.move_ip(10, 10)
    boundaries_rect = all_objs.rect.inflate(20, 20)
    all_objs.clear()


    return (
        boundaries_rect,
        control_area_objs.rect.copy(),
    )
