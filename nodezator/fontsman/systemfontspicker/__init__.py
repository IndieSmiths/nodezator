"""Facility w/ class for visualizing and picking system fonts."""

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

from ...config import APP_REFS, SAMPLE_UNICODE_CHARACTERS_PATH

from ...pygamesetup import SCREEN_RECT, SERVICES_NS

from ...dialog import create_and_show_dialog

from ...logman.main import get_new_logger

from ...ourstdlibs.pyl import load_pyl

from ...our3rdlibs.userlogger import USER_LOGGER

from ...loopman.main import LoopHolder

from ...classes2d.single import Object2D

from ...classes2d.collections import List2D

from ...surfsman.render import render_rect, render_not_found_icon

from ...textman.render import render_text

from ...fontsman.constants import ENC_SANS_BOLD_FONT_PATH



### module level contants/values/objects

FONT_PREVIEW_SIZE = (200, 100)

PLACEHOLDER_PREVIEW_SURF = Surface(FONT_PREVIEW_SIZE).convert()
PLACEHOLDER_PREVIEW_SURF.fill('white')

## create logger for module
logger = get_new_logger(__name__)


SYS_FONT_NAMES_SET = set(get_fonts())
SYS_FONT_NAMES_SORTED = sorted(SYS_FONT_NAMES_SET)

try:
    SAMPLE_UNICODE_CHARS_DATA = load_pyl(SAMPLE_UNICODE_CHARACTERS_PATH)

except Exception as err:
    raise RuntimeError("Couldn't load sample unicode characters") from err


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

        ### render and align text objects

        label_texts, char_texts = zip(*SAMPLE_UNICODE_CHARS_DATA.items())

        labels_2d = List2D(

            Object2D.from_surface(

                render_text(
                    f'{label_text}:',
                    font_height=17,
                    font_key=ENC_SANS_BOLD_FONT_PATH,
                )

            )

            for label_text in label_texts

        )

        char_groups = [
            char_text.replace(',', '').replace(' ', '')
            for char_text in char_texts
        ]

        char_groups_2d = List2D(

            List2D(

                Object2D.from_surface(
                    render_text(
                        text=char,
                        font_height=17,
                        font_key=self.font_name,
                    )
                )

                for char in char_group
            )

            for char_group in char_groups

        )

        labels_2d.rect.snap_rects_ip(
            retrieve_pos_from='bottomleft',
            assign_pos_to='topleft',
        )

        labels_2d.rect.move_ip(4, 4)

        for char_group in char_groups_2d:

            char_group.rect.snap_rects_ip(
                retrieve_pos_from='topleft',
                assign_pos_to='topright',
                offset_pos_by=(4, 0),
            )

        padded_max_right = (
            max(label_2d.rect.right for label_2d in labels_2d) + 4
        )

        for label_2d, char_group in zip(labels_2d, char_groups):
            char_group.rect.topleft = (padded_max_right, label_2d.rect.top)

        ### blit onto preview surface

        blit_on_preview = self.font_preview_panel.image.blit

        for label_2d, char_group in zip(labels_2d, char_groups):

            blit_on_preview(label_2d.image, label_2d.rect)

            for char_obj in char_group:
                blit_on_preview(char_obj.image, char_obj.rect)

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
