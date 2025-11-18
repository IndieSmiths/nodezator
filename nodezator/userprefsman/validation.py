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


### function definitions

def validate_prefs_data(prefs_data):
    """Raise exception if preferences data doesn't validate.

    In some cases, the absence of a key may be fixed by inserting a
    default value instead of triggering an exception.
    """
    ### ensure preferences data is a dict

    if not isinstance(prefs_data, dict):
        raise TypeError("Preferences data must be a dictionary.")

    ### integers >= 0

    for key in (
        "USER_LOGGER_MAX_LINES",
        "CUSTOM_STDOUT_MAX_LINES",
        "NUMBER_OF_BACKUPS",
    ):

        if key not in prefs_data:
            raise KeyError(KEY_ERROR_FORMATTER(key))

        value = prefs_data[key]

        if not isinstance(value, int) or not value >= 0:
            raise TypeError(f"{repr(key)} key must be 'int' >= 0")

    ### socket detection

    ## graphics

    key = 'SOCKET_DETECTION_GRAPHICS'

    if key not in prefs_data:
        raise KeyError(KEY_ERROR_FORMATTER(key))

    value = prefs_data[key]

    if not isinstance(value, str):
        raise TypeError(f"{repr(key)} key must be 'str'")

    if value not in AVAILABLE_SOCKET_DETECTION_GRAPHICS:

        raise ValueError(
            f"value in {repr(key)} key must be"
            " one of the following strings:"
            f" {AVAILABLE_SOCKET_DETECTION_GRAPHICS}"
        )

    ## reaching and full detection distances

    for key in ('DETECTION_DISTANCE', 'GRASPING_DISTANCE'):

        if key not in prefs_data:
            raise KeyError(KEY_ERROR_FORMATTER(key))

        value = prefs_data[key]

        if not isinstance(value, int):
            raise TypeError(f"{repr(key)} key must be 'int'")

        if value < 0:
            raise ValueError(f"{repr(key)} key must be >= 0")

    if prefs_data['DETECTION_DISTANCE'] <= prefs_data['GRASPING_DISTANCE']:

        raise ValueError(
            "value in 'DETECTION_DISTANCE' key must be higher than value in"
            " 'GRASPING_DISTANCE' key"
        )

    ### available languages

    locale_key = "LOCALE"

    if locale_key not in prefs_data:
        prefs_data['LOCALE'] = 'en_us'

    locale_value = prefs_data[locale_key]

    if locale_value not in AVAILABLE_LOCALES:

        raise ValueError(
            f"value in {repr(locale_key)} key must be"
            " one of the following strings:"
            f" {AVAILABLE_LOCALES}"
        )

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
