"""Common surfaces for nodes."""

### third-party imports

from pygame import Surface, Rect

from pygame.draw import line as draw_line

from pygame.transform import rotate as rotate_surface


### local imports

from ...ourstdlibs.collections.general import FactoryDict

from ...surfsman.render import (
    render_rect,
    render_surface_from_svg_text,
    combine_surfaces,
)

from ...surfsman.icon import render_layered_icon

from ...surfsman.cache import NOT_FOUND_SURF_MAP

from ...svgutils.generalshapes import (
    get_circle_svg_text_from_radius,
    get_polygon_svg_text,
)

from ...svgobjs.elements import SVG, Circle
from ...svgobjs.utils import get_svg_formatted_color

from ...fontsman.constants import FIRA_MONO_BOLD_FONT_PATH

from ...colorsman.colors import (
    NODE_BODY_BG,
    COMMENTED_OUT_NODE_BG,
    NODE_OUTLINE,
    NODE_KEYWORD_KEY_OUTLINE,
    NODE_KEYWORD_KEY_FILL,
    WIDGET_ADD_BUTTON_FILL,
    WIDGET_ADD_BUTTON_OUTLINE,
    WIDGET_REMOVE_BUTTON_FILL,
    WIDGET_REMOVE_BUTTON_OUTLINE,
    SUBP_MOVE_BUTTON_FG,
    SUBP_MOVE_BUTTON_BG,
    NODE_CATEGORY_COLORS,
    UNPACKING_ICON_COLOR,
    BLACK,
)

from .constants import NODE_OUTLINE_THICKNESS, NODE_CORNER_RADIUS



###### create map of top corner surfaces

def _get_top_corners(fill_color):
    """Create 2-tuple of top corners of given color."""

    radius = NODE_CORNER_RADIUS
    outline = NODE_OUTLINE_THICKNESS

    outline_increment = outline - 1 if outline % 2 else outline

    height = width = radius*2 + outline_increment

    cx = cy = width // 2

    circle_surf = (

        render_surface_from_svg_text(

            str(

                SVG(

                    width  = width,
                    height = height,

                    children=[

                        Circle(
                            r=radius,
                            cx=cx,
                            cy=cy,
                            fill=get_svg_formatted_color(fill_color),
                            stroke=get_svg_formatted_color(NODE_OUTLINE),
                            stroke_width=outline,
                        )

                    ]

                )
            )

        )

    )

    rect = circle_surf.get_rect()

    corner_size = tuple(n//2 for n in rect.size)

    return (
        circle_surf.subsurface((0, 0), corner_size),
        circle_surf.subsurface(rect.midtop, corner_size),
    )


TOP_CORNERS_MAP = FactoryDict(_get_top_corners)


##

def _get_bottom_corners(fill_color):
    """Create 2-tuple of bottom corners of given color."""

    radius = NODE_CORNER_RADIUS
    outline = NODE_OUTLINE_THICKNESS

    outline_increment = outline - 1 if outline % 2 else outline

    height = width = radius*2 + outline_increment

    cx = cy = width // 2

    circle_surf = (

        render_surface_from_svg_text(

            str(

                SVG(

                    width  = width,
                    height = height,

                    children=[

                        Circle(
                            r=radius,
                            cx=cx,
                            cy=cy,
                            fill=get_svg_formatted_color(fill_color),
                            stroke=get_svg_formatted_color(NODE_OUTLINE),
                            stroke_width=outline,
                        )

                    ]

                )
            )

        )

    )

    rect = circle_surf.get_rect()

    corner_size = tuple(n//2 for n in rect.size)

    return (
        circle_surf.subsurface((0, rect.centery), corner_size),
        circle_surf.subsurface((rect.centerx, rect.centery), corner_size),
    )


(
    NORMAL_BOTTOM_CORNERS,
    COMMENTED_OUT_BOTTOM_CORNERS,
) = (

    _get_bottom_corners(fill_color)

    for fill_color in (

        ## normal bottom corners
        NODE_BODY_BG,

        ## commented out bottom corners
        COMMENTED_OUT_NODE_BG,

    )

)


##
CORNER_WIDTH, CORNER_HEIGHT = NORMAL_BOTTOM_CORNERS[0].get_size()


###### create map of roof surfaces (rectangle between top
###### corners)

def _get_node_roof(width, fill_color):

    roof_width = width - (CORNER_WIDTH*2)
    roof_height = CORNER_HEIGHT

    roof = render_rect(
        roof_width,
        roof_height,
        fill_color,
    )

    draw_line(
        roof,
        NODE_OUTLINE,
        (0, 0),
        (roof_width, 0),
        NODE_OUTLINE_THICKNESS,
    )

    return roof


NODE_ROOFS_MAP = FactoryDict(_get_node_roof)


###### create map to store body head surfaces
######
###### a surf representing the head part of a node's body,
###### which has the same color of the node's roof and top
###### corners in order to look like they all are a single
###### object

def _unpack_for_render_rect(args):
    return render_rect(*args)

BODY_HEAD_SURFS_MAP = FactoryDict(_unpack_for_render_rect)


###### create map of node foot surfaces (rectangle between bottom
###### corners)

def _get_node_foot(args):
    width, fill_color = args

    foot_width = width - (CORNER_WIDTH*2)
    foot_height = CORNER_HEIGHT

    foot = render_rect(
        foot_width,
        CORNER_HEIGHT,
        fill_color,
    )

    # since line thickness is applied from top to bottom,
    # we had to use a value equivalent to the foot height
    # minus the thickness of the line

    line_bottom = foot_height - NODE_OUTLINE_THICKNESS

    line_start = (0, line_bottom)
    line_end = (foot_width, line_bottom)

    draw_line(foot, NODE_OUTLINE, line_start, line_end, NODE_OUTLINE_THICKNESS)

    return foot


NODE_FOOTS_MAP = FactoryDict(_get_node_foot)


###### create map of surfaces for sigmode toggle button


def get_button_surfs(bg_color):
    """Create 2-tuple of surfaces with given background color."""

    size = (10, 10)

    rect = Rect(0, 0, *size)

    polygon_points1 = tuple(

        getattr(rect, attr_name)
        for attr_name in ('topleft', 'midbottom', 'topright')

    )

    polygon_points2 = tuple(

        getattr(rect, attr_name)
        for attr_name in ('topleft', 'midright', 'bottomleft')

    )

    polygon_surf1 = (

        render_surface_from_svg_text(

            get_polygon_svg_text(
                width=10,
                height=10,
                points=polygon_points1,
                fill_color=(255, 255, 255),
                outline_color=None,
            )

        )

    )

    polygon_surf2 = (

        render_surface_from_svg_text(

            get_polygon_svg_text(
                width=10,
                height=10,
                points=polygon_points2,
                fill_color=(255, 255, 255),
                outline_color=None,
            )

        )

    )


    surf1 = Surface(size).convert()
    surf1.fill(bg_color)
    surf2 = surf1.copy()

    surf1.blit(polygon_surf1, (0, 0))
    surf2.blit(polygon_surf2, (0, 0))

    return (surf1, surf2)


SIGMODE_TOGGLE_BUTTON_MAP = FactoryDict(get_button_surfs)


###### load and store other commonly used surfaces

### add/remove buttons' surfaces

ADD_BUTTON_SURF, REMOVE_BUTTON_SURF = (

    render_layered_icon(
        chars=[chr(ordinal) for ordinal in ordinals],
        dimension_name="height",
        dimension_value=14,
        colors=colors,
        background_width=14,
        background_height=14,
    )

    for ordinals, colors in (

        (
            (79, 80),
            (WIDGET_ADD_BUTTON_OUTLINE, WIDGET_ADD_BUTTON_FILL),
        ),

        (
            (125, 126),
            (WIDGET_REMOVE_BUTTON_OUTLINE, WIDGET_REMOVE_BUTTON_FILL),
        ),

    )

)


### subparameter moving buttons

(SUBP_UP_BUTTON_SURF, SUBP_DOWN_BUTTON_SURF) = (

    render_layered_icon(
        chars=[chr(82)],
        dimension_name="height",
        dimension_value=7,
        colors=[SUBP_MOVE_BUTTON_FG],
        background_width=10,
        background_height=10,
        offset_pos_by=(-1, -1),
        background_color=SUBP_MOVE_BUTTON_BG,
        flip_x=flip_x,
        flip_y=flip_y,
        depth_finish_thickness=1,
    )

    for flip_x, flip_y in (
        (False, False),
        (False, True),
    )

)


### subparameter unpacking buttons

(

    NORMAL_ITERABLE_UNPACKING_SURF,
    COMMENTED_OUT_ITERABLE_UNPACKING_SURF,

) = (

    render_layered_icon(
        chars="*",
        font_path=FIRA_MONO_BOLD_FONT_PATH,
        dimension_name="height",
        dimension_value=14,
        colors=[UNPACKING_ICON_COLOR],
        background_width=16,
        background_height=16,
        background_color=bg_color,
    )

    for bg_color in (
        NODE_BODY_BG,
        COMMENTED_OUT_NODE_BG,
    )

)


(

    NORMAL_DICT_UNPACKING_SURF,
    COMMENTED_OUT_DICT_UNPACKING_SURF,

) = (

    combine_surfaces(

        [
            surf,
            surf,
        ],

        background_color=bg_color,

    )

    for surf, bg_color in (

        (
            NORMAL_ITERABLE_UNPACKING_SURF,
            NODE_BODY_BG,
        ),

        (
            COMMENTED_OUT_ITERABLE_UNPACKING_SURF,
            COMMENTED_OUT_NODE_BG,
        ),

    )

)

UNPACKING_ICON_SURFS_MAP = {
    ("var_pos", False): NORMAL_ITERABLE_UNPACKING_SURF,
    ("var_pos", True): COMMENTED_OUT_ITERABLE_UNPACKING_SURF,
    ("var_key", False): NORMAL_DICT_UNPACKING_SURF,
    ("var_key", True): COMMENTED_OUT_DICT_UNPACKING_SURF,
}


### keyword key icon surf and its rect

KEYWORD_KEY_SURF = render_layered_icon(

    chars=[chr(ordinal) for ordinal in (102, 103)],
    dimension_name="height",
    dimension_value=16,

    colors=[
        NODE_KEYWORD_KEY_OUTLINE,
        NODE_KEYWORD_KEY_FILL,
    ],

    background_width=16,
    background_height=16,

)

KEYWORD_KEY_RECT = KEYWORD_KEY_SURF.get_rect()


### reload icon for preview toolbar button 

_arrow_up = render_layered_icon(

    chars=[chr(ordinal) for ordinal in (52, 53)],
    dimension_name="width",
    dimension_value=18,
    colors=[BLACK, (30, 130, 70)],
    background_width=20,
    background_height=20,
    retrieve_pos_from="midbottom",
    assign_pos_to="midbottom",
    offset_pos_by=(0, -2),

)

_arrow_down = rotate_surface(_arrow_up, 180)

RELOAD_PREVIEW_BUTTON_SURF = combine_surfaces(

    [_arrow_up, _arrow_down],
    retrieve_pos_from="center",
    assign_pos_to="center",

)

PREVIEW_PANEL_NOT_FOUND_SURFACE = NOT_FOUND_SURF_MAP[(256, 256)]

