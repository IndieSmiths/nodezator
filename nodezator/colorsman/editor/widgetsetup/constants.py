"""Constants for setting up the colors editor's widgets."""

### local import
from ....config import APP_REFS


### height of text in pixels; also used as the height for
### widgets
FONT_HEIGHT = APP_REFS.general_font_height

### padding of text in pixels; it is creates additional padding in addition
### to the height of text, but it is not used in widgets
TEXT_PADDING = 5


### icon

ICON_HEIGHT = FONT_HEIGHT
ICON_PADDING = 5
ICON_BG_HEIGHT = ICON_HEIGHT + (ICON_PADDING * 2)
