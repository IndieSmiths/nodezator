"""General SVG shapes."""

### standard library imports

from collections.abc import Iterable

from xml.dom.minidom import parseString

from re import search, sub


### third-party library imports

from pygame import Rect

from pygame.math import Vector2


### local import

from ..ourstdlibs.mathutils import get_rect_from_points

from .common import format_color



### constants

RECT_FORMATTER = """
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">

    <rect
        x="{x}" y="{y}" width="{width}" height="{height}"
        rx="{rx}" ry="{ry}"
        fill="{fill_color}" stroke="{stroke_color}" stroke-width="{stroke_width}"
    />

</svg>
""".strip().format

CIRCLE_FORMATTER = """
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">

    <circle
        cx="{cx}" cy="{cy}" r="{r}"
        fill="{fill_color}" stroke="{stroke_color}" stroke-width="{stroke_width}"
     />

</svg>
""".strip().format

ELLIPSE_FORMATTER = """
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">

    <ellipse
        cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"
        fill="{fill_color}" stroke="{stroke_color}" stroke-width="{stroke_width}"
     />

</svg>
""".strip().format

LINE_FORMATTER = """
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">

    <line
        x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"
        stroke="{stroke_color}" stroke-width="{stroke_width}"
     />

</svg>
""".strip().format


### functions


def get_rect_svg_text(
    x, y, width, height,
    rx=0, ry=0,
    fill_color=None,
    outline_color=None,
    outline_width=0,
):
    """Return SVG text representing file with a rect."""
    ### format fill color and outline color into a format
    ### used in SVG

    fill_color = format_color(fill_color)
    stroke_color = format_color(outline_color)

    ### define the dimensions of the SVG

    width = width + (outline_width * 2)
    height = height + (outline_width * 2)

    ### pass our data to a str.format() instance that formats the data
    ### into a string representing the contents of a svg file describing
    ### our rect, returning such string

    return (
        RECT_FORMATTER(
            width=width,
            height=height,
            x=x, y=y,
            rx=rx, ry=ry,
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_width=outline_width,
        )
    )


def get_circle_svg_text(
    cx, cy, r,
    fill_color=None,
    outline_color=None,
    outline_width=0,
):
    """Return SVG text representing file with a circle."""

    ### format fill color and outline color into a format
    ### used in SVG

    fill_color = format_color(fill_color)

    stroke_color = format_color(outline_color)

    ### define the dimensions of the SVG, based on the radius and
    ### the outline width

    width = height = (r * 2) + (outline_width * 2)

    ### pass our data to a str.format() instance that formats the data
    ### into a string representing the contents of a svg file describing
    ### our circle, returning such string

    return (
        CIRCLE_FORMATTER(
            width=width,
            height=height,
            cx=cx, cy=cy, r=r,
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_width=outline_width,
        )
    )

def get_circle_svg_text_from_radius(
    r,
    fill_color=None,
    outline_color=None,
    outline_width=0,
):
    """Return SVG text representing file with a circle given the radius.

    The remaining values are calculated based on the radius and
    outline width.
    """
    ### format fill color and outline color into a format
    ### used in SVG

    fill_color = format_color(fill_color)

    stroke_color = format_color(outline_color)

    ### define the dimensions of the SVG and the center of the circle,
    ### based on the radius and the outline width

    width = height = (r * 2) + (outline_width * 2)
    cx = cy = width // 2

    ### pass our data to a str.format() instance that formats the data
    ### into a string representing the contents of a svg file describing
    ### our circle, returning such string

    return (
        CIRCLE_FORMATTER(
            width=width,
            height=height,
            cx=cx, cy=cy, r=r,
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_width=outline_width,
        )
    )

def get_ellipse_svg_text(
    cx, cy, rx, ry,
    fill_color=None,
    outline_color=None,
    outline_width=0,
):
    """Return SVG text representing file with an ellipse."""
    ### format fill color and outline color into a format
    ### used in SVG

    fill_color = format_color(fill_color)

    stroke_color = format_color(outline_color)

    ### define the dimensions of the SVG

    width = (rx * 2) + (outline_width * 2)
    height = (ry * 2) + (outline_width * 2)

    ### pass our data to a str.format() instance that formats the data
    ### into a string representing the contents of a svg file describing
    ### our ellipse, returning such string

    return (
        ELLIPSE_FORMATTER(
            width=width,
            height=height,
            cx=cx, cy=cy, rx=rx, ry=ry,
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_width=outline_width,
        )
    )

def get_line_svg_text(
    x1, y1, x2, y2,
    outline_color=None,
    outline_width=0,
):
    """Return SVG text representing file with a line."""
    ### represent points as 2d vectors

    v1 = Vector2(x1, y1)
    v2 = Vector2(x2, y2)

    ### define bounding area of points

    points_bounding_area = Rect(get_rect_from_points(v1, v2))

    ### offset it to origin, moving the points along with it by the
    ### same amount
    points_bounding_offset = -Vector2(points_bounding_area.topleft)

    points_bounding_area.move_ip(points_bounding_offset)

    v1 += points_bounding_offset
    v2 += points_bounding_offset

    ### create an additional stroke bounding area, by adding extra
    ### padding to the points bounding area;
    ###
    ### this area accounts for the extra space taken by the line
    ### thickness, that is, the thickness of the stroke
    stroke_bounding_area = points_bounding_area.inflate((outline_width,)*2)

    ### offset stroke bounding area area to origin and move points by the
    ### same amount
    ###
    ### we do not move the points bounding area because at this point we
    ### won't need it anymore

    stroke_bounding_offset = -Vector2(stroke_bounding_area.topleft)

    stroke_bounding_area.move_ip(stroke_bounding_offset)

    v1 += stroke_bounding_offset
    v2 += stroke_bounding_offset

    ### now redefine the points coordinates and the svg dimensions with
    ### the points and stroke bounding area

    x1, y1 = v1
    x2, y2 = v2

    width, height = stroke_bounding_area.size

    stroke_color = format_color(outline_color)

    ### finally pass our data to a str.format() instance that formats
    ### the data into a string representing the contents of a svg file
    ### describing our line, returning such string

    return (
        LINE_FORMATTER(
            width=width,
            height=height,
            x1=x1, y1=y1, x2=x2, y2=y2,
            stroke_color=stroke_color,
            stroke_width=outline_width,
        )
    )

