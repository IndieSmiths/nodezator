"""Facility w/ class for visualizing and picking system fonts."""

### standard library imports

from string import (
    ascii_uppercase,
    ascii_lowercase,
    digits,
    punctuation,
)


### third-party imports

from pygame import Rect, Surface

from pygame.locals import (
    QUIT,
    KEYUP,
    K_ESCAPE,
    K_RETURN,
    K_KP_ENTER,
    K_a,
    K_s,
    K_d,
    K_w,
)

from pygame.font import SysFont, get_fonts, match_font

from pygame.math import Vector2


### local imports

from ...config import APP_REFS

from ...pygamesetup import SCREEN_RECT, SERVICES_NS

from ...dialog import create_and_show_dialog

from ...logman.main import get_new_logger

from ...our3rdlibs.userlogger import USER_LOGGER

from ...loopman.main import LoopHolder

from ...classes2d.single import Object2D

from ...classes2d.collections import List2D

from ...surfsman.render import render_rect, render_not_found_icon

from ...textman.render import render_text

from .render import PLACEHOLDER_PREVIEW_SURF, render_char_info



CHARS = (
    ascii_uppercase
    + ascii_lowercase
    + digits
    + punctuation
)

### create logger for module
logger = get_new_logger(__name__)


SYS_FONT_NAMES_SET = set(get_fonts())
SYS_FONT_NAMES_SORTED = sorted(SYS_FONT_NAMES_SET)
SYS_FONTS_MAP = {}


class SystemFontsPicker(Object2D, LoopHolder):
    """Lists system fonts and allows users to pick one or more."""

    def __init__(self):

        caption = (
            Object2D.from_surface(
                render_text(
                    text="Pick system font(s)",
                )
            )
        )

        selected_fonts_panel = (
            Object2D.from_surface(render_rect(1080, 100, (180, 180, 180)))
        )

        all_fonts_panel = (
            Object2D.from_surface(render_rect(640, 560, (180, 180, 180)))
        )

        font_preview_panel = self.font_preview_panel = (
            Object2D.from_surface(render_not_found_icon((420, 560)))
        )

        selected_fonts_panel.rect.topleft = caption.rect.move(0, 10).bottomleft

        all_fonts_panel.rect.topleft = (
            selected_fonts_panel.rect.move(0, 20).bottomleft
        )

        font_preview_panel.rect.topleft = (
            all_fonts_panel.rect.move(20, 0).topright
        )

        ###

        self.all_panels = List2D(

            (
                caption,
                selected_fonts_panel,
                all_fonts_panel,
                font_preview_panel,
            )

        )

        self.all_panels.rect.center = SCREEN_RECT.center

        self.rect = self.all_panels.rect.inflate(10, 10)
        self.image = Surface(self.rect.size).convert()
        self.image.fill('grey')

        self.clean_image = self.image.copy()

        ###
        self.no_preview_surf = font_preview_panel.image

        ###

        sys_font_2d_objs = self.sys_font_2d_objs = List2D(

            Object2D.from_surface(
                PLACEHOLDER_PREVIEW_SURF,
                font_name = font_name,
            )

            for font_name in SYS_FONT_NAMES_SORTED

        )

        sys_font_2d_objs.rect.lay_rects_like_table_ip(
            dimension_name='width',
            dimension_unit='pixels',
            max_dimension_value=640,
            cell_padding=20,
        )

        sys_font_2d_objs.rect.topleft = all_fonts_panel.rect.topleft

        ###
        self.selected_font_2d_objs = List2D()
        self.font_names = ('',)

        ### center system fonts picker and append centering method
        ### as a window resize setup

        self.center_font_viewer()

        APP_REFS.window_resize_setups.append(self.center_font_viewer)

    def center_font_viewer(self):

        diff = Vector2(SCREEN_RECT.center) - self.rect.center

        self.rect.center = SCREEN_RECT.center
        self.all_panels.rect.center = SCREEN_RECT.center

        self.offset = -Vector2(self.rect.topleft)

        self.sys_font_2d_objs.rect.move_ip(diff)

        if any(item for item in self.font_names):
            self.selected_font_2d_objs.rect.move_ip(diff)

    def pick_system_fonts(self, font_names, index=0):

        font_names = self.font_names = tuple(

            font_name
            for font_name in font_names
            if match_font(font_name) is not None

        )

        max_index = len(font_names) - 1
        index = max(0, min(index, max_index))

        self.font_name = (

            font_names[index]
            if font_names
            else ''

        )

        ###

        if self.font_name:
            self.prepare_preview()

        else:
            self.font_preview_panel.image = self.no_preview_surf

        ###
        self.loop()

        ###
        return self.font_names

    def prepare_preview(self):

        font = SYS_FONTS_MAP[self.font_name]

        #self.char_objs.rect.lay_rects_like_table_ip(
        #    dimension_name='width',
        #    dimension_unit='pixels',
        #    max_dimension_value=780,
        #    cell_padding=5,
        #)

    def handle_input(self):

        self.handle_events()
        self.handle_key_states()

    def handle_events(self):

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:

                self.running = False
                self.font_names = None

            elif event.type == KEYUP:

                if event.key in (K_RETURN, K_KP_ENTER, K_ESCAPE):

                    self.running = False
                    self.font_names = None

    ### TODO create methods in the RectsManager class to automatically scroll
    ### objects within a scroll area;
    ###
    ### make sure classes2d/collections.py has a suitable way to draw objects
    ### in such arrangement (within a scroll area); maybe a thourough review of
    ### classesman/collections.py is needed;

    def handle_key_states(self):

        key_pressed_states = SERVICES_NS.get_pressed_keys()

        if key_pressed_states[K_a]:
            ... #self.char_objs.rect.move_ip(-20, 0)

        elif key_pressed_states[K_s]:
            ... #self.char_objs.rect.move_ip(0, 20)

        elif key_pressed_states[K_w]:
            ... #self.char_objs.rect.move_ip(0, -20)

        elif key_pressed_states[K_d]:
            ... #self.char_objs.rect.move_ip(20, 0)

    def draw(self):

        super().draw()

        for obj in self.all_panels:
            obj.draw()

        ### update screen
        SERVICES_NS.update_screen()


pick_system_fonts = SystemFontsPicker().pick_system_fonts
