"""Constants for the callable node class."""

### local imports

from ...config import APP_REFS

from ...fontsman.constants import (
    NOTO_SANS_REGULAR_FONT_PATH,
    NOTO_SANS_FONT_HEIGHT,
    NOTO_SANS_MONO_MEDIUM_FONT_PATH,
    NOTO_SANS_MONO_MEDIUM_FONT_HEIGHT,
)

from ...colorsman.colors import (
    NODE_BODY_BG,
    COMMENTED_OUT_NODE_BG,
    NODE_LABELS,
)



NODE_OUTLINE_THICKNESS = 2

NODE_CORNER_RADIUS = 6

BODY_CONTENT_OFFSET = APP_REFS.general_font_height + 2

### distance between outputs
DISTANCE_BETWEEN_OUTPUTS = 4

### distance from a variable parameter's label to its
### first subparameter
SUBPARAM_OFFSET_FROM_LABEL = 2

### width of subparameter keyword entries
SUBPARAM_KEYWORD_ENTRY_WIDTH = 140

### distance between parameters
DISTANCE_BETWEEN_PARAMS = 4

### distance between subparameters
DISTANCE_BETWEEN_SUBPARAMS = 8

### distance between last output's bottom and the first input
INPUT_OFFSET = 4

### label text (input and output labels)

NORMAL_LABEL_TEXT_SETTINGS = {
    'font_key': APP_REFS.general_font_key,
    'font_height': APP_REFS.general_font_height,
    'foreground_color': NODE_LABELS,
    'background_color': NODE_BODY_BG,
}

COMMENTED_OUT_LABEL_TEXT_SETTINGS = {
    'font_key': APP_REFS.general_font_key,
    'font_height': APP_REFS.general_font_height,
    'foreground_color': NODE_LABELS,
    'background_color': COMMENTED_OUT_NODE_BG,
}


### side visualization text

SIDEVIZ_TEXT_SETTINGS = {
    'font_height': NOTO_SANS_FONT_HEIGHT,
    'font_path': NOTO_SANS_REGULAR_FONT_PATH,
    'foreground_color': (15, 15, 15),
    'background_color': (230, 230, 235),
}

SIDEVIZ_MONOSPACED_TEXT_SETTINGS = {
    'font_height': NOTO_SANS_MONO_MEDIUM_FONT_HEIGHT,
    'font_path': NOTO_SANS_MONO_MEDIUM_FONT_PATH,
    'foreground_color': (15, 15, 15),
    'background_color': (230, 230, 235),
}

SIDEVIZ_PYTHON_SOURCE_SETTINGS = {
    'font_height': NOTO_SANS_MONO_MEDIUM_FONT_HEIGHT,
    'font_path': NOTO_SANS_MONO_MEDIUM_FONT_PATH,
    'foreground_color': (235, 235, 235),
    'background_color': (15, 15, 15),
}
