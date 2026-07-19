"""Function to extend VisualRelatedOperations class."""

### local imports

from ....surfsman.render import render_rect

from ....colorsman.colors import NODE_BODY_BG, COMMENTED_OUT_NODE_BG

from ..constants import BODY_CONTENT_OFFSET, NODE_OUTLINE_THICKNESS

from ..surfs import NODE_ROOFS_MAP, NODE_FOOTS_MAP



def reposition_callable_elements(self):
    """Reposition objects inside the node in callable mode.

    The repositioning is made from the input
    downwards (the top rectsman doesn't need to be
    repositioned, it always stays at the same relative
    position within the node).

    Another administrative task is performed, which is
    updating the height of self.rect.
    """
    ###

    midtop = self.rect.midtop if self.rect else self.midtop

    (
        topleft_corner_rect,
        topright_corner_rect,
        bottomleft_corner_rect,
        bottomright_corner_rect,

    ) = (

        corner.rect
        for corner in self.corners

    )

    topleft_corner_rect.top = topright_corner_rect.top = midtop[1]

    title_rect = self.title_text_obj.rect
    title_rect.midtop = midtop
    title_rect.move_ip(0, 2)

    topleft_corner_rect.right = title_rect.left - 20
    topright_corner_rect.left = title_rect.right + 20

    ###

    roof = self.roof

    roof_width = topright_corner_rect.left - topleft_corner_rect.right

    roof.image = NODE_ROOFS_MAP[(roof_width, self.category_color)]

    roof.rect.size = roof.image.get_size()
    roof.rect.midtop = midtop

    ### reference the top rectsman locally
    top_rectsman = self.top_rectsman

    ### position callable output socket

    self.callable_output_socket.rect.midtop = (
        top_rectsman.move(0, -2).bottomright
    )

    ### define a top coordinate which is the bottom of
    ### the top of the node plus the body content
    ### offset given as a constant
    top = top_rectsman.bottom + BODY_CONTENT_OFFSET

    ### position the id text object

    ## reference the rect of the id text object locally
    id_text_rect = self.id_text_obj.rect

    ## align its centerx with title rect's centerx
    id_text_rect.centerx = title_rect.centerx

    ## align its top with the last defined top; also push it
    ## 4 pixels down for extra padding
    id_text_rect.top = top + 4

    ##
    top = id_text_rect.bottom - 2

    ## position bottom corners

    bottomleft_corner_rect.top = bottomright_corner_rect.top = top

    bottomleft_corner_rect.left = topleft_corner_rect.left
    bottomright_corner_rect.right = topright_corner_rect.right

    ##

    bg_color = (

        COMMENTED_OUT_NODE_BG
        if self.data.get('commented_out', False)

        else NODE_BODY_BG

    )

    ## generate visual for foot and position it

    foot = self.foot
    foot_rect = foot.rect

    foot_width = roof_width

    foot.image = NODE_FOOTS_MAP[(foot_width, bg_color)]

    foot_rect.size = foot.image.get_size()

    foot_rect.top = top
    foot_rect.left = bottomleft_corner_rect.right

    ###
    bottom_rectsman = self.bottom_rectsman

    ### perform extra administrative task: generate body surface and
    ### update its rect

    body = self.body

    body_rect = body.rect

    body_rect.width = top_rectsman.width
    body_rect.height = bottom_rectsman.top - top_rectsman.bottom

    body_rect.midtop = top_rectsman.midbottom

    body.image = render_rect(*body_rect.size, bg_color)

    ### perform extra administrative task: update size and position
    ### of self.rect

    ## width

    left = top_rectsman.left
    right = self.callable_output_socket.rect.right

    self.rect.width = right - left

    ## height
    self.rect.height = bottom_rectsman.bottom - top_rectsman.top

    ## midtop
    self.rect.midtop = top_rectsman.midtop
