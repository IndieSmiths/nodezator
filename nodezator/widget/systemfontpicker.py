"""Facility for system font picker widget."""

### third-party imports
from pygame.font import SysFont, get_fonts


### local imports

from ..fontsman.preview.cache import (
    FONT_PREVIEWS_DB,
    update_cache_for_font_preview,
)

from ..surfsman.cache import NOT_FOUND_SURF_MAP



SYS_FONTS_SET = set(get_fonts())
SYS_FONTS_SORTED = sorted(SYS_FONTS_SET)
SYS_FONTS_MAP = {}


class SystemFontPicker:
    """Helps users pick system fonts and display them."""

    def __init__(
        self,
        value='',
        loop_holder=None,
        width=155,
        name='system_font_picker',
        command=empty_function,
        update_behind=empty_function,
        draw_behind=empty_function,
        draw_on_window_resize=empty_function,
        coordinates_name='topleft',
        coordinates_value=(0, 0),
    ):

        ### ensure value argument received is a python literal

        if not self.validate(value):
            raise TypeError("'value' received must be a python literal")

        ### create placeholder surface, used whenever we need to display a
        ### font which wasn't loaded yet

        ### store some of the arguments in their own
        ### attributes

        self.name = name
        self.value = value
        self.command = command
        self.loop_holder = loop_holder

        ### create and position rect
        rect = Rect(0, 0, width, height=155)

        ### create/update surface

    def validate(self, value):

        try:
            literal_eval(repr(value))
        except:
            return False
        else:
            return True

    def update_previews(self):
        """"""
        font_names = (self.value,) if isinstance(self.value, str) else self.value

        for font_name in font_names:
            update_cache_for_font_preview(font_name)

        self.update_image()

    def blit_value_representation(self):
        """Blit representation of video in current path."""
        image = self.image

        rect = (
            1,
            BUTTON_HEIGHT + 2,
            self.width - 2,
            self.height - ((BUTTON_HEIGHT * 2) + 2),
        )

        draw_rect(image, PATHPREVIEW_BG, rect)

        ###

        if self.value == '':
            preview_surf = NOT_FOUND_SURF_MAP[(rect[2], rect[3])]

        ###

        else:

            preview_surf = FONT_PREVIEWS_DB[self.current_value][
                {
                    "font_size": 20,
                    "chars": PREVIEW_CHARS,
                    "width": rect[2],
                    "height": rect[3],
                    "not_found_width": rect[2],
                    "not_found_height": rect[3],
                }
            ]

        image.blit(preview_surf, rect)

        super().blit_path_representation()

    def preview_paths(self):
        """Preview font(s) from path(s)."""

        try:
            view_fonts(self.value)

        except FileNotFoundError:
            error_msg = "Font file wasn't found."

        except PygameError:
            error_msg = "Couldn't load font file"

        else:
            error_msg = ''

        if error_msg:

            print(error_msg)
            set_status_message(error_msg)
