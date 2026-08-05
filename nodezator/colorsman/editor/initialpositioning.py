
def position_elements(self):

    ### position buttons

    ## reference the colors panel locally, since we'll reference it so much
    ## futher ahead
    colors_panel = self.colors_panel

    ## position

    move_left_button.rect.topleft = colors_panel.rect.move(85, 5).bottomleft
    move_right_button.rect.topleft = move_left_button.rect.move(5, 0).topright
    remove_color_button.rect.topleft = move_right_button.rect.move(5, 0).topright
    add_color_button.rect.topleft = remove_color_button.rect.move(5, 0).topright
    color_add_option_menu.rect.midleft = add_color_button.rect.move(5, 0).midright
    sort_colors_button.rect.midleft = color_add_option_menu.rect.move(20, 0).midright
    color_sorting_holder.rect.midleft = sort_colors_button.rect.move(5, 0).midright
    reverse_order_button.rect.midleft = color_sorting_holder.rect.move(20, 0).midright
    shuffle_button.rect.topleft = reverse_order_button.rect.move(5, 0).topright
    remove_duplicates_button.rect.topleft = shuffle_button.rect.move(5, 0).topright
    html_colors_button.rect.topleft = colors_panel.rect.move(25, 38).bottomleft
    pygame_colors_button.rect.topleft = html_colors_button.rect.move(5, 0).topright
    import_colors_button.rect.topleft = pygame_colors_button.rect.move(5, 0).topright
    export_colors_button.rect.topleft = import_colors_button.rect.move(5, 0).topright
    ok_button.rect.bottomright = self.rect.move(-10, -10).bottomright
    cancel_button.rect.bottomright = ok_button.rect.move(-10, 0).bottomleft
    alpha_checkbutton.rect.midright = self.scale_map["alpha"].rect.move(-10, 0).midleft
    alpha_checkbutton_label.rect.midright = alpha_checkbutton.rect.move(-2, -2).midleft
    view_button.rect.midleft = remove_duplicates_button.rect.move(5, 0).midright

    ### position scales

    ## define a starting position from where to position the scales
    x, y = self.rect.move(144, 225).topleft

    ## define a vertical padding (space between the scale widgets)
    vertical_padding = 10

    for scale in scales:

        scale.rect.topleft = (x, y)

        ### update the y coordinates to be assigned to
        ### the next scale

        y = (
            ## the current value of y
            y
            ## plus the height of the scale
            + scale.rect.height
            ## plus the vertical padding
            + vertical_padding
        )

    ### position entries

    for entry, scale in zip(self.scale_entries, self.scales):
        entry.rect.midleft = scale.rect.move(105, -2).midright

    hex_entry_topleft = self.scales[-1].rect.move(-69, 35).bottomleft
    html_name_entry_midleft = self.hex_entry.rect.move(135, 0).midright
    pygame_name_entry_midleft = self.html_name_entry.rect.move(154, 0).midright

    ### position labels

    ## reference individual scales
    hue, light, sat, value, red, green, blue, alpha = self.scales

    ## toplefts

    hue.rect.move(10, 0).topright),
    light.rect.move(10, 0).topright),
    sat.rect.move(10, 0).topright),
    value.rect.move(10, 0).topright),
    red.rect.move(10, 0).topright),
    green.rect.move(10, 0).topright),
    blue.rect.move(10, 0).topright),
    alpha.rect.move(-115, 29).bottomleft),
    alpha.rect.move(50, 29).bottomleft),
    alpha.rect.move(360, 29).bottomleft),
    alpha.rect.move(10, 0).topright),
    self.colors_panel.rect.move(-25, 5).bottomleft),
    self.colors_panel.rect.move(-25, 38).bottomleft),
    title_obj.rect.topleft = self.rect.move(5, 5).topleft
