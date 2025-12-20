"""Font preview render utilities."""

### third-party imports

from pygame import error as PygameError

from pygame.font import Font, SysFont, match_font


### local imports

from ...classes2d.single import Object2D

from ...classes2d.collections import List2D

from ...surfsman.render import render_rect, render_not_found_icon

from ...colorsman.colors import BLACK, WHITE



### TODO refactor this

def render_font_preview(
    font_key,
    font_size,
    chars,
    width,
    height,
    not_found_width=0,
    not_found_height=0,
):
    """Return surface with given chars."""

    ### XXX perhaps font instances created here should be cached as well

    if isinstance(font_key, str):

        if match_font(font_key) is None:

            ### if width and height in case the font file wasn't found were
            ### provided, create a surface with a drawing indicating it wasn't
            ### found

            if not_found_width and not_found_height:

                return render_not_found_icon(
                    (not_found_width, not_found_height)
                )

            ### otherwise raise exception explaining the problem

            else:
                raise ValueError("Couldn't find system font with given name.")

        else:
            render = SysFont(font_key, font_size).render

    else:

        try:
            render = Font(font_key, font_size).render

        except (
            FileNotFoundError,
            IsADirectoryError,
            PygameError,
            PermissionError,
        ):

            ### if width and height in case the font file wasn't found were
            ### provided, create a surface with a drawing indicating it wasn't
            ### found

            if not_found_width and not_found_height:

                return render_not_found_icon(
                    (not_found_width, not_found_height)
                )


            ### otherwise reraise the exception
            else:
                raise

    ### create and align chars

    char_objs = List2D(

        Object2D.from_surface(

            render(char, True, BLACK, WHITE)

        )

        for char in chars

    )

    char_objs.rect.snap_rects_intermittently_ip(
        dimension_name='width',
        dimension_unit='pixels',
        max_dimension_value=width,
        retrieve_pos_from='topright',
        assign_pos_to='topleft',
        intermittent_pos_from='bottomleft',
        intermittent_pos_to='topleft',
    )

    ### create preview surface and blit chars on it

    surf = render_rect(width, height, WHITE)

    for char_obj in char_objs:
        surf.blit(char_obj.image, char_obj.rect)

    ### finally, return the preview
    return surf
