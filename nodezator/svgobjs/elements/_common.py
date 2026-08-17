"""Facility with objects/values of common usage."""

### standard library imports

from functools import partialmethod

from textwrap import indent



REFS = type('Object', (), {})


class ContainerElement:
    """Common methods for elements that contain others (<svg> and <g>)."""

    def __init__(self, children=(), **kwargs):

        ### set values for all listed attribute names, taking the values
        ### from kwargs if available, or from default values set as class
        ### attributes when not available, or using None if neither is
        ### available

        for attr_name in self.attr_names:

            setattr(

                self,
                attr_name,

                kwargs.get(

                    attr_name, 
                    getattr(self, attr_name, None)

                ),

            )

        ### create a list of children from the given children

        self._children = []

        if children:
            self.extend(children)

    def append(self, obj):

        if isinstance(obj, REFS.SVG):
            raise TypeError("SVG instances cannot be child elements.")

        self._children.append(obj)

    def append_obj(self, obj_name, **kwargs):

        self.append(
            getattr(REFS, obj_name)(**kwargs)
        )

    append_line = partialmethod(append_obj, obj_name='Line')
    append_polyline = partialmethod(append_obj, obj_name='PolyLine')

    append_rect = partialmethod(append_obj, obj_name='Rect')
    append_circle = partialmethod(append_obj, obj_name='Circle')
    append_ellipse = partialmethod(append_obj, obj_name='Ellipse')
    append_path = partialmethod(append_obj, obj_name='Path')

    append_g = append_group = partialmethod(append_obj, obj_name='G')

    def extend(self, new_children):

        for child in new_children:
            self.append(child)

    def remove_obj(self, obj):
        self._children.remove(obj)

    def __repr__(self):

        text = f'{self.__class__.__name__}('

        text += ', '.join(
            f'{attr_name}=' + repr(getattr(self, attr_name))
            for attr_name in self.attr_names
        )

        if self._children:
            text += ', children'

        text += ')'

        return text

    def __str__(self):

        tag_name = self.tag_name

        opening_tag_text = f'<{tag_name}'

        for attr_name in self.attr_names:

            value = getattr(self, attr_name)

            if value is not None:
                opening_tag_text += f' {attr_name}="{value}"'

        opening_tag_text += '>'

        children_text = indent(

            ## text
            '\n'.join(str(child) for child in self._children),

            ## indent/prefix
            '    ',

        )

        return opening_tag_text + '\n' + (

            children_text + '\n'
            if children_text

            else ''

        ) + f'</{tag_name}>'


class Shape:
    """Common methods for shapes.

    That is, elements that represent shapes/drawings (including <path>).
    """

    def __init__(self, **kwargs):

        ### set values for all listed attribute names, using values
        ### from kwargs, from default values set as class attributes
        ### or None when those are not available

        for attr_name in self.attr_names:

            setattr(

                self,
                attr_name,

                kwargs.get(
                    attr_name,
                    getattr(self, attr_name, None)
                ),

            )

    def __repr__(self):

        text = f'{self.__class__.__name__}('

        attr_text_list = []

        for attr_name in self.attr_names:

            value = repr(getattr(self, attr_name))
            attr_text_list.append(f'{attr_name}={value}')

        text += ', '.join(attr_text_list)

        return text + ')'

    def __str__(self):

        return f'<{self.tag_name} ' + ' '.join(

            (
                attr_name.replace('_', '-')
                + '="'
                + str(getattr(self, attr_name))
                + '"'
            )

            for attr_name in self.attr_names
            if getattr(self, attr_name) is not None

        ) + ' />'

