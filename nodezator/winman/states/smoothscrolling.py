"""Window manager event handling for 'smoothscrolling' state."""

### third-party imports

from pygame.locals import (

    QUIT,
    KEYDOWN,
    KMOD_CTRL,
    KMOD_SHIFT,

    K_q,

)


### local imports

from ...pygamesetup import SERVICES_NS

from ...config import APP_REFS

from ...loopman.exception import QuitAppException, ContinueLoopException



class SmoothscrollingState:
    """Methods related to 'smoothscrolling' state."""

    def smoothscrolling_event_handling(self):
        """Get and respond to events."""

        for event in SERVICES_NS.get_events():

            ### QUIT

            if event.type == QUIT:
                raise QuitAppException

            ### KEYDOWN

            elif event.type == KEYDOWN:

                ## Application related operations

                # quit

                if event.key == K_q and event.mod & KMOD_CTRL:
                    raise QuitAppException


    def smoothscrolling_keyboard_input_handling(self):
        pass

    def smoothscrolling_update(self):
        """Scroll if there's scrolling to do, otherwise leave state."""

        if self.smoothscrolling_steps:
            APP_REFS.ea.scroll(*self.smoothscrolling_steps.popleft())

        else:

            self.set_state('loaded_file')
            raise ContinueLoopException

    ### draw

    def smoothscrolling_draw(self):
        """Draw method for the 'smoothscrolling_ state."""
        self.background.draw()

        APP_REFS.ea.grid_drawing_behaviour()
        APP_REFS.ea.draw_selected()
        APP_REFS.gm.draw()

        for item in self.labels_drawing_methods:
            item()
        for item in self.switches_drawing_methods:
            item()

        self.separator.draw()
        self.menubar.draw_top_items()

        SERVICES_NS.update_screen()
