"""Class extension for preparation of visual objects."""

### third-party import
from pygame import Rect


### local imports

from ....config import APP_REFS

from ....classes2d.single import Object2D

from ....textman.render import render_text
from ....textman.cache import CachedTextObject

from ....surfsman.cache import EMPTY_SURF

from ....rectsman.main import RectsManager

from ....iconfactory import ICON_MAP

from ....colorsman.colors import (
    NODE_CATEGORY_COLORS,
    NODE_TITLE,
    BLACK,
)

## other objects for composition

from ..surfs import (
    TOP_CORNERS_MAP,
    NORMAL_BOTTOM_CORNERS,
    SIGMODE_TOGGLE_BUTTON_MAP,
)


## class extensions

from .bodysetup.main import BodySetupOperations

from .sigmode import SignatureModeVisualPreparations
from .calmode import CallableModeVisualPreparations




class VisualPreparations(
    BodySetupOperations,
    SignatureModeVisualPreparations,
    CallableModeVisualPreparations,
):
    """Manages creation and setup of node visuals."""

    ### define remaining methods

    def create_visual_elements(self):
        """Create visual elements for node."""
        ### start by storing the nodes category color
        self.store_category_color_data()

        ### reference and pick tiny icons representing this node when
        ### commented out or not

        self.reference_tiny_icons()
        self.pick_tiny_icon()

        ## create list to store corners
        ##
        ## corners will use surfaces from imported maps
        self.corners = []

        ### create elements situated on top of the node
        self.create_top_objects()

        ### create title of node
        self.create_title_text_object()

        ### create sigmode toggle button
        self.create_sigmode_toggle_button()

        ### create elements situated on bottom of the node
        self.create_bottom_objects()

        ### create text object representing node id
        self.create_node_id_text()

        ### create a body for the node
        self.body = Object2D.from_surface(EMPTY_SURF)

        ### gather references to "background" and text elements
        ### for easy retrieval and drawing

        self.background_and_text_elements = (
            self.roof,
            self.body,
            self.foot,
            self.title_text_obj,
            self.id_text_obj,
            *self.corners,
        )

        ### create a rect to be used as the boundaries of the node
        self.rect = Rect(0, 0, 0, 0)

        ### create expanded signature mode visuals
        self.create_exp_mode_visual_elements()

        ### create collapsed signature mode visuals
        self.create_col_mode_visual_elements()

        ### create callable mode visuals
        self.create_callable_mode_visual_elements()


    def store_category_color_data(self):
        """Store category related color data for the node.

        This color will be used for some elements of the
        node. All nodes in the same category have the same
        color.

        The functionality in this method was isolated
        so that it can be overriden by subclasses as
        neeeded.
        """

        self.color_index = (

            APP_REFS
            .category_index_map

            [
                self
                .data["script_id"]
                [:2]
            ]
        )

        self.category_color = NODE_CATEGORY_COLORS[self.color_index]

    def reference_tiny_icons(self):
        """Reference tiny icons representing the node.

        Icons represent node in commented out and normal state.

        Icons are used when displaying a bird's eye view of the graph.
        """
        index = self.color_index

        normal_key = f'color_index_{index}_node'
        commented_out_key = f'commented_out_{normal_key}'

        self.normal_icon = ICON_MAP[normal_key]
        self.commented_out_icon = ICON_MAP[commented_out_key]

    def create_top_objects(self):
        """Create objects that lie on top of the node."""
        ### create roof and top corner objects

        ## roof
        roof = self.roof = Object2D.from_surface(EMPTY_SURF)

        # topleft corner

        topleft_corner = (
            Object2D.from_surface(
                TOP_CORNERS_MAP[self.category_color][0]
            )
        )

        # topright corner

        topright_corner = (
            Object2D.from_surface(
                TOP_CORNERS_MAP[self.category_color][1]
            )
        )

        self.corners.append(topleft_corner)
        self.corners.append(topright_corner)

        ### store a rects manager to manage the position
        ### of the objects on top of the node

        ## get a callable which returns the rects to be
        ## managed

        get_top_rects = (
            roof.rect,
            topleft_corner.rect,
            topright_corner.rect,
        ).__iter__

        ## use it to instantite the rects manager and
        ## store it in its own attribute
        self.top_rectsman = RectsManager(get_top_rects)

    def create_title_text_object(self):
        """Instatiate object representing title of the node.

        Create and store a text object to represent the
        node's title. We use the name of the callable the
        node represents as the text.
        """

        self.title_text_obj = (

            CachedTextObject(

                text=self.title_text,

                text_settings={
                    'font_key': APP_REFS.general_font_key,
                    'font_height': APP_REFS.general_font_height,
                    'foreground_color': NODE_TITLE,
                    'background_color': self.category_color,
                },

            )

        )

    def create_sigmode_toggle_button(self):
        """Instatiate button to toggle between signature modes."""

        self.sigmode_toggle_button = (

            Object2D.from_surface(
                surface=SIGMODE_TOGGLE_BUTTON_MAP[self.category_color][0],
                on_mouse_release = self.toggle_sigmode,
            )

        )

    def create_bottom_objects(self):
        """Create objects that lie at the node's bottom."""

        ### create foot

        ### the actual surface for the foot will be generated later
        ### when we know the needed width

        ### the actual surfaces for the bottom corners might change
        ### if the node is currently commented out, but we we don't need
        ### to worry about it here (this is taken care of in another spot)

        ## foot
        self.foot = Object2D.from_surface(EMPTY_SURF)

        ### create remaining corners using imported surfaces

        # bottomleft corner
        bottomleft_corner = Object2D.from_surface(NORMAL_BOTTOM_CORNERS[0])

        # bottomright corner
        bottomright_corner = Object2D.from_surface(NORMAL_BOTTOM_CORNERS[1])

        self.corners.append(bottomleft_corner)
        self.corners.append(bottomright_corner)

        ### create and store a rects manager to manage the
        ### position of the objects on the bottom of the
        ### node

        ## get a callable which returns the rects to be
        ## managed

        get_bottom_rects = (
            bottomleft_corner.rect,
            bottomright_corner.rect,
            self.foot.rect,
        ).__iter__

        ## use it to instantiate the rects manager and
        ## store it on its own attribute
        self.bottom_rectsman = RectsManager(get_bottom_rects)

    def create_node_id_text(self):
        """Create text object to representing node's id.

        It won't be positioned yet, just created for now.
        """
        ### instantiate

        node_id = self.id

        self.id_text_obj = Object2D.from_surface(

            render_text(

                text=f" {node_id} ",

                ### text settings

                font_key=APP_REFS.general_font_key,
                font_height=APP_REFS.general_font_height,
                foreground_color=NODE_TITLE,
                background_color=self.category_color,
                border_thickness=1,
                border_color=BLACK,
            )

        )
