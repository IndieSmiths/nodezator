"""Facility for loading and distributing translated text."""

### standard library imports

from collections import deque

from itertools import takewhile


### local imports

from .config import TRANSLATIONS_DIR

from .ourstdlibs.behaviour import CallList



### module level helper objects

is_space = lambda c: c == ' '

AVAILABLE_LOCALES = set()


### function to create translation namespace

def get_translations_namespace():
    """Load translated texts, gather them in namespace and return it."""

    ### root node
    translations = TranslationNode()

    ### populate it

    ptm = {} # ptm = parent tracking map

    translation_sheets_paths = (
        path
        for path in TRANSLATIONS_DIR.iterdir()
        if path.suffix.lower() == '.txt'
    )

    for path in translation_sheets_paths:

        sheet = TranslationNode()
        sheet_name = path.stem
        setattr(translations, sheet_name, sheet)
    
        ptm.clear()

        # parent of node of level 0 have the sheet as their parent node
        ptm[0] = sheet

        ###

        lines = path.read_text(encoding='utf-8').splitlines()
        lines_deque = deque(lines)

        watch_out_for_translations = False

        previous_level = 0

        for line in lines:

            ###
            lines_deque.popleft()
            ###

            stripped_line = line.strip()

            ### empty lines or lines starting with '#' are ignored

            if (
                not stripped_line
                or stripped_line[0] == '#'
            ):
                continue

            ### determine current level based on number of spaces
            ### 0 spaces == level 1
            ### 4 spaces == level 2
            ### 8 spaces == level 3
            ### and so on

            spaces = ''.join(takewhile(is_space, line))

            no_of_spaces = len(spaces)

            current_level = (no_of_spaces // 4) + 1

            ###
            remaining_text = line[no_of_spaces:]

            ###

            if current_level < previous_level:
                watch_out_for_translations = False

            ### if we are dealing with translations, simply
            ### store the translation in the parent object
            ### using the locale code as the attribute name

            if watch_out_for_translations:

                locale, _, translation = remaining_text.partition(' ')

                # locale

                formatted_locale = (
                    locale
                    .lower()           # ensure lowercase
                    .replace('-', '_') # ensure '-' is replaced with '_'
                )
                
                # register locale
                AVAILABLE_LOCALES.add(formatted_locale)

                # store translation in parent's translation map

                parent = ptm[current_level-2]

                tmap = (
                    parent._translation_map
                    [parent._identifier_to_be_registered]
                )

                tmap[formatted_locale] = translation

            else:

                # peek into next lines to see if we are dealing
                # with translations or identifiers
                #
                # if dealing with translations, we use hte leaf
                # class, otherwise we use the node class

                for deque_line in lines_deque:

                    stripped_deque_line = deque_line.strip()

                    if (
                        not stripped_deque_line
                        or stripped_deque_line[0] == '#'
                    ):
                        continue

                    if ' ' in stripped_deque_line:
                        watch_out_for_translations = True

                    break

                parent = ptm[current_level-1]

                if watch_out_for_translations:

                    if not parent._has_translation_map:

                        parent._translation_map = {}
                        parent._has_translation_map = True

                    parent._translation_map[remaining_text] = {}
                    parent._identifier_to_be_registered = remaining_text

                else:

                    # instantiate and store object in parent's attribute

                    node = TranslationNode()
                    setattr(parent, remaining_text, node)

                    # store it as a parent obj
                    ptm[current_level] = node

            ### mark current level as the previous level
            previous_level = current_level

    ### clear the helper map
    ptm.clear()

    ### return namespace
    return translations


# helper class;
#
# simple class that falls back to en_us translation
# when another locale fails when retrieved

class TranslationNode():

    # placeholder attribute (to be set within the user preferences
    # subpackage)
    _user_prefs = None

    def __init__(self):

        self._has_translation_map = False
        self._identifier_to_be_registered = ''

    def __getattr__(self, attr_name):

        if not self._has_translation_map:

            raise RuntimeError(
                f"TranslationNode obj doesn't have '{attr_name}' attribute."
            )

        return (
            self._translation_map[attr_name]
            .get(self._user_prefs['LOCALE'], 'en_us')
        )

### translation namespace
TRANSLATIONS = get_translations_namespace()

### collections of callbacks to reset text surfaces in response to
### changing language
on_language_change = CallList()

