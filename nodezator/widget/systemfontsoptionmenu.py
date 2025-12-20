"""Facility for system font option menu widget."""

### third-party imports
from pygame.font import SysFont, get_fonts


### local imports

from ..ourstdlibs.behaviour import empty_function

from ..surfsman.cache import NOT_FOUND_SURF_MAP

from ..fontsman.preview.cache import (
    FONT_PREVIEWS_DB,
    update_cache_for_font_preview,
)

from ..fontsman.systemfontspicker import pick_system_fonts

from ..textman.render import render_text



BUTTON_HEIGHT = 18


class SystemFontOptionMenu:
    """Helps users pick system fonts and display them."""

    def __init__(
        self,
        value='',
        string_when_single=True,
        loop_holder=None,
        width=155,
        name='system_font_option_menu',
        command=empty_function,
        update_behind=empty_function,
        draw_behind=empty_function,
        draw_on_window_resize=empty_function,
        coordinates_name='topleft',
        coordinates_value=(0, 0),
    ):

        ### store string_when_single argument
        self.string_when_single = string_when_single

        ### ensure value argument received is valid
        self.validate_value(value)

        ### store more of the arguments in their own
        ### attributes

        self.name = name
        self.value = value
        self.command = command
        self.loop_holder = loop_holder

        ### create image and rect, then position rect

        self.image = Surface((width, 100)).convert()
        self.image.fill('grey')
        self.rect = self.image.get_rect()

        setattr(
            self.rect,
            coordinates_name,
            coordinates_value,
        )

        ###
        self.update_image()

    def validate_value(self, value):

        try:
            literal_eval(repr(value))

        except Exception as err:
            raise ValueError("Value is not a Python literal") from err

        value_type = type(value)

        ### if value is a string, it can be any value, so we don't need
        ### to do anything else

        if value_type is str:
            pass

        ### if value is a tuple, though, more conditions need to be checked

        elif value_type is tuple:

            ## it must not be empty

            if not value:
                raise ValueError("if 'value' is a tuple, it must not be empty")

            ## all of its items must be strings

            elif any(

                not isinstance(item, str)
                for item in value

            ):

                raise TypeError(
                    "if 'value' is a tuple, all of its items must be strings"
                )

            ## if 'string_when_single' flag is on, it cannot have a single value
            ## (otherwise it should be a string instead)

            elif self.string_when_single and len(value) == 1:

                raise TypeError(
                    "with 'string_when_single' enabled, when the value"
                    " contains a single font name, it must be a string,"
                    " not a tuple"
                )

        ### if type isn't one of the allowed types, raise
        ### TypeError with suitable message

        else:
            raise TypeError("'value' must be a string or tuple of strings")

    def update_previews(self):
        """"""
        font_names = (

            (self.value,)
            if isinstance(self.value, str)

            else self.value

        )

        for font_name in font_names:
            update_cache_for_font_preview(font_name)

        self.update_image()

    def update_image(self):
        """Update widget image."""
        ###
        image = self.image

        ### clean image surface
        image.fill('grey')

        ###
        value = self.value

        ### create variable specifying whether the value
        ### is a string
        value_is_string = isinstance(value, str)

        ### create variable specifying whether there's more
        ### than one font name

        multiple_names = not value_is_string and len(value) > 1

        ### if there are multiple font names...

        if multiple_names:

            ### define current font name
            self.current_font_name = value[self.value_index]

        ### if there's just one font name, though...

        else:

            ### define font name
            self.current_font_name = value if value_is_string else value[0]

        ### blit all buttons

        #for surf, rect in zip(self.button_surfs, self.button_rects):
        #    image.blit(surf, rect)

        ### blit font representation
        self.blit_value_representation()

        ### draw depth finish
        draw_depth_finish(image)

    def blit_value_representation(self):
        """Blit representation of current font."""
        image = self.image

        rect = (
            1,
            BUTTON_HEIGHT + 2,
            self.rect.width - 2,
            self.rect.height - ((BUTTON_HEIGHT * 2) + 2),
        )

        draw_rect(image, 'grey', rect)

        ###

        if self.value == '':
            preview_surf = NOT_FOUND_SURF_MAP[(rect[2], rect[3])]

        ###

        else:

            preview_surf = FONT_PREVIEWS_DB[self.current_font_name][
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

        ### blit rest of elements

        rect = self.image.get_rect()
        rect.topleft = rect.move(1, -BUTTON_HEIGHT).bottomleft
        rect.height = BUTTON_HEIGHT - 2
        rect.move_ip(0, 1)

        draw_rect(self.image, 'grey', rect)

        ###

        blit_aligned(

            surface_to_blit=(

                render_text(
                    text=str(self.current_font_name),
                    font_path=ENC_SANS_BOLD_FONT_PATH,
                    font_height=ENC_SANS_BOLD_FONT_HEIGHT,
                    padding=1,
                    max_width=152,
                    ommit_direction="left",
                )

            ),

            target_surface=self.image,
            retrieve_pos_from="bottomright",
            assign_pos_to="bottomright",
            offset_pos_by=(-1, -1),
        )

        if isinstance(self.value, str) or len(self.value) == 1:
            return

        ### blit entry

        #self.image.blit(
        #    self.index_entry.image, self.button_rects[1].move(1, 0).topright
        #)

    def preview_fonts(self):
        """Preview font(s) from system."""

        try:
            view_fonts(self.value)

        except FileNotFoundError:
            error_msg = "System font wasn't found."

        except PygameError:
            error_msg = "Couldn't load font file"

        except Exception as err:
            error_msg = str(err)

        else:
            error_msg = ''

        if error_msg:

            print(error_msg)
            set_status_message(error_msg)

    def get(self):
        """Return the widget value."""
        return self.value

    def set(
        self,
        value,
        custom_command=True,
        update_image=True,
    ):
        """Set the value of the widget.

        value (string or tuple of strings representing paths)
            new value for widget.
        custom_command (boolean)
            indicates whether the custom command stored
            upon instantiation should be called after
            updating the value.
        update_image (boolean)
            indicates whether the update_image method
            should be called after updating the value.
        """
        ### validate value received
        try:
            self.validate_value(value)

        ### if it doesn't validate, report error and exit
        ### method by returning

        except (TypeError, ValueError) as err:

            print(err)
            return

        ### changes are only performed if the new value is
        ### indeed different from the current one

        if self.value != value:

            ### store new value
            self.value = value

            ### reset index
            self.value_index = 0

            ### reset index value and max value

            entry = self.index_entry

            entry.set(0, False)

            max_value = 0 if isinstance(value, str) else len(value) - 1

            entry.set_range(0, max_value)

            ### if requested, execute the custom command
            if custom_command:
                self.command()

            ### if requested, update the widget image
            if update_image:
                self.update_image()
