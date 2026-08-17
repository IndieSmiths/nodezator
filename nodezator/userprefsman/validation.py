"""Facility for user preferences validation."""

### local imports

from ..translatedtext import AVAILABLE_LOCALES

from .constants import TEST_SESSION_SETTINGS_KEY



### constants

ORDERED_SOCKET_DETECTION_GRAPHICS = (
    'assisting_line',
    'reaching_hands',
    'hands_and_eyes',
    'baseball_elements',
    'baseball_elements_and_eyes',
)

AVAILABLE_SOCKET_DETECTION_GRAPHICS = set(ORDERED_SOCKET_DETECTION_GRAPHICS) 

SOCKET_DETECTION_GRAPHICS_KEY_TO_NAME_MAP = {
    'assisting_line': "Assisting line",
    'reaching_hands': "Reaching hands",
    'hands_and_eyes': "Hands and eyes",
    'baseball_elements': "Baseball elements",
    'baseball_elements_and_eyes': "Baseball elements and eyes",
}

KEY_ERROR_FORMATTER = ("{!r} key not present in user preferences").format

TEXT_EDITOR_BEHAVIOR_OPTIONS = ('default', 'vim-like')

GENERAL_FONT_HEIGHT_RANGE = range(16, 40)
MONO_FONT_HEIGHT_RANGE = range(16, 40)

FONT_KIND_OPTIONS = ('default', 'system_font', 'font_file')


### function definitions

def validate_prefs_data(prefs_data):
    """Raise exception if preferences data doesn't validate.

    In most cases, the problem will be fixed instead of raising an error.
    """
    ### ensure preferences data is a dict

    if not isinstance(prefs_data, dict):
        raise TypeError("Preferences data must be a dictionary.")

    ### integers >= 0

    for key, default in (
        ('USER_LOGGER_MAX_LINES', 1000),
        ('CUSTOM_STDOUT_MAX_LINES', 1000),
        ('NUMBER_OF_BACKUPS', 5),
    ):

        if key not in prefs_data:

            prefs_data[key] = default
            continue

        value = prefs_data[key]

        if not isinstance(value, int) or not value >= 0:
            prefs_data[key] = default

    ### integers within range

    for key, value_range, default in (
        ('GENERAL_FONT_HEIGHT', GENERAL_FONT_HEIGHT_RANGE, 17),
        ('MONO_FONT_HEIGHT', MONO_FONT_HEIGHT_RANGE, 20),
    ):

        if key not in prefs_data:

            prefs_data[key] = default
            continue

        value = prefs_data[key]

        if not isinstance(value, int) or value not in value_range:
            prefs_data[key] = default

    ### text editor behavior

    key = 'TEXT_EDITOR_BEHAVIOR'

    if key not in prefs_data:
        prefs_data[key] = 'default'

    value = prefs_data[key]

    if (
        not isinstance(value, str)
        or value not in TEXT_EDITOR_BEHAVIOR_OPTIONS
    ):
        prefs_data[key] = 'default'

    ### socket detection

    ## graphics

    key = 'SOCKET_DETECTION_GRAPHICS'

    if key not in prefs_data:
        prefs_data[key] = 'reaching_hands'

    value = prefs_data[key]

    if (
        not isinstance(value, str)
        or value not in AVAILABLE_SOCKET_DETECTION_GRAPHICS
    ):
        prefs_data[key] = 'reaching_hands'

    ## reaching and full detection distances

    for key, default in (
        ('DETECTION_DISTANCE', 150),
        ('GRASPING_DISTANCE', 75),
    ):

        if key not in prefs_data:
            prefs_data[key] = default

        value = prefs_data[key]

        if not isinstance(value, int) or value < 0:
            prefs_data[key] = default

    if prefs_data['DETECTION_DISTANCE'] <= prefs_data['GRASPING_DISTANCE']:

        prefs_data['DETECTION_DISTANCE'] = 150
        prefs_data['GRASPING_DISTANCE'] = 75


    ### available languages

    locale_key = "LOCALE"

    if locale_key not in prefs_data:
        prefs_data['LOCALE'] = 'en_us'

    locale_value = prefs_data[locale_key]

    if locale_value not in AVAILABLE_LOCALES:
        prefs_data['LOCALE'] = 'en_us'

    ### more font settings (besides the font heights already checked earlier)

    for key in ('GENERAL_FONT_KIND', 'MONO_FONT_KIND'):

        if key not in prefs_data:

            prefs_data[key] = 'default'
            continue

        value = prefs_data[key]

        if not isinstance(value, str) or value not in FONT_KIND_OPTIONS:
            prefs_data[key] = 'default'

    for key in ('GENERAL_FONT_TO_USE', 'MONO_FONT_TO_USE'):

        if key not in prefs_data:

            prefs_data[key] = ''
            continue

        value = prefs_data[key]

        if not isinstance(value, str):
            prefs_data[key] = ''

    ### test session data

    if TEST_SESSION_SETTINGS_KEY in prefs_data:
        validate_test_settings_data(prefs_data[TEST_SESSION_SETTINGS_KEY])


def validate_test_settings_data(test_settings_data):
    """Raise exception if test settings data doesn't validate."""

    key = TEST_SESSION_SETTINGS_KEY

    ### ensure test settings data is a dict

    if not isinstance(test_settings_data, dict):

        raise TypeError(
            f"Test settings data from '{key}' key in user preferences"
            " must be a dictionary."
        )

    ### ensure its contents validate as well

    for subkey in ('test_cases_ids', 'playback_speed'):

        if subkey not in test_settings_data:

            raise (

                KeyError

                (
                    f"'{subkey}' not present in '{key}' key"
                    " from user preferences"
                )

            )

        elif subkey == 'test_cases_ids':

            value = test_settings_data[subkey]

            if not isinstance(value, tuple):

                raise (

                    TypeError

                    (
                        f"'{subkey}' subkey from '{key}' key"
                        " in user preferences must hold a tuple."
                    )

                )

            elif (
                any(
                    not isinstance(item, int)
                    for item in value
                )
            ):

                raise (
                    TypeError
                    (
                        f"'{subkey}' subkey from '{key}' key"
                        " in user preferences must hold at least one item"
                        " and all items must be integers"
                    )
                )

        elif subkey == 'playback_speed':

            value = test_settings_data[subkey]

            if not isinstance(value, int):

                raise (

                    TypeError

                    (
                        f"'{subkey}' subkey from '{key}' key"
                        " in user preferences must hold an int."
                    )

                )

            elif value < 0:

                raise (

                    ValueError

                    (
                        f"'{subkey}' subkey from '{key}' key"
                        " in user preferences must hold an integer >= 0"
                    )

                )
