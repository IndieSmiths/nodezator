"""Facility for visuals related node class extension."""

### XXX module docstring isn't accurate

### standard library import
from functools import partial


### local imports

from .....textman.cache import CachedTextObject

from ....widget.utils import WIDGET_CLASS_MAP

from ....socket.surfs import type_to_codename

from ...utils import update_with_widget


## classes for composition

from ....socket.input import InputSocket

from .....widget.defaultholder import DefaultHolder



def create_parameter_objs(self, param_obj, label_text_settings):
    """Build socket and widget for the parameter.

    The parameter in question must not be of variable
    kind.

    This function is meant to extend the
    VisualRelatedPreparations class as one of its methods.

    Parameters
    ==========
    param_obj (inspect.Parameter instance)
        an object representing a parameter from a callable
        object, containing related data.
    label_text_settings (dict)
        text settings used for labels.
    """
    ### retrieve the name of the parameter
    param_name = param_obj.name

    ### create and store text object representing parameter

    self.parameter_text_obj_map[param_name] = (

        CachedTextObject(
            text=param_name,
            text_settings=label_text_settings,
        )

    )

    ### let's also alias the live instances map for
    ### the input sockets using a variable of low
    ### character count, for better code layout
    isl_flmap = self.input_socket_live_flmap

    ### also retrieve the expected type of the
    ### parameter and use it to obtain a string
    ### representing a codename for the type;
    ###
    ### no type enforcement is ever performed,
    ### though

    expected_type = self.type_map[param_name]
    type_codename = type_to_codename(expected_type)

    ### instantiate socket

    input_socket = (

        InputSocket(
            node=self,
            type_codename=type_codename,
            parameter_name=param_name,
        )

    )

    ### store the input socket instance in the
    ### live instance map for input sockets
    isl_flmap[param_name] = input_socket

    ## this dict subclass instance needs to be updated
    ## every time it is changed
    isl_flmap.update()


    ### try retrieving the widget meta map for the
    ### parameter
    try:
        param_widget_meta = self.widget_meta[param_name]

    ### if widget metadata for the parameter doesn't
    ### exists, we just pass: no widget will be created
    except KeyError:
        pass

    ### otwerwise, we use the retrieved metadata to
    ### properly instantiate and set a widget

    else:

        ## retrieve widget class using the widget name
        ## from the parameter widget metadata

        widget_name = param_widget_meta["widget_name"]
        widget_cls = WIDGET_CLASS_MAP[widget_name]

        ## retrieve keyword arguments to use when
        ## instantiating the widget
        kwargs = param_widget_meta["widget_kwargs"]

        ## if we are dealing with a text display widget,
        ## replace the 'font_path' option by an appropriate one;
        ##
        ## the 'font_path' option, used in previous version isn't
        ## valid anymore; in fact, it shouldn't have been exposed
        ## to users to begin with (that is, not the way it was, but
        ## as a toggle, like now)

        if widget_name == 'text_display' and 'font_path' in kwargs:

            fpath = kwargs.pop('font_path')

            kwargs['pick_monospaced_font'] = (
                True if fpath == 'mono_bold' else False
            )

        ## instantiate the widget using the keyword arguments
        ## as well as the position data

        try:
            widget = widget_cls(name=param_name, **kwargs)

        except Exception as err:

            raise RuntimeError(
                "Error while trying to instantiate"
                f" widget for '{param_name}' parameter"
                f" of '{self.title_text}' node"
                f" of id #{self.id} with data from"
                " the parameter widget metadata map"
            ) from err

        ## if available, set widget value as defined
        ## by the user in its last editing session

        param_widget_value_map = self.data["param_widget_value_map"]

        # check existence of value
        try:
            value = param_widget_value_map[param_name]

        # if not available, use the current value of
        # the widget to fill it (unless it is a
        # default holder widget, a special widget
        # which can't be edited, and in fact may
        # even hold non-JSON-serializable values)

        except KeyError:

            if not isinstance(widget, DefaultHolder):

                # by ensuring the value being seen
                # in the widget is the one to be
                # used, we avoid confusion, that is,
                # what you see is what you get (except
                # for the default holder widget, of
                # course, but it is a special case of
                # which the users must be made aware
                # anyway)

                (param_widget_value_map[param_name]) = widget.get()

        # otherwise, do the opposite: set the value
        # on the widget
        else:
            widget.set(value)

        ## also define a command to update the
        ## widget value in the node data and
        ## assign it to the command attribute of
        ## the widget

        command = partial(
            update_with_widget, param_widget_value_map, param_name, widget
        )

        widget.command = command

        ## store the widget instance in the live map
        self.widget_live_flmap[param_name] = widget

        # this dict subclass instance must be updated
        # whenever it is changed
        self.widget_live_flmap.update()
