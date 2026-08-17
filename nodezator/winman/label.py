"""Label related class extension for WindowManager."""

### standard library imports

from math import floor

from functools import partial

from itertools import cycle


### local imports

from ..config import APP_REFS

from ..translatedtext import TRANSLATIONS

from ..pygamesetup import SCREEN_RECT

from ..colorsman.colors import WM_LABEL_FG, WM_LABEL_BG

from ..textman.label.autolabel import AutoLabel



### translations
t = TRANSLATIONS.window_manager

### constant definition

AUTOLABEL_KWARGS = {
    'font_height': APP_REFS.mono_font_height,
    'font_key': APP_REFS.mono_font_key,
    'foreground_color': WM_LABEL_FG,
    'background_color': (*WM_LABEL_BG, 130),
}


##### utility function

def get_scrolling_amount(assistant):
    """Return formatted scrolling amount.

    Parameters
    ==========
    assistant (the editing.EditingAssistant instance)
        A context object with useful information for our purpose.
    """

    return "({:>4}, {:>4})".format(

        ### scrolling amount;
        ###
        ### we get the opposite of the scrolling amount vector and map it
        ### to the int constructor;
        ###
        ### (using the opposite is a usability measure, so the scrolling amount
        ### shows a number as if the screen had moved, when in fact it were the
        ### objects in the world which moved in the opposite direction)
        *map(int, -assistant.scrolling_amount)

    )


##### class definition

class MonitorLabelSetup:
    """Data and behaviour for monitor label setup."""

    def instantiate_labels(self):
        """Instantiate and set monitoring labels."""
        ### status label

        self.status_label = (

            AutoLabel(
                partial(getattr, APP_REFS, "status_message"),
                formatter=(t.status + ": {}").format,
                text="--",
                **AUTOLABEL_KWARGS,
            )

        )

        ### scrolling amount

        self.scrolling_label = (

            AutoLabel(
                partial(get_scrolling_amount, APP_REFS.ea),
                formatter="x, y: {}".format,
                text="(    0,    0)",
                **AUTOLABEL_KWARGS,
            )

        )

        ### position labels
        self.reposition_labels()

        ### gather draw and update behaviours from labels

        labels = (
            self.status_label,
            self.scrolling_label,
        )

        self.labels_update_methods = [label.update for label in labels]

        self.labels_drawing_methods = [label.draw for label in labels]

    def reposition_labels(self):

        self.status_label.rect.bottomleft = SCREEN_RECT.bottomleft

        self.scrolling_label.rect.bottomleft = self.status_label.rect.topleft
