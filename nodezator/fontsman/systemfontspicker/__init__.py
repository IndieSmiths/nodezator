"""Facility w/ class for visualizing and picking system fonts."""

### standard library imports

from itertools import chain

from collections import defaultdict


### third-party imports

from pygame import Rect, Surface, error as PygameError

from pygame.locals import (

    QUIT,

    KEYDOWN,
    KEYUP,

    K_ESCAPE,
    K_RETURN,
    K_KP_ENTER,

    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_PAGEDOWN,
    K_PAGEUP,
    K_HOME,
    K_END,
    K_w,
    K_a,
    K_s,
    K_d,

    KMOD_SHIFT,

    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
)

from pygame.font import SysFont, get_fonts, match_font

from pygame.math import Vector2

from pygame.transform import smoothscale

from pygame.draw import (
    rect as draw_rect,
    line as draw_line,
)


### local imports

from ...config import (
    APP_REFS,
    SAMPLE_UNICODE_CHARS_PATH,
    SORTED_SYS_FONT_NAMES,
)

from ...pygamesetup import SERVICES_NS

from ...pygamesetup.constants import SCREEN_RECT

from ...dialog import show_dialog_from_key

from ...logman.main import get_new_logger

from ...ourstdlibs.pyl import load_pyl

from ...ourstdlibs.collections.general import FactoryDict

from ...our3rdlibs.userlogger import USER_LOGGER

from ...our3rdlibs.button import Button

from ...loopman.main import LoopHolder

from ...classes2d.single import Object2D

from ...classes2d.collections import List2D

from ...surfsman.render import render_rect, combine_surfaces

from ...surfsman.icon import render_layered_icon

from ...textman.render import render_text

from ...fontsman.preview.cache import FONT_PREVIEWS_DB

from ...fontsman.constants import ENC_SANS_BOLD_FONT_PATH

from ...fontsman.cache import UnattainableFontHeightError

from ...colorsman.colors import (
    BUTTON_FG,
    BUTTON_BG,
    WINDOW_FG,
    WINDOW_BG,
)


### module level contants/values/objects

try:
    SAMPLE_UNICODE_CHARS_DATA = load_pyl(SAMPLE_UNICODE_CHARS_PATH)

except Exception as err:
    raise RuntimeError("Couldn't load sample unicode characters") from err


FONT_HEIGHT_FOR_LARGE_PREVIEW = 24

LABEL_TEXTS, _char_texts = zip(*SAMPLE_UNICODE_CHARS_DATA)

STRINGS_WITH_SAMPLE_CHARACTERS = [
    char_text.replace(',', '')
    for char_text in _char_texts
]

LARGE_PREVIEW_LABELS_2D = List2D(

    Object2D.from_surface(

        render_text(
            f'{label_text}:',
            font_height=FONT_HEIGHT_FOR_LARGE_PREVIEW,
            font_key=ENC_SANS_BOLD_FONT_PATH,
        )

    )

    for label_text in LABEL_TEXTS

)

LARGE_PREVIEW_LABELS_2D.rect.snap_rects_ip(
    retrieve_pos_from='bottomleft',
    assign_pos_to='topleft',
)

LARGE_PREVIEW_LABELS_2D.rect.move_ip(4, 0)

LARGE_PREVIEW_LABELS_PADDED_MAX_RIGHT = (
    max(label_2d.rect.right for label_2d in LARGE_PREVIEW_LABELS_2D)
    + 4
)


_SPACE_CHAR = (
    render_text(
        ' ',
        font_height=FONT_HEIGHT_FOR_LARGE_PREVIEW,
        font_key=ENC_SANS_BOLD_FONT_PATH,
    )
)

_RED_TOFU = _SPACE_CHAR.copy()
_RED_TOFU.fill('red')

def _get_custom_tofu(str_with_sample_chars):


    return combine_surfaces(

        surfaces = [

            _SPACE_CHAR if char == ' ' else _RED_TOFU
            for char in str_with_sample_chars

        ],

        retrieve_pos_from='topright',
        assign_pos_to='topleft',

    )

CUSTOM_TOFU_WHEN_CANT_RENDER_CHAR_GROUPS = (

    List2D(


        Object2D.from_surface(
            _get_custom_tofu(str_with_sample_chars)
        )


        for str_with_sample_chars in STRINGS_WITH_SAMPLE_CHARACTERS

    )

)

##

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

##

SELECTED_ITEM_SIZE = (330, 60)

SELECTED_ITEM_CLEARED_SURF = Surface(SELECTED_ITEM_SIZE).convert()
SELECTED_ITEM_CLEARED_SURF.fill('white')

X_SURF = render_layered_icon(
    chars=[chr(126)],
    dimension_name='height',
    dimension_value=20,
    colors=[(204, 0, 0)],
)

X_RECT = X_SURF.get_rect()


## create logger for module
logger = get_new_logger(__name__)


class SystemFontsPicker(Object2D, LoopHolder):
    """Lists system fonts and allows users to pick one or more."""

    def __init__(self):

        caption = (
            Object2D.from_surface(
                render_text(
                    text="Pick system font(s)",
                    foreground_color=WINDOW_FG,
                )
            )
        )

        selected_fonts_panel = self.selected_fonts_panel = (
            Object2D.from_surface(render_rect(1080, 60, (180, 180, 180)))
        )

        available_fonts_panel = (
            Object2D.from_surface(render_rect(640, 580, (180, 180, 180)))
        )

        font_preview_panel = self.font_preview_panel = (
            Object2D.from_surface(render_rect(420, 580, (255, 255, 255)))
        )

        ###

        selected_fonts_panel.rect.topleft = caption.rect.move(0, 50).bottomleft

        available_fonts_panel.rect.topleft = (
            selected_fonts_panel.rect.move(0, 40).bottomleft
        )

        font_preview_panel.rect.topleft = (
            available_fonts_panel.rect.move(40, 0).topright
        )

        ###

        buttons = self.buttons = List2D(

            Button.from_text(
                text=text,
                padding=5,
                foreground_color=BUTTON_FG,
                background_color=BUTTON_BG,
                command=command,
            )

            for text, command in (
                ("Cancel", self.cancel),
                ("Submit", self.submit),
            )

        )

        buttons.rect.snap_rects_ip(
            retrieve_pos_from='topright',
            assign_pos_to='topleft',
            offset_pos_by=(5, 0),
        )

        buttons.rect.topright = font_preview_panel.rect.move(0, 10).bottomright

        ###

        ###

        self.all_objs = List2D(

            (
                caption,
                selected_fonts_panel,
                available_fonts_panel,
                font_preview_panel,
                *buttons,
            )

        )

        self.all_objs.rect.center = SCREEN_RECT.center

        self.rect = self.all_objs.rect.inflate(10, 10)
        self.image = Surface(self.rect.size).convert()
        self.image.fill(WINDOW_BG)

        ### blit labels

        self.blit_labels(
            selected_fonts_panel.rect,
            available_fonts_panel.rect,
            font_preview_panel.rect,
        )

        ### reference important objects

        ## for all fonts panel

        self.available_fonts_panel_surf = available_fonts_panel.image

        self.blit_onto_available_fonts_panel = available_fonts_panel.image.blit
        self.fill_available_fonts_panel = available_fonts_panel.image.fill

        self.available_fonts_rect = available_fonts_panel.rect
        self.available_fonts_panel_colliderect = (
            available_fonts_panel.rect.colliderect
        )

        ## for selected fonts panel

        self.blit_onto_selected_fonts_panel = selected_fonts_panel.image.blit
        self.fill_selected_fonts_panel = selected_fonts_panel.image.fill

        self.selected_fonts_rect = selected_fonts_panel.rect
        self.selected_fonts_panel_colliderect = (
            selected_fonts_panel.rect.colliderect
        )

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

        sys_font_2d_objs_rect.topleft = available_fonts_panel.rect.topleft

        ###
        self.height_of_sys_font_2d_objs = sys_font_2d_objs_rect.height

        ###

        height_percentage = (
            available_fonts_panel.rect.height
            / sys_font_2d_objs_rect.height
        )

        height = round(height_percentage * available_fonts_panel.rect.height)

        scroll_rect = self.scroll_rect = Rect()
        scroll_rect.width = 15
        scroll_rect.height = height if height >= 15 else 15

        scroll_surf = Surface(scroll_rect.size).convert()
        scroll_surf.fill('grey30')

        draw_rect(
            scroll_surf,
            'white',
            scroll_surf.get_rect(),
            1,
        )

        _smaller_rect = scroll_surf.get_rect().inflate(-8, -8)

        for point_name_a, point_name_b in (
            ('topleft', 'topright'),
            ('bottomleft', 'bottomright'),
            ('midleft', 'midright'),
        ):

            draw_line(
                scroll_surf,
                'white',
                getattr(_smaller_rect, point_name_a),
                getattr(_smaller_rect, point_name_b),
                1,
            )

        scroll_rect.topleft = available_fonts_panel.rect.topright

        self.scroll_handle = Object2D()
        self.scroll_handle.image = scroll_surf
        self.scroll_handle.rect = scroll_rect

        ###

        farthest_bottom = sys_font_2d_objs_rect.bottom
        self.nearest_bottom = available_fonts_panel.rect.bottom
        self.height_range = farthest_bottom - self.nearest_bottom

        self.scroll_rect_trav_height = (
            available_fonts_panel.rect.height - scroll_rect.height
        )

        ###
        self.scroll_grab_height = None

        ###

        scroll_guide_rect = available_fonts_panel.rect.copy()
        scroll_guide_rect.left = scroll_guide_rect.right
        scroll_guide_rect.width = 15

        offset = -Vector2(self.rect.topleft)
        draw_rect(self.image, 'grey90', scroll_guide_rect.move(offset))

        ###

        self.selected_font_2d_objs = List2D()

        self.selected_obj_cache = defaultdict(Object2D)

        self.selected_obj_rect_cache = (

            defaultdict(
                Rect(0, 0, *SELECTED_ITEM_SIZE).copy
            )

        )

        self.font_names = ()
        self.previewed_font_name = ''

        ### attributes to assist in scrolling
        self.dx = self.dy = 0
        ###

        ### center system fonts picker and append centering method
        ### as a window resize setup

        self.center_font_viewer()

        APP_REFS.window_resize_setups.append(self.center_font_viewer)

    def center_font_viewer(self):

        diff = Vector2(SCREEN_RECT.center) - self.rect.center

        self.rect.center = SCREEN_RECT.center
        self.all_objs.rect.center = SCREEN_RECT.center

        self.offset = -Vector2(self.rect.topleft)

        self.sys_font_2d_objs.rect.move_ip(diff)

        self.scroll_rect.move_ip(diff)

        if any(item for item in self.font_names):
            self.selected_font_2d_objs.rect.move_ip(diff)

    def blit_labels(
        self,
        selected_fonts_panel_rect,
        available_fonts_panel_rect,
        font_preview_panel_rect,
    ):

        blit_on_image = self.image.blit
        offset = -Vector2(self.rect.topleft)

        for text, rect in (

            ("Selected fonts", selected_fonts_panel_rect),
            ("All available fonts", available_fonts_panel_rect),
            ("Font preview", font_preview_panel_rect),

        ):

            text_surf = (

                render_text(
                    text=text,
                    foreground_color=WINDOW_FG,
                )

            )

            text_rect = text_surf.get_rect()

            text_rect.bottomleft = rect.move(0, -2).topleft

            blit_on_image(text_surf, text_rect.move(offset))


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

        ###
        self.previewed_font_name = ''
        self.font_preview_panel.image.fill('white')

        ### create flag indicating whether picking fonts should be cancelled
        self.must_cancel = False

        ###
        self.loop()

        ###
        return None if self.must_cancel else self.font_names

    def update_preview(self, font_name):

        if font_name == self.previewed_font_name: return

        ###
        self.previewed_font_name = font_name

        ###

        default_font_text_surf, current_font_text_surf = (
            FONT_NAME_SURFS_MAP[font_name]
        )

        def_rect = default_font_text_surf.get_rect()
        cur_rect = current_font_text_surf.get_rect()

        def_rect.topleft = (4, 4)
        cur_rect.topleft = def_rect.move(0, 2).bottomleft

        image = self.font_preview_panel.image
        image.fill('white')

        blit_on_preview = image.blit

        blit_on_preview(default_font_text_surf, def_rect)
        blit_on_preview(current_font_text_surf, cur_rect)

        ### render and align text objects

        try:

            char_groups_2d = List2D(


                Object2D.from_surface(
                    render_text(
                        text=str_with_sample_chars,
                        font_height=FONT_HEIGHT_FOR_LARGE_PREVIEW,
                        font_key=font_name,
                    )
                )

                for str_with_sample_chars in STRINGS_WITH_SAMPLE_CHARACTERS

            )

        except (UnattainableFontHeightError, PygameError, Exception) as err:

            print(
                "Error while trying to generate large preview for"
                f" {font_name}: {err}"
            )

            char_groups_2d = CUSTOM_TOFU_WHEN_CANT_RENDER_CHAR_GROUPS

        LARGE_PREVIEW_LABELS_2D.rect.topleft = cur_rect.move(0, 16).bottomleft

        for label_2d, char_group in (
            zip(LARGE_PREVIEW_LABELS_2D, char_groups_2d)
        ):

            char_group.rect.topleft = (
                LARGE_PREVIEW_LABELS_PADDED_MAX_RIGHT,
                label_2d.rect.top,
            )

        ### blit onto preview surface

        for label_2d, char_group in (
            zip(LARGE_PREVIEW_LABELS_2D, char_groups_2d)
        ):

            blit_on_preview(label_2d.image, label_2d.rect)
            blit_on_preview(char_group.image, char_group.rect)

    def update_selected_objs(self):

        objs = self.selected_font_2d_objs
        objs.clear()

        if not self.font_names:
            return

        append = objs.append
        obj_cache = self.selected_obj_cache
        rect_cache = self.selected_obj_rect_cache

        for index, font_name in enumerate(self.font_names):

            obj = obj_cache[index]

            obj.font_name = font_name

            obj.image = SELECTED_FONT_SURFS_MAP[font_name]
            obj.rect = rect_cache[index]
            append(obj)

        objs.rect.snap_rects_ip(
            retrieve_pos_from = 'topright',
            assign_pos_to = 'topleft',
            offset_pos_by = (4, 0),
        )

        objs.rect.topleft = self.selected_fonts_panel.rect.topleft


    def handle_input(self):

        self.handle_events()
        self.handle_key_states()

    def handle_events(self):

        for event in SERVICES_NS.get_events():

            if event.type == MOUSEBUTTONUP:

                self.on_mouse_release(event)
                self.scroll_grab_height = None

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.on_mouse_click(event)

            elif event.type == KEYDOWN:

                if event.key == K_PAGEDOWN:
                    self.dy += -self.available_fonts_rect.height

                elif event.key == K_PAGEUP:
                    self.dy += self.available_fonts_rect.height

                elif event.key == K_HOME:
                    self.dy += self.height_of_sys_font_2d_objs

                elif event.key == K_END:
                    self.dy += -self.height_of_sys_font_2d_objs

            elif event.type == KEYUP:

                if event.key in (K_RETURN, K_KP_ENTER):
                    self.submit()

                elif event.key == K_ESCAPE:
                    self.cancel()

            elif event.type == QUIT:
                self.cancel()

    def cancel(self):

        self.running = False
        self.must_cancel = True

    def submit(self):
        self.running = False

    def on_mouse_release(self, event):

        mouse_pos = event.pos

        shift_pressed = SERVICES_NS.get_pressed_mod_keys() & KMOD_SHIFT

        if self.available_fonts_rect.collidepoint(mouse_pos):

            colliderect = self.available_fonts_panel_colliderect

            for obj in self.sys_font_2d_objs:

                if colliderect(obj.rect) and obj.rect.collidepoint(mouse_pos):

                    if not shift_pressed and obj.font_name not in self.font_names:
                        self.font_names += (obj.font_name,)

                    elif shift_pressed and obj.font_name in self.font_names:

                        self.font_names = tuple(
                            font_name
                            for font_name in self.font_names
                            if font_name != obj.font_name
                        )

                    self.update_preview(obj.font_name)

                    self.update_selected_objs()

                    return

        elif self.selected_fonts_rect.collidepoint(mouse_pos):

            for obj in self.selected_font_2d_objs:

                X_RECT.topright = obj.rect.topright

                if X_RECT.collidepoint(mouse_pos):

                    self.font_names = tuple(
                        font_name
                        for font_name in self.font_names
                        if font_name != obj.font_name
                    )

                    self.update_selected_objs()

                    return

                elif obj.rect.collidepoint(mouse_pos):

                    self.update_preview(obj.font_name)
                    return

        elif self.buttons.rect.collidepoint(mouse_pos):

            for button in self.buttons:

                if button.rect.collidepoint(mouse_pos):

                    button.command()
                    return

    def on_mouse_click(self, event):

        mouse_pos = event.pos

        if self.scroll_rect.collidepoint(mouse_pos):
            self.scroll_grab_height = mouse_pos[1] - self.scroll_rect.top

    def handle_key_states(self):

        key_pressed_states = SERVICES_NS.get_pressed_keys()


        if key_pressed_states[K_w] or key_pressed_states[K_UP]:
            self.dy += 70

        elif key_pressed_states[K_s] or key_pressed_states[K_DOWN]:
            self.dy += -70

        ###
        if self.dy:
            self.scroll_dy()

        ###

        if key_pressed_states[K_a] or key_pressed_states[K_LEFT]:
            self.dx += 20

        elif key_pressed_states[K_d] or key_pressed_states[K_RIGHT]:
            self.dx += -20

        if self.dx:
            self.scroll_dx()

    def scroll_dy(self, move_scroll_rect=True):

        dy = self.dy
        self.dy = 0

        sys_font_2d_objs_rect = self.sys_font_2d_objs_rect

        sys_font_2d_objs_rect.move_ip(0, dy)

        available_fonts_rect = self.available_fonts_rect

        if dy < 0:

            if sys_font_2d_objs_rect.bottom < available_fonts_rect.bottom:
                sys_font_2d_objs_rect.bottom = available_fonts_rect.bottom

        else:

            if sys_font_2d_objs_rect.top > available_fonts_rect.top:
                sys_font_2d_objs_rect.top = available_fonts_rect.top

        if move_scroll_rect:

            current_bottom = sys_font_2d_objs_rect.bottom

            percentage = 1 - (
                (current_bottom - self.nearest_bottom) / self.height_range
            )

            self.scroll_rect.topleft = (
                available_fonts_rect
                .move(0, self.scroll_rect_trav_height * percentage)
                .topright
            )

    def scroll_dx(self):

        dx = self.dx
        self.dx = 0

        if not self.font_names: return

        objs_rectsman = self.selected_font_2d_objs.rect
        panel_rect = self.selected_fonts_rect

        if objs_rectsman.width <= panel_rect.width: return

        objs_rectsman.move_ip(dx, 0)

        if dx < 0:

            if objs_rectsman.right < panel_rect.right:
                objs_rectsman.right = panel_rect.right

        else:

            if objs_rectsman.left > panel_rect.left:
                objs_rectsman.left = panel_rect.left

    def update(self):

        if self.scroll_grab_height is None: return


        mouse_height = SERVICES_NS.get_mouse_pos()[1]

        scroll_rect = self.scroll_rect
        scroll_rect.top = mouse_height - self.scroll_grab_height

        available_fonts_rect = self.available_fonts_rect

        if scroll_rect.top < available_fonts_rect.top:
            scroll_rect.top = available_fonts_rect.top

        elif scroll_rect.bottom > available_fonts_rect.bottom:
            scroll_rect.bottom = available_fonts_rect.bottom

        ###

        travelled_distance = scroll_rect.top - available_fonts_rect.top
        percentage = 1 - (travelled_distance / self.scroll_rect_trav_height)

        bottom = self.nearest_bottom + (percentage * self.height_range)

        self.dy = bottom - self.sys_font_2d_objs_rect.bottom

        if self.dy:
            self.scroll_dy(move_scroll_rect=False)

    def draw(self):

        ### draw widget's background
        super().draw()

        ### draw on all fonts panel

        offset = -Vector2(self.available_fonts_rect.topleft)
        colliderect = self.available_fonts_panel_colliderect
        blit_operation = self.blit_onto_available_fonts_panel
        available_fonts_panel_surf = self.available_fonts_panel_surf

        font_names = self.font_names

        self.fill_available_fonts_panel('grey80')

        for obj in self.sys_font_2d_objs:

            if colliderect(obj.rect):

                if obj.image is PLACEHOLDER_PREVIEW_SURF:
                    _update_sys_font_2d_list_item(obj)

                offset_rect = obj.rect.move(offset)

                blit_operation(obj.image, offset_rect)

                if obj.font_name in font_names:

                    draw_rect(
                        available_fonts_panel_surf,
                        'blue',
                        offset_rect,
                        2,
                    )

        ### draw on selected fonts panel

        self.fill_selected_fonts_panel('grey80')

        offset = -Vector2(self.selected_fonts_rect.topleft)
        colliderect = self.selected_fonts_panel_colliderect
        blit_operation = self.blit_onto_selected_fonts_panel

        for obj in self.selected_font_2d_objs:

            if colliderect(obj.rect):
                blit_operation(obj.image, obj.rect.move(offset))

        ### draw panels

        for obj in self.all_objs:
            obj.draw()

        ### scroll handle
        self.scroll_handle.draw()

        ### update screen
        SERVICES_NS.update_screen()


pick_system_fonts = SystemFontsPicker().pick_system_fonts


### helper functions/objects

def _update_sys_font_2d_list_item(obj):

    image = obj.image = PLACEHOLDER_PREVIEW_SURF.copy()

    font_name = obj.font_name

    default_font_text_surf, current_font_text_surf = (
        FONT_NAME_SURFS_MAP[font_name]
    )

    image.blit(default_font_text_surf, (0, 0))
    image.blit(

        current_font_text_surf,

        (
            default_font_text_surf.get_width() + 4,
            0,
        )
    )

    image.blit(
        FONT_PREVIEWS_DB[font_name][FONT_PREVIEW_SETTINGS],
        (0, 25),
    )

## cache for preview of selected fonts

def _create_surf_for_selected_font(font_name):

    image = SELECTED_ITEM_CLEARED_SURF.copy()

    default_font_text_surf, current_font_text_surf = (
        FONT_NAME_SURFS_MAP[font_name]
    )

    image.blit(default_font_text_surf, (2, 2))
    image.blit(

        current_font_text_surf,

        (

            2,
            default_font_text_surf.get_height() + 2,

        )
    )

    X_RECT.top = 0
    X_RECT.right = image.get_width()

    image.blit(X_SURF, X_RECT)

    return image

SELECTED_FONT_SURFS_MAP = FactoryDict(_create_surf_for_selected_font)


## default and custom font name surf caches

def _get_font_name_surfs(font_name):

    height = FONT_PREVIEW_SETTINGS['font_size']

    default_surf = render_text(
        font_name,
        font_height=height,
        font_key=ENC_SANS_BOLD_FONT_PATH,
    )

    custom_surf = _get_custom_font_text_surf(

        font_name,
        height,
        default_surf,

    )

    return (default_surf, custom_surf)

FONT_NAME_SURFS_MAP = FactoryDict(_get_font_name_surfs)


def _get_custom_font_text_surf(font_name, height, default_surf):

    try:

        current_font_text_surf = (

            render_text(
                font_name,
                font_height=height,
                font_key=font_name,
            )

        )

    except UnattainableFontHeightError as err:

        print(f"Suppressed error for {font_name!r}: {err}")

        final_surf = default_surf.copy()
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
                default_surf.get_size(),
                final_surf,
            )

        current_font_text_surf = final_surf

    return current_font_text_surf
