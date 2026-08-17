"""Constants for the splash screen."""

### local imports

from ..config import APP_REFS

from ..colorsman.colors import (
    SPLASH_FONT,
    SPLASH_BG,
    SPLASH_URL_FG,
    SPLASH_URL_BG,
)



TEXT_SETTINGS = {
    'font_height': APP_REFS.general_font_height,
    'font_key': APP_REFS.general_font_key,
    'padding': 0,
    'foreground_color': SPLASH_FONT,
    'background_color': SPLASH_BG,
}

URL_TEXT_SETTINGS = {
    'font_height': APP_REFS.general_font_height,
    'font_key': APP_REFS.general_font_key,
    'padding': 2,
    'foreground_color': SPLASH_URL_FG,
    'background_color': SPLASH_URL_BG,
}

TITLE_FONT_HEIGHT = 68

SOFTWARE_KIND_FONT_HEIGHT = 20
SUBHEADING_FONT_HEIGHT = 28

RELEASE_LEVEL_TEXT_SETTINGS = {
    'font_height': 20,
    'font_key': APP_REFS.general_font_key,
    'padding': 2,
    'foreground_color': SPLASH_BG,
    'background_color': SPLASH_FONT,
}

SHADOW_THICKNESS = 5
