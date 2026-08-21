"""Facility with functions for initial positioning of file manager contents."""

### local imports

from .constants import (
    CURRENT_LABEL_TOP,
    PANELS_LABELS_TOP,
    FILEMAN_WIDTH,
    DIR_PANEL_WIDTH,
    BKM_PANEL_WIDTH,
    FONT_HEIGHT,
)



def perform_initial_positioning(fm):
    """Position objects from given file manager.

    Parameters
    ==========
    fm (fileman.main.FileManager instance)
    """

    fm.navigation_entry.rect.left = fm.navigation_entry_offset[0]
    fm.navigation_entry.rect.top = CURRENT_LABEL_TOP

    dp = fm.dir_panel

    dp.rect.left = 10
    dp.rect.top = PANELS_LABELS_TOP + FONT_HEIGHT
    dp.path_objects.rect.topleft = dp.rect.move(1, 1).topleft

    bp = fm.bkm_panel

    bp.rect.left = dp.rect.right + 10
    bp.rect.top = dp.rect.top
    bp.bookmark_objs.rect.topleft = bp.rect.move(1, 1).topleft

    fm.selection_entry.rect.left = 100
    fm.selection_entry.rect.top = dp.rect.bottom

