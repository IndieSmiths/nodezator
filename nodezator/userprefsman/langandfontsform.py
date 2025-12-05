"""Form for lang and font preferences editing."""

### standard library import
from functools import partialmethod


### third-party imports

from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    KEYUP,
    K_ESCAPE,
    K_RETURN,
    K_KP_ENTER,
)


### local imports

from ..pygamesetup import SERVICES_NS, SCREEN_RECT, blit_on_screen

from ..config import APP_REFS

from ..translatedtext import TRANSLATIONS

from .main import USER_PREFS, CONFIG_FILEPATH

from .validation import (
    AVAILABLE_LOCALES,
    GENERAL_FONT_HEIGHT_RANGE,
    MONO_FONT_HEIGHT_RANGE,
    FONT_KIND_OPTIONS,
    validate_prefs_data,
)

from ..dialog import create_and_show_dialog

from ..ourstdlibs.pyl import save_pyl

from ..ourstdlibs.behaviour import (
    empty_function,
    get_oblivious_callable,
)

from ..our3rdlibs.button import Button

from ..our3rdlibs.behaviour import set_status_message


from ..classes2d.single import Object2D
from ..classes2d.collections import List2D

from ..fontsman.constants import (
    ENC_SANS_BOLD_FONT_HEIGHT,
    ENC_SANS_BOLD_FONT_PATH,
)

from ..textman.render import render_text

from ..surfsman.cache import UNHIGHLIGHT_SURF_MAP

from ..surfsman.draw import draw_border, draw_depth_finish

from ..surfsman.render import render_rect

from ..loopman.main import LoopHolder

from ..widget.intfloatentry.main import IntFloatEntry

from ..widget.optionmenu.main import OptionMenu

from ..colorsman.colors import (
    CONTRAST_LAYER_COLOR,
    BUTTON_FG,
    BUTTON_BG,
    WINDOW_FG,
    WINDOW_BG,
)



### translations
t = TRANSLATIONS.language_and_fonts_form

### constants

TEXT_SETTINGS = {
    "font_height": ENC_SANS_BOLD_FONT_HEIGHT,
    "font_path": ENC_SANS_BOLD_FONT_PATH,
    "padding": 5,
    "foreground_color": WINDOW_FG,
    "background_color": WINDOW_BG,
}

BUTTON_SETTINGS = {
    "font_height": ENC_SANS_BOLD_FONT_HEIGHT,
    "font_path": ENC_SANS_BOLD_FONT_PATH,
    "padding": 5,
    "depth_finish_thickness": 1,
    "foreground_color": BUTTON_FG,
    "background_color": BUTTON_BG,
}


class UserPreferencesLanguageAndFontsForm(Object2D, LoopHolder):
    """Form for editing user preferences for language and fonts."""

    def __init__(self):
        """Setup form objects."""
        ### build widgets
        self.build_form_widgets()

        ### assign rect and surf for background

        self.rect = self.widgets.rect.inflate(20, 20)
        self.image = render_rect(*self.rect.size, WINDOW_BG)

        draw_border(self.image)

        ### store a semitransparent object

        self.rect_size_semitransp_obj = Object2D.from_surface(
            surface=render_rect(*self.rect.size, (*CONTRAST_LAYER_COLOR, 130)),
            coordinates_name="center",
            coordinates_value=SCREEN_RECT.center,
        )

        ### assign behaviour
        self.update = empty_function

        ### center edition form and append centering
        ### method as a window resize setup

        self.center_preferences_form()

        APP_REFS.window_resize_setups.append(self.center_preferences_form)

    def center_preferences_form(self):
        self.rect.center = self.widgets.rect.center = SCREEN_RECT.center

    def build_form_widgets(self):
        """Build widgets to hold settings for edition."""
        ### create list to hold widgets
        widgets = self.widgets = List2D()

        ### instantiate a caption for the form

        caption_label = Object2D.from_surface(
            surface=(
                render_text(
                    text=t.caption,
                    border_thickness=2,
                    border_color=(TEXT_SETTINGS["foreground_color"]),
                    **TEXT_SETTINGS,
                )
            ),
        )

        widgets.append(caption_label)

        labels = List2D()

        ### create specific widgets to edit user preferences

        for label_text in (
            t.language,
            t.general_font_height,
            t.mono_font_height,
            t.general_font,
            t.mono_font,
        ):

            label_obj = Object2D.from_surface(
                render_text(text=f"{label_text}:", **TEXT_SETTINGS)
            )

            labels.append(label_obj)

        labels.rect.snap_rects_ip(
            retrieve_pos_from='bottomleft',
            assign_pos_to='topleft',
            offset_pos_by=(0, 5),
        )

        labels.rect.topleft = widgets.rect.move(0, 5).bottomleft

        widgets.extend(labels)

        ###

        lang_option_menu = OptionMenu(
            loop_holder=self,
            options=AVAILABLE_LOCALES,
            value=USER_PREFS['LOCALE'],
            draw_on_window_resize=self.draw,
            name='LOCALE',
            max_width=0,
        )

        general_font_size_intfloat_entry = IntFloatEntry(
            loop_holder=self,
            value=USER_PREFS['GENERAL_FONT_HEIGHT'],
            name='GENERAL_FONT_HEIGHT',
            width=90,
            min_value=min(GENERAL_FONT_HEIGHT_RANGE),
            max_value=max(GENERAL_FONT_HEIGHT_RANGE),
            numeric_classes_hint='int',
            allow_none=False,
            draw_on_window_resize=self.draw,
        )

        mono_font_size_intfloat_entry = IntFloatEntry(
            loop_holder=self,
            value=USER_PREFS['MONO_FONT_HEIGHT'],
            name='MONO_FONT_HEIGHT',
            min_value=min(MONO_FONT_HEIGHT_RANGE),
            max_value=max(MONO_FONT_HEIGHT_RANGE),
            width=90,
            numeric_classes_hint='int',
            allow_none=False,
            draw_on_window_resize=self.draw,
        )

        general_font_to_use_option_menu = self.gen_font_option = OptionMenu(
            loop_holder=self,
            options=FONT_KIND_OPTIONS,
            value=USER_PREFS['GENERAL_FONT_KIND'],
            name='GENERAL_FONT_KIND',
            draw_on_window_resize=self.draw,
            max_width=0,
        )

        mono_font_to_use_option_menu = self.mono_font_option = OptionMenu(
            loop_holder=self,
            options=FONT_KIND_OPTIONS,
            value=USER_PREFS['MONO_FONT_KIND'],
            name='MONO_FONT_KIND',
            draw_on_window_resize=self.draw,
            max_width=0,
        )

        self.prefs_widgets = prefs_widgets = List2D(
            [
                lang_option_menu,
                general_font_size_intfloat_entry,
                mono_font_size_intfloat_entry,
                general_font_to_use_option_menu,
                mono_font_to_use_option_menu,
            ]
        )

        right = max(label.rect.right for label in labels) + 5

        for pref_widget, label in zip(prefs_widgets, labels):
            pref_widget.rect.midleft = (right, label.rect.centery)

        widgets.extend(prefs_widgets)

        ###

        ### create, position and store form related buttons

        ## submit button

        self.finish_button = Button.from_text(
            text=t.finish,
            command=self.finish_form,
            **BUTTON_SETTINGS,
        )

        draw_depth_finish(self.finish_button.image)

        self.finish_button.rect.topright = widgets.rect.move(0, 5).bottomright

        ## cancel button

        self.cancel_button = Button.from_text(
            text=t.cancel,
            command=self.exit_loop,
            **BUTTON_SETTINGS,
        )

        draw_depth_finish(self.cancel_button.image)

        self.cancel_button.rect.midright = self.finish_button.rect.move(-5, 0).midleft

        ## store

        self.finish_button.rect.topright = widgets.rect.move(0, 5).bottomright

        self.cancel_button.rect.topright = self.finish_button.rect.move(-5, 0).topleft

        widgets.extend((self.cancel_button, self.finish_button))

    def edit_lang_and_fonts_settings(self):

        ### blit the screen-size semitransparent surf in the
        ### canvas to increase constrast
        blit_on_screen(UNHIGHLIGHT_SURF_MAP[SCREEN_RECT.size], (0, 0))

        ###
        self.loop()

        ### blit semitransparent surface over area occupied
        ### by self.rect so the form appears unhighlighted
        self.unhighlight()

    def handle_input(self):
        """Process events from event queue."""

        for event in SERVICES_NS.get_events():
            ### QUIT
            if event.type == QUIT:
                self.quit()

            ### KEYUP

            elif event.type == KEYUP:

                ## exit the preferences dialog by
                ## pressing "Esc"

                if event.key == K_ESCAPE:
                    self.exit_loop()

                ## confirm edition by pressing one of the "enter" keys

                elif event.key in (K_RETURN, K_KP_ENTER):
                    self.finish_form()

            ### MOUSEBUTTONDOWN

            elif event.type == MOUSEBUTTONDOWN:

                if event.button == 1:

                    if self.rect.collidepoint(event.pos):
                        self.on_mouse_click(event)

            ### MOUSEBUTTONUP

            elif event.type == MOUSEBUTTONUP:

                if event.button == 1:

                    if self.rect.collidepoint(event.pos):
                        self.on_mouse_release(event)

                    ## cancel editing form if mouse left
                    ## button is released out of boundaries
                    else:
                        self.exit_loop()

    def mouse_method_on_collision(self, method_name, event):
        """Invoke inner widget if it collides with mouse.

        Parameters
        ==========

        method_name (string)
            name of method to be called on the colliding
            widget.
        event (event object of MOUSEBUTTON~ type)
            it is required in order to comply with
            mouse interaction protocol used; here we
            use it to retrieve the position of the
            mouse when the first button was released.

            Check pygame.event module documentation on
            pygame website for more info about this event
            object.
        """
        ### retrieve position from attribute in event obj
        mouse_pos = event.pos

        ### search for a colliding obj among the widgets

        for obj in self.widgets:

            if obj.rect.collidepoint(mouse_pos):

                colliding_obj = obj
                self.unhighlight()
                break

        else:
            return

        ### if you manage to find a colliding obj, execute
        ### the requested method on it, passing along the
        ### received event

        try:
            method = getattr(colliding_obj, method_name)
        except AttributeError:
            pass
        else:
            method(event)

    on_mouse_click = partialmethod(
        mouse_method_on_collision,
        "on_mouse_click",
    )

    on_mouse_release = partialmethod(
        mouse_method_on_collision,
        "on_mouse_release",
    )

    def finish_form(self):
        """Assign new category indices and exit loop."""

        prefs_copy = USER_PREFS.copy()

        prefs_copy.update(

            (widget.name, widget.get())
            for widget in self.prefs_widgets

        )

        try:
            validate_prefs_data(prefs_copy)

        except Exception as err:

            message = f"Some error happened: {err}"
            create_and_show_dialog(message, level_name='error')

            return

        else:

            try:
                save_pyl(prefs_copy, CONFIG_FILEPATH)

            except Exception as err:

                message = f"Couldn't save config file: {err}"
                create_and_show_dialog(message, level_name='error')

                return

            else:

                # TODO make sure changes propagate to
                # wherever relevant (for instance,
                # assign max_lines to user logger and
                # also take care of max lines for
                # the custom stdout)
                USER_PREFS.update(prefs_copy)

        ### notify user via dialog and status message

        message = (
            "User preferences changed. Some changes may"
            " only take effect after restarting the app"
        )

        set_status_message(message)

        create_and_show_dialog(message, level_name='info')

        ### trigger exit of the loop
        self.exit_loop()

    def draw(self):
        """Draw itself and widgets.

        Extends Object2D.draw.
        """
        ### draw self (background)
        super().draw()

        ### draw widgets
        self.widgets.call_draw()

        ### update screen
        SERVICES_NS.update_screen()

    def unhighlight(self):
        """Draw semitransparent surface on self.rect area.

        Done to make form appear unhighlighted.
        """
        blit_on_screen(UNHIGHLIGHT_SURF_MAP[self.rect.size], self.rect)


edit_lang_and_fonts_settings = (
    UserPreferencesLanguageAndFontsForm()
    .edit_lang_and_fonts_settings
)
