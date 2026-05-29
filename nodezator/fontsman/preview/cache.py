"""Facility for font preview surfaces storage and sharing.

This module provides 02 objects of interest for when we want to reuse
previews of fonts. The other objects are support objects not meant to
be imported/touched in any way.

The ones you want to import are:

1) The FontPreviewsDatabase instance called
   FONT_PREVIEWS_DB

     This is an example of its usage:

     font_preview_surf = (
       FONT_PREVIEWS_DB[font_key][font_settings]
     )

     In other words, here we obtain a cached text surface for the font
     represented by the given key (either the name of a font system as
     a string or the path to a font file as a pathlib.Path object),
     rendered according to the given font settings.

02) the update_cache_for_font_preview() function;
"""

### local imports

from ...ourstdlibs.dictutils import (
    settings_to_hashable_repr,
    hashable_repr_to_settings,
)

from .render import render_font_preview



class FontPreviewsDatabase(dict):
    """Dict to store maps related to font preview surfaces.

    Extends the built-in dict.
    """

    def __missing__(self, key):
        """Create, store and return dict for given key.

        That is, the key is either a string representing the name
        of a system font, or a pathlib.Path object representing the
        location wherein to find a font file.

        Parameters
        ==========
        key (string or pathlib.Path)
            represents name of system font (if a string) or path to font file
            (if a pathlib.Path), for font to be loaded.
        """
        ### we create a surface map for the key, store and
        ### return it

        font_preview_surface_map = self[key] = FontPreviewSurfaceMap(key)

        return font_preview_surface_map


FONT_PREVIEWS_DB = FontPreviewsDatabase()


class FontPreviewSurfaceMap(dict):
    """Map to store font preview surfaces;

    has extra behaviour.
    """

    def __init__(self, font_key):
        """Store font path.

        Parameters
        ==========
        font_key (string or pathlib.Path)
            represents name of system font (if a string) or path to font file
            (if a pathlib.Path), for font to be loaded.
        """
        self.font_key = font_key

    def __getitem__(self, font_settings):
        """Return surface showing text rendered with font and given settings.

        Parameters
        ==========
        font_settings (dict)
            contains settings defining how the font must
            be rendered;
        """
        ### convert the render settings (a dict) to a custom
        ### tuple representing them, to use as dictionary key
        tuple_key = settings_to_hashable_repr(font_settings)

        ### try returning the value for the tuple we
        ### just obtained, which, if existent, should
        ### be a surface rendered with the corresponding
        ### settings
        try:
            return super().__getitem__(tuple_key)

        ### if such value doesn't exist (a key error is
        ### raised), we create the corresponding surface,
        ### and return it while at the same time creating
        ### a new item using the tuple key

        except KeyError:

            return self.setdefault(
                tuple_key, render_font_preview(self.font_key, **font_settings)
            )


###


def update_cache_for_font_preview(font_key):

    surf_map = FONT_PREVIEWS_DB[font_key]
    existing_keys = list(surf_map)

    for key in existing_keys:

        font_settings = hashable_repr_to_settings(key)

        old_surf = surf_map[font_settings]

        new_surf = render_font_preview(font_key, **font_settings)

        if old_surf.get_size() == new_surf.get_size():
            old_surf.blit(new_surf, (0, 0))

        else:
            surf_map[key] = new_surf
