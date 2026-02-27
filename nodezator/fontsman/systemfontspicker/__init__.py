"""Facility w/ class for visualizing and picking system fonts."""

### standard library import
from itertools import chain


### third-party imports

from pygame import Rect, Surface, error as PygameError

from pygame.locals import (

    QUIT,

    KEYUP,

    K_ESCAPE,
    K_RETURN,
    K_KP_ENTER,

    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_w,
    K_a,
    K_s,
    K_d,

    KMOD_SHIFT,

    MOUSEBUTTONUP,
)

from pygame.font import SysFont, get_fonts, match_font

from pygame.math import Vector2

from pygame.transform import smoothscale


### local imports

from ...config import (
    APP_REFS,
    SAMPLE_UNICODE_CHARS_PATH,
    SORTED_SYS_FONT_NAMES,
)

from ...pygamesetup import SCREEN_RECT, SERVICES_NS

from ...dialog import show_dialog_from_key

from ...logman.main import get_new_logger

from ...ourstdlibs.pyl import load_pyl

from ...our3rdlibs.userlogger import USER_LOGGER

from ...loopman.main import LoopHolder

from ...classes2d.single import Object2D

from ...classes2d.collections import List2D

from ...surfsman.render import render_rect

from ...textman.render import render_text

from ...fontsman.preview.cache import FONT_PREVIEWS_DB

from ...fontsman.constants import ENC_SANS_BOLD_FONT_PATH

from ...fontsman.cache import UnattainableFontHeightError



### module level contants/values/objects

try:
    SAMPLE_UNICODE_CHARS_DATA = load_pyl(SAMPLE_UNICODE_CHARS_PATH)

except Exception as err:
    raise RuntimeError("Couldn't load sample unicode characters") from err


FONT_LIST_ITEM_SIZE = (640, 90)
FONT_PREVIEW_AREA_SIZE = (640, 65)

PLACEHOLDER_PREVIEW_SURF = Surface(FONT_LIST_ITEM_SIZE).convert()
PLACEHOLDER_PREVIEW_SURF.fill('white')

PREVIEW_CHARS = ' '.join(

    chain(

        char_group.replace(',', '').replace(' ', '') + ' '

        for _, char_group in SAMPLE_UNICODE_CHARS_DATA

    )

)

FONT_PREVIEW_SETTINGS = {
    'font_size': 22,
    'chars': PREVIEW_CHARS,
    'width': FONT_PREVIEW_AREA_SIZE[0],
    'height': FONT_PREVIEW_AREA_SIZE[1],
    'not_found_width': FONT_PREVIEW_AREA_SIZE[0],
    'not_found_height': FONT_PREVIEW_AREA_SIZE[1],
}

## create logger for module
logger = get_new_logger(__name__)


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
            Object2D.from_surface(render_rect(420, 560, (255, 255, 255)))
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

        ### reference important objects

        self.no_preview_surf = font_preview_panel.image

        self.blit_onto_all_fonts_panel = all_fonts_panel.image.blit
        self.fill_all_fonts_panel = all_fonts_panel.image.fill

        self.all_fonts_rect = all_fonts_panel.rect
        self.all_fonts_panel_colliderect = all_fonts_panel.rect.colliderect

        ###

        sys_font_2d_objs = self.sys_font_2d_objs = List2D(

            Object2D.from_surface(
                PLACEHOLDER_PREVIEW_SURF,
                font_name = font_name,
            )

            for font_name in SORTED_SYS_FONT_NAMES

        )

        sys_font_2d_objs_rect = self.sys_font_2d_objs_rect = (
            sys_font_2d_objs.rect
        )

        sys_font_2d_objs_rect.snap_rects_ip(

            retrieve_pos_from='bottomleft',
            assign_pos_to='topleft',
            offset_pos_by=(0, 5),

        )

        sys_font_2d_objs_rect.topleft = all_fonts_panel.rect.topleft

        ###
        self.selected_font_2d_objs = List2D()
        self.font_names = ('',)
        self.previewed_font_name = ''

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

        ### if list obtained from pygame.font.get_fonts() is empty,
        ### it shouldn't be possible to use this system fonts picker;
        ###
        ### in such case, we display a dialog instead and exit immediatelly;

        if not SORTED_SYS_FONT_NAMES:

            show_dialog_from_key(
                'cant_use_picker_for_no_system_fonts_were_detected'
            )

            return None

        ###

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
            self.update_preview(self.font_name)

        else:
            self.font_preview_panel.image.fill('white')

        ###
        self.loop()

        ###
        return self.font_names

    def update_preview(self, font_name):

        ### TODO
        ### - should blit name of font using default font and
        ### this custom font being previewed

        if font_name == self.previewed_font_name: return

        ###
        self.previewed_font_name = font_name

        ### render and align text objects

        label_texts, char_texts = zip(*SAMPLE_UNICODE_CHARS_DATA)

        labels_2d = List2D(

            Object2D.from_surface(

                render_text(
                    f'{label_text}:',
                    font_height=24,
                    font_key=ENC_SANS_BOLD_FONT_PATH,
                )

            )

            for label_text in label_texts

        )

        char_groups = [
            char_text.replace(',', '')
            for char_text in char_texts
        ]

        ### TODO
        ### - should protect against pygame.error ("Text has zero width")
        ### - should protect against custom UnattainableFontHeightError
        ### (like raised from "notocoloremoji" font)

        char_groups_2d = List2D(


            Object2D.from_surface(
                render_text(
                    text=char_group,
                    font_height=24,
                    font_key=font_name,
                )
            )


            for char_group in char_groups

        )

        labels_2d.rect.snap_rects_ip(
            retrieve_pos_from='bottomleft',
            assign_pos_to='topleft',
        )

        labels_2d.rect.move_ip(4, 4)

        padded_max_right = (
            max(label_2d.rect.right for label_2d in labels_2d) + 4
        )

        for label_2d, char_group in zip(labels_2d, char_groups_2d):
            char_group.rect.topleft = (padded_max_right, label_2d.rect.top)

        ### blit onto preview surface

        self.font_preview_panel.image.fill('white')

        blit_on_preview = self.font_preview_panel.image.blit

        for label_2d, char_group in zip(labels_2d, char_groups_2d):

            blit_on_preview(label_2d.image, label_2d.rect)
            blit_on_preview(char_group.image, char_group.rect)

    def handle_input(self):

        self.handle_events()
        self.handle_key_states()

    def handle_events(self):

        for event in SERVICES_NS.get_events():

            if event.type == MOUSEBUTTONUP:
                self.on_mouse_release(event)

            elif event.type == KEYUP:

                if event.key in (K_RETURN, K_KP_ENTER, K_ESCAPE):

                    self.running = False
                    self.font_names = None

            elif event.type == QUIT:

                self.running = False
                self.font_names = None

    def on_mouse_release(self, event):

        mouse_pos = event.pos

        shift_pressed = SERVICES_NS.get_pressed_mod_keys() & KMOD_SHIFT

        if self.all_fonts_rect.collidepoint(mouse_pos):
            
            colliderect = self.all_fonts_panel_colliderect

            for obj in self.sys_font_2d_objs:

                if colliderect(obj.rect) and obj.rect.collidepoint(mouse_pos):

                    if not shift_pressed and obj.font_name not in self.font_names:
                        self.font_names += (obj.font_name,)

                    elif shift_pressed and obj.font_name in self.font_names:

                        self.font_names = tuple(
                            obj.font_name
                            for font_name in self.font_names
                            if font_name != obj.font_name
                        )

                    self.font_name = obj.font_name
                    self.update_preview(obj.font_name)

                    return

    def handle_key_states(self):

        key_pressed_states = SERVICES_NS.get_pressed_keys()

        sys_font_2d_objs_rect = self.sys_font_2d_objs_rect


        dy = 0

        if key_pressed_states[K_w] or key_pressed_states[K_UP]:
            dy = 70

        elif key_pressed_states[K_s] or key_pressed_states[K_DOWN]:
            dy = -70

        if dy:

            sys_font_2d_objs_rect.move_ip(0, dy)

            all_fonts_rect = self.all_fonts_rect

            if dy < 0:

                if sys_font_2d_objs_rect.bottom < all_fonts_rect.bottom:
                    sys_font_2d_objs_rect.bottom = all_fonts_rect.bottom

            else:

                if sys_font_2d_objs_rect.top > all_fonts_rect.top:
                    sys_font_2d_objs_rect.top = all_fonts_rect.top

        ###

        if key_pressed_states[K_a] or key_pressed_states[K_LEFT]:
            ... #self.char_objs.rect.move_ip(-20, 0)

        elif key_pressed_states[K_d] or key_pressed_states[K_RIGHT]:
            ... #self.char_objs.rect.move_ip(0, 20)

    def draw(self):

        super().draw()

        offset = -Vector2(self.all_fonts_rect.topleft)
        colliderect = self.all_fonts_panel_colliderect
        blit_operation = self.blit_onto_all_fonts_panel

        self.fill_all_fonts_panel('green')

        for obj in self.sys_font_2d_objs:

            if colliderect(obj.rect):

                if obj.image is PLACEHOLDER_PREVIEW_SURF:
                    update_sys_font_2d_preview(obj)


                blit_operation(obj.image, obj.rect.move(offset))

        for obj in self.all_panels:
            obj.draw()

        ### update screen
        SERVICES_NS.update_screen()


pick_system_fonts = SystemFontsPicker().pick_system_fonts


### helper function

def update_sys_font_2d_preview(obj):

    image = obj.image = PLACEHOLDER_PREVIEW_SURF.copy()

    height = 22

    default_font_text_surf = (

        render_text(
            obj.font_name,
            font_height=height,
            font_key=ENC_SANS_BOLD_FONT_PATH,
        )

    )

    image.blit(default_font_text_surf, (0, 0))

    try:

        current_font_text_surf = (

            render_text(
                obj.font_name,
                font_height=height,
                font_key=obj.font_name,
            )

        )

    except UnattainableFontHeightError as err:

        font_name = obj.font_name

        print(f"Suppressed error for {font_name!r}: {err}")

        final_surf = default_font_text_surf.copy()
        final_surf.fill('white')

        try:

            surf = (
                SysFont(font_name, height)
                .render(font_name, True, 'black', 'white')
                .convert()
            )

        except (PygameError, Exception) as err:

            print(
                "Another suppressed error for"
                f" {font_name!r}: {err}"
            )

            final_surf.fill('red')

        else:

            smoothscale(
                surf,
                default_font_text_surf.get_size(),
                final_surf,
            )

        current_font_text_surf = final_surf

    image.blit(

        current_font_text_surf,

        (
            default_font_text_surf.get_width() + 4,
            0,
        )
    )

    image.blit(
        FONT_PREVIEWS_DB[obj.font_name][FONT_PREVIEW_SETTINGS],
        (0, 25),
    )
