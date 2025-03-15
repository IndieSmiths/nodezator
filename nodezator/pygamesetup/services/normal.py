
### standard library imports
from warnings import catch_warnings, simplefilter


### third-party imports

from pygame.locals import RESIZABLE

from pygame.version import vernum as pygame_vernum

from pygame.display import set_mode

from pygame.event import get as get_events, set_allowed

from pygame.key import (
    get_pressed as get_pressed_keys,
    get_mods as get_pressed_mod_keys,
    stop_text_input,
)

from pygame.mouse import (
    set_visible as set_mouse_visibility,
    get_pos as get_mouse_pos,
    set_pos as set_mouse_pos,
    get_pressed as get_mouse_pressed,
)

from pygame.display import update as update_screen


### local imports

from ..constants import (
    SCREEN,
    SCREEN_RECT,
    SIZE,
    GENERAL_NS,
    GENERAL_SERVICE_NAMES,
    FPS,
    maintain_fps,
    watch_window_size,
)



### create and use function to activate normal behaviour

def set_behaviour(services_namespace, reset_window_mode=True):
    """Setup normal mode."""
    ### set normal services as current ones.

    our_globals = globals()

    for attr_name in GENERAL_SERVICE_NAMES:

        value = our_globals[attr_name]
        setattr(services_namespace, attr_name, value)

    ### allow all kinds of events (by passing None to
    ### pygame.event.set_allowed), except text input ones (by
    ### stopping text input events),
    ### which should be enabled only when appropriate

    set_allowed(None)
    stop_text_input()

    ### reset window mode if requested

    if reset_window_mode:

        ### use pygame.display.set_mode

        ## under the circumstances in the if-block below, set_mode() raises
        ## a warning that shouldn't be raised (as explained in issue #3385 of
        ## pygame-ce's repository), so we make the call in a context that
        ## temporarily suppresses warnings

        if SIZE == (0, 0) and pygame_vernum in ((2, 5, 2), (2, 5, 3)):

            with catch_warnings():
                simplefilter('ignore')
                set_mode(SIZE, RESIZABLE)

        ## otherwise we can make the call normally

        else:
            set_mode(SIZE, RESIZABLE)

        ## perform setups related to window size
        watch_window_size()



def frame_checkups():
    """Perform various checkups.

    Meant to be used at the beginning of each frame in the
    app loop.
    """
    ### keep a constants framerate
    maintain_fps(FPS)

    ### increment frame number
    GENERAL_NS.frame_index += 1

    ### keep an eye on the window size
    watch_window_size()

def frame_checkups_with_fps(fps):
    """Same as frame_checkups(), but uses given fps."""
    ### keep a constants framerate
    maintain_fps(fps)

    ### increment frame number
    GENERAL_NS.frame_index += 1

    ### keep an eye on the window size
    watch_window_size()
