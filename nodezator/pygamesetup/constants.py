
### standard library import
from functools import partial


### third-party imports

from pygame import (
    init as init_pygame,
    get_sdl_version,
    locals as pygame_locals,
    Surface,
)

from pygame.mixer import pre_init as pre_init_mixer

from pygame.key import set_repeat

from pygame.locals import RESIZABLE, KMOD_NONE

from pygame.time import Clock

from pygame.font import SysFont

from pygame.draw import rect as draw_rect

from pygame.display import set_icon, set_caption, set_mode

from pygame.image import load as load_image


# choose appropriate window resize event type according to
# availability

try:
    from pygame.locals import WINDOWRESIZED
except ImportError:
    from pygame.locals import VIDEORESIZE
    WINDOW_RESIZE_EVENT_TYPE = VIDEORESIZE
else:
    WINDOW_RESIZE_EVENT_TYPE = WINDOWRESIZED


### local imports

from ..config import APP_REFS, DATA_DIR

from ..appinfo import FULL_TITLE, ABBREVIATED_TITLE



### pygame initialization setups

## pygame mixer pre-initialization
pre_init_mixer(44100, -16, 2, 4096)

## pygame initialization
init_pygame()


### create a callable to reset the caption to a
### default state whenever needed, then use
### it to set the caption

reset_caption = partial(set_caption, FULL_TITLE, ABBREVIATED_TITLE)
reset_caption()

### set icon and caption for window

image_path = str(DATA_DIR / "app_icon.png")
set_icon(load_image(image_path))


### set key repeating (unit: milliseconds)

set_repeat(
    500, # delay (time before repetition begins)
    30, # interval (interval between repetitions)
)


### create/set screen

SIZE = (
    # this value causes window size to equal screen resolution
    (0, 0)
    if get_sdl_version() >= (1, 2, 10)

    # if sld isn't >= (1, 2, 10) though, it would raise an exception,
    # so we need to provide a proper size
    else (1280, 720)
)

SCREEN = set_mode(SIZE, RESIZABLE)
SCREEN_RECT = SCREEN.get_rect()
blit_on_screen = SCREEN.blit



### framerate-related values/objects

FPS = 24

_CLOCK = Clock()

maintain_fps = _CLOCK.tick
get_fps = _CLOCK.get_fps


### anonymous object to keep track of general values;
###
### values are introduced/update during app's usage:
### frame index is incremented, reset to -1, mode name
### is changed as we switch to other modes, etc.

GENERAL_NS = type("Object", (), {})()

GENERAL_NS.frame_index = -1
GENERAL_NS.mode_name = 'normal'


### name of key pygame services used by all different modes

GENERAL_SERVICE_NAMES = (

    "get_events",

    "get_pressed_keys",
    "get_pressed_mod_keys",

    "get_mouse_pos",
    "get_mouse_pressed",

    "set_mouse_pos",
    "set_mouse_visibility",

    "update_screen",

    "frame_checkups",
    "frame_checkups_with_fps",

)

### label text rendering operations

render_label_text = SysFont('Arial', 16, bold=True).render

Object = type("Object", (), {})

def get_label_object(text, label_fg, label_bg, label_outline, padding):

    ### render the text itself

    text_surface = render_label_text(
        text,
        True,
        label_fg,
        label_bg,
    )

    ### create a surface with the sides incremented by
    ### double the padding

    label_surface = (

        Surface(

            tuple(
                v + (padding * 2)
                for v in text_surface.get_size()
            )

        ).convert()

    )

    ### fill the surface with the outline color
    label_surface.fill(label_outline)

    ### draw a slightly smaller rect inside the surface with the
    ### filling color

    draw_rect(
        label_surface,
        label_bg,
        label_surface.get_rect().inflate(-2, -2),
    )

    ### blit the text inside the surface where the padding
    ### ends
    label_surface.blit(text_surface, (padding, padding))

    ### create label rect
    label_rect = label_surface.get_rect()

    ### instantiate and populate label object

    label = Object()
    label.__dict__.update(image=label_surface, rect=label_rect)

    ### finally return the label
    return label


## event values to strip

EVENT_KEY_STRIP_MAP = {

  'MOUSEMOTION': {
    'buttons': (0, 0, 0),
    'touch': False,
    'window': None,
  },

  'MOUSEBUTTONDOWN': {
    'button': 1,
    'touch': False,
    'window': None,
  },

  'MOUSEBUTTONUP': {
    'button': 1,
    'touch': False,
    'window': None,
  },

  'KEYUP': {
    'mod': KMOD_NONE,
    'unicode': '',
    'window': None,
  },

  'KEYDOWN': {
    'mod': KMOD_NONE,
    'unicode': '',
    'window': None,
  },

  'TEXTINPUT': {
    'window': None,
  },

}

### event name to make compact

EVENT_COMPACT_NAME_MAP = {
    'KEYDOWN': 'kd',
    'KEYUP': 'ku',
    'MOUSEMOTION': 'mm',
    'MOUSEBUTTONUP': 'mbu',
    'MOUSEBUTTONDOWN': 'mbd',
}


### available keys

KEYS_MAP = {

    item : getattr(pygame_locals, item)

    for item in dir(pygame_locals)

    if item.startswith('K_')

}

SCANCODE_NAMES_MAP = {

    getattr(pygame_locals, name): name

    for name in dir(pygame_locals)

    if name.startswith('KSCAN')

}


MOD_KEYS_MAP = {

    item: getattr(pygame_locals, item)

    for item in dir(pygame_locals)

    if (
        item.startswith('KMOD')
        and item != 'KMOD_NONE'
    )

}


### temporary file cleaning

def clean_temp_files():
    """Clean temporary files."""

    ### remove temporary paths
    APP_REFS.temp_filepaths_man.ensure_removed()

    ### remove swap path if it there's one

    try:
        swap_path = APP_REFS.swap_path
    except AttributeError:
        pass
    else:
        swap_path.unlink()


### 

def watch_window_size():
    """Perform setups needed if window was resized."""
    ### obtain current size
    current_size = SCREEN.get_size()

    ### if current screen size is different from the one
    ### we stored...

    if current_size != SCREEN_RECT.size:

        ### perform window resize setups

        SCREEN_RECT.size = current_size
        APP_REFS.window_resize_setups()

        ### redraw the window manager
        APP_REFS.window_manager.draw()

        ### update the screen copy
        APP_REFS.SCREEN_COPY = SCREEN.copy()

        ### if there's a request to draw after the setups,
        ### do so and delete the request

        if hasattr(
            APP_REFS,
            "draw_after_window_resize_setups",
        ):

            APP_REFS.draw_after_window_resize_setups()
            del APP_REFS.draw_after_window_resize_setups
